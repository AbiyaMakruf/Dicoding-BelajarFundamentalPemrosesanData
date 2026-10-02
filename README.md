# Dicoding - Belajar Fundamental Pemrosesan Data

## Penilaian Proyek
Proyek ini merupakan submission akhir untuk kelas Dicoding **Belajar Fundamental Pemrosesan Data (BFPD)** yang dirancang untuk meraih predikat tertinggi **Bintang 5 / Advanced (4.0 Poin)**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![pandas 2.2.x](https://img.shields.io/badge/pandas-2.2.x-orange.svg)](https://pandas.pydata.org/)
[![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup-4.13.x-purple.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![SQLAlchemy 2.0.x](https://img.shields.io/badge/SQLAlchemy-2.0.x-red.svg)](https://www.sqlalchemy.org/)
[![Pytest 99% Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen.svg)](#pengujian-dan-evaluasi-unit-testing--coverage)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Completed (Bintang 5 / Advanced)](https://img.shields.io/badge/Status-Completed%20(Bintang%205)-brightgreen.svg)](#)

---

## Deskripsi Project
Proyek ini membangun alur kerja **ETL (Extract, Transform, Load) Pipeline** otomatis berskala produksi (*production-grade*) untuk mengumpulkan, membersihkan, dan memuat data produk fashion dari kompetitor retail **Fashion Studio** ([https://fashion-studio.dicoding.dev](https://fashion-studio.dicoding.dev)).

Pipeline ini dirancang dengan prinsip **Modular Software Engineering**, kepatuhan pada standar konversi data, penanganan galat (*robust error handling*) di setiap fungsi, dan validasi komprehensif melalui **Unit Testing** dengan cakupan pengujian mencapai **99%**.

Seluruh kriteria penilaian telah dipenuhi hingga tingkat tertinggi:
1. **Kriteria 1 (Modular Code & Error Handling): Advanced (4.0 pts)** — Pemisahan modul `extract.py`, `transform.py`, `load.py`, penambahan kolom `timestamp`, scraping 50 halaman (1.000 data mentah), dan *try-except error handling* pada setiap fungsi.
2. **Kriteria 2 (Repositori Data Multi-Penyimpanan): Advanced (4.0 pts)** — Dukungan pemuatan data ke **3 jenis repositori**: Flat file (CSV), Google Sheets via Google Sheets API (Service Account), dan Relational Database (PostgreSQL via SQLAlchemy).
3. **Kriteria 3 (Unit Testing & Test Coverage): Advanced (4.0 pts)** — Memiliki 62 pengujian otomatis di direktori `tests/` tanpa kegagalan dengan *code coverage* sebesar **99%** (standar Advanced: 80%–100%).

---

## Daftar Isi
- [Struktur Repositori](#struktur-repositori)
- [Gambaran Dataset](#gambaran-dataset)
- [Arsitektur dan Alur ETL Pipeline](#arsitektur-dan-alur-etl-pipeline)
  - [1. Ekstraksi Data (Extract)](#1-ekstraksi-data-extract)
  - [2. Transformasi dan Pembersihan Data (Transform)](#2-transformasi-dan-pembersihan-data-transform)
  - [3. Pemuatan Data (Load)](#3-pemuatan-data-load)
- [Pengujian dan Evaluasi (Unit Testing & Coverage)](#pengujian-dan-evaluasi-unit-testing--coverage)
- [Instalasi dan Setup](#instalasi-dan-setup)
- [Panduan Menjalankan Pipeline](#panduan-menjalankan-pipeline)
- [Ketentuan Berkas Submission](#ketentuan-berkas-submission)

---

## Struktur Repositori

```text
Dicoding-BelajarFundamentalPemrosesanData/
├── main.py                     # Skrip utama orkestrator ETL Pipeline
├── requirements.txt            # Dependensi pustaka Python
├── submission.txt              # Berkas petunjuk eksekusi submission untuk reviewer
├── products.csv                # Data hasil akhir pembersihan (867 baris x 7 atribut)
├── README.md                   # Dokumentasi lengkap proyek
├── utils/                      # Modul modular kode ETL
│   ├── __init__.py             # Inisialisasi package utils
│   ├── extract.py              # Logika web scraping 50 halaman + timestamp
│   ├── transform.py            # Pembersihan, filtering data invalid, konversi kurs
│   └── load.py                 # Pemuatan data ke CSV, Google Sheets, & PostgreSQL
├── tests/                      # Rangkaian pengujian unit test otomatis
│   ├── __init__.py             # Inisialisasi package tests
│   ├── test_extract.py         # Unit test modul ekstraksi (HTTP mocking & parsing)
│   ├── test_transform.py       # Unit test modul transformasi & konversi tipe
│   └── test_load.py            # Unit test modul pemuatan (CSV, Sheets API, DB mock)
└── ai-agent/                   # Dokumen referensi dan instruksi submission
    ├── instruksi_submission.md # Panduan submission yang telah dirapikan (5 section)
    ├── contoh-readme.md        # Templat acuan dokumentasi proyek
    └── menyimpan_data_ke_googlesheet.md # Panduan integrasi Google Sheets API
```

---

## Gambaran Dataset

Dataset diekstraksi secara langsung dari situs web katalog produk **Fashion Studio** ([https://fashion-studio.dicoding.dev](https://fashion-studio.dicoding.dev)) yang mencakup **50 halaman** (*20 produk per halaman*) dengan total **1.000 data mentah**.

### Skema Atribut Data Bersih (`products.csv`)

| Nama Kolom | Tipe Data | Deskripsi Atribut | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| **`Title`** | `object (str)` | Nama produk pakaian (di luar 'Unknown Product') | `T-shirt 2` |
| **`Price`** | `float64` | Harga produk terkonversi ke Rupiah (Kurs: Rp16.000) | `1634400.0` |
| **`Rating`** | `float64` | Rating produk murni dalam bentuk desimal | `3.9` |
| **`Colors`** | `int64` | Jumlah varian warna pakaian (angka murni) | `3` |
| **`Size`** | `object (str)` | Ukuran pakaian (dibersihkan dari prefix `Size: `) | `M` |
| **`Gender`** | `object (str)` | Kategori jenis kelamin (dibersihkan dari prefix `Gender: `) | `Women` |
| **`timestamp`** | `object (str)` | Waktu ISO 8601 saat ekstraksi data berlangsung | `2026-10-02T17:56:04.296607` |

---

## Arsitektur dan Alur ETL Pipeline

```mermaid
flowchart LR
    A["Website Target\n(fashion-studio.dicoding.dev)\n50 Halaman (1.000 Item)"] -->|requests + bs4| B["Extract (utils/extract.py)\n- Web scraping 50 halaman\n- Rekam timestamp ISO\n- Error handling"]
    B -->|Raw DataFrame| C["Transform (utils/transform.py)\n- Filter 'Unknown Product'\n- Konversi USD ke IDR (x16.000)\n- Parsing Rating float & Colors int\n- Strip 'Size:' & 'Gender:'\n- Drop Duplicates & Dropna"]
    C -->|Clean DataFrame (867 rows)| D["Load (utils/load.py)"]
    D --> E["1. Flat File\nproducts.csv"]
    D --> F["2. Cloud Spreadsheet\nGoogle Sheets API"]
    D --> G["3. Relational DB\nPostgreSQL Table"]
```

### 1. Ekstraksi Data (Extract)
- **Fungsi:** `fetch_page()`, `parse_product_card()`, `scrape_page()`, `extract_data()`.
- **Target:** Mengiterasi seluruh 50 halaman secara berurutan menggunakan `requests.Session` yang dioptimalkan dengan header *User-Agent* peramban modern.
- **Kriteria Skilled:** Menyisipkan kolom `timestamp` pada setiap produk yang dicatat pada saat scraping berlangsung.
- **Kriteria Advanced:** Dilengkapi blok `try...except` pada setiap fungsi untuk menangani galat jaringan (`requests.RequestException`), kartu produk yang tidak lengkap, maupun kegagalan tak terduga.

### 2. Transformasi dan Pembersihan Data (Transform)
- **Fungsi:** `clean_price()`, `clean_rating()`, `clean_colors()`, `clean_size()`, `clean_gender()`, `filter_invalid_products()`, `transform_data()`.
- **Tahapan Pembersihan:**
  1. **Filtering Nilai Invalid:** Menghapus produk bernilai `"Unknown Product"` (*100 baris tereliminasi*).
  2. **Pembersihan Harga:** Mengonversi harga Dolar (`$xxx.xx`) ke Rupiah (dikali Rp16.000) dan mengonversi produk `"Price Unavailable"` menjadi `None`.
  3. **Pembersihan Rating:** Mengekstrak angka desimal murni dari pola string (misal `"Rating: ⭐ 3.9 / 5"` $\rightarrow$ `3.9`), serta mengeliminasi `"Invalid Rating"` dan `"Not Rated"`.
  4. **Pembersihan Warna:** Mengekstrak bilangan bulat dari pola `"X Colors"` $\rightarrow$ `X` bertipe integer.
  5. **Pembersihan Ukuran & Gender:** Menghilangkan teks awalan `"Size: "` dan `"Gender: "`.
  6. **Deduplikasi & Dropna:** Menjalankan `.drop_duplicates()` dan `.dropna()` untuk menjamin data bebas dari baris ganda dan nilai kosong (*33 baris bernilai null dihapus*).
  7. **Hasil Akhir:** Menghasilkan **867 baris data bersih** dengan skema tipe data yang 100% konsisten.

### 3. Pemuatan Data (Load)
- **Fungsi:** `load_to_csv()`, `load_to_google_sheets()`, `load_to_postgres()`, `load_data()`.
- **Dukungan 3 Repositori Data (Advanced 4 Poin):**
  1. **Flat File (CSV):** Menyimpan langsung ke berkas `products.csv` menggunakan encoding UTF-8.
  2. **Google Sheets:** Menggunakan OAuth2 Service Account (`google-sheets-api.json`) dan `google-api-python-client` untuk menuliskan baris data ke Google Spreadsheet.
  3. **PostgreSQL:** Menggunakan SQLAlchemy `create_engine` dan `psycopg2-binary` untuk memuat tabel basis data `products`.

---

## Pengujian dan Evaluasi (Unit Testing & Coverage)

Seluruh komponen ETL pipeline diuji menggunakan pustaka **pytest** dan **coverage**. Teknik isolasi pengujian (*mocking*) menggunakan `unittest.mock` diterapkan untuk mensimulasikan respons HTTP eksternal, otentikasi Google Sheets API, dan koneksi engine database relasional.

### Hasil Coverage Pengujian (`pytest --cov=utils`)

| Modul Pengujian | Berkas Kode | Jumlah Baris (Stmts) | Baris Terlewat (Miss) | Coverage (%) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `tests/test_extract.py` | `utils/extract.py` | 97 | 0 | **100%** | PASS |
| `tests/test_transform.py` | `utils/transform.py` | 114 | 0 | **100%** | PASS |
| `tests/test_load.py` | `utils/load.py` | 98 | 3 | **97%** | PASS |
| **TOTAL KESELURUHAN** | **`utils/`** | **309** | **3** | **99%** | **PASS (Bintang 5)** |

> Standar Kriteria Advanced Dicoding adalah **80% – 100%**. Proyek ini berhasil melampaui batas minimum dengan capaian **99%** dan **62 test cases berhasil dilewati tanpa kegagalan (0 errors, 0 failures)**.

---

## Instalasi dan Setup

1. **Clone repositori:**
   ```bash
   git clone https://github.com/AbiyaMakruf/Dicoding-BelajarFundamentalPemrosesanData.git
   cd Dicoding-BelajarFundamentalPemrosesanData
   ```

2. **Buat dan aktifkan virtual environment (disarankan):**
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependensi pustaka:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Lingkungan (Opsional untuk Google Sheets & PostgreSQL):**
   Buat berkas `.env` di root project jika ingin menghubungkan ke Google Sheets dan PostgreSQL secara langsung:
   ```env
   # Google Sheets Configuration
   SPREADSHEET_ID=your_spreadsheet_id_here

   # PostgreSQL Configuration
   DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/fashion_db
   ```

---

## Panduan Menjalankan Pipeline

### 1. Menjalankan ETL Pipeline Utama
Eksekusi pipeline secara keseluruhan untuk mengambil data dari 50 halaman, melakukan transformasi, dan menyimpan hasilnya:
```bash
python main.py
```
*Output berkas `products.csv` akan langsung terbentuk di root project.*

### 2. Menjalankan Unit Testing
Jalankan seluruh rangkaian 62 pengujian otomatis:
```bash
python -m pytest tests -v
```

### 3. Memeriksa Laporan Test Coverage
Periksa persentase cakupan pengujian kode secara rinci:
```bash
python -m coverage run -m pytest tests
python -m coverage report -m
```

---

## Ketentuan Berkas Submission

Untuk mengumpulkan tugas ke platform Dicoding, pastikan berkas-berkas berikut berada di root project dan diarsipkan ke dalam format ZIP:
* `main.py` *(Wajib)*
* `utils/extract.py`, `utils/transform.py`, `utils/load.py` *(Wajib)*
* `tests/test_extract.py`, `tests/test_transform.py`, `tests/test_load.py` *(Wajib)*
* `requirements.txt` *(Wajib)*
* `submission.txt` *(Wajib)*
* `products.csv` *(Wajib)*
* `google-sheets-api.json` *(Wajib jika mengaktifkan Google Sheets)*
* `README.md` *(Dokumentasi pendukung)*

> **Catatan Pengemasan:** Jangan menyertakan folder virtual environment (`.venv/` atau `env/`) ke dalam arsip ZIP agar ukuran berkas tetap ringkas dan mematuhi aturan pengumpulan Dicoding.
