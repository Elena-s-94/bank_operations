import pandas as pd
import pytest
from src.read_csv_xlsx import read_excel_file, read_csv_file


def test_read_excel_file_returns_dataframe(tmp_path):
    fake_df = pd.DataFrame({
        "Дата операции": ["31.12.2021 16:44:00"],
        "Номер карты": ["*4556"],
        "Сумма операции": [-1000],
    })
    test_file = tmp_path / "test.xlsx"
    fake_df.to_excel(test_file, index=False)

    df = read_excel_file(str(test_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["Дата операции"])


def test_read_excel_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_excel_file("несуществующий_файл.xlsx")


def test_read_csv_file_returns_dataframe(tmp_path):
    fake_df = pd.DataFrame({"col": [1, 2, 3]})
    test_file = tmp_path / "test.csv"
    fake_df.to_csv(test_file, index=False, encoding="utf-8")

    df = read_csv_file(str(test_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3


def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv_file("несуществующий_файл.csv")
