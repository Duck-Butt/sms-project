from nlp.intent import classify_intent

tests = [
    "오늘 급식 뭐야?",
    "학교 주소 알려줘",
    "내일 뭐해?",
    "시간표 알려줘",
    "학과 정보 궁금해",
    "그냥 안녕"
]

for t in tests:
    print(t, "→", classify_intent(t))
