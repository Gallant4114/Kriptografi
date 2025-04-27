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

5. Dokumentasi (15 poin) – Github
- Spesifikasi algoritma Mini-AES (5)
- Flowchart Mini-AES dan Key Expansion (5)
- Implementasi program
- Penjelasan TestCase
- Analisis: kelebihan dan keterbatasan Mini-AES (5)

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
