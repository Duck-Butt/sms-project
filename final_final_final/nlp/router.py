# nlp/router.py
from nlp.intent import classify_intent
from nlp.date_parser import extract_date
def process_user_input(user_input, data):
    intent = classify_intent(user_input)
    date = extract_date(user_input)
    filtered_data = {}

    # 1) 급식 정보 필터링
    if intent == "meal":
        filtered_meals = [m for m in data.get("급식_데이터", []) if m.get("date") == date]
        filtered_data["급식정보"] = filtered_meals

    # 2) 학교 정보
    school_info = data.get("학교_일반_정보", {})
    filtered_data["학교정보"] = school_info
    # 3) 오늘 날짜 질문 처리 ← 여기
    if intent == "date_query":
        from datetime import datetime
        today = datetime.now()
        filtered_data["오늘날짜"] = today.strftime("%Y년 %m월 %d일 %A")

    # 최종 반환
    return {
        "intent": intent,
        "date": date,
        "data": filtered_data
    }

