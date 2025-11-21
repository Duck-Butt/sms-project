import pandas as pd
import json

df = pd.read_csv("sadong_meals_2025.csv", encoding='utf-8-sig')

data = []
for _, row in df.iterrows():
    year = 2025  # 연도 고정
    month = int(str(row["월"])[-2:])  # 202510 → 10
    day = int(row["날짜"])
    full_date = f"{year}-{month:02d}-{day:02d}"

    data.append({
        "월": row["월"],
        "날짜": row["날짜"],
        "date": full_date,  # 이 부분 추가
        "급식종류": row["급식종류"],
        "메뉴": row["메뉴"],
        "알레르기": row["알레르기"]
    })

with open("school_meals_api_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 급식 데이터 JSON 변환 완료 → school_meals_api_data.json")
