from nlp.router import process_user_input

dummy_data = {
    "학교정보": {"이름": "OO고등학교"},
    "급식정보": [{"date": "2025-11-22", "menu": "비빔밥"}]
}

tests = [
    "오늘 급식 뭐야?",
    "학교 주소 알려줘",
    "12월 3일 급식 알려줘"
]

for t in tests:
    print("입력:", t)
    print(process_user_input(t, dummy_data))
    print("-" * 40)
