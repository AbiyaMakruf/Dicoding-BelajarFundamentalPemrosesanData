import sys
import logging
import os
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ETL_Pipeline")

DEFAULT_SPREADSHEET_ID = "1X683BhBBnKemrD-P5opO4g0QPMybhZqtGPEbBSHoPjI"


def get_spreadsheet_id_from_submission(file_path: str = "submission.txt") -> str | None:
    try:
        if os.path.exists(file_path):
            import re
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", content)
            if match:
                return match.group(1)
    except Exception as exc:
        logger.warning(f"Tidak dapat membaca spreadsheet ID dari {file_path}: {exc}")
    return DEFAULT_SPREADSHEET_ID


def run_pipeline(
    base_url: str = "https://fashion-studio.dicoding.dev",
    total_pages: int = 50,
    exchange_rate: float = 16000.0,
    output_csv_path: str = "products.csv",
    service_account_path: str = "google-sheets-api.json",
    spreadsheet_id: str | None = None,
    postgres_conn_string: str | None = None,
) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "status": "failed",
        "extracted_rows": 0,
        "transformed_rows": 0,
        "load_results": {},
    }

    try:
        logger.info("=" * 60)
        logger.info("   MEMULAI ETL PIPELINE - FASHION STUDIO DATA PROCESSING   ")
        logger.info("=" * 60)

        logger.info(f"[TAHAP 1] Ekstraksi data dari {base_url} ({total_pages} halaman)...")
        raw_df = extract_data(base_url=base_url, total_pages=total_pages)
        summary["extracted_rows"] = len(raw_df)

        if raw_df.empty:
            logger.error("Tahap ekstraksi tidak menghasilkan data. Pipeline dihentikan.")
            return summary

        logger.info(f"Ekstraksi selesai: Berhasil mengumpulkan {len(raw_df)} baris data mentah.")

        logger.info("[TAHAP 2] Transformasi dan pembersihan data...")
        clean_df = transform_data(raw_df, exchange_rate=exchange_rate)
        summary["transformed_rows"] = len(clean_df)

        if clean_df.empty:
            logger.error("Tahap transformasi menghasilkan DataFrame kosong. Pipeline dihentikan.")
            return summary

        logger.info(f"Transformasi selesai: Berhasil memvalidasi {len(clean_df)} baris data bersih.")
        logger.info("Ringkasan tipe data kolom:")
        for col, dtype in clean_df.dtypes.items():
            logger.info(f"  - {col}: {dtype}")

        logger.info("[TAHAP 3] Pemuatan data ke repositori data...")
        load_targets = ["csv"]

        target_sheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID") or get_spreadsheet_id_from_submission()
        if target_sheet_id and os.path.exists(service_account_path):
            load_targets.append("google_sheets")
        elif target_sheet_id:
            logger.info(f"Target Google Sheets disiapkan (ID: {target_sheet_id}). Mencoba pemuatan...")
            load_targets.append("google_sheets")

        db_conn = postgres_conn_string or os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
        if db_conn or os.getenv("POSTGRES_DB"):
            load_targets.append("postgres")
        else:
            load_targets.append("postgres")

        load_results = load_data(
            clean_df,
            targets=load_targets,
            output_csv_path=output_csv_path,
            spreadsheet_id=target_sheet_id,
            service_account_path=service_account_path,
            postgres_conn_string=db_conn,
        )
        summary["load_results"] = load_results
        summary["status"] = "success"

        logger.info("=" * 60)
        logger.info("           ETL PIPELINE BERHASIL DISELESAIKAN!           ")
        logger.info(f" Total diekstrak    : {summary['extracted_rows']} baris")
        logger.info(f" Total data bersih  : {summary['transformed_rows']} baris")
        logger.info(f" Status repositori  : {summary['load_results']}")
        logger.info("=" * 60)

        return summary
    except Exception as exc:
        logger.error(f"Terjadi kesalahan fatal dalam pipeline: {exc}", exc_info=True)
        summary["status"] = "error"
        summary["error"] = str(exc)
        return summary


def main():
    try:
        result = run_pipeline()
        if result.get("status") == "success":
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as exc:
        logger.critical(f"Kesalahan fatal pada main(): {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
