import streamlit as st
from PIL import Image
import json
from riskAnalysisProcessor import riskAnalysisProcessor  # RiskAnalysisProcessor 클래스 가져오기

def handle_error(message, exception=None):
    """에러 처리 함수."""
    error_message = {"message": f"오류 발생: {message}", "exception": str(exception) if exception else None}
    return error_message

def initialize_processor():
    """RiskAnalysisProcessor 인스턴스를 초기화."""
    try:
        return riskAnalysisProcessor(), None
    except ValueError as e:
        return None, handle_error("환경 변수 설정 오류", e)

def analyze_image(processor, image_path):
    """이미지 분석 실행."""
    try:
        return processor.analyze_image_risks(image_path)[0], processor.analyze_image_risks(image_path)[1], None
    except Exception as e:
        return None, None, handle_error("이미지 분석 중 오류 발생", e)

def extract_choices_data(response, key, data_key):
    """ChatCompletion 객체에서 데이터를 추출."""
    try:
        choices = response.choices
        if not choices or len(choices) == 0:
            return None, {"message": f"choices에 데이터가 없습니다. ({key})"}
        tool_calls = choices[0].message.tool_calls
        if not tool_calls or len(tool_calls) == 0:
            return None, {"message": f"tool_calls에 데이터가 없습니다. ({key})"}
        arguments = tool_calls[0].function.arguments
        return json.loads(arguments).get(data_key), None
    except Exception as e:
        return None, handle_error(f"{key} 데이터 추출 중 오류 발생", e)

# Streamlit 애플리케이션
def main():
    st.markdown(
        """
        <style>
        .css-1offfwp.e1ewe7hr3 {  /* 페이지 제목 스타일 */
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
        }
        .css-12ttj6m.e1fqkh3o2 {  /* 업로드 버튼 스타일 */
            margin-top: 20px;
            text-align: center;
        }
        .stButton button {
            background-color: #4CAF50; /* 녹색 버튼 */
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        }
        .stTextInput {
            margin-top: 15px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.title("📸 POSCO 니어미스 신고 App")

    # Step 1: 파일 업로드 UI
    uploaded_file = st.file_uploader("📂 이미지를 선택하세요", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Step 2: 업로드된 이미지 표시
        image = Image.open(uploaded_file)
        save_path = f"uploaded_{uploaded_file.name}"
        image.save(save_path)

        st.image(image, caption="업로드된 이미지", use_column_width=True)

        # Step 3: 코멘트 입력창 표시
        comment = st.text_input("📝 코멘트를 입력하세요:", placeholder="코멘트를 입력해 주세요...")
        
        # Step 4: "사진 신고하기" 버튼 활성화
        if st.button("📤 사진 신고하기"):
            try:
                # Step 5: RiskAnalysisProcessor 초기화
                processor, error = initialize_processor()
                if error:
                    st.error(error["message"])
                    if error["exception"]:
                        st.error(f"세부 정보: {error['exception']}")
                    st.stop()

                # Step 6: 이미지 분석 실행
                with st.spinner("이미지 분석 중..."):
                    analysis_response, image_base64, error = analyze_image(processor, save_path)
                    if error:
                        st.error(error["message"])
                        if error["exception"]:
                            st.error(f"세부 정보: {error['exception']}")
                        st.stop()

                # Step 7: 분석 결과 content 추출
                analyzed_text = analysis_response.choices[0].message.content
                st.subheader("분석 결과 Content")
                st.text(analyzed_text)

                # Step 8: 분석 결과를 JSON으로 변환
                with st.spinner("분석 결과를 JSON으로 변환 중..."):
                    json_response = processor.format_risk_as_json(analyzed_text)
                    json_data, error = extract_choices_data(json_response, "JSON 변환", "data")
                    if error:
                        st.warning(error["message"])
                    if json_data:
                        st.json(json_data)

                # Step 9: 분석 값 요약
                with st.spinner("담당자 정보를 탐색 중..."):
                    personnel_response = processor.retrieve_information(json_data)
                    personnel_data, error = extract_choices_data(personnel_response, "담당자 탐색", "risks")
                    if error:
                        st.warning(error["message"])
                    if personnel_data:
                        st.json(personnel_data)
                        
            except Exception as e:
                error = handle_error("이미지 처리 중 오류 발생", e)
                st.error(error["message"])
                if error["exception"]:
                    st.error(f"세부 정보: {error['exception']}")

# 메인 함수 실행
if __name__ == "__main__":
    main()
def analyze_image(processor, image_path):
    try:
        return processor.analyze_image_risks(image_path), None
    except Exception as e:
        return None, handle_error("이미지 분석 중 오류 발생", e)