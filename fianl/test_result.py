from nlp.router import process_user_input

# 예시 데이터
chatbot_data = {
    # 학교 정보와 급식 데이터 로드
}

user_input = "10월 24일 급식을 알려줘"

result = process_user_input(user_input, chatbot_data)

print("=== result 전체 ===")
print(result)
print("=== result['data'] 키 목록 ===")
print(result['data'].keys())

