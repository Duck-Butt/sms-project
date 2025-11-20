import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

school_code = "B000023098"
base_url = f"https://school.koreacharts.com/school/meals/{school_code}"
months = ["202510", "202509", "202508", "202507", "202506"]

all_data = []

for m in months:
    url = f"{base_url}/contents.html" if m == "202510" else f"{base_url}/{m}.html"
    print(f"📦 {m} 수집 중 → {url}")

    res = requests.get(url, verify=False)
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all("table")

    for table in tables:
        for row in table.find_all("tr"):
            cols = [col.get_text(strip=True) for col in row.find_all(["th", "td"])]
            if len(cols) >= 2:
                row_data = [m] + cols
                # ✅ 데이터 길이 맞추기 (5열 고정)
                while len(row_data) < 5:
                    row_data.append("")
                all_data.append(row_data)

    time.sleep(1)

df = pd.DataFrame(all_data, columns=["월", "날짜", "급식종류", "메뉴", "알레르기"])
df.to_csv("sadong_meals_2025.csv", index=False, encoding='utf-8-sig')

print("✅ 전체 월 데이터 저장 완료!")
