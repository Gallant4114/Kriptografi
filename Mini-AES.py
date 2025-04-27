# library buat GUI
import tkinter as tk
from tkinter import ttk

# s-box dan inverse s-box untuk subtitusi
Sbox = [
    0xA, 0x4, 0x3, 0xB,
    0x8, 0xE, 0x2, 0x5,
    0x1, 0xF, 0x9, 0xC,
    0x6, 0x0, 0xD, 0x7
]

# membuat invers s-box berdasarkan s-box
InvSbox = [0] * 16
for i, val in enumerate(Sbox):
    InvSbox[val] = i

# Fungsi perkalian dalam Galois Field / GF(2^4)
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
    return result & 0xF  # hasil 4bit

# fungsi menghasilkan round keys dari key utama
def key_expansion(key):
    nibbles = [(key >> 12) & 0xF, (key >> 8) & 0xF, (key >> 4) & 0xF, key & 0xF]
    round_keys = [(nibbles[0] << 12) | (nibbles[1] << 8) | (nibbles[2] << 4) | nibbles[3]]
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

# integer 16 bit dikonversi ke state matrix 2x2
def int_to_state(n):
    return [
        [(n >> 12) & 0xF, (n >> 8) & 0xF],
        [(n >> 4) & 0xF, n & 0xF]
    ]

# konversi state matrix ke integer 16 bit
def state_to_int(state):
    return (state[0][0] << 12) | (state[0][1] << 8) | (state[1][0] << 4) | state[1][1]

# subtitusi setiap nibble dengan s-box
def sub_nibbles(state, sbox):
    return [[sbox[cell] for cell in row] for row in state]

# shiftrow mini AES, elemen baris kedua di-swap
def shift_rows(state):
    return [state[0], [state[1][1], state[1][0]]]

# fungsi MixColumns (ubah kolom state dengan operasi GF)
def mix_columns(state):
    new_state = [[0]*2 for _ in range(2)]
    for i in range(2):
        a = state[0][i]
        b = state[1][i]
        new_state[0][i] = gf_mult(1, a) ^ gf_mult(4, b)
        new_state[1][i] = gf_mult(4, a) ^ gf_mult(1, b)
    return new_state

# Inverse MixColumns untuk dekripsi
def inverse_mix_columns(state):
    new_state = [[0]*2 for _ in range(2)]
    for i in range(2):
        a = state[0][i]
        b = state[1][i]
        new_state[0][i] = gf_mult(9, a) ^ gf_mult(2, b)
        new_state[1][i] = gf_mult(2, a) ^ gf_mult(9, b)
    return new_state

# AddRoundKey (XOR antara state dan kunci round)
def add_round_key(state, round_key):
    key_state = int_to_state(round_key)
    return [[state[i][j] ^ key_state[i][j] for j in range(2)] for i in range(2)]

# enkripsi mini AES
def encrypt(plaintext, key):
    round_keys = key_expansion(key)
    state = int_to_state(plaintext)
    state = add_round_key(state, round_keys[0])
    log = [f"After initial AddRoundKey: {state_to_int(state):04x}"]
    for r in range(1, 4):
        state = sub_nibbles(state, Sbox)
        state = shift_rows(state)
        if r != 3:
            state = mix_columns(state)
        state = add_round_key(state, round_keys[r])
        log.append(f"Round {r} output: {state_to_int(state):04x}")
    return state_to_int(state), log

# Dekripsi mini AES
def decrypt(ciphertext, key):
    round_keys = key_expansion(key)
    state = int_to_state(ciphertext)
    state = add_round_key(state, round_keys[3])
    log = [f"After initial AddRoundKey (K3): {state_to_int(state):04x}"]
    for r in range(3, 0, -1):
        state = shift_rows(state)
        state = sub_nibbles(state, InvSbox)
        state = add_round_key(state, round_keys[r-1])
        if r != 1:
            state = inverse_mix_columns(state)
        log.append(f"Round {4 - r} decryption step: {state_to_int(state):04x}")
    return state_to_int(state), log

# GUI dengan Tkinter
class MiniAESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-AES Encryption/Decryption")
        
        self.plaintext_label = ttk.Label(root, text="Plaintext (4 hex digits):")
        self.plaintext_entry = ttk.Entry(root)
        
        self.ciphertext_label = ttk.Label(root, text="Ciphertext (4 hex digits):")
        self.ciphertext_entry = ttk.Entry(root)
        
        self.key_label = ttk.Label(root, text="Key (4 hex digits):")
        self.key_entry = ttk.Entry(root)
        
        self.encrypt_button = ttk.Button(root, text="Encrypt", command=self.encrypt)
        self.decrypt_button = ttk.Button(root, text="Decrypt", command=self.decrypt)
        
        self.log = tk.Text(root, height=10, width=50)
        
        # layout GUI
        self.plaintext_label.grid(row=0, column=0, padx=5, pady=5)
        self.plaintext_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.ciphertext_label.grid(row=1, column=0, padx=5, pady=5)
        self.ciphertext_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.key_label.grid(row=2, column=0, padx=5, pady=5)
        self.key_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.encrypt_button.grid(row=3, column=0, padx=5, pady=5)
        self.decrypt_button.grid(row=3, column=1, padx=5, pady=5)
        
        self.log.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    def encrypt(self):
        try:
            plaintext = int(self.plaintext_entry.get(), 16)
            key = int(self.key_entry.get(), 16)
            ciphertext, logs = encrypt(plaintext, key)
            self.ciphertext_entry.delete(0, tk.END)
            self.ciphertext_entry.insert(0, f"{ciphertext:04x}")

            for log in logs :
                self.log.insert(tk.END, log + '\n')

            self.log.insert(tk.END, f"Encrypted: {plaintext:04x} -> {ciphertext:04x}\n")
        except ValueError:
            self.log.insert(tk.END, "Error: Invalid input (use hex digits)\n")
    
    def decrypt(self):
        try:
            ciphertext = int(self.ciphertext_entry.get(), 16)
            key = int(self.key_entry.get(), 16)
            plaintext, logs = decrypt(ciphertext, key)
            self.plaintext_entry.delete(0, tk.END)
            self.plaintext_entry.insert(0, f"{plaintext:04x}")

            for log in logs :
                self.log.insert(tk.END, log + '\n')

            self.log.insert(tk.END, f"Decrypted: {ciphertext:04x} -> {plaintext:04x}\n")
        except ValueError:
            self.log.insert(tk.END, "Error: Invalid input (use hex digits)\n")

# start GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniAESApp(root)
    root.mainloop()