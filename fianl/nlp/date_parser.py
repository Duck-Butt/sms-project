# nlp/date_parser.py
from datetime import datetime, timedelta
import re

def extract_date(text: str):
    text = text.strip()

    # 오늘 / 내일 / 모레
    today = datetime.now()
    if "오늘" in text:
        return today.strftime("%Y-%m-%d")
    if "내일" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    if "모레" in text:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")

    # 12월 3일 형식
    match = re.search(r"(\d{1,2})월\s*(\d{1,2})일", text)
    if match:
        month, day = match.groups()
        year = today.year
        return f"{year}-{int(month):02d}-{int(day):02d}"

    return None
