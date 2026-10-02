"""
Modul Load untuk ETL Pipeline Fashion Studio.
Bertanggung jawab untuk menyimpan data yang telah ditransformasikan ke tiga jenis repositori:
1. Flat file (CSV)
2. Google Sheets via Google Sheets API (Service Account)
3. Database Relasional PostgreSQL via SQLAlchemy & psycopg2
"""

import os
import logging
from typing import Any, Dict, Optional, Sequence
import pandas as pd
from sqlalchemy import create_engine

# Import library Google API
try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    Credentials = None
    build = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_to_csv(df: pd.DataFrame, output_path: str = "products.csv") -> str:
    """
    Menyimpan DataFrame ke dalam berkas flat file berformat CSV.

    Args:
        df: DataFrame yang telah dibersihkan.
        output_path: Path lokasi penyimpanan file CSV (default: 'products.csv').

    Returns:
        Path file CSV yang berhasil disimpan.
    """
    try:
        if df is None:
            raise ValueError("DataFrame tidak boleh bernilai None.")

        # Buat direktori induk jika belum ada
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        df.to_csv(output_path, index=False, encoding="utf-8")
        logger.info(f"[CSV] Berhasil menyimpan {len(df)} baris data ke '{output_path}'.")
        return output_path
    except Exception as exc:
        logger.error(f"[CSV] Gagal menyimpan data ke CSV '{output_path}': {exc}")
        raise exc


def load_to_google_sheets(
    df: pd.DataFrame,
    spreadsheet_id: Optional[str] = None,
    service_account_path: str = "google-sheets-api.json",
    sheet_name: str = "Sheet1",
) -> bool:
    """
    Menyimpan DataFrame ke dalam Google Sheets menggunakan Google Sheets API dan Service Account.

    Args:
        df: DataFrame yang telah dibersihkan.
        spreadsheet_id: ID Google Sheets (dapat diambil dari env SPREADSHEET_ID).
        service_account_path: Path berkas kredensial service account JSON.
        sheet_name: Nama worksheet target (default: 'Sheet1').

    Returns:
        True jika berhasil mengunggah data, False jika gagal.
    """
    try:
        if df is None:
            raise ValueError("DataFrame tidak boleh bernilai None.")

        # Ambil spreadsheet_id dari argumen atau environment variable
        target_spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
        if not target_spreadsheet_id:
            logger.warning("[Google Sheets] Spreadsheet ID tidak disediakan (argumen atau env SPREADSHEET_ID).")
            return False

        if not os.path.exists(service_account_path):
            logger.warning(f"[Google Sheets] Berkas service account '{service_account_path}' tidak ditemukan.")
            return False

        if Credentials is None or build is None:
            raise ImportError("Modul google-auth atau google-api-python-client belum terinstal.")

        # Autentikasi menggunakan file service account
        credentials = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        # Siapkan payload: baris header + baris nilai
        header = list(df.columns)
        # Konversi NaN menjadi string kosong dan serialisasikan data
        cleaned_records = df.fillna("").values.tolist()
        values = [header] + cleaned_records

        body = {"values": values}
        range_name = f"{sheet_name}!A1"

        logger.info(f"[Google Sheets] Mengunggah {len(values)} baris data ke spreadsheet ID: {target_spreadsheet_id}...")
        result = (
            sheet.values()
            .update(
                spreadsheetId=target_spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        updated_cells = result.get("updatedCells", 0)
        logger.info(f"[Google Sheets] Sukses! {updated_cells} sel berhasil diperbarui.")
        return True
    except Exception as exc:
        logger.error(f"[Google Sheets] Terjadi kesalahan saat memuat data ke Google Sheets: {exc}")
        return False


def load_to_postgres(
    df: pd.DataFrame,
    connection_string: Optional[str] = None,
    table_name: str = "products",
    if_exists: str = "replace",
) -> bool:
    """
    Menyimpan DataFrame ke dalam tabel database PostgreSQL menggunakan SQLAlchemy.

    Args:
        df: DataFrame yang telah dibersihkan.
        connection_string: URL koneksi PostgreSQL (misal: postgresql+psycopg2://user:pass@host:port/dbname).
        table_name: Nama tabel tujuan di PostgreSQL (default: 'products').
        if_exists: Penanganan tabel jika sudah ada ('replace', 'append', 'fail').

    Returns:
        True jika berhasil menyimpan data, False jika gagal.
    """
    try:
        if df is None:
            raise ValueError("DataFrame tidak boleh bernilai None.")

        # Ambil URL koneksi dari argumen atau environment variable
        db_url = connection_string or os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
        if not db_url:
            db_user = os.getenv("POSTGRES_USER", "postgres")
            db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
            db_host = os.getenv("POSTGRES_HOST", "localhost")
            db_port = os.getenv("POSTGRES_PORT", "5432")
            db_name = os.getenv("POSTGRES_DB", "fashion_db")
            db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

        logger.info(f"[PostgreSQL] Menghubungkan ke database dan menyimpan ke tabel '{table_name}'...")
        engine = create_engine(db_url)

        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)
        logger.info(f"[PostgreSQL] Sukses memuat {len(df)} baris data ke tabel '{table_name}'.")
        return True
    except Exception as exc:
        logger.error(f"[PostgreSQL] Gagal memuat data ke PostgreSQL: {exc}")
        return False


def load_data(
    df: pd.DataFrame,
    targets: Sequence[str] = ("csv", "google_sheets", "postgres"),
    output_csv_path: str = "products.csv",
    spreadsheet_id: Optional[str] = None,
    service_account_path: str = "google-sheets-api.json",
    postgres_conn_string: Optional[str] = None,
    postgres_table: str = "products",
) -> Dict[str, Any]:
    """
    Fungsi orkestrasi untuk memuat data ke beberapa repositori data secara modular:
    - Flat file CSV
    - Google Sheets
    - PostgreSQL

    Args:
        df: DataFrame produk bersih.
        targets: Tuple/list target repositori yang diinginkan.
        output_csv_path: Path tujuan berkas CSV.
        spreadsheet_id: ID Google Sheets.
        service_account_path: Path berkas kredensial service account.
        postgres_conn_string: URL koneksi PostgreSQL.
        postgres_table: Nama tabel database.

    Returns:
        Dictionary status pemuatan per repositori target.
    """
    results: Dict[str, Any] = {}
    try:
        logger.info(f"Memulai proses pemuatan data (load) ke target: {targets}...")

        if "csv" in targets:
            try:
                csv_res = load_to_csv(df, output_path=output_csv_path)
                results["csv"] = bool(csv_res)
            except Exception as e:
                results["csv"] = False
                logger.error(f"Pemuatan ke CSV gagal: {e}")

        if "google_sheets" in targets:
            gs_res = load_to_google_sheets(
                df,
                spreadsheet_id=spreadsheet_id,
                service_account_path=service_account_path,
            )
            results["google_sheets"] = gs_res

        if "postgres" in targets:
            pg_res = load_to_postgres(
                df,
                connection_string=postgres_conn_string,
                table_name=postgres_table,
            )
            results["postgres"] = pg_res

        logger.info(f"Hasil pemuatan data: {results}")
        return results
    except Exception as exc:
        logger.error(f"Error saat mengeksekusi load_data: {exc}")
        return results
