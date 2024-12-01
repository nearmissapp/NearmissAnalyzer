from PIL import Image
import json
from riskAnalysisProcessor import riskAnalysisProcessor  # RiskAnalysisProcessor 클래스 가져오기

# 에러 처리 함수
def handle_error(message, exception=None):
    """에러 처리 함수."""
    print(f"오류 발생: {message}")
    if exception:
        print(f"세부 정보: {exception}")
    raise SystemExit  # Jupyter에서 프로세스를 중지

# Step 1: 이미지 읽기 및 클래스 초기화
def initialize_processor_and_load_image(file_path):
    """이미지를 읽고 RiskAnalysisProcessor 클래스를 초기화합니다."""
    try:
        image = Image.open(file_path)
        print("이미지가 성공적으로 읽혔습니다.")
        image.show()
    except Exception as e:
        handle_error("이미지 파일을 열 수 없습니다.", e)

    try:
        processor = riskAnalysisProcessor()
        print("RiskAnalysisProcessor 클래스가 성공적으로 초기화되었습니다.")
    except ValueError as e:
        handle_error("환경 변수 설정 오류", e)

    return image, file_path, processor

# Step 2: 이미지 분석 실행
def analyze_image(processor, image_path):
    """이미지 분석 실행."""
    print("\n=== 이미지 분석 시작 ===")
    try:
        analysis_response, image_base64 = processor.analyze_image_risks(image_path)
        print("이미지 분석이 완료되었습니다.")
        print("\n[원문 데이터]:")
        print(analysis_response)
        return analysis_response, image_base64
    except Exception as e:
        handle_error("이미지 분석 중 오류 발생", e)

# Step 3: 분석 결과를 JSON 변환
def convert_analysis_to_json(processor, analysis_response):
    """이미지 분석 결과를 JSON으로 변환."""
    print("\n=== 분석 결과 JSON 변환 ===")
    try:
        analyzed_text = analysis_response.choices[0].message.content
        json_response = processor.format_risk_as_json(analyzed_text)
        print("JSON 변환이 완료되었습니다.")
        
        print("\n[JSON 데이터]:")
        print(json_response)
        return json_response
    except Exception as e:
        handle_error("JSON 변환 중 오류 발생", e)

# Step 4: 담당자 및 관련 문서 정보 탐색
def retrieve_information(processor, json_response):
    """JSON 데이터를 기반으로 관련 정보를 탐색."""
    print("\n=== 담당자 및 관련 정보 탐색 ===")
    try:
        choices = json_response.choices
        if choices and len(choices) > 0:
            tool_calls = choices[0].message.tool_calls
            if tool_calls and len(tool_calls) > 0:
                arguments = tool_calls[0].function.arguments
                json_data = json.loads(arguments)["data"]
            else:
                handle_error("tool_calls에 데이터가 없습니다.")
        else:
            handle_error("choices에 데이터가 없습니다.")
    except Exception as e:
        handle_error("JSON 데이터 처리 중 오류 발생", e)

    # 정보 탐색 실행
    try:
        retrieve_response = processor.retrieve_information(json_data)
        print("정보 탐색이 완료되었습니다.")
        print("\n[원문 데이터]:")
        print(retrieve_response)

        # choices와 tool_calls에서 데이터 추출
        choices = getattr(retrieve_response, 'choices', None)
        if choices and len(choices) > 0:
            tool_calls = getattr(choices[0].message, 'tool_calls', None)
            if tool_calls and len(tool_calls) > 0:
                function_object = tool_calls[0].function
                if hasattr(function_object, 'arguments'):
                    arguments = function_object.arguments
                    # JSON 문자열 파싱
                    parsed_data = json.loads(arguments)
                    nearmiss_details = parsed_data.get('risks', None)

                    if nearmiss_details:
                        print("\n[최종 요약 데이터]:")
                        print(json.dumps(nearmiss_details, indent=4, ensure_ascii=False))
                        return nearmiss_details
                    else:
                        print("요약 데이터가 없습니다.")
                else:
                    print("function 객체에 arguments 속성이 없습니다.")
            else:
                print("tool_calls에 데이터가 없습니다.")
        else:
            print("choices에 데이터가 없습니다.")
    except Exception as e:
        print(f"정보 탐색 결과 처리 중 오류 발생: {e}")


print("=== 니어미스 신고 프로그램 ===")
file_path = "image/test1.jpeg"  # 고정된 이미지 경로

# Step 1: 이미지 읽기 및 클래스 초기화
image, save_path, processor = initialize_processor_and_load_image(file_path)

# Step 2: 이미지 분석 실행
analysis_response, image_base64 = analyze_image(processor, save_path)

# Step 3: 분석 결과를 JSON 변환
json_response = convert_analysis_to_json(processor, analysis_response)

# Step 4: 담당자 및 관련 문서 탐색
nearmiss_response = retrieve_information(processor, json_response)

# Step 5: 사진 및 기타정보 입력
for entry in nearmiss_response:
    entry["image_base64"] = image_base64

# 결과 확인
print("\n=== 결과 확인 ===")
for entry in nearmiss_response:
    # Base64의 앞 20글자만 출력
    entry_copy = entry.copy()  # 원본 데이터를 수정하지 않기 위해 복사
    entry_copy["image_base64"] = entry["image_base64"][:20] + "..."  # 앞 20글자 + "..."로 축약
    print(json.dumps(entry_copy, indent=4, ensure_ascii=False))