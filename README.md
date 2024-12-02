# Near-Miss Reporting System

## 개요
이 프로젝트는 **POSCO 및 POSCO 그룹의 제철소 및 작업 현장**에서 발생할 수 있는 잠재적 위험 요소(니어미스)를 분석하고, 관련 정보를 체계화하여 제공하는 시스템입니다. **OpenAI API**와 **Python** 기반으로 구현되었으며, 이미지 데이터를 입력받아 위험 요소를 분석하고, JSON 포맷으로 변환한 뒤 관련 정보를 검색합니다.

---

## 주요 기능

1. **이미지 기반 위험 분석**
   - 이미지를 입력받아 잠재적 위험 요소를 식별하고, 위험 수준을 평가합니다.
   - 위험 요소와 관련된 사고 시나리오를 시뮬레이션합니다.

2. **JSON 형식 변환**
   - 분석된 데이터를 구조화된 JSON 포맷으로 변환하여 활용 가능성을 높입니다.

3. **문서 기반 추가 정보 검색**
   - 위험 요소에 대해 문서(니어미스 사례집)를 참조하여 추가적인 정보를 제공합니다.
   - 위험 완화 방안, 담당자 정보, 관련 문서 요약을 반환합니다.

4. **Base64 이미지 인코딩**
   - 입력된 이미지를 Base64로 변환하여 OpenAI API와 상호작용할 수 있도록 지원합니다.

---

## 코드 구성

### 1. `main.py`
- 프로그램의 메인 엔트리 포인트입니다.
- 주요 작업:
  - 이미지를 로드하고 `RiskAnalysisProcessor` 클래스를 초기화.
  - 이미지를 분석하여 JSON 데이터를 생성.
  - JSON 데이터를 바탕으로 추가 정보를 검색.

### 2. `prompts_and_tools.py`
- OpenAI API에 전달할 **프롬프트**와 **도구**를 정의합니다.
- 주요 내용:
  - **시스템 프롬프트**: 위험 분석, JSON 변환, 추가 정보 검색을 위한 지침.
  - **사용자 프롬프트**: 이미지 위험 분석 및 데이터 구조화를 위한 명세.
  - **도구 정의**: OpenAI API가 호출할 수 있는 기능을 명시.

### 3. `riskAnalysisProcessor.py`
- OpenAI API와의 상호작용을 담당하는 클래스입니다.
- 주요 메서드:
  1. **`encode_image_to_base64`**: 이미지 파일을 Base64로 인코딩.
  2. **`analyze_image_risks`**: OpenAI API를 호출하여 이미지 위험 요소 분석.
  3. **`format_risk_as_json`**: 분석된 데이터를 JSON 포맷으로 변환.
  4. **`retrieve_information`**: JSON 데이터를 바탕으로 문서를 검색하고 관련 정보를 추출.

---

## 실행 방법

### 1. 환경 설정
1. `.env` 파일에 OpenAI API 키를 설정합니다.
   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   ```
2. 프로젝트 디렉토리에 필요한 폴더와 파일을 준비합니다.
   - 분석할 이미지 파일: `images/` 디렉토리.
   - 문서 데이터: `documents/` 디렉토리.

### 2. 의존성 설치
필요한 Python 패키지를 설치합니다.
```bash
pip install openai python-dotenv python-docx pillow
```

### 3. 실행
다음 명령어를 실행하여 프로그램을 시작합니다.
```bash
python main.py
```

---

## 결과 예시

### 위험 분석 결과(JSON)
```json
{
  "index": 1,
  "riskLevel": 4,
  "content": {
    "potentialRisk": "추락",
    "mitigationPlan": "안전 난간 설치 및 주의 표지 부착",
    "simulation": "작업자가 높은 장소에서 균형을 잃고 추락하는 사고 시나리오"
  },
  "keywords": ["추락", "안전 난간", "주의 표지"],
  "manager": [
    {
      "name": "홍길동",
      "department": "안전 관리팀",
      "contact": "010-1234-5678"
    }
  ],
  "documents": [
    {
      "title": "니어미스 사례집 _ 추락",
      "document_summary": "작업장에서 발생 가능한 추락 사고와 이에 대한 예방 조치."
    }
  ]
}
```

---

## 주요 파일 설명

### 1. **이미지 파일**
- 분석할 이미지는 `images/` 디렉토리에 저장됩니다.
- 파일 형식: `.jpeg`, `.png` 등.

### 2. **문서 파일**
- `documents/` 디렉토리에 문서를 저장하며, 파일명은 키워드로 구성됩니다.
- 예: `니어미스 사례집 _ 추락.docx`


