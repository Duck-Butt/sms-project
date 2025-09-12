import requests
from bs4 import BeautifulSoup
import json

def scrape_school_data(url):
    """
    지정된 URL에서 공지사항 데이터를 스크랩하고 정리합니다.
    실제 웹사이트 구조에 맞게 수정해야 합니다.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
    except requests.exceptions.RequestException as e:
        print(f"웹사이트에 접속할 수 없습니다: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # 예시: 공지사항 목록을 추출
    # 실제 웹사이트의 HTML 태그와 클래스명에 맞게 '.board-list a' 부분을 수정하세요.
    notice_elements = soup.select('.board-list a')

    data = []
    # 여기에 실제 질문-답변 쌍을 만드는 로직을 추가합니다.
    # 예시: 공지사항 제목을 질문으로, 링크를 답변으로 활용
    for notice in notice_elements:
        title = notice.text.strip()
        link = notice['href']
        if title:
            qa_pair = {
                "질문": title,
                "답변": f"관련 정보는 다음 링크에서 확인할 수 있습니다: {link}"
            }
            data.append(qa_pair)

    # 직접 수기로 작성한 데이터도 추가할 수 있습니다.
    manual_data = [
        {"질문": "이번 학기 수강 신청 기간이 언제야?", "답변": "이번 학기 수강 신청은 9월 1일부터 9월 5일까지래! 놓치지 마!"},
        {"질문": "학생증 재발급은 어떻게 해?", "답변": "학생증 재발급은 학생지원팀에 가서 신청하면 돼. 신분증 지참은 필수!"}
    ]
    data.extend(manual_data)

    return data

def save_data_to_json(data, filename="school_data.json"):
    """
    파이썬 리스트를 JSON 파일로 저장합니다.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 성공적으로 {filename}에 저장되었습니다.")

if __name__ == '__main__':
    # 크롤링할 학교 웹사이트의 실제 URL로 변경하세요.
    school_website_url = "https://school.gyo6.net/sadonggo/main.do?sysId=sadonggo"
    scraped_data = scrape_school_data(school_website_url)
    if scraped_data:
        save_data_to_json(scraped_data)