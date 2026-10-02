import unittest
import pandas as pd
import numpy as np

from utils.transform import (
    clean_price,
    clean_rating,
    clean_colors,
    clean_size,
    clean_gender,
    filter_invalid_products,
    transform_data,
)


class TestTransform(unittest.TestCase):
    def test_clean_price_valid(self):
        result = clean_price("$100.00", exchange_rate=16000.0)
        self.assertEqual(result, 1600000.0)
        self.assertIsInstance(result, float)

    def test_clean_price_with_comma(self):
        result = clean_price("$1,250.50", exchange_rate=16000.0)
        self.assertEqual(result, 1250.50 * 16000.0)

    def test_clean_price_unavailable(self):
        self.assertIsNone(clean_price("Price Unavailable"))
        self.assertIsNone(clean_price("unavailable"))

    def test_clean_price_none_and_nan(self):
        self.assertIsNone(clean_price(None))
        self.assertIsNone(clean_price(np.nan))
        self.assertIsNone(clean_price(""))

    def test_clean_price_no_digits(self):
        self.assertIsNone(clean_price("Free"))

    def test_clean_price_exception(self):
        class BrokenObj:
            def __str__(self):
                raise RuntimeError("Crash on string conversion")

        result = clean_price(BrokenObj())
        self.assertIsNone(result)

    def test_clean_rating_valid_decimal(self):
        result = clean_rating("Rating: ⭐ 3.9 / 5")
        self.assertEqual(result, 3.9)
        self.assertIsInstance(result, float)

    def test_clean_rating_valid_integer(self):
        result = clean_rating("Rating: ⭐ 4 / 5")
        self.assertEqual(result, 4.0)

    def test_clean_rating_invalid_string(self):
        self.assertIsNone(clean_rating("Rating: ⭐ Invalid Rating / 5"))
        self.assertIsNone(clean_rating("Rating: Not Rated"))

    def test_clean_rating_none_and_nan(self):
        self.assertIsNone(clean_rating(None))
        self.assertIsNone(clean_rating(np.nan))
        self.assertIsNone(clean_rating(""))

    def test_clean_rating_exception(self):
        class BrokenObj:
            def __str__(self):
                raise RuntimeError("Crash on string conversion")

        result = clean_rating(BrokenObj())
        self.assertIsNone(result)

    def test_clean_colors_plural(self):
        result = clean_colors("3 Colors")
        self.assertEqual(result, 3)
        self.assertIsInstance(result, int)

    def test_clean_colors_singular(self):
        result = clean_colors("1 Color")
        self.assertEqual(result, 1)

    def test_clean_colors_none_and_nan(self):
        self.assertIsNone(clean_colors(None))
        self.assertIsNone(clean_colors(np.nan))
        self.assertIsNone(clean_colors("No Color Info"))

    def test_clean_colors_exception(self):
        class BrokenObj:
            def __str__(self):
                raise RuntimeError("Crash on string conversion")

        result = clean_colors(BrokenObj())
        self.assertIsNone(result)

    def test_clean_size_valid(self):
        self.assertEqual(clean_size("Size: M"), "M")
        self.assertEqual(clean_size("Size:  XXL "), "XXL")

    def test_clean_size_without_prefix(self):
        self.assertEqual(clean_size("XL"), "XL")

    def test_clean_size_none_and_empty(self):
        self.assertIsNone(clean_size(None))
        self.assertIsNone(clean_size(np.nan))
        self.assertIsNone(clean_size("Size: "))

    def test_clean_size_exception(self):
        class BrokenObj:
            def __str__(self):
                raise RuntimeError("Crash on string conversion")

        result = clean_size(BrokenObj())
        self.assertIsNone(result)

    def test_clean_gender_valid(self):
        self.assertEqual(clean_gender("Gender: Women"), "Women")
        self.assertEqual(clean_gender("Gender:  Unisex "), "Unisex")

    def test_clean_gender_without_prefix(self):
        self.assertEqual(clean_gender("Men"), "Men")

    def test_clean_gender_none_and_empty(self):
        self.assertIsNone(clean_gender(None))
        self.assertIsNone(clean_gender(np.nan))
        self.assertIsNone(clean_gender("Gender: "))

    def test_clean_gender_exception(self):
        class BrokenObj:
            def __str__(self):
                raise RuntimeError("Crash on string conversion")

        result = clean_gender(BrokenObj())
        self.assertIsNone(result)

    def test_filter_invalid_products(self):
        data = {
            "Title": ["T-shirt 1", "Unknown Product", "unknown product", "Jacket 2", None, ""],
            "Price": ["$10.00", "$100.00", "$100.00", "$20.00", "$30.00", "$40.00"],
        }
        df = pd.DataFrame(data)
        filtered = filter_invalid_products(df)

        self.assertEqual(len(filtered), 2)
        self.assertListEqual(list(filtered["Title"]), ["T-shirt 1", "Jacket 2"])

    def test_filter_invalid_products_empty_or_no_title(self):
        empty_df = pd.DataFrame()
        self.assertTrue(filter_invalid_products(empty_df).empty)

        no_title_df = pd.DataFrame({"Price": ["$10.00"]})
        self.assertEqual(len(filter_invalid_products(no_title_df)), 1)

    def test_filter_invalid_products_exception(self):
        result = filter_invalid_products(None)
        self.assertIsNone(result)

    def test_transform_data_pipeline_success(self):
        sample_data = {
            "Title": [
                "Unknown Product",
                "T-shirt 2",
                "Hoodie 3",
                "Pants 16",
                "T-shirt 2",
            ],
            "Price": ["$100.00", "$100.00", "$200.00", "Price Unavailable", "$100.00"],
            "Rating": [
                "Rating: ⭐ Invalid Rating / 5",
                "Rating: ⭐ 3.9 / 5",
                "Rating: ⭐ 4.8 / 5",
                "Rating: Not Rated",
                "Rating: ⭐ 3.9 / 5",
            ],
            "Colors": ["5 Colors", "3 Colors", "4 Colors", "1 Color", "3 Colors"],
            "Size": ["Size: M", "Size: M", "Size: L", "Size: S", "Size: M"],
            "Gender": ["Gender: Men", "Gender: Women", "Gender: Unisex", "Gender: Men", "Gender: Women"],
            "timestamp": [
                "2026-10-02T10:00:00",
                "2026-10-02T10:00:00",
                "2026-10-02T10:00:00",
                "2026-10-02T10:00:00",
                "2026-10-02T10:00:00",
            ],
        }
        df_raw = pd.DataFrame(sample_data)
        clean_df = transform_data(df_raw, exchange_rate=16000.0)

        self.assertEqual(len(clean_df), 2)
        self.assertEqual(clean_df.loc[0, "Price"], 1600000.0)
        self.assertIsInstance(clean_df["Price"].iloc[0], (float, np.floating))
        self.assertEqual(clean_df.loc[0, "Rating"], 3.9)
        self.assertEqual(clean_df.loc[1, "Rating"], 4.8)
        self.assertIsInstance(clean_df["Rating"].iloc[0], (float, np.floating))
        self.assertEqual(clean_df.loc[0, "Colors"], 3)
        self.assertIsInstance(clean_df["Colors"].iloc[0], (int, np.integer))
        self.assertEqual(clean_df.loc[0, "Size"], "M")
        self.assertEqual(clean_df.loc[0, "Gender"], "Women")
        self.assertEqual(clean_df.loc[0, "timestamp"], "2026-10-02T10:00:00")
        self.assertEqual(clean_df.isnull().sum().sum(), 0)
        self.assertEqual(clean_df.duplicated().sum(), 0)

    def test_transform_data_empty_input(self):
        empty_df = pd.DataFrame()
        result = transform_data(empty_df)
        self.assertTrue(result.empty)
        expected_cols = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
        self.assertListEqual(list(result.columns), expected_cols)

    def test_transform_data_exception(self):
        result = transform_data(None)
        self.assertTrue(result.empty)
        expected_cols = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
        self.assertListEqual(list(result.columns), expected_cols)


if __name__ == "__main__":
    unittest.main()
