import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import requests
import pandas as pd

from utils.extract import (
    fetch_page,
    parse_product_card,
    scrape_page,
    extract_data,
)


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.sample_card_html = """
        <div class="collection-card">
            <h3 class="product-title">T-shirt 2</h3>
            <div class="price-container">
                <span class="price">$102.15</span>
            </div>
            <p>Rating: ⭐ 3.9 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Women</p>
        </div>
        """
        self.soup = BeautifulSoup(self.sample_card_html, "html.parser")
        self.card = self.soup.find("div", class_="collection-card")

    @patch("requests.get")
    def test_fetch_page_success_without_session(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body>Success</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_page("https://fashion-studio.dicoding.dev/")
        self.assertEqual(result, "<html><body>Success</body></html>")
        mock_get.assert_called_once()

    def test_fetch_page_success_with_session(self):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "<html><body>Session Success</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response

        result = fetch_page("https://fashion-studio.dicoding.dev/page2", session=mock_session)
        self.assertEqual(result, "<html><body>Session Success</body></html>")
        mock_session.get.assert_called_once()

    @patch("requests.get", side_effect=requests.RequestException("Connection error"))
    def test_fetch_page_request_exception(self, mock_get):
        result = fetch_page("https://invalid-url.com")
        self.assertIsNone(result)

    @patch("requests.get", side_effect=Exception("Unexpected generic error"))
    def test_fetch_page_generic_exception(self, mock_get):
        result = fetch_page("https://invalid-url.com")
        self.assertIsNone(result)

    def test_parse_product_card_valid(self):
        timestamp = "2026-10-02T10:00:00"
        result = parse_product_card(self.card, timestamp=timestamp)

        self.assertIsNotNone(result)
        self.assertEqual(result["Title"], "T-shirt 2")
        self.assertEqual(result["Price"], "$102.15")
        self.assertEqual(result["Rating"], "Rating: ⭐ 3.9 / 5")
        self.assertEqual(result["Colors"], "3 Colors")
        self.assertEqual(result["Size"], "Size: M")
        self.assertEqual(result["Gender"], "Gender: Women")
        self.assertEqual(result["timestamp"], timestamp)

    def test_parse_product_card_unavailable_price(self):
        unavail_html = """
        <div class="collection-card">
            <h3 class="product-title">Pants 16</h3>
            <span class="price-unavailable">Price Unavailable</span>
            <p>Rating: Not Rated</p>
            <p>1 Color</p>
            <p>Size: S</p>
            <p>Gender: Men</p>
        </div>
        """
        soup = BeautifulSoup(unavail_html, "html.parser")
        card = soup.find("div", class_="collection-card")
        result = parse_product_card(card)

        self.assertIsNotNone(result)
        self.assertEqual(result["Title"], "Pants 16")
        self.assertEqual(result["Price"], "Price Unavailable")
        self.assertEqual(result["Colors"], "1 Color")
        self.assertIsNotNone(result["timestamp"])

    def test_parse_product_card_none(self):
        result = parse_product_card(None)
        self.assertIsNone(result)

    def test_parse_product_card_empty_or_broken(self):
        broken_html = '<div class="collection-card"></div>'
        soup = BeautifulSoup(broken_html, "html.parser")
        card = soup.find("div", class_="collection-card")
        result = parse_product_card(card)

        self.assertIsNotNone(result)
        self.assertIsNone(result["Title"])
        self.assertIsNone(result["Price"])

    def test_parse_product_card_exception(self):
        mock_broken_card = MagicMock()
        mock_broken_card.find.side_effect = Exception("Parsing crash")
        result = parse_product_card(mock_broken_card)
        self.assertIsNone(result)

    def test_scrape_page_invalid_page_number(self):
        result = scrape_page(0)
        self.assertEqual(result, [])

    @patch("utils.extract.fetch_page", return_value=None)
    def test_scrape_page_fetch_failed(self, mock_fetch):
        result = scrape_page(1)
        self.assertEqual(result, [])

    @patch("utils.extract.fetch_page")
    def test_scrape_page_success(self, mock_fetch):
        mock_html = f"<html><body>{self.sample_card_html}</body></html>"
        mock_fetch.return_value = mock_html

        result = scrape_page(1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "T-shirt 2")
        mock_fetch.assert_called_with("https://fashion-studio.dicoding.dev", session=None)

    @patch("utils.extract.fetch_page")
    def test_scrape_page_number_greater_than_1(self, mock_fetch):
        mock_html = f"<html><body>{self.sample_card_html}</body></html>"
        mock_fetch.return_value = mock_html

        result = scrape_page(5)
        self.assertEqual(len(result), 1)
        mock_fetch.assert_called_with("https://fashion-studio.dicoding.dev/page5", session=None)

    @patch("utils.extract.fetch_page", side_effect=Exception("Fatal scrape error"))
    def test_scrape_page_exception(self, mock_fetch):
        result = scrape_page(2)
        self.assertEqual(result, [])

    @patch("utils.extract.scrape_page")
    def test_extract_data_success(self, mock_scrape):
        mock_item = {
            "Title": "Hoodie 3",
            "Price": "$496.88",
            "Rating": "Rating: ⭐ 4.8 / 5",
            "Colors": "3 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Unisex",
            "timestamp": "2026-10-02T10:00:00",
        }
        mock_scrape.return_value = [mock_item]

        df = extract_data(total_pages=3)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn("timestamp", df.columns)
        self.assertIn("Title", df.columns)
        self.assertEqual(mock_scrape.call_count, 3)

    @patch("utils.extract.scrape_page", return_value=[])
    def test_extract_data_empty_result(self, mock_scrape):
        df = extract_data(total_pages=2)
        self.assertTrue(df.empty)
        expected_cols = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
        self.assertListEqual(list(df.columns), expected_cols)

    @patch("utils.extract.scrape_page", side_effect=Exception("General extraction failure"))
    def test_extract_data_exception(self, mock_scrape):
        df = extract_data(total_pages=1)
        self.assertTrue(df.empty)
        expected_cols = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
        self.assertListEqual(list(df.columns), expected_cols)


if __name__ == "__main__":
    unittest.main()
