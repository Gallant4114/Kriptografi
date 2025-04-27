import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import csv

# S-box dan inverse S-box untuk subtitusi
Sbox = [
    0xA, 0x4, 0x3, 0xB,
    0x8, 0xE, 0x2, 0x5,
    0x1, 0xF, 0x9, 0xC,
    0x6, 0x0, 0xD, 0x7
]

InvSbox = [0] * 16
for i, val in enumerate(Sbox):
    InvSbox[val] = i

# Fungsi perkalian dalam Galois Field GF(2^4)


def gf_mult(a, b):
    result = 0
    a = a & 0xF
    b = b & 0xF
    for _ in range(4):
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x10:
            a ^= 0x13  # XOR dengan reduksi polinomial x^4 + x + 1 (0x13)
        b >>= 1
    return result & 0xF

# Key expansion untuk menghasilkan round keys


def key_expansion(key):
    nibbles = [(key >> 12) & 0xF, (key >> 8) &
               0xF, (key >> 4) & 0xF, key & 0xF]
    round_keys = [(nibbles[0] << 12) | (nibbles[1] << 8)
                  | (nibbles[2] << 4) | nibbles[3]]
    Rcon = [0x01, 0x02, 0x04]
    for i in range(3):
        temp = Sbox[nibbles[3]] ^ Rcon[i]
        w4 = nibbles[0] ^ temp
        w5 = nibbles[1] ^ w4
        w6 = nibbles[2] ^ w5
        w7 = nibbles[3] ^ w6
        nibbles = [w4, w5, w6, w7]
        round_keys.append((w4 << 12) | (w5 << 8) | (w6 << 4) | w7)
    return round_keys

# Konversi antara integer dan state matrix


def int_to_state(n):
    return [
        [(n >> 12) & 0xF, (n >> 8) & 0xF],
        [(n >> 4) & 0xF, n & 0xF]
    ]


def state_to_int(state):
    return (state[0][0] << 12) | (state[0][1] << 8) | (state[1][0] << 4) | state[1][1]

# Operasi dasar Mini-AES


def sub_nibbles(state, sbox):
    return [[sbox[cell] for cell in row] for row in state]


def shift_rows(state):
    return [state[0], [state[1][1], state[1][0]]]


def mix_columns(state):
    new_state = [[0]*2 for _ in range(2)]
    for i in range(2):
        a = state[0][i]
        b = state[1][i]
        new_state[0][i] = gf_mult(1, a) ^ gf_mult(4, b)
        new_state[1][i] = gf_mult(4, a) ^ gf_mult(1, b)
    return new_state


def inverse_mix_columns(state):
    new_state = [[0]*2 for _ in range(2)]
    for i in range(2):
        a = state[0][i]
        b = state[1][i]
        new_state[0][i] = gf_mult(9, a) ^ gf_mult(2, b)
        new_state[1][i] = gf_mult(2, a) ^ gf_mult(9, b)
    return new_state


def add_round_key(state, round_key):
    key_state = int_to_state(round_key)
    return [[state[i][j] ^ key_state[i][j] for j in range(2)] for i in range(2)]

# Fungsi enkripsi/dekripsi satu blok


def encrypt_block(plaintext, key):
    round_keys = key_expansion(key)
    state = int_to_state(plaintext)
    state = add_round_key(state, round_keys[0])
    log = ["Initial AddRoundKey: " + format(state_to_int(state), '04x')]

    for r in range(1, 4):
        state = sub_nibbles(state, Sbox)
        log.append(f"Round {r} SubNibbles: " +
                   format(state_to_int(state), '04x'))

        state = shift_rows(state)
        log.append(f"Round {r} ShiftRows: " +
                   format(state_to_int(state), '04x'))

        if r != 3:
            state = mix_columns(state)
            log.append(f"Round {r} MixColumns: " +
                       format(state_to_int(state), '04x'))

        state = add_round_key(state, round_keys[r])
        log.append(f"Round {r} AddRoundKey: " +
                   format(state_to_int(state), '04x'))

    return state_to_int(state), log


def decrypt_block(ciphertext, key):
    round_keys = key_expansion(key)
    state = int_to_state(ciphertext)
    state = add_round_key(state, round_keys[3])
    log = ["Initial AddRoundKey (K3): " + format(state_to_int(state), '04x')]

    for r in range(3, 0, -1):
        state = shift_rows(state)
        log.append(f"Round {4-r} InvShiftRows: " +
                   format(state_to_int(state), '04x'))

        state = sub_nibbles(state, InvSbox)
        log.append(f"Round {4-r} InvSubNibbles: " +
                   format(state_to_int(state), '04x'))

        state = add_round_key(state, round_keys[r-1])
        log.append(f"Round {4-r} AddRoundKey: " +
                   format(state_to_int(state), '04x'))

        if r != 1:
            state = inverse_mix_columns(state)
            log.append(f"Round {4-r} InvMixColumns: " +
                       format(state_to_int(state), '04x'))

    return state_to_int(state), log

# Mode operasi blok


def ecb_encrypt(plaintext_hex, key_hex, block_size=16):
    blocks = [plaintext_hex[i:i+4] for i in range(0, len(plaintext_hex), 4)]
    ciphertext = ""
    log = []
    for block in blocks:
        plaintext = int(block, 16)
        key = int(key_hex, 16)
        encrypted, block_log = encrypt_block(plaintext, key)
        ciphertext += format(encrypted, '04x')
        log.extend(block_log)
    return ciphertext, log


def ecb_decrypt(ciphertext_hex, key_hex):
    blocks = [ciphertext_hex[i:i+4] for i in range(0, len(ciphertext_hex), 4)]
    plaintext = ""
    log = []
    for block in blocks:
        ciphertext = int(block, 16)
        key = int(key_hex, 16)
        decrypted, block_log = decrypt_block(ciphertext, key)
        plaintext += format(decrypted, '04x')
        log.extend(block_log)
    return plaintext, log


def cbc_encrypt(plaintext_hex, key_hex, iv=None):
    if iv is None:
        iv = random.randint(0, 0xFFFF)
    iv_hex = format(iv, '04x')

    blocks = [plaintext_hex[i:i+4] for i in range(0, len(plaintext_hex), 4)]
    ciphertext = ""
    log = [f"IV: {iv_hex}"]
    prev_block = iv

    key = int(key_hex, 16)

    for block in blocks:
        plaintext = int(block, 16) ^ prev_block
        encrypted, block_log = encrypt_block(plaintext, key)
        ciphertext += format(encrypted, '04x')
        prev_block = encrypted
        log.extend(block_log)

    return iv_hex + ciphertext, log


def cbc_decrypt(ciphertext_hex, key_hex):
    iv = int(ciphertext_hex[:4], 16)
    blocks = [ciphertext_hex[i+4:i+8]
              for i in range(0, len(ciphertext_hex)-4, 4)]
    plaintext = ""
    log = [f"IV: {format(iv, '04x')}"]
    prev_block = iv

    key = int(key_hex, 16)

    for block in blocks:
        ciphertext = int(block, 16)
        decrypted, block_log = decrypt_block(ciphertext, key)
        plaintext_block = decrypted ^ prev_block
        plaintext += format(plaintext_block, '04x')
        prev_block = ciphertext
        log.extend(block_log)

    return plaintext, log

# Fungsi avalanche effect test


def avalanche_test():
    # Test perubahan 1-bit pada plaintext
    key = 0x2B7E
    plaintext1 = 0x3243
    plaintext2 = plaintext1 ^ 0x8000  # Ubah MSB

    cipher1, _ = encrypt_block(plaintext1, key)
    cipher2, _ = encrypt_block(plaintext2, key)

    diff = bin(cipher1 ^ cipher2).count('1')
    return f"Perubahan 1-bit pada plaintext mengubah {diff}/16 bit ciphertext"

# GUI Application


class MiniAESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-AES Encryption/Decryption")

        # Mode selection
        self.mode_var = tk.StringVar(value="ECB")
        self.mode_label = ttk.Label(root, text="Mode Operasi:")
        self.ecb_radio = ttk.Radiobutton(
            root, text="ECB", variable=self.mode_var, value="ECB")
        self.cbc_radio = ttk.Radiobutton(
            root, text="CBC", variable=self.mode_var, value="CBC")

        # Input fields
        self.plaintext_label = ttk.Label(root, text="Plaintext (hex):")
        self.plaintext_entry = ttk.Entry(root)

        self.ciphertext_label = ttk.Label(root, text="Ciphertext (hex):")
        self.ciphertext_entry = ttk.Entry(root)

        self.key_label = ttk.Label(root, text="Key (4 hex digits):")
        self.key_entry = ttk.Entry(root)
        self.generate_key_btn = ttk.Button(
            root, text="Generate Key", command=self.generate_key)

        self.iv_label = ttk.Label(root, text="IV (CBC mode, 4 hex digits):")
        self.iv_entry = ttk.Entry(root)
        self.generate_iv_btn = ttk.Button(
            root, text="Generate IV", command=self.generate_iv)

        # Buttons
        self.encrypt_button = ttk.Button(
            root, text="Encrypt", command=self.encrypt)
        self.decrypt_button = ttk.Button(
            root, text="Decrypt", command=self.decrypt)
        self.avalanche_btn = ttk.Button(
            root, text="Avalanche Test", command=self.run_avalanche_test)
        self.clear_btn = ttk.Button(root, text="Clear", command=self.clear_all)

        # File operations
        self.export_btn = ttk.Button(
            root, text="Export Log", command=self.export_log)
        self.import_btn = ttk.Button(
            root, text="Import File", command=self.import_file)

        # Log display
        self.log = tk.Text(root, height=15, width=70, wrap=tk.WORD)
        self.scrollbar = ttk.Scrollbar(
            root, orient=tk.VERTICAL, command=self.log.yview)
        self.log.configure(yscrollcommand=self.scrollbar.set)

        # Layout
        self.mode_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ecb_radio.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.cbc_radio.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        self.plaintext_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.plaintext_entry.grid(
            row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.ciphertext_label.grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ciphertext_entry.grid(
            row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.key_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.key_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        self.generate_key_btn.grid(row=3, column=2, padx=5, pady=5)

        self.iv_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.iv_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)
        self.generate_iv_btn.grid(row=4, column=2, padx=5, pady=5)

        self.encrypt_button.grid(row=5, column=0, padx=5, pady=5)
        self.decrypt_button.grid(row=5, column=1, padx=5, pady=5)
        self.avalanche_btn.grid(row=5, column=2, padx=5, pady=5)

        self.clear_btn.grid(row=6, column=0, padx=5, pady=5)
        self.export_btn.grid(row=6, column=1, padx=5, pady=5)
        self.import_btn.grid(row=6, column=2, padx=5, pady=5)

        self.log.grid(row=7, column=0, columnspan=3,
                      padx=5, pady=5, sticky=tk.NSEW)
        self.scrollbar.grid(row=7, column=3, sticky=tk.NS)

        # Configure grid weights
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Initialize IV for CBC mode
        self.generate_iv()

    def generate_key(self):
        key = random.randint(0, 0xFFFF)
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, f"{key:04x}")

    def generate_iv(self):
        iv = random.randint(0, 0xFFFF)
        self.iv_entry.delete(0, tk.END)
        self.iv_entry.insert(0, f"{iv:04x}")

    def encrypt(self):
        try:
            plaintext = self.plaintext_entry.get().strip()
            key = self.key_entry.get().strip()

            if not plaintext or not key:
                raise ValueError("Plaintext dan key harus diisi")
            if len(key) != 4:
                raise ValueError("Key harus 4 digit hex")

            mode = self.mode_var.get()
            self.log.insert(tk.END, f"\n=== ENCRYPTION ({mode} mode) ===\n")

            if mode == "ECB":
                ciphertext, logs = ecb_encrypt(plaintext, key)
            else:  # CBC
                iv = self.iv_entry.get().strip()
                if len(iv) != 4:
                    raise ValueError("IV harus 4 digit hex")
                ciphertext, logs = cbc_encrypt(plaintext, key, int(iv, 16))

            self.ciphertext_entry.delete(0, tk.END)
            self.ciphertext_entry.insert(0, ciphertext)

            for log in logs:
                self.log.insert(tk.END, log + "\n")

            self.log.insert(
                tk.END, f"\nEncrypted: {plaintext} -> {ciphertext}\n")
            self.log.see(tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.log.insert(tk.END, f"Error: {str(e)}\n")
            self.log.see(tk.END)

    def decrypt(self):
        try:
            ciphertext = self.ciphertext_entry.get().strip()
            key = self.key_entry.get().strip()

            if not ciphertext or not key:
                raise ValueError("Ciphertext dan key harus diisi")
            if len(key) != 4:
                raise ValueError("Key harus 4 digit hex")

            mode = self.mode_var.get()
            self.log.insert(tk.END, f"\n=== DECRYPTION ({mode} mode) ===\n")

            if mode == "ECB":
                plaintext, logs = ecb_decrypt(ciphertext, key)
            else:  # CBC
                if len(ciphertext) < 4:
                    raise ValueError(
                        "Ciphertext CBC harus termasuk IV (min 8 digit hex)")
                plaintext, logs = cbc_decrypt(ciphertext, key)

            self.plaintext_entry.delete(0, tk.END)
            self.plaintext_entry.insert(0, plaintext)

            for log in logs:
                self.log.insert(tk.END, log + "\n")

            self.log.insert(
                tk.END, f"\nDecrypted: {ciphertext} -> {plaintext}\n")
            self.log.see(tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.log.insert(tk.END, f"Error: {str(e)}\n")
            self.log.see(tk.END)

    def run_avalanche_test(self):
        result = avalanche_test()
        self.log.insert(tk.END, "\n=== AVALANCHE EFFECT TEST ===\n")
        self.log.insert(tk.END, result + "\n")
        self.log.see(tk.END)

    def clear_all(self):
        self.plaintext_entry.delete(0, tk.END)
        self.ciphertext_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.generate_iv()
        self.log.delete(1.0, tk.END)

    def export_log(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"),
                       ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            data = self.log.get(1.0, tk.END)
            try:
                if filename.endswith('.csv'):
                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        for line in data.split('\n'):
                            writer.writerow([line])
                else:
                    with open(filename, 'w') as f:
                        f.write(data)
                messagebox.showinfo("Success", f"Log saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def import_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"),
                       ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            try:
                if filename.endswith('.csv'):
                    with open(filename, 'r') as f:
                        reader = csv.reader(f)
                        content = '\n'.join([row[0] for row in reader])
                else:
                    with open(filename, 'r') as f:
                        content = f.read()

                # Try to detect if it's plaintext or ciphertext
                lines = content.split('\n')
                if any("cipher" in line.lower() for line in lines):
                    self.ciphertext_entry.delete(0, tk.END)
                    self.ciphertext_entry.insert(0, lines[-1].split()[-1])
                else:
                    self.plaintext_entry.delete(0, tk.END)
                    self.plaintext_entry.insert(0, lines[0].strip())

                self.log.insert(tk.END, f"\nLoaded content from {filename}\n")
                self.log.see(tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniAESApp(root)
    root.mainloop()
