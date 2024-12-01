아래는 첨부한 파이썬 코드를 기반으로 작성한 README 파일 내용입니다.

---

# Near-Miss Reporting System

## 개요
이 프로젝트는 **POSCO 제조 현장**에서 수집된 이미지 데이터를 분석하여 잠재적 위험 요소를 평가하고, 관련 위험성을 JSON 포맷으로 변환하며, 담당자 및 관련 문서 정보를 검색할 수 있는 시스템입니다. 

---

## 주요 기능

1. **이미지 기반 위험 분석**
   - 입력된 이미지에서 위험 요소를 식별하고, 위험 수준을 평가하며, 잠재적 사고 시뮬레이션을 수행합니다.
   
2. **JSON 형식 변환**
   - 분석된 결과를 구조화된 JSON 데이터로 변환합니다.
   
3. **담당자 및 문서 정보 검색**
   - 위험 요소와 관련된 담당자 및 문서 정보를 요약하여 제공합니다.

---

## 코드 구조

### 1. `main.py`
- 시스템의 메인 엔트리 포인트.
- 주요 단계:
  1. **이미지 읽기 및 클래스 초기화**
  2. **위험 분석 실행**
  3. **분석 결과 JSON 변환**
  4. **담당자 및 관련 정보 탐색**

### 2. `prompts_and_tools.py`
- OpenAI API에 제공할 프롬프트 및 도구 정의.
- 주요 내용:
  - **System Prompt**: 이미지 분석, JSON 변환, 정보 검색을 위한 명세.
  - **User Prompt**: 이미지 위험 분석 지침과 예제 출력 포맷.
  - **TOOL** : 응답 형식 지정을 위한 Function Call



### 3. `riskAnalysisProcessor.py`
- **`RiskAnalysisProcessor` 클래스 정의**:
  - OpenAI API와 상호작용하여 이미지 데이터를 기반으로 위험 요소를 분석하고, JSON 형식으로 변환하며, 관련 정보를 검색하는 기능을 제공합니다.

#### 주요 함수 설명

1. **`__init__(self)`**
   - 클래스 초기화 메서드.
   - `.env` 파일에서 OpenAI API 키를 불러오고, 초기화된 OpenAI 클라이언트를 설정합니다.
   - API 키가 누락되었을 경우 `ValueError`를 발생시켜 사용자에게 알림.

2. **`encode_image_to_base64(self, image_path)`**
   - **기능**: 이미지 파일을 Base64 형식으로 인코딩.
   - **입력**: 이미지 파일 경로 (`image_path`).
   - **출력**: Base64로 인코딩된 이미지 문자열.
   - OpenAI API에 이미지를 전송하기 전에 적합한 형식으로 변환.

3. **`analyze_image_risks(self, image_path)`**
   - **기능**: 이미지를 분석하여 잠재적 위험 요소를 평가 (레포트 작성).
   - **입력**: 분석할 이미지 파일 경로 (`image_path`).
   - **출력**: OpenAI API 응답 및 Base64로 인코딩된 이미지.
   - OpenAI API 호출:
     - 시스템 프롬프트와 사용자 프롬프트를 사용하여 메시지를 전달.
     - GPT 모델을 통해 위험 분석 결과를 생성.
   - 에러 발생 시 예외 메시지를 반환.

4. **`format_risk_as_json(self, analyzed_image_risks)`**
   - **기능**: 분석된 잠재적 위험 요소 레포팅 데이터를 구조화된 JSON 형식으로 변환.
   - **입력**: 분석 결과 텍스트 (`analyzed_image_risks`).
   - **출력**: JSON 포맷의 OpenAI API 응답.
   - JSON 변환을 위한 OpenAI API 호출:
     - 시스템 및 사용자 프롬프트를 전달.
     - API에서 제공하는 도구(`TOOLS["format_risk_as_json"]`)를 활용하여 결과를 구조화.
   - 에러 발생 시 예외 메시지를 반환.

5. **`retrieve_information(self, formatted_risks_json)`**
   - **기능**: JSON 데이터에서 관련 담당자 정보와 문서 정보를 검색.
   - **입력**: JSON 형식의 위험 요소 데이터 (`formatted_risks_json`).
   - **출력**: OpenAI API를 통해 검색된 담당자 및 문서 요약 정보.
   - OpenAI API 호출:
     - `TOOLS["retrieve_information"]`를 활용하여 JSON 데이터 기반의 요약 정보를 생성.
   - 에러 발생 시 예외 메시지를 반환.



---

## 실행 방법

### 1. 환경 설정
- `.env` 파일에 OpenAI API 키를 설정하세요:
  ```
  OPENAI_API_KEY=your_api_key_here
  ```

### 2. 이미지 파일 준비
- 분석할 이미지를 프로젝트 디렉토리의 `image` 폴더에 저장합니다. 예: `image/test1.jpeg`.

### 3. 실행
- 터미널에서 다음 명령어를 실행합니다:
  ```bash
  python main.py
  ```

### 4. 출력 결과
- 터미널에 분석 결과가 출력됩니다.
- JSON 데이터는 분석된 위험 요소 및 관련 정보를 포함합니다.

---

## 결과 출력 예시

### 위험 분석 레포트
```json
{
  "index": 1,
  "riskLevel": "상",
  "content": {
    "potentialRisk": "추락",
    "mitigationPlan": "안전 난간 설치 및 경고 표지 배치",
    "simulation": "작업자가 높은 장소에서 추락하여 중상을 입는 시나리오"
  },
  "keywords": ["추락", "안전 난간", "경고 표지"],
  "personnel": [
    {
      "name": "홍추락",
      "department": "포스코 (포항)열연부",
      "contact": "010-3456-7890"
    }
  ],
  "documents": [
    {
      "title": "안전관리법 시행령",
      "document_id": 48
    }
  ]
}
```


---

## 주의사항
1. `OPENAI_API_KEY`가 정확히 설정되어 있어야 합니다.
2. 분석할 이미지는 `.jpeg` 또는 `.png` 형식이어야 합니다.

