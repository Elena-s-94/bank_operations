from unittest.mock import MagicMock, patch

from src.read_csv_xlsx import read_csv_file, read_excel_file


@patch("src.read_csv_xlsx.pd.read_csv")
def test_read_csv_file_success(mock_read_csv):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{"id": 1, "state": "EXECUTED", "amount": "1000"}]
    mock_read_csv.return_value = mock_df

    result = read_csv_file("data/transactions.csv")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == 1
    mock_read_csv.assert_called_once_with("data/transactions.csv", sep=";")


@patch("src.read_csv_xlsx.pd.read_csv")
def test_read_csv_file_not_found(mock_read_csv):
    mock_read_csv.side_effect = FileNotFoundError("Файл не найден")
    result = read_csv_file("nonexistent.csv")
    assert result == []


@patch("src.read_csv_xlsx.pd.read_excel")
def test_read_excel_file_success(mock_read_excel):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{"id": 2, "state": "EXECUTED", "amount": "5000"}]
    mock_read_excel.return_value = mock_df

    result = read_excel_file("data/transactions_excel.xlsx")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == 2
    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")


@patch("src.read_csv_xlsx.pd.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
    result = read_excel_file("nonexistent.xlsx")
    assert result == []
