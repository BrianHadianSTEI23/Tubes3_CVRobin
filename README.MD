<div align="center">

#CVRobin
### *Sistem Pelacakan Pelamar Cerdas Anda*

</div>

**CVRobin** adalah sebuah *Applicant Tracking System* (ATS) berbasis desktop yang dirancang untuk menyederhanakan dan mengoptimalkan proses rekrutmen. Dibangun dengan Flet dan Python, aplikasi ini mampu mem-parsing, menganalisis, dan mencocokkan CV secara cerdas menggunakan serangkaian algoritma pencocokan string yang canggih.

Proyek ini merupakan Tugas Besar 3 untuk mata kuliah IF2211 Strategi Algoritma di Institut Teknologi Bandung.

---

## 🚀 Fitur Utama

- **Pencarian Cerdas:** Temukan kandidat terbaik dengan kata kunci spesifik.
- **Analisis Mendalam:** Ekstraksi informasi penting dari CV PDF secara otomatis.
- **Algoritma Fleksibel:** Pilih antara algoritma **KMP**, **Boyer-Moore**, atau **Aho-Corasick** untuk pencocokan.
- **Toleransi Kesalahan:** Fitur *Fuzzy Matching* dengan **Levenshtein Distance** untuk menangani salah ketik.
- **Keamanan Data:** Informasi pelamar dienkripsi menggunakan skema kustom untuk privasi maksimal.
- **Antarmuka Intuitif:** UI yang bersih dan modern dibangun dengan Flet.

---

## ⚙️ Algoritma Inti

CVRobin memanfaatkan dua algoritma pencocokan string utama untuk melakukan *exact matching*.

### Knuth-Morris-Pratt (KMP)
Algoritma KMP mengoptimalkan pencarian dengan menghindari perbandingan yang tidak perlu. Kunci dari KMP adalah tabel "border" (atau *failure function*) yang dibuat dari pola (kata kunci). Ketika terjadi ketidakcocokan, tabel ini memberitahu seberapa jauh pola bisa digeser tanpa kehilangan potensi kecocokan. Ini membuatnya jauh lebih efisien daripada pendekatan brute-force.

### Boyer-Moore (BM)
Algoritma Boyer-Moore seringkali menjadi yang tercepat dalam praktik. Keunggulannya terletak pada dua teknik: pemindaian dari kanan ke kiri (*looking-glass technique*) dan pergeseran cerdas (*character-jump technique*). Ketika ketidakcocokan ditemukan, BM menggunakan heuristik "bad character" untuk melakukan pergeseran besar, melompati bagian teks yang tidak relevan.

---

## 🛠️ Panduan Instalasi dan Penggunaan

Ikuti langkah-langkah berikut untuk menjalankan CVRobin di mesin lokal Anda.

### 1. Prasyarat
Pastikan Anda telah menginstal perangkat lunak berikut:
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- `uv` (Pengelola paket Python, instal dengan `pip install uv`)

### 2. Instalasi
Clone repository dan siapkan environment.

```bash
# 1. Clone repository ini
git clone [https://github.com/BrianHadianSTEI23/CVRobin.git](https://github.com/BrianHadianSTEI23/CVRobin.git)

# 2. Masuk ke direktori proyek
cd CVRobin

# 3. Buat virtual environment menggunakan uv
uv venv

# 4. Aktifkan virtual environment

# 5. Instal semua dependensi yang diperlukan


### 3. Konfigurasi Database
Aplikasi ini memerlukan koneksi ke database MySQL.


```.env

```

### 4. Menjalankan Aplikasi
Setelah semua dependensi terinstal dan database terkonfigurasi, jalankan aplikasi dengan perintah berikut:

```bash

```

Aplikasi CVRobin akan terbuka, dan Anda siap untuk mulai menganalisis CV!

---

## 👥 Dibuat Oleh Tim CVRobin

Proyek ini dibuat dengan cinta dan strategi algoritma oleh:

- **Abrar Abhirama W.** - `13523038`
- **Brian Albar Hadian** - `13523048`
- **Faqih M. Syuhada** - `13523057`

Program Studi Teknik Informatika, Institut Teknologi Bandung.
