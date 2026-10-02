# Instruksi Submission: Membangun ETL Pipeline Sederhana

Panduan lengkap pengerjaan dan penilaian Proyek Akhir kelas **Belajar Fundamental Pemrosesan Data** di Dicoding.

---

## 1. Pengantar

Selamat kepada Anda yang telah menyelesaikan seluruh materi kelas Belajar Fundamental Pemrosesan Data!

### Rangkuman Materi Pembelajaran
- **Software Engineering dengan Python:** Membangun fondasi kuat mencakup praktik terbaik penulisan kode modular, pengelolaan proyek, dan unit testing.
- **Repositori Data:** Memahami berbagai jenis repositori penyimpanan data mulai dari flat file (CSV), database relasional (PostgreSQL), hingga NoSQL dan cloud spreadsheet (Google Sheets).
- **ETL Pipeline:** Menguasai konsep dan implementasi ekstraksi data (web scraping), transformasi data (pembersihan, penanganan missing values, konversi tipe data), serta pemuatan data (loading) ke repositori data.
- **Automasi Python:** Menerapkan penjadwalan tugas dan automasi alur kerja pemrosesan data.

### Studi Kasus
Anda adalah seorang **Data Engineer** yang bekerja untuk sebuah perusahaan retail fashion dan design. Di tengah persaingan pasar yang pesat, kompetitor kerap memainkan harga, promo, dan variasi model baju. Perusahaan menugaskan tim data untuk meneliti harga dan produk kompetitor terpilih, yaitu **Fashion Studio** (memasarkan t-shirt, pants, jacket, outerwear, hoodie, crewneck, dll.).

- **Target Website Scrape:** [https://fashion-studio.dicoding.dev](https://fashion-studio.dicoding.dev)
- **Tugas Utama:** Membangun alur ETL (*Extract, Transform, Load*) sederhana untuk mengambil data kompetitor dari 50 halaman website, membersihkan serta memvalidasi data, dan menyimpannya ke repositori data agar siap digunakan oleh tim Data Science.

---

## 2. Kriteria Submission

Setiap kriteria memiliki bobot penilaian 0 sampai 4 poin (*points*). Untuk dinyatakan **Lulus**, Anda wajib mendapatkan minimal **2 poin (Basic)** pada setiap kriteria. Submission akan ditolak (*Reject*) jika ada kriteria yang bernilai 0 poin.

### Kriteria 1: Membuat ETL Pipeline dengan Prinsip Modular Code
Pipeline ETL harus dibangun dengan prinsip modularitas kode, di mana kode tahapan *extract*, *transform*, dan *load* dipisahkan ke dalam berkas Python masing-masing (misal di dalam folder `utils/`). Seluruh proses diorkestrasi melalui `main.py` dan wajib melampirkan `requirements.txt`.

#### Rekomendasi Struktur Direktori:
```text
submission-pemda/
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── main.py
├── requirements.txt
├── submission.txt
├── products.csv
└── google-sheets-api.json
```

#### Rubrik Penilaian Kriteria 1:
- **Reject (0 pts):**
  - Tahapan ETL tidak disimpan dalam berkas terpisah atau dibuat dalam bentuk notebook (`.ipynb`).
  - Tidak melampirkan berkas `requirements.txt`.
  - Ekstraksi tidak mengambil data dari website resmi `https://fashion-studio.dicoding.dev/`.
  - Data hasil scraping tidak mencakup atribut: *Title, Price, Colors, Size, Gender*.
  - Tahap transformasi gagal: kolom `Price` tidak dikonversi ke Rupiah (kurs Rp16.000), terdapat nilai null, data duplikat, data invalid, atau tipe data tidak sesuai rubrik.
  - Tahap load gagal: data yang disimpan tidak bersih atau tidak disimpan dalam format `.CSV`.
- **Basic (2 pts):**
  - Berhasil mengekstrak data dari seluruh 50 halaman website (halaman 1 s.d. 50) dengan total awal 1.000 data.
  - Mengambil atribut: `Title`, `Price`, `Rating`, `Colors`, `Size`, dan `Gender`.
  - Transformasi data:
    - Kolom `Price` dikonversi dari Dolar ke Rupiah dengan kurs Rp16.000.
    - Menghapus data bernilai null (`.dropna()`) dan data duplikat (`.drop_duplicates()`).
    - Menghapus data invalid seperti produk bernama `"Unknown Product"`.
    - Kolom `Rating` bertipe float murni (bukan string `"Invalid Rating"` atau `"4.8 / 5"`).
    - Kolom `Colors` bertipe integer/angka saja (bukan string `"3 Colors"`).
    - Kolom `Size` bertipe string ukuran saja (tanpa teks awalan `"Size: "`).
    - Kolom `Gender` bertipe string jenis kelamin saja (tanpa teks awalan `"Gender: "`).
  - Loading data: menyimpan data hasil pembersihan ke dalam berkas `.CSV`.
- **Skilled (3 pts):**
  - Memenuhi seluruh ketentuan Basic.
  - Menambahkan kolom baru bernama `timestamp` yang mencatat waktu tahapan ekstraksi data (web scraping).
- **Advanced (4 pts):**
  - Memenuhi seluruh ketentuan Skilled.
  - Setiap fungsi dalam berkas tahapan ETL pipeline (`extract.py`, `transform.py`, `load.py`) memiliki setidaknya satu mekanisme penanganan kesalahan (*error handling* / try-except).

---

### Kriteria 2: Menyimpan Data dalam Repositori Data
Data hasil pipeline harus disimpan ke dalam repositori data yang didukung agar dapat diakses kembali oleh tim data.

#### Tiga Jenis Repositori yang Diizinkan:
1. **Flat File (CSV):** Berkas `products.csv`.
2. **Google Sheets:**
   - Akses spreadsheet diatur ke *"Anyone with the link"* sebagai **EDITOR**.
   - Melampirkan berkas kredensial service account Google Sheets API (`google-sheets-api.json`).
3. **PostgreSQL Database:** Menyimpan data ke dalam tabel basis data relasional PostgreSQL.

*(Catatan: Tidak diperkenankan menggunakan jenis repositori di luar ketiga jenis di atas. Setiap fungsi penyimpanan wajib dipisahkan secara modular).*

#### Rubrik Penilaian Kriteria 2:
- **Reject (0 pts):**
  - ETL pipeline tidak menyimpan data ke repositori mana pun.
  - Menyimpan ke jenis repositori yang tidak diizinkan.
  - Google Sheets tidak dapat diakses reviewer atau tidak melampirkan berkas Service Account (`.json`).
- **Basic (2 pts):**
  - ETL pipeline berhasil menyimpan data ke dalam 1 repositori: berkas `.CSV`.
- **Skilled (3 pts):**
  - ETL pipeline berhasil menyimpan data ke dalam 2 repositori: `.CSV` dan Google Sheets, atau `.CSV` dan PostgreSQL.
- **Advanced (4 pts):**
  - ETL pipeline berhasil menyimpan data ke dalam **3 jenis repositori data sekaligus**: `.CSV`, Google Sheets, dan PostgreSQL.

---

### Kriteria 3: Menerapkan Unit Test
ETL pipeline wajib divalidasi mutunya melalui pengujian otomatis (*unit testing*).

#### Ketentuan Unit Testing:
- Seluruh berkas unit test wajib diletakkan dalam satu folder khusus bernama `tests/` (misalnya: `test_extract.py`, `test_transform.py`, `test_load.py`).
- Menguji fungsi-fungsi ETL yang dibangun.
- Disarankan menggunakan teknik mocking (`unittest.mock`) untuk fungsi yang berinteraksi dengan eksternal (HTTP requests, database, API Google Sheets).
- Pengujian dijalankan tanpa error atau kegagalan (*0 failures, 0 errors*).

#### Rubrik Penilaian Kriteria 3:
- **Reject (0 pts):**
  - Proyek tidak memiliki unit test, berkas test tidak berada di folder `tests/`, test mengalami kegagalan/error, atau *test coverage* di bawah 20%.
- **Basic (2 pts):**
  - Memiliki unit test di folder `tests/` dengan *test coverage* minimal 20%.
- **Skilled (3 pts):**
  - Memenuhi kriteria sebelumnya dengan *test coverage* berada pada rentang **50% – 79%**.
- **Advanced (4 pts):**
  - Memenuhi kriteria sebelumnya dengan *test coverage* mencapai **80% – 100%**.

---

## 3. Ketentuan Penilaian

### Formula Perhitungan Nilai Akhir
Nilai akhir submission ditentukan menggunakan formula:
$$\text{Nilai Akhir} = \frac{\text{Total Points}}{\text{Jumlah Kriteria}}$$

*(Formula di atas berlaku apabila setiap kriteria mendapatkan minimal 2 poin / tidak ada kriteria yang ditolak).*

### Tabel Skala Penilaian Submission
| Nilai Akhir | Predikat Dicoding | Nilai Huruf | Level of Mastery | Makna Nilai | Keterangan |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **< 1.0** | **Rejected** | E | - | Tidak Lulus | Belum memenuhi kompetensi minimal. |
| **1.0 – < 2.0** | **Bintang 2** | D | Below Basic | Kurang | Memenuhi kompetensi minimal tetapi perlu banyak peningkatan. |
| **2.0 – < 3.0** | **Bintang 3** | C | Basic | Cukup | Memenuhi seluruh kompetensi dasar dari learning objective. |
| **3.0 – < 4.0** | **Bintang 4** | B | Skilled | Mahir | Memenuhi seluruh kriteria kompetensi dengan mahir. |
| **4.0** | **Bintang 5** | A | Advanced | Tingkat Lanjut | Memenuhi seluruh kriteria pada level tertinggi (*Advanced*). |

---

## 4. Tips dan Trik

1. **Struktur Tag HTML Price:**
   - Pada website target, elemen harga memiliki variasi tag HTML antara harga valid (misal: `$100.00` dengan kelas `.price`) dan produk yang tidak memiliki harga (`Price Unavailable`). Pastikan penanganan selektor menangani kedua kondisi ini.
2. **Method Pandas yang Membantu Transformasi:**
   - `.replace()`: Membersihkan string atau mengganti simbol mata uang.
   - `str.extract(r'...')`: Mengekstrak angka atau pola tertentu dari string (seperti rating numerik atau jumlah warna).
   - `.strip()`: Menghilangkan spasi berlebih pada awal/akhir teks.
   - `.drop_duplicates()`: Menghapus baris rekaman yang duplikat.
   - `.dropna()`: Menghapus baris yang mengandung *missing value* / NaN.
3. **Error Handling:**
   - Terapkan blok `try...except` pada setiap fungsi penting dengan pencatatan log (*logging*) agar alur program tidak terputus seketika dan reviewer dapat melihat penanganan kesalahan yang baik.
4. **Mocking dalam Unit Test:**
   - Gunakan `unittest.mock.patch` atau fixture `pytest-mock` saat menguji fungsi scraping (`requests.Session.get`), koneksi database (`psycopg2` / `create_engine`), dan API Google Sheets (`googleapiclient.discovery.build`). Mocking memastikan pengujian berjalan cepat, deterministik, dan dapat dijalankan di lingkungan CI/reviewer yang terisolasi.
5. **Rekomendasi Dependensi (`requirements.txt`):**
   ```text
   python-crontab~=3.2
   sqlalchemy~=2.0
   psycopg2-binary~=2.9
   pandas~=2.2
   requests~=2.32
   beautifulsoup4~=4.12
   google-auth~=2.36
   google-api-python-client~=2.152
   pytest~=8.0
   pytest-cov~=6.0
   python-dotenv~=1.0
   ```
6. **Exploratory Data Analysis (EDA):**
   - Lakukan eksplorasi awal struktur HTML dan tipe data hasil ekstraksi untuk memastikan seluruh pola teks abnormal teridentifikasi sebelum menyusun modul pembersihan data akhir.

---

## 5. Lainnya

### Ketentuan Pengiriman Berkas Submission
- **Wajib Menyertakan Berkas `submission.txt`:**
  Berkas ini berisi petunjuk eksekusi bagi reviewer dengan format:
  ```bash
  # Menjalankan skrip
  python3 main.py

  # Menjalankan unit test pada folder tests
  python3 -m pytest tests

  # Menjalankan test coverage pada folder tests
  coverage run -m pytest tests

  # Url Google Sheets:
  https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit?usp=sharing
  ```
- **Melampirkan `products.csv`:** Berkas CSV hasil pembersihan data wajib disertakan di root project.
- **Melampirkan `google-sheets-api.json`:** Berkas kredensial service account Google Sheets.
- **Pengemasan Berkas (ZIP):**
  - Berkas submission diunggah dalam format ZIP.
  - **PENTING:** Jangan menyertakan virtual environment (folder `.venv/` atau `env/`) ke dalam arsip ZIP untuk menghindari ukuran berkas yang membengkak.
  - Pastikan tidak membuat struktur *ZIP di dalam ZIP*.

### Ketentuan Submission Ditolak (*Reject*)
Submission akan langsung ditolak jika:
1. Setiap kriteria submission tidak terpenuhi (ada kriteria bernilai 0 pts).
2. Ketentuan kelengkapan berkas submission tidak terpenuhi.
3. Terbukti melakukan kecurangan, plagiasi, atau mengumpulkan pekerjaan pihak lain tanpa izin.

### Ketentuan Proses Review
- Tim Reviewer mengulas submission dalam waktu selambat-lambatnya 3 (tiga) hari kerja (tidak termasuk akhir pekan dan hari libur nasional).
- Mekanisme review difokuskan pada fungsionalitas aplikasi, integritas data, dan pengujian.
- Notifikasi hasil review akan dikirimkan melalui email terdaftar dan dapat dipantau langsung pada dashboard Dicoding.