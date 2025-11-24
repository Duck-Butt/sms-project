from nlp.date_parser import extract_date

tests = [
    "오늘 급식 뭐야",
    "내일 급식 알려줘",
    "모레 점심 뭐임",
    "12월 3일 급식 알려줘",
    "날짜 없음 테스트"
]

for t in tests:
    print(t, "→", extract_date(t))
