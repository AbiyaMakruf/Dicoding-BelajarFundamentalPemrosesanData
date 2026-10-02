import logging
import re
from typing import Any, Optional
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def clean_price(val: Any, exchange_rate: float = 16000.0) -> Optional[float]:
    try:
        if val is None or pd.isna(val):
            return None

        val_str = str(val).strip()
        if "unavailable" in val_str.lower():
            return None

        match = re.search(r"(\d+(?:\.\d+)?)", val_str.replace(",", ""))
        if not match:
            return None

        usd_val = float(match.group(1))
        idr_val = float(usd_val * exchange_rate)
        return idr_val
    except Exception as exc:
        logger.error(f"Error saat membersihkan nilai price: {exc}")
        return None


def clean_rating(val: Any) -> Optional[float]:
    try:
        if val is None or pd.isna(val):
            return None

        val_str = str(val).strip()
        lower_str = val_str.lower()
        if "invalid" in lower_str or "not rated" in lower_str:
            return None

        match = re.search(r"(\d+(?:\.\d+)?)\s*(?:/\s*5)?", val_str)
        if match:
            return float(match.group(1))
        return None
    except Exception as exc:
        logger.error(f"Error saat membersihkan nilai rating: {exc}")
        return None


def clean_colors(val: Any) -> Optional[int]:
    try:
        if val is None or pd.isna(val):
            return None

        val_str = str(val).strip()
        match = re.search(r"(\d+)", val_str)
        if match:
            return int(match.group(1))
        return None
    except Exception as exc:
        logger.error(f"Error saat membersihkan nilai colors: {exc}")
        return None


def clean_size(val: Any) -> Optional[str]:
    try:
        if val is None or pd.isna(val):
            return None

        val_str = str(val).strip()
        cleaned = re.sub(r"^Size:\s*", "", val_str, flags=re.IGNORECASE).strip()
        return cleaned if cleaned else None
    except Exception as exc:
        logger.error(f"Error saat membersihkan nilai size: {exc}")
        return None


def clean_gender(val: Any) -> Optional[str]:
    try:
        if val is None or pd.isna(val):
            return None

        val_str = str(val).strip()
        cleaned = re.sub(r"^Gender:\s*", "", val_str, flags=re.IGNORECASE).strip()
        return cleaned if cleaned else None
    except Exception as exc:
        logger.error(f"Error saat membersihkan nilai gender: {exc}")
        return None


def filter_invalid_products(df: pd.DataFrame) -> pd.DataFrame:
    try:
        if df.empty or "Title" not in df.columns:
            return df

        is_valid_title = (
            df["Title"].notna()
            & (df["Title"].astype(str).str.strip().str.lower() != "unknown product")
            & (df["Title"].astype(str).str.strip() != "")
        )
        filtered_df = df[is_valid_title].copy()
        logger.info(f"Filter invalid products: {len(df) - len(filtered_df)} baris invalid dihapus.")
        return filtered_df
    except Exception as exc:
        logger.error(f"Error saat memfilter produk tidak valid: {exc}")
        return df


def transform_data(df: pd.DataFrame, exchange_rate: float = 16000.0) -> pd.DataFrame:
    try:
        logger.info(f"Memulai proses transformasi data ({len(df)} baris data awal)...")
        if df.empty:
            logger.warning("DataFrame yang akan ditransformasi kosong.")
            return pd.DataFrame(columns=["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"])

        working_df = df.copy()

        working_df = filter_invalid_products(working_df)

        working_df["Price"] = working_df["Price"].apply(lambda p: clean_price(p, exchange_rate=exchange_rate))
        working_df["Rating"] = working_df["Rating"].apply(clean_rating)
        working_df["Colors"] = working_df["Colors"].apply(clean_colors)
        working_df["Size"] = working_df["Size"].apply(clean_size)
        working_df["Gender"] = working_df["Gender"].apply(clean_gender)

        initial_count = len(working_df)
        working_df = working_df.drop_duplicates()
        dedup_count = len(working_df)
        logger.info(f"Deduplikasi data: Menghapus {initial_count - dedup_count} baris duplikat.")

        working_df = working_df.dropna()
        drop_null_count = len(working_df)
        logger.info(f"Pembersihan null: Menghapus {dedup_count - drop_null_count} baris bernilai null.")

        working_df["Title"] = working_df["Title"].astype(str)
        working_df["Price"] = working_df["Price"].astype(float)
        working_df["Rating"] = working_df["Rating"].astype(float)
        working_df["Colors"] = working_df["Colors"].astype(int)
        working_df["Size"] = working_df["Size"].astype(str)
        working_df["Gender"] = working_df["Gender"].astype(str)
        if "timestamp" in working_df.columns:
            working_df["timestamp"] = working_df["timestamp"].astype(str)

        working_df = working_df.reset_index(drop=True)

        logger.info(f"Transformasi data berhasil diselesaikan. Menghasilkan {len(working_df)} baris data bersih.")
        return working_df
    except Exception as exc:
        logger.error(f"Error saat transformasi data: {exc}")
        return pd.DataFrame(columns=["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"])
