import os
import urllib.request

# Папка для данных
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

files = [
    {
        "url": "https://raw.githubusercontent.com/skypro-008/transactions/main/transactions.csv",
        "filename": "transactions.csv"
    },
    {
        "url": "https://github.com/skypro-008/transactions/raw/main/transactions_excel.xlsx",
        "filename": "transactions_excel.xlsx"
    }
]

for item in files:
    path = os.path.join(data_dir, item["filename"])
    print(f"Скачиваю {item['filename']}...")
    urllib.request.urlretrieve(item["url"], path)
    print(f"Готово: {path}")

print("Все файлы скачаны!")
