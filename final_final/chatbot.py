# chatbot.py

import google.generativeai as genai
import json
from nlp.router import process_user_input
import os

# 1. Gemini API 키 설정
API_KEY = "AIzaSyAJo3hgTfXcZIgikPbGt9QtT7AHhtg-YDE" 
genai.configure(api_key=API_KEY)

# 데이터 파일 정의
MEAL_API_FILE = "school_meals_api_data.json"
INFO_FILE = "school_info.json"

def load_data(filename, key_name):
    """지정된 JSON 파일에서 데이터를 불러옵니다."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return {key_name: json.load(f)}
    except FileNotFoundError:
        if filename == MEAL_API_FILE:
            print(f"경고: {filename} 파일을 찾을 수 없습니다. API 호출 코드를 먼저 실행해 주세요.")
        return {key_name: []}
    except json.JSONDecodeError:
        print(f"경고: {filename} 파일의 JSON 형식이 잘못되었습니다.")
        return {key_name: []}

def get_chatbot_response(user_query, external_data):
    """
    Gemini API를 호출하여 답변을 생성합니다.
    """
    # 시스템 프롬프트: 챗봇의 역할 정의
    system_prompt = (
        "너는 우리 학교의 친절하고 똑똑한 AI 챗봇이야. "
        "마치 친구처럼 편안하고 재미있게 대답해 줘. "
        "아래 제공된 데이터와 너의 기존 지식을 활용해서 답변해 줘. "
        "만약 모르는 내용이라면 '아직 잘 모르는 내용이야. 학교 홈페이지를 확인해 보는 건 어때?'라고 친절하게 대답해."
        "만약 3개 이상의 정보를 묻는 경우 개조식 형태로 답변해줘. 학생들이 한 눈에 내용을 파악하기 쉽도록 해줘."
    )

    # 모든 데이터를 JSON 문자열로 변환하여 프롬프트에 포함
    data_string = json.dumps(external_data, ensure_ascii=False, indent=2)
    
    # 최종 프롬프트 구성
    final_prompt = f"""
{system_prompt}

---

아래는 현재 시점에서 제공된 최신 학교 관련 데이터(일반 정보 및 API를 통해 가져온 급식 정보)야.
{data_string}

---

사용자 질문: {user_query}
"""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(final_prompt)
    return response.text

if __name__ == '__main__':
    
    # 1. 두 개의 데이터 파일에서 정보를 불러와 통합
    school_info = load_data("school_info.json", "학교_일반_정보")
    meal_info = load_data("school_meals_api_data.json", "급식_데이터")

    chatbot_data = {**school_info, **meal_info}

    
    # 2. 챗봇 시작 안내
    print("안녕하세요! 저는 당신의 학교 생활을 도와줄 챗봇이에요. 무엇이 궁금한가요? (종료하려면 'exit'를 입력하세요)")

    while True:
        user_input = input("나: ")
        if user_input.lower() == 'exit':
            print("챗봇을 종료합니다. 안녕!")
            break
        
        result = process_user_input(user_input, chatbot_data)

        selected_data = {}
        if result['intent'] == 'meal' and result['date']:
            selected_data['학교정보'] = result['data']['학교정보']
            selected_data['급식정보'] = [
                item for item in chatbot_data['급식_데이터']
                if item['date'] == result['date']
            ]


        else:
            selected_data = result['data']

        # 3. 답변 생성
        result = process_user_input(user_input, chatbot_data)
        response_text = get_chatbot_response(user_input, result['data'])
        print(f"챗봇: {response_text}")