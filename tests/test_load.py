import os
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

from utils.load import (
    load_to_csv,
    load_to_google_sheets,
    load_to_postgres,
    load_data,
)


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame({
            "Title": ["T-shirt 2", "Hoodie 3"],
            "Price": [1634400.0, 7950080.0],
            "Rating": [3.9, 4.8],
            "Colors": [3, 3],
            "Size": ["M", "L"],
            "Gender": ["Women", "Unisex"],
            "timestamp": ["2026-10-02T10:00:00", "2026-10-02T10:00:00"],
        })
        self.temp_csv = "tests/temp_test_output.csv"

    def tearDown(self):
        if os.path.exists(self.temp_csv):
            os.remove(self.temp_csv)

    def test_load_to_csv_success(self):
        output_file = load_to_csv(self.sample_df, output_path=self.temp_csv)
        self.assertEqual(output_file, self.temp_csv)
        self.assertTrue(os.path.exists(self.temp_csv))

        read_df = pd.read_csv(self.temp_csv)
        self.assertEqual(len(read_df), 2)
        self.assertEqual(read_df.loc[0, "Title"], "T-shirt 2")

    def test_load_to_csv_none_dataframe(self):
        with self.assertRaises(ValueError):
            load_to_csv(None, output_path=self.temp_csv)

    @patch("pandas.DataFrame.to_csv", side_effect=IOError("Disk write error"))
    def test_load_to_csv_io_error(self, mock_to_csv):
        with self.assertRaises(IOError):
            load_to_csv(self.sample_df, output_path=self.temp_csv)

    def test_load_to_google_sheets_none_df(self):
        result = load_to_google_sheets(None)
        self.assertFalse(result)

    def test_load_to_google_sheets_missing_spreadsheet_id(self):
        result = load_to_google_sheets(self.sample_df, spreadsheet_id="")
        self.assertFalse(result)

    def test_load_to_google_sheets_missing_service_account_file(self):
        result = load_to_google_sheets(
            self.sample_df,
            spreadsheet_id="test_sheet_id_123",
            service_account_path="non_existent_key.json",
        )
        self.assertFalse(result)

    @patch("os.path.exists", return_value=True)
    @patch("utils.load.Credentials", None)
    def test_load_to_google_sheets_missing_modules(self, mock_exists):
        result = load_to_google_sheets(
            self.sample_df,
            spreadsheet_id="dummy_sheet_id",
            service_account_path="dummy_key.json",
        )
        self.assertFalse(result)

    @patch("os.path.exists", return_value=True)
    @patch("utils.load.Credentials.from_service_account_file")
    @patch("utils.load.build")
    def test_load_to_google_sheets_success(self, mock_build, mock_creds, mock_exists):
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_values = MagicMock()
        mock_update = MagicMock()

        mock_update.execute.return_value = {"updatedCells": 14}
        mock_values.update.return_value = mock_update
        mock_sheets.values.return_value = mock_values
        mock_service.spreadsheets.return_value = mock_sheets
        mock_build.return_value = mock_service

        result = load_to_google_sheets(
            self.sample_df,
            spreadsheet_id="dummy_sheet_id",
            service_account_path="dummy_key.json",
        )
        self.assertTrue(result)
        mock_values.update.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("utils.load.Credentials.from_service_account_file", side_effect=Exception("Auth failure"))
    def test_load_to_google_sheets_exception(self, mock_creds, mock_exists):
        result = load_to_google_sheets(
            self.sample_df,
            spreadsheet_id="dummy_sheet_id",
            service_account_path="dummy_key.json",
        )
        self.assertFalse(result)

    def test_load_to_postgres_none_df(self):
        result = load_to_postgres(None)
        self.assertFalse(result)

    @patch("utils.load.create_engine")
    def test_load_to_postgres_success(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        with patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            result = load_to_postgres(
                self.sample_df,
                connection_string="postgresql+psycopg2://user:pass@localhost:5432/test_db",
                table_name="test_products",
            )
            self.assertTrue(result)
            mock_to_sql.assert_called_once_with(
                name="test_products",
                con=mock_engine,
                if_exists="replace",
                index=False,
            )

    @patch("utils.load.create_engine")
    def test_load_to_postgres_default_env(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        with patch.object(pd.DataFrame, "to_sql"):
            with patch.dict(os.environ, {"POSTGRES_USER": "myuser", "POSTGRES_DB": "mydb"}):
                result = load_to_postgres(self.sample_df, connection_string=None)
                self.assertTrue(result)

    @patch("utils.load.create_engine", side_effect=Exception("Database connection refused"))
    def test_load_to_postgres_exception(self, mock_create_engine):
        result = load_to_postgres(
            self.sample_df,
            connection_string="postgresql://invalid:5432/db",
        )
        self.assertFalse(result)

    @patch("utils.load.load_to_csv", return_value="products.csv")
    @patch("utils.load.load_to_google_sheets", return_value=True)
    @patch("utils.load.load_to_postgres", return_value=True)
    def test_load_data_all_targets_success(self, mock_pg, mock_gs, mock_csv):
        results = load_data(
            self.sample_df,
            targets=("csv", "google_sheets", "postgres"),
            spreadsheet_id="test_sheet",
        )
        self.assertTrue(results["csv"])
        self.assertTrue(results["google_sheets"])
        self.assertTrue(results["postgres"])

    @patch("utils.load.load_to_csv", side_effect=Exception("CSV write failed"))
    def test_load_data_csv_failure(self, mock_csv):
        results = load_data(self.sample_df, targets=("csv",))
        self.assertFalse(results["csv"])

    def test_load_data_general_exception(self):
        results = load_data(self.sample_df, targets=None)
        self.assertEqual(results, {})


if __name__ == "__main__":
    unittest.main()
