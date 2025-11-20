# date_parser.py

import re
from datetime import datetime, timedelta

def extract_date(text):
    today = datetime.today()

    if "오늘" in text:
        return today.strftime("%Y-%m-%d")
    elif "내일" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "모레" in text:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")

    # 숫자 날짜 (예: 11월 5일)
    match = re.search(r"(\d+)월\s*(\d+)일", text)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        year = today.year
        return f"{year}-{month:02d}-{day:02d}"

    return None
