from PIL import Image
import json
from risk_analyzer import RiskAnalysisProcessor  # RiskAnalysisProcessor 클래스 가져오기
from db_writer import DatabaseManager
import os  # os 모듈 추가
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 에러 처리 함수
def handle_error(message, exception=None):
    """에러 처리 함수."""
    if exception:
        print(f"세부 정보: {exception}")
    raise SystemExit  # Jupyter에서 프로세스를 중지

# Step 0: 파일 이름으로 파일 경로 완성
def complete_file_path(file_name, directory="image"):
    """파일 이름을 사용하여 파일 경로를 완성합니다."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith(file_name):
                return os.path.join(root, file)
    handle_error(f"{file_name}에 해당하는 파일을 찾을 수 없습니다.")

# Step 1: 이미지 읽기 및 클래스 초기화
def initialize_processor_and_load_image(file_path):
    """이미지를 읽고 RiskAnalysisProcessor 클래스를 초기화합니다."""
    try:
        image = Image.open(file_path)
        image.show()
    except Exception as e:
        handle_error("이미지 파일을 열 수 없습니다.", e)

    try:
        processor = RiskAnalysisProcessor()
    except ValueError as e:
        handle_error("환경 변수 설정 오류", e)

    return image, file_path, processor

# Step 2: 이미지 분석 실행
def analyze_image(processor, image_path):
    """이미지 분석 실행."""
    try:
        analysis_response, image_base64 = processor.analyze_image_risks(image_path)
        return analysis_response, image_base64
    except Exception as e:
        handle_error("이미지 분석 중 오류 발생", e)

# Step 3: 분석 결과를 JSON 변환
def convert_analysis_to_json(processor, analysis_response):
    """이미지 분석 결과를 JSON으로 변환."""
    try:
        analyzed_text = analysis_response.choices[0].message.content
        json_response = processor.format_risk_as_json(analyzed_text)
        return json_response
    except Exception as e:
        handle_error("JSON 변환 중 오류 발생", e)

# Step 4: 담당자 및 관련 문서 정보 탐색
def retrieve_information(processor, json_response):
    """JSON 데이터를 기반으로 관련 정보를 탐색."""
    def extract_data(choices, error_message):
        if choices and len(choices) > 0:
            tool_calls = choices[0].message.tool_calls
            if tool_calls and len(tool_calls) > 0:
                arguments = tool_calls[0].function.arguments
                return json.loads(arguments)
            else:
                handle_error(error_message)
        else:
            handle_error(error_message)

    try:
        json_data = extract_data(json_response.choices, "choices에 데이터가 없습니다.")["data"]
    except Exception as e:
        handle_error("정보 검색 중 오류 발생", e)

    doc_search_keyword = json_data['content']['potentialRisk']
    retrieve_response = processor.retrieve_information([json_data], doc_search_keyword)
    
    try:
        risk_data = extract_data(retrieve_response.choices, "retrieve_response의 choices에 데이터가 없습니다.")["risks"]
    except Exception as e:
        handle_error("retrieve_response 처리 중 오류 발생", e)
    
    return risk_data

# Step 5: 사진 및 기타 정보 입력
def add_image_to_entries(hazard_response, image_base64):
    """유해위험 응답에 이미지 정보를 추가합니다."""
    updated_response = hazard_response.copy()
    updated_response['image_base64'] = image_base64
    return updated_response

# Step 6: 데이터베이스에 저장
def save_to_database(hazard_response, db_config):
    """유해위험 응답을 데이터베이스에 저장합니다."""
    db_manager = DatabaseManager(db_config)
    db_manager.save(hazard_response)

def send_email(subject, body, to_email):
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "rhdtka21@gmail.com"  # 발신자 이메일 주소
    password = os.getenv("EMAIL_APP_PASSWORD")  # 환경 변수에서 앱 비밀번호 가져오기

    # 이메일 메시지 생성
    msg = MIMEMultipart()
    msg['From'] = "유해위험 신고앱"  # 발신자 이름 추가
    msg['To'] = to_email
    msg['Subject'] = subject

    # 이메일 본문 추가
    msg.attach(MIMEText(body, 'plain'))

    server = None  # server 변수를 초기화합니다.
    try:
        # SMTP 서버에 연결
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS 보안 시작
        server.login(from_email, password)  # 로그인

        # 이메일 전송
        server.sendmail(from_email, to_email, msg.as_string())
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
    finally:
        if server is not None:  # server가 None이 아닐 때만 quit 호출
            server.quit()  # 서버 연결 종료

# print("=== 유해위험 신고 프로그램 ===")
# file_name = "기차"  # file_name 변수 추가
# file_path = complete_file_path(file_name)  # file_path를 complete_file_path 함수로 설정

# # Step 1: 이미지 읽기 및 클래스 초기화
# print("Step 1: 이미지 읽기 및 클래스 초기화 시작")
# image, save_path, processor = initialize_processor_and_load_image(file_path)
# print("Step 1 완료: 이미지 및 프로세서 초기화 완료")

# # Step 2: 이미지 분석 실행
# print("Step 2: 이미지 분석 실행 시작")
# analysis_response, image_base64 = analyze_image(processor, save_path)
# print("Step 2 완료: 이미지 분석 결과")
# print(analysis_response)

# # Step 3: 분석 결과를 JSON 변환
# print("Step 3: 분석 결과를 JSON 변환 시작")
# json_response = convert_analysis_to_json(processor, analysis_response)
# print("Step 3 완료: JSON 변환 결과")
# print(json_response)

# # Step 4: 담당자 및 관련 문서 탐색
# print("Step 4: 담당자 및 관련 문서 탐색 시작")
# hazard_response = retrieve_information(processor, json_response)
# print("Step 4 완료: 탐색 결과")
# print(hazard_response)

# # Step 5: 사진 및 기타 정보 입력
# print("Step 5: 사진 및 기타 정보 입력 시작")
# hazard_response = add_image_to_entries(hazard_response, image_base64)
# print("Step 5 완료: 이미지 정보 추가 완료")

# # Step 6: 데이터베이스에 저장
# print("Step 6: 데이터베이스에 저장 시작")
# db_config = {
#     "host": "222.122.202.31",
#     "database": "postgres",
#     "user": "postgres",
#     "password": "",
#     "port": 5432
# }
# save_to_database(hazard_response, db_config)
# print("Step 6 완료: 데이터베이스 저장 완료")

# # 결과 확인
# print("\n=== 결과 확인 ===")
# hazard_response_copy = hazard_response.copy()
# hazard_response_copy["image_base64"] = hazard_response_copy["image_base64"][:20] + "..."
# print(json.dumps(hazard_response_copy, indent=4, ensure_ascii=False))

# # 이메일 전송
# print("\n=== 이메일 전송 ===")
# email_subject = "유해위험 신고 알림"
# email_body = json.dumps(hazard_response_copy, indent=4, ensure_ascii=False)
# send_email(subject=email_subject, body=email_body, to_email="seok.jw@posco.com")

# # db 확인
# print("\n=== db 확인 ===")
# db_manager = DatabaseManager(db_config)
# db_manager.fetch_all()

