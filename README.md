# Project Tengah Semester
## Kriptografi B Kelompok 10

## Anggota Kelompok
|Nama|NRP|
|-|-|
|M. Abhinaya Al Faruqi|5027231011|
|Gallant Damas H|50027231037|
|Dionisius Marcell Putra Indranto|5027231044|
|Johanes Edward Nathanael|5027231067|
***

## Dokumentasi

![Screenshot 2025-04-27 233922](https://github.com/user-attachments/assets/006fe7a5-1c08-4ef5-9d0e-258f0582166c)

### A. Spesifikasi algoritma Mini-AES
Berikut adalah spesifikasi dari algoritma
- Blok: 16-bit (4 nibbles)
- Kunci: 16-bit
- Operasi:
  - SubNibbles: Substitusi menggunakan S-box 4-bit
  - ShiftRows: Pergeseran pada baris kedua
  - MixColumns: Operasi campuran kolom di GF(2^4)
  - AddRoundKey: XOR dengan round key
- Jumlah Round: 3 round
- Key Expansion: Menggunakan rotasi dan substitusi nibble serta XOR dengan Rcon
- Mode Operasi:
  - ECB (Electronic Codebook)
  - CBC (Cipher Block Chaining) dengan IV


### B. Flowchart Mini-AES dan Key Expansion
**Flowchart Enkripsi:**
Start

  ↓
  
Input plaintext dan key

  ↓
  
Key Expansion

  ↓
  
Initial AddRoundKey

  ↓
  
FOR 1..3:
    - SubNibbles
    - ShiftRows
    - (MixColumns saat round bukan terakhir)
    - AddRoundKey
    
  ↓
  
Output Ciphertext

![image](https://github.com/user-attachments/assets/cbbac05a-41e2-47ce-ab85-f1ffa8a5e2b9)

![image](https://github.com/user-attachments/assets/8f945588-046b-450c-bb83-006d0989957f)

![image](https://github.com/user-attachments/assets/0b418157-c8f4-412f-8c2f-6fc07b588646)


**Flowchart Dekripsi:**

![image](https://github.com/user-attachments/assets/f6b79baf-4cc0-4e7f-807f-3905439f7ca8)

![image](https://github.com/user-attachments/assets/5b006ea8-cb81-421b-a942-f5d2cf7da726)

![image](https://github.com/user-attachments/assets/e91e6ab4-2f62-4bc7-bd5f-363c4cba9a8e)


**Flowchart Key Expansion:**
Input 16-bit Key

  ↓
  
Pisah menjadi 4 nibble

  ↓
  
FOR setiap round:
    - Rotasi nibble
    - Substitusi dengan S-box
    - XOR dengan Rcon
    - XOR dengan bagian key sebelumnya
    
  ↓
  
Output Round Keys

![image](https://github.com/user-attachments/assets/5d01e631-64d0-4d8a-b1d0-d6b0eb7f9850)

![image](https://github.com/user-attachments/assets/832315fc-6ff1-4673-b704-f0074f4caa81)

![image](https://github.com/user-attachments/assets/e83cc1ab-8ad1-4813-b932-665b0aadc463)


### C. Implementasi program
- Program ini ditulis dengan bahasa Python
- GUI dibuat dengan library Tkinter
- Isi program adalah sebagai berikut:
  - Enkripsi dan dekripsi Mini-AES
  - Mode ECB dan CBC
  - Avalanche Effect Testing
  - Import dan Export file

### D. Penjelasan TestCase

Enkripsi dengan ECB

![Screenshot 2025-04-27 235311](https://github.com/user-attachments/assets/f7ca78b6-c97e-4656-b056-e2f083034a41)

Dekripsi dengan ECB

![Screenshot 2025-04-27 235342](https://github.com/user-attachments/assets/429205bf-6492-44ba-96ce-5f4f4bb5f3ee)

Enkripsi dengan CBC

![Screenshot 2025-04-27 235513](https://github.com/user-attachments/assets/16e487a4-d163-44e1-a133-f916b81fb465)

Dekripsi dengan CBC

![Screenshot 2025-04-27 235552](https://github.com/user-attachments/assets/2f01e8d1-4202-4088-b691-afbfc8487db6)

**Test Case Avalanche**

Menggunakan Sample Key yang sama yaitu 1A2B dengan Plaintext 1(0123) dan Plaintext 2(0122) yang hanya memiliki perbedaan 1 bit, memberikan hasil yang berbeda sesuai dengan Avalanche Test
![image](https://github.com/user-attachments/assets/f211e432-4c08-4543-8261-8bd5916f6e21)

![image](https://github.com/user-attachments/assets/1e2943c8-3b69-4008-a755-ef5f44d4798a)

Jika dibandingkan, 
Ciphertext C1: 1dbc (biner 0001 1101 1011 1100)

Ciphertext C2: e1a6 (biner 1110 0001 1010 0110)

Lakukan XOR maka hasilnya: 1111 1100 0001 1010 

Jika kita menghitung hasil pada XOR: 1+1+1+1 + 1+1+0+0 + 0+0+0+1 + 1+0+1+0 = 4 + 2 + 1 + 2 = 9 bit. Maka Testcase Avalanche berhasil karena 9/16 bit atau 56% output telah terubah hanya berdasarkan 1 perubahan input. 


### E. Analisis: kelebihan dan keterbatasan Mini-AES
**Kelebihan**
1. Implementasi ringan untuk pembelajaran dasar kriptografi.
2. Struktur mirip AES karena terdapat SubBytes, ShiftRows, MixColumns, AddRoundKey.
3. Mudah dipahami: Blok kecil (16-bit) dan menggunakan algoritma sederhana.

**Keterbatasan**
1. Tidak aman untuk penggunaan nyata karena ukuran blok kecil sehingga mudah bruteforce.
2. Key Expansion sederhana tidak kompleks seperti AES standar.
3. Tidak mendukung padding: Harus input kelipatan 16-bit.

***

### A. Spesifikasi Dasar
1. Implementasi Mini-AES 16-bit (35 poin)
- Representasi plaintext dan key: 16-bit (4 nibble) (2,5)
- Operasi meliputi:

  - SubNibbles (menggunakan S-Box 4-bit) (8)
  - ShiftRows (5)
  - MixColumns (dengan matriks sederhana pada GF(24)) (10)
  - AddRoundKey (7)

- Jumlah round: 3 (2,5)

2. Key Expansion (Round Key Generator) (20 poin)
- Key awal: 16-bit (10)
- Algoritma key expansion sederhana untuk menghasilkan round keys (10)

3. Program (30 poin)
- Menerima Input: Plaintext (16-bit) dan key (16-bit) (5)
- Mengeluarkan Output: Ciphertext (16-bit) (5)
- Minimal 3 test case dengan expected output benar (10)
- Tampilkan output proses tiap round (5)
- Memiliki GUI, menggunakan Tkinter, Streamlit (web-based), dsb (5)

### Spesifikasi Tambahan
1. Implementasi Dekripsi Mini-AES (7 poin)
- Tambahkan fungsi dekripsi
- Implementasi inverse operations:

  - Inverse S-Box
  - Inverse MixColumns
  - Inverse ShiftRows

- Output dekripsi harus menghasilkan kembali plaintext awal

3. Analisis Keamanan dan Avalanche Effect (5 poin)
- Uji sensitivitas terhadap perubahan 1-bit di plaintext atau key
- Jelaskan efek avalanche (bit perubahan pada ciphertext)

4. Mode Operasi Blok (ECB/CBC) (6 poin)
- Tambahkan implementasi mode operasi blok:

  - ECB (Electronic Codebook)
  - CBC (Cipher Block Chaining) lengkap dengan simulasi IV (Initialization Vector).

- Mendukung input teks lebih panjang dari 16-bit (contoh: 64-bit diproses sebagai 4 blok).
- Proses enkripsi/dekripsi harus mempertahankan mode terpilih.

6. Export dan Import File (2 poin)
- Simpan input/output dan log proses ke file TXT/CSV
- Load file untuk proses enkripsi/dekripsi
