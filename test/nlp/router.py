import pandas as pd
from .intent import classify_intent
from nlp.date_parser import extract_date
from nlp.intent import classify_intent


def get_meal(date):
    df = pd.read_csv("data/lunch.csv")
    row = df[df['date'] == date]
    if len(row) == 0:
        return "해당 날짜에 급식 정보가 없습니다."
    return row.iloc[0]['menu']

def get_schedule(date):
    df = pd.read_csv("data/calendar.csv")
    row = df[df['date'] == date]
    if len(row) == 0:
        return "해당 날짜에 일정이 없습니다."
    return row.iloc[0]['event']

def get_notice():
    df = pd.read_csv("data/notice.csv")
    latest = df.iloc[0]
    return f"[{latest['title']}] {latest['content']}"

def process_user_input(text):
    intent = classify_intent(text)
    date = extract_date(text)

    if intent == "meal":
        if date:
            return get_meal(date)
        return "언제 급식을 알고 싶은지 알려줘!"

    if intent == "schedule":
        if date:
            return get_schedule(date)
        return "어느 날짜 일정이 궁금한가요?"

    if intent == "notice":
        return get_notice()

    return "무슨 정보를 원하시는지 잘 이해하지 못했어요."
