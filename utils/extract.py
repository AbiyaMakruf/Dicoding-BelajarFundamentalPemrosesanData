import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def fetch_page(url: str, session: Optional[requests.Session] = None, timeout: int = 15) -> Optional[str]:
    try:
        requester = session if session is not None else requests
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requester.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as req_err:
        logger.error(f"Error saat mengambil URL {url}: {req_err}")
        return None
    except Exception as exc:
        logger.error(f"Terjadi kesalahan tak terduga saat mengambil URL {url}: {exc}")
        return None


def parse_product_card(card: Any, timestamp: Optional[str] = None) -> Optional[Dict[str, Any]]:
    try:
        if card is None:
            return None

        title_el = card.find(class_="product-title")
        title = title_el.text.strip() if title_el and title_el.text else None

        price_el = card.find(class_="price")
        price_unavail = card.find(class_=lambda x: x and "unavail" in x.lower())
        if price_el and price_el.text:
            price_text = price_el.text.strip()
        elif price_unavail and price_unavail.text:
            price_text = price_unavail.text.strip()
        else:
            price_text = None

        paras = [p.text.strip() for p in card.find_all("p") if p.text]
        rating_text = None
        colors_text = None
        size_text = None
        gender_text = None

        for p_text in paras:
            if "Rating:" in p_text:
                rating_text = p_text
            elif "Colors" in p_text or "Color" in p_text:
                colors_text = p_text
            elif "Size:" in p_text:
                size_text = p_text
            elif "Gender:" in p_text:
                gender_text = p_text

        extracted_time = timestamp if timestamp else datetime.now().isoformat()

        return {
            "Title": title,
            "Price": price_text,
            "Rating": rating_text,
            "Colors": colors_text,
            "Size": size_text,
            "Gender": gender_text,
            "timestamp": extracted_time,
        }
    except Exception as exc:
        logger.error(f"Error saat mem-parsing kartu produk: {exc}")
        return None


def scrape_page(
    page_number: int,
    session: Optional[requests.Session] = None,
    base_url: str = "https://fashion-studio.dicoding.dev",
) -> List[Dict[str, Any]]:
    try:
        if page_number < 1:
            logger.warning(f"Nomor halaman {page_number} tidak valid. Harus >= 1.")
            return []

        url = base_url if page_number == 1 else f"{base_url.rstrip('/')}/page{page_number}"
        html_content = fetch_page(url, session=session)

        if not html_content:
            logger.warning(f"Gagal mendapatkan konten dari halaman {page_number} ({url})")
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        cards = soup.find_all("div", class_="collection-card")

        results: List[Dict[str, Any]] = []
        extraction_time = datetime.now().isoformat()

        for card in cards:
            parsed = parse_product_card(card, timestamp=extraction_time)
            if parsed is not None:
                results.append(parsed)

        logger.info(f"Halaman {page_number}: Berhasil mengekstrak {len(results)} produk.")
        return results
    except Exception as exc:
        logger.error(f"Error saat scraping halaman {page_number}: {exc}")
        return []


def extract_data(
    base_url: str = "https://fashion-studio.dicoding.dev",
    total_pages: int = 50,
    session: Optional[requests.Session] = None,
) -> pd.DataFrame:
    try:
        logger.info(f"Memulai proses ekstraksi data dari {base_url} (total {total_pages} halaman)...")
        all_records: List[Dict[str, Any]] = []
        active_session = session if session is not None else requests.Session()

        try:
            for page in range(1, total_pages + 1):
                page_data = scrape_page(page, session=active_session, base_url=base_url)
                all_records.extend(page_data)
        finally:
            if session is None:
                active_session.close()

        df = pd.DataFrame(all_records)
        expected_columns = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        logger.info(f"Proses ekstraksi selesai. Total data yang berhasil diekstrak: {len(df)} baris.")
        return df[expected_columns]
    except Exception as exc:
        logger.error(f"Error saat mengekstrak seluruh data: {exc}")
        return pd.DataFrame(columns=["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"])
