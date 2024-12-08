#app.py

from flask import Flask, request, jsonify
import json
from main import (
    complete_file_path,
    initialize_processor_and_load_image,
    analyze_image,
    convert_analysis_to_json,
    retrieve_information,
    add_image_to_entries,
    save_to_database,
    send_email
)
import os
import logging
from logging import FileHandler
from datetime import datetime

app = Flask(__name__)

# 로그 설정
file_handler = FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

@app.route('/analyze-image', methods=['POST'])
def analyze_image_api():
    try:
        caller_ip = request.remote_addr
        logging.info(f"API call received - Caller IP: {caller_ip}")

        # 이미지 파일 받기
        image_file = request.files.get('image')
        if not image_file:
            logging.warning(f"No image file provided - Caller IP: {caller_ip}")
            return jsonify({"error": "Image file is required."}), 400

        # 이미지 저장
        original_file_name = image_file.filename
        file_extension = original_file_name.split('.')[-1]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        sanitized_file_name = original_file_name.replace(" ", "_").replace("|", "_")
        new_file_name = f"{timestamp}_{caller_ip}_{sanitized_file_name}"
        file_path = os.path.join("image", new_file_name)
        logging.info(f"Image saved: {new_file_name}")
        image_file.save(file_path)

        # Step 1: 이미지 읽기 및 클래스 초기화
        image, save_path, processor = initialize_processor_and_load_image(file_path)
        logging.info(f"Image and processor initialization complete - Caller IP: {caller_ip}")

        # Step 2: 이미지 분석 실행
        analysis_response, image_base64 = analyze_image(processor, save_path)
        logging.info(f"Image analysis complete - Caller IP: {caller_ip}")

        # Step 3: 분석 결과를 JSON 변환
        json_response = convert_analysis_to_json(processor, analysis_response)
        logging.info(f"Analysis result converted to JSON - Caller IP: {caller_ip}")

        # Step 4: 담당자 및 관련 문서 탐색
        hazard_response = retrieve_information(processor, json_response)
        logging.info(f"Responsible person and related documents retrieved - Caller IP: {caller_ip}")

        # Step 5: 사진 및 기타 정보 입력
        hazard_response = add_image_to_entries(hazard_response, image_base64)
        logging.info(f"Image and other information added - Caller IP: {caller_ip}")

        # Step 6: 데이터베이스에 저장
        db_config = {
            "host": "222.122.202.31",
            "database": "postgres",
            "user": "postgres",
            "password": "",
            "port": 5432
        }
        save_to_database(hazard_response, db_config)
        logging.info(f"Data saved to database - Caller IP: {caller_ip}")

        # 이메일 전송
        email_subject = "유해위험 신고 알림"
        hazard_response_copy = hazard_response.copy()
        del hazard_response_copy["image_base64"]
        email_body = json.dumps(hazard_response_copy, indent=4, ensure_ascii=False)
        send_email(subject=email_subject, body=email_body, to_email="seok.jw@posco.com")
        logging.info(f"Email sent - Caller IP: {caller_ip}")

        return jsonify({"message": "Image analysis and data storage completed."}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)} - Caller IP: {caller_ip}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
