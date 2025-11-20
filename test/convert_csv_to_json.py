import pandas as pd
import json

# CSV 파일 불러오기
df = pd.read_csv("sadong_meals_2025.csv", encoding='utf-8-sig')

# JSON 구조로 변환
data = []
for _, row in df.iterrows():
    data.append({
        "월": row["월"],
        "날짜": row["날짜"],
        "급식종류": row["급식종류"],
        "메뉴": row["메뉴"],
        "알레르기": row["알레르기"]
    })

# JSON 파일로 저장
with open("school_meals_api_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 급식 데이터 JSON 변환 완료 → school_meals_api_data.json")
