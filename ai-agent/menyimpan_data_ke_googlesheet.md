Latihan: Menyimpan Data ke Google Sheets
Ada dua cara untuk menyimpan data ke Google Sheets, yaitu secara manual dan menggunakan Google Sheets API.



Menyimpan Data secara Manual
Mari mulai materi dengan membuat spreadsheet baru, silakan akses url https://docs.google.com/spreadsheets/ dan klik “Blank spreadsheet”.

dos-e40a52b5908b497462307658c622452b20250206172423.jpeg

Setelah diklik, Anda akan melihat tampilan seperti di bawah ini.

dos-2b4abac8149d63f0e3760aee674b004220250206172422.jpeg

Langkah selanjutnya, Anda perlu mendefinisikan nama spreadsheet dan menentukan kolom serta nilai yang akan diisi dalam spreadsheet tersebut. Misalnya, Anda ingin membuat sebuah basis data pelanggan (customer database) maka bisa melakukan hal berikut.

Ubah nama spreadsheet menjadi “Customer Database”. 
Buat kolom customer yang terdiri dari “Nama Pelanggan”, “Alamat”, “Alamat Email”, “Nama Barang”, “Total Barang”, dan “Total Harga.”
Dengan mengikuti perintah di atas, Anda dapat membuat spreadsheet seperti tampilan di bawah ini.

dos-fac4fcf469dba3c95050f11d81e53dbe20250206172422.jpeg

Langkah selanjutnya adalah mengisi nilai dalam kolom-kolom tersebut. Misalnya Anda dapat mengisi kolom dengan nilai berikut.

Nama Pelanggan: Evans
Alamat: Jl. Batik Kumeli, Kota Bandung
Alamat Email: evansaja@gmail.com
Nama Barang: Monitor Samsung 4K
Jumlah Barang: 2
Total Harga: 9000000    
dos-9f2ad81b1a5052344fd527eb240e82cb20250206172423.jpeg

 

Menyimpan Data Menggunakan Google Sheets API
Cara kedua adalah mengotomatiskan penyimpanan data melalui Google Sheets API. Metode ini akan sangat efektif jika Anda perlu menyimpan data secara berulang ke Google Sheets karena proses tersebut bisa menjadi repetitif dan memakan waktu jika dilakukan secara manual. Oleh karena itu, Anda perlu mengotomatiskan tugas ini menggunakan sebuah program.

Hanya saja, Anda perlu melakukan upaya yang lebih untuk mempersiapkan skrip dan environment-nya.

Pertama, Google Sheets API dikelola melalui Google Cloud, platform ini umumnya digunakan untuk kebutuhan cloud computing. Tenang saja, saat ini Anda tidak membutuhkan pengetahuan mendalam tentang Google Cloud, hanya cukup berfokus pada penggunaan Google Sheets API saja.

dos-937e685fd8563dc2e16b3832c5e1116820250206172423.jpeg

Kedua, Anda perlu memahami konsep service account Google Cloud. 

dos-7b9e8c5440a8a1be42074f05299c9d8420250206172423.jpeg

Service account bekerja layaknya “kunci” yang diberikan pada aplikasi agar bisa membuka “pintu” layanan Google Cloud, dalam hal ini layanan Google Sheets API. 

Mengapa butuh service account? Anda membuat service account khusus untuk suatu aplikasi agar mempunyai “izin” dalam mengakses layanan Google Cloud tertentu, seperti layanan Google Sheets API. 

Izin tersebut berupa role dan permission yang dapat Anda bayangkan seperti jabatan dalam dunia nyata. Layaknya bapak Prabowo Subianto yang memiliki role sebagai Presiden Indonesia, ia memiliki permission (izin) untuk mengatur negara Indonesia.

Dalam service account, kita bisa mengatur role sebagai editor dengan izinnya membuat aplikasi kita bisa membaca, mengubah, menambahkan, dan menghapus data pada layanan tertentu (dalam konteks ini adalah Google Sheets API).

Baiklah! Mari kita mulai praktiknya.

 

Mengaktifkan Google Sheets API
Untuk mengaktifkan Google Sheets API, silakan membuka laman berikut: https://console.developers.google.com/. Jika Anda belum login menggunakan akun Google, silakan login terlebih dahulu. 

Catatan:
Anda bisa mengabaikan perintah membuat project baru jika sudah memiliki project default bernama “My First Project”.

Setelah itu, buat project Google Cloud baru dengan klik “nama project” atau “Select a project” pada Google Cloud.

dos-da099fdb5ec8f55834db3471d9f8345720250206172421.jpeg

Di dalamnya, klik “New Project”.

dos-6e4dde5920d5fef5cdb52f73756285e420250206172422.jpeg

Setelah itu, isi “Project name” sesuai dengan keinginan Anda, lalu klik “Create”.

dos-be87278ad545c1552ff5c07bc51c58c920250206172423.jpeg

Setelah berhasil membuat project, pastikan Anda telah terhubung dengan project tersebut.

dos-3008c366fcf339a4a34dde46b7a4e87d20250605143442.png

Lalu, pada halaman pencarian, ketik “Google Sheets API” dan klik icon tersebut.

dos-ae5c2c5b04c4f358982f066507760f3d20250206172423.jpeg

Setelah itu, klik “Enable”.

dos-a690ecbde714c31a3dbd1cddf57ddd3920250206172422.jpeg



Membuat Service Account
Setelah berhasil diaktifkan, langkah selanjutnya adalah membuat service account. Silakan mengakses laman https://console.cloud.google.com/apis/dashboard atau klik “APIs & Services” pada menu navigasi di pojok kiri atas. 

dos-e18ca7d354188ec9c4c5878958a2685e20250206172423.jpeg

Setelah itu, klik Credentials → + CREATE CREDENTIALS → Service Account.

dos-32967fa5ece549b242e990802549dd9020250206172423.jpeg

Di dalamnya, Anda dapat mengisi data sesuai dengan keinginan atau mengikuti contoh di bawah ini.

dos-1c9802e78114f52623f7f7ef7bffc9c720250206172423.jpeg

Klik “CREATE AND CONTINUE” dan pilih role Basic → Editor.

dos-564410b7f90eae7af7f2acae2fad3e8120250206172423.jpeg

Setelah selesai, klik “CONTINUE” dan “DONE”.

dos-610407b14eed3b412f18c30a6fdefc9e20250206172423.jpeg

 

Membuat Service Account Key
Setelah service account berhasil dibuat, kita perlu membuat “Key” atas service account tersebut. Klik service account yang sudah Anda buat sebelumnya.

dos-884dbd90b72c337ae51ec870ffd044c720250206172423.jpeg

Di dalamnya, klik “KEYS” → “ADD KEY” → “Create new key”.

dos-4c7ad59f8858c57578b30297c4c5e86420250206172423.jpeg

Pilih format .JSON sebagai format file key Anda dan klik “CREATE”.

dos-6ff607ba1bd908b2860f61305229f3fe20250206172423.jpeg

Anda akan mendapatkan file dengan format .JSON dan memiliki struktur seperti di bawah ini.

dos-d51f087e4dbf5cf23b6cbc742824c15c20250206172423.jpeg

Perhatikan nilai `client_email` berisi informasi email yang perlu Anda copy dan bagi akses spreadsheet-nya ke email tersebut. 

 

Memberikan Akses Google Sheets kepada Service Account
Sekarang, buka kembali document spreadsheets “Customer Database” yang sebelumnya telah Anda buat. Kita perlu memberikan akses “Editor” kepada client_email.

dos-598457759c8081dc502a3cf2bf90b0ec20250206172423.jpeg

Tambahkan email yang terdapat pada ‘client_email’ dan berikan hak akses sebagai “Editor”.

dos-75afe2d6008dd869ed6351b1fb1fc8f520250206172423.jpeg

Phew! Persiapan telah selesai dilakukan.

Saatnya, kita menambahkan data ke dalam Google Sheets melalui skrip Python.



Membuat Skrip Python
Silakan membuat sebuah folder bernama “googlesheets-exercise” dan buka folder tersebut melalui Visual Studio Code atau kode editor kesukaan Anda.

Berikut adalah struktur proyek kali ini.

googlesheets-exercise
├── .env
    └── ...
├── client_secret.json 
├── write_data.py
├── requirements.txt
Hal pertama yang harus Anda lakukan adalah memindahkan service account key yang sebelumnya telah diunduh dan mengubah namanya menjadi client_secret.json. Perhatikan bahwa penting untuk menyimpan file tersebut pada sejajar dengan berkas write_data.py.

Selanjutnya, kita membutuhkan bantuan dari library bernama google-auth dan google-api-python-client untuk membuat skrip ini. Silakan membuat berkas requirements.txt dengan isi sebagai berikut.

requirements.txt
google-auth ~=2.36
google-api-python-client ~=2.152
Setelah siap, mari mulai mempersiapkan virtual environment untuk proyek ini.

Buka terminal pada Visual Studio Code Anda dan buat virtual environment melalui package bernama ‘virtualenv’.

Catatan:
Pilih salah satu sintaks di bawah ini yang dapat berjalan pada terminal Anda.

Linux/Ubuntu
Windows
python3 -m venv .env
Lalu, jalankan perintah di bawah ini untuk mengaktifkannya (Pilih berdasarkan jenis terminal Anda).

Platform	Shell	
Command untuk mengaktifkan virtual environment

POSIX

bash/zsh

$ source .env/bin/activate

fish

$ source .env/bin/activate.fish

csh/tcsh

$ source .env/bin/activate.csh

pwsh

$ .env/bin/Activate.ps1

Windows

cmd.exe

C:\> .env\Scripts\activate.bat

PowerShell

PS C:\> .env\Scripts\Activate.ps1

Setelah berhasil diaktifkan, instal library yang dibutuhkan dengan menjalankan perintah berikut.

pip install -r requirements.txt
Persiapan telah usai!

Lanjut, kita masuk ke berkas write_data.py. Silakan tambahkan kode di bawah ini dalam berkas Anda.

write_data.py
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
 
SERVICE_ACCOUNT_FILE = './client_secret.json'
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
 
credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
 
SPREADSHEET_ID = '<Ganti dengan spreadsheet ID Anda>'
RANGE_NAME = 'Sheet1!A2:F11'
 
def main():
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
        values = [
            ['Evans', 'Jl.Batik Kumeli, Kota Bandung', 'evansaja@gmail.com', 'Monitor Samsung 4K', '2', '9000000']
        ]
        body = {
            'values': values
        }
 
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
 
        print("Berhasil menambahkan data!")
    except Exception as e:
         print(f"An error occurred: {e}")
 
if __name__ == '__main__':
    main()
Pada kode di atas, hal pertama yang dilakukan adalah meng-import library yang sebelumnya telah diinstal. 

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
‘Credentials’ adalah class yang digunakan untuk autentikasi agar bisa mengakses Google Sheets. Adapun, ‘build’ adalah fungsi yang akan digunakan untuk mengakses Google Sheets API yang sebelumnya telah kita persiapkan melalui layanan Google Cloud.

Berikutnya, pada bagian kode SERVICE_ACCOUNT_FILE, kita menyimpan berkas service account key dalam variabel bernama SERVICE_ACCOUNT_FILE.

SERVICE_ACCOUNT_FILE = './client_secret.json'
Lanjut, pada variabel SCOPES, kita mendefinisikan “izin” untuk membaca dan memodifikasi spreadsheets. 

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
Setelah siap, kita langsung melakukan autentikasi menggunakan baris kode berikut.

credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
Ingat bahwa kita mengambil class Credentials dari library ‘google.oauth2.service_account’ yang sebelumnya telah di-import dan bekerja layaknya saat ini mulai “masuk” ke Google Sheets melalui service account key sebagai “kunci”-nya.

Selanjutnya, kita menyiapkan spreadsheets ID serta range baris dan kolom pada spreadsheets. Kedua variabel ini digunakan untuk menunjuk pada spreadsheet lokasi kita menyimpan dan baris serta kolom berapa yang kita inginkan.

SPREADSHEET_ID = '<Ganti dengan spreadsheet ID Anda>'
RANGE_NAME = 'Sheet1!A2:F11'
Ganti isi dari variabel SPREADSHEET_ID dengan spreadsheet ID yang dapat Anda temukan pada alamat url Google Sheets.

dos-03702c3689e249f27cbb8b31d48a3a0520250206172423.jpeg

RANGE_NAME adalah variabel berisi spesifik rentang baris dan kolom yang akan kita tambahkan. Isi dari variabel tersebut menggunakan teknik A1 Notation sebagai string untuk menjelaskan pada API lokasi sheets serta baris dan kolom yang akan kita tambahkan datanya.

dos-4631c4c99a72f925ee58ebda4e4b946b20250206172423.jpeg

Perlu diingat bahwa rentang yang Anda masukkan harus sesuai dengan jumlah data yang akan ditambahkan. Misalnya, Anda akan menambahkan dua baris data dari A2 sampai F3, tetapi dalam rentang yang didefinisikan hanya dari A2 sampai F2 saja. Hal tersebut akan memunculkan kesalahan pada program yang dibuat.

dos-38cadd57848d6ae5d04a235ea667bcaa20250206172421.jpeg

Kotak hijau menunjukkan rentang baris dan kolom dari A2 sampai F2.

 

dos-93bed5c3a42bb463016a7769fbd7f1d920250206172420.jpeg

Kotak merah menunjukkan rentang baris dan kolom dari A2 sampai F3

Lanjut pada fungsi utama, yaitu ‘main()’, yang merupakan bagian utama dari kode kita, di sini kita melakukan semua langkah untuk menambahkan data ke spreadsheet. Bagian ‘try…except’ adalah tindakan pengamanan jika terjadi kesalahan, kode langsung berhenti dan menampilkan pesan kesalahan.

def main():
    try:
        # ... kode di dalam fungsi ...
    except Exception as e:
         print(f"An error occurred: {e}")
 
if __name__ == '__main__':
    main()
Penjelasan dilanjut pada kode dalam fungsi main().

Baris kode berikut untuk menghubungkan skrip yang dibuat dengan Google Sheets API.

service = build('sheets', 'v4', credentials=credential)
sheet = service.spreadsheets()
Lalu, kita mendefinisikan data yang akan ditambahkan dan menyimpannya ke dalam variabel ‘values’.

values = [
    ['Evans', 'Jl.Batik Kumeli, Kota Bandung', 'evansaja@gmail.com', 'Monitor Samsung 4K', '2', '9000000']
]
Data di atas merujuk pada pelanggan bernama Evans yang berasal dari Kota Bandung membeli dua buah monitor Samsung 4K dengan total pembelian adalah 9.000.000 rupiah.

Selanjutnya, kita membungkus data tersebut dalam variabel “body” yang menjadi format wajib untuk mengirim data ke Google Sheets API.

    body = {
        'values': values
    }
Berikutnya, kita menulis data yang sudah didefinisikan dalam spreadsheet.

result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME,
    valueInputOption='RAW',
    body=body
).execute()
Kode di atas adalah perintah untuk menulis atau menambahkan data ke dalam spreadsheet. Kita memberikan ID spreadsheet (spreadsheetId), lokasi data berupa rentang (range), format data (valueInputOption), dan tentunya data yang akan ditambahkan (body).

Jika seluruh program berjalan dengan lancar, kita akan melihat pesan berupa “Berhasil menambahkan data!”.

print("Berhasil menambahkan data!")
Lanjut, saatnya kita mengeksekusi skrip tersebut. Buka terminal Anda dan jalankan perintah berikut. 

python write_data.py
Jika berhasil, Anda akan mendapatkan pesan yang disebutkan sebelumnya seperti di bawah ini.

dos-473ca7eb35e57fed03f2453beb9689d720250206172421.jpeg

Tidak hanya itu, data yang kita inginkan harusnya berhasil ditambahkan dalam Google Sheets.

dos-6bcaff11e8f858afc12a0a25167fc6b220250206172423.jpeg

Hebat! Anda sudah berhasil menambahkan data ke dalam Google Sheets melalui skrip Python.

Jika mengalami kegagalan, silakan baca ulang kembali semua perintah di atas dan perhatikan hal-hal berikut.

Pastikan Google Sheets API berhasil diaktifkan.
Berhasil membuat service account dengan role sebagai editor.
Menambahkan akses terhadap alamat email dari variabel ‘client_email’ pada service account key (.JSON) ke Google Sheets dengan role sebagai editor.
Pastikan nama berkas service account diganti menjadi ‘client_secret.json’ dan disimpan ke dalam berkas proyek.
Pada skrip Python, pastikan memasukkan spreadsheet ID dan rentang kolom yang sesuai.
Jika tetap mengalami kendala, silakan mengajukan diskusi di Forum Diskusi.

Terakhir, penambahan data tidak terbatas pada satu sheets saja dan kita juga bisa melakukan pengambilan data (read data) dari Google Sheets tersebut. Untuk melihat detail tersebut, Anda dapat merujuk pada dokumen berikut: https://developers.google.com/sheets/api/guides/values#methods.