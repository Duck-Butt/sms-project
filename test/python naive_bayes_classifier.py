import math
from collections import defaultdict

# 탐구 보고서에 사용될 20개 문장 데이터셋 정의 (스팸 10개, 정상 10개)
# 이 데이터셋은 텍스트 분류기 학습에 사용됩니다.
data = [
    ("무료 당첨 이벤트, 지금 바로 클릭하세요!", "spam"),
    ("급전 대출 가능! 비대면 신청하세요", "spam"),
    ("이벤트 초대합니다. 특별한 혜택을 놓치지 마세요.", "spam"),
    ("당신만을 위한 비밀 초대, 클릭 필수", "spam"),
    ("50% 할인 쿠폰 발급! 즉시 확인하세요", "spam"),
    ("재택 알바 고수익 보장! 관심 있으시면 연락 주세요", "spam"),
    ("긴급 입금 확인 필요. 계좌 정보를 입력하세요", "spam"),
    ("무료 수신 거부 번호를 입력하세요.", "spam"),
    ("VIP 회원만 받는 주식 정보.", "spam"),
    ("축하합니다! 상금 100만원 당첨!", "spam"),
    
    ("다음 주 회의 시간은 수요일 5시로 확정되었음.", "ham"),
    ("오늘 점심 메뉴는 돈까스가 좋겠어.", "ham"),
    ("도서관에서 빌린 책 반납일 확인 부탁드립니다.", "ham"),
    ("내일 발표 자료 초안을 메일로 보낼게.", "ham"),
    ("이번 주말에 같이 영화 보러 갈래?", "ham"),
    ("학교 숙제 범위가 어디까지인지 알려줘.", "ham"),
    ("친구 생일 선물은 뭘로 준비할까 고민이야.", "ham"),
    ("보고서 작성 마감 기한을 확인해야 함.", "ham"),
    ("최근 읽었던 미적분학 도서가 좋았음.", "ham"),
    ("저녁 약속은 7시 역 앞에서 만나자.", "ham"),
]

# 2. 라플라스 스무딩 (Laplace Smoothing) 파라미터 (alpha=1) 정의
SMOOTHING_ALPHA = 1

class NaiveBayesClassifier:
    def __init__(self):
        # 클래스별 로그 사전 확률 (Priors)
        self.log_prior = {}
        # 클래스별 단어별 로그 우도 확률 (Likelihoods)
        self.log_likelihood = defaultdict(lambda: defaultdict(float))
        # 클래스별 총 단어 수 (스무딩 분모 계산용)
        self.class_word_count = defaultdict(int)
        # 전체 단어 사전 (고유 단어 집합 - |V|)
        self.vocabulary = set()
        # 미학습 단어를 위한 최소 로그 우도 확률
        self.min_log_likelihood = 0.0

    def _tokenize(self, text):
        """텍스트를 소문자로 변환하고 구두점을 제거한 후 단어로 분리합니다."""
        return text.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').split()

    # 1. 모델 학습 (Training) 구현
    def train(self, data):
        """데이터셋을 학습하여 확률값들을 계산합니다."""
        class_counts = defaultdict(int)
        
        # 1단계: 빈도수 및 단어 사전 구축
        for text, classification in data:
            class_counts[classification] += 1
            tokens = self._tokenize(text)
            
            for token in tokens:
                self.class_word_count[classification] += 1
                self.log_likelihood[classification][token] += 1  # 임시적으로 빈도수를 저장
                self.vocabulary.add(token)

        V = len(self.vocabulary)
        N = len(data)
        
        # 사전 확률 (Log Prior) 계산
        for classification in class_counts:
            # P(클래스)를 log(P(클래스))로 저장하여 나중에 덧셈으로 처리합니다.
            self.log_prior[classification] = math.log(class_counts[classification] / N)

        # 2 & 3단계: 우도 확률 (Log Likelihood) 계산 및 라플라스 스무딩/로그 변환 적용
        for classification in self.log_likelihood:
            total_words = self.class_word_count[classification]
            
            # 스무딩이 적용된 분모 (총 단어 수 + 단어 사전 크기 * alpha)
            denominator = total_words + V * SMOOTHING_ALPHA

            for token in self.log_likelihood[classification]:
                count = self.log_likelihood[classification][token]
                # P(단어|클래스) = (C(단어) + alpha) / (N_클래스 + |V| * alpha)
                probability = (count + SMOOTHING_ALPHA) / denominator
                
                # 로그 확률로 변환하여 저장 (언더플로우 방지)
                self.log_likelihood[classification][token] = math.log(probability)

            # 훈련 데이터에 없는 단어에 대한 최소 확률 설정 (스무딩 적용된 최소 확률)
            min_probability = SMOOTHING_ALPHA / denominator
            self.min_log_likelihood = math.log(min_probability)

    # 4. 성능 평가 및 테스트 (분류) 구현
    def classify(self, text):
        """새로운 텍스트를 분류하여 사후 확률이 가장 높은 클래스를 반환합니다."""
        tokens = self._tokenize(text)
        scores = {}
        
        for classification in self.log_prior:
            # 사후 확률 점수 = log(P(클래스))
            score = self.log_prior[classification] 
            
            # log(P(단어|클래스))를 더함 (로그의 덧셈은 원래 확률의 곱셈과 동일)
            for token in tokens:
                # 훈련된 단어이면 해당 log_likelihood를 사용
                if token in self.log_likelihood[classification]:
                    score += self.log_likelihood[classification][token]
                # 훈련되지 않은 단어이면 스무딩을 적용한 최소 확률을 사용
                else:
                    # 미학습 단어로 인한 제로 확률을 방지하는 핵심 과정
                    score += self.min_log_likelihood 
            
            scores[classification] = score

        # 점수(로그 확률)가 가장 높은 클래스가 최종 분류 결과입니다.
        predicted_class = max(scores, key=scores.get)
        
        return predicted_class, scores

# --- 코드 실행 및 탐구 결과 도출 (보고서 3.2에 삽입될 내용) ---

# 1. 모델 학습 실행
classifier = NaiveBayesClassifier()
classifier.train(data)

# 2. 테스트 문장 정의
test_sentence = input("테스트할 메세지를 입력해주세요. : ")
predicted_class, scores = classifier.classify(test_sentence)

print("--- 3.2. 나이브 베이즈 모델 구현 및 분류 시연 결과 ---")
print(f"테스트 문장: '{test_sentence}'")
print("-" * 50)
print("1. 로그 사후 확률 계산 결과 (Log P(클래스|D) - 점수가 높을수록 확률 높음):")
for classification, score in scores.items():
    print(f"   Log P({classification}|D): {score:.6f}")

print("\n2. 최종 분류 결과:")
print(f"   예측된 클래스: {predicted_class.upper()}") 
print("-" * 50)

# 3. 모델 성능 정량 평가 (정확도 측정)
def evaluate(classifier, test_data):
    """테스트 데이터셋에 대한 정확도 측정"""
    correct_predictions = 0
    for text, true_class in test_data:
        predicted_class, _ = classifier.classify(text)
        if predicted_class == true_class:
            correct_predictions += 1
    accuracy = correct_predictions / len(test_data)
    return accuracy

# 학습 데이터에 대한 정확도 측정 (Self-test Accuracy)
accuracy = evaluate(classifier, data) 
print(f"\n3. 학습 데이터에 대한 정확도 (Self-test Accuracy): {accuracy:.2f}")

