INTENT_PATTERNS = {
    "meal": ["급식", "밥", "점심", "메뉴"],
    "schedule": ["일정", "행사", "스케줄"],
    "notice": ["공지", "안내", "알림"],
    "location": ["위치", "어디", "찾아가", "교무실"],
}

def classify_intent(text):
    for intent, keywords in INTENT_PATTERNS.items():
        for kw in keywords:
            if kw in text:
                return intent
    return "unknown"
