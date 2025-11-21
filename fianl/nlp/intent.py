# nlp/intent_classifier.py

def classify_intent(text: str):
    text = text.lower()

    if any(word in text for word in ["급식", "밥", "점심", "식단"]):
        return "meal"
    if any(word in text for word in ["학과", "시간표", "주소", "건물"]):
        return "info"
    if any(word in text for word in ["오늘", "내일", "모레", "월", "일"]):
        return "date_query"
    if any(word in text for word in ["오늘이 며칠이지", "오늘 날짜"]):
        return "date_query"


    return "general"
