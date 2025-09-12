import google.generativeai as genai
import json

# Gemini API 키를 여기에 입력하세요.
# 보안을 위해 환경 변수로 관리하는 것을 추천합니다.
API_KEY = "AIzaSyAJo3hgTfXcZIgikPbGt9QtT7AHhtg-YDE"
genai.configure(api_key=API_KEY)

def load_data(filename="school_data.json"):
    """
    JSON 파일에서 데이터를 불러옵니다.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"오류: {filename} 파일을 찾을 수 없습니다. scraper.py를 먼저 실행해 주세요.")
        return []

def get_chatbot_response(user_query, data):
    """
    Gemini API를 호출하여 답변을 생성합니다.
    """
    # 시스템 프롬프트: 챗봇의 역할과 말투를 정의합니다.
    system_prompt = (
        "너는 우리 학교의 친절하고 똑똑한 AI 챗봇이야. "
        "마치 친구처럼 편안하고 재미있게 대답해 줘. "
        "아래 제공된 데이터와 너의 기존 지식을 활용해서 답변해 줘. "
        "만약 모르는 내용이라면 '아직 잘 모르는 내용이야. 학교 홈페이지를 확인해 보는 건 어때?'라고 친절하게 대답해."
    )

    # 데이터 문자열로 변환하여 프롬프트에 포함
    data_string = json.dumps(data, ensure_ascii=False)
    
    # 최종 프롬프트 구성
    final_prompt = f"""
    {system_prompt}

    ---
    
    아래는 학교 관련 질문과 답변 데이터야.
    {data_string}

    ---
    
    사용자 질문: {user_query}
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(final_prompt)
    return response.text

if __name__ == '__main__':
    # school_data.json 파일에서 데이터 불러오기
    school_data = load_data()
    if not school_data:
        exit()

    print("안녕하세요! 저는 당신의 학교 생활을 도와줄 챗봇이에요. 무엇이 궁금한가요? (종료하려면 'exit'를 입력하세요)")

    while True:
        user_input = input("나: ")
        if user_input.lower() == 'exit':
            print("챗봇을 종료합니다. 안녕!")
            break
        
        response_text = get_chatbot_response(user_input, school_data)
        print(f"챗봇: {response_text}")