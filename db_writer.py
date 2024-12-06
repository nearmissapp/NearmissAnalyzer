# db_writer.py

import psycopg2
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime  # datetime 모듈 추가
import os
import subprocess
import platform

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
        except Exception as e:
            print(f"데이터베이스 연결 중 오류 발생: {e}")

    def disconnect(self):
        """데이터베이스 연결을 종료합니다."""
        if self.connection:
            self.connection.close()

    def fetch_all(self):
        """데이터베이스에서 모든 레코드를 조회하고 DataFrame으로 출력합니다."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            # image_base64 열을 제외한 쿼리
            select_query = '''
            SELECT record_index, risk_level, content_potential_risk, content_mitigation_plan,
                   content_simulation, keywords, manager_name, manager_department,
                   manager_contact_phone, manager_contact_email, document_title, document_summary,
                   user_name, password, created_at, created_by
            FROM public."TB_NEARMISS_REPORT_ANALYZER";
            '''
            cursor.execute(select_query)
            records = cursor.fetchall()

            # 컬럼 이름 가져오기
            colnames = [desc[0] for desc in cursor.description]

            # 모든 컬럼을 표시하도록 설정
            pd.set_option('display.max_columns', None)

            # DataFrame으로 변환
            df = pd.DataFrame(records, columns=colnames)

            # DataFrame을 CSV 파일로 저장
            csv_file_path = 'output.csv'
            df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
            print(f"CSV 파일로 저장 완료: {csv_file_path}")

            # CSV 파일 자동 실행
            if platform.system() == "Windows":
                os.startfile(csv_file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", csv_file_path])
            else:  # Linux
                subprocess.call(["xdg-open", csv_file_path])

            print(df)

        except Exception as e:
            print(f"데이터베이스 조회 중 오류 발생: {e}")
        finally:
            if self.connection:
                cursor.close()
                self.disconnect()

    def save(self, data):
        """데이터베이스에 데이터를 저장합니다."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO public."TB_NEARMISS_REPORT_ANALYZER" (
                record_index, risk_level, content_potential_risk, content_mitigation_plan,
                content_simulation, keywords, manager_name, manager_department,
                manager_contact_phone, manager_contact_email, document_title, document_summary, image_base64,
                user_name, password, created_at, created_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # JSON 데이터에서 필요한 값 추출
            index = data["index"]
            risk_level = data["riskLevel"]
            potential_risk = data["content"]["potentialRisk"]
            mitigation_plan = data["content"]["mitigationPlan"]
            simulation = data["content"]["simulation"]
            keywords = data["keywords"]

            manager_name = data["manager"][0]["name"]
            manager_department = data["manager"][0]["department"]
            manager_contact_phone = data["manager"][0]["phonenumber"]
            manager_contact_email = data["manager"][0]["email"]

            document_title = data["documents"][0]["title"]
            document_summary = data["documents"][0]["document_summary"]
            image_base64 = data["image_base64"]

            # user_name 및 password 설정
            user_name = "석정우"
            password = "default_password"  # 적절한 기본 비밀번호 설정

            # created_at 설정
            created_at = datetime.now()  # 현재 시간

            # created_by 설정
            created_by = "석정우"  # 적절한 기본 사용자 이름 설정

            # 데이터베이스에 삽입
            cursor.execute(insert_query, (
                index, risk_level, potential_risk, mitigation_plan,
                simulation, keywords, manager_name, manager_department,
                manager_contact_phone, manager_contact_email, document_title, document_summary, image_base64, user_name, password, created_at, created_by
            ))

            self.connection.commit()
            print("데이터 저장 완료")

        except Exception as e:
            print(f"데이터 저장 중 오류 발생: {e}")
        finally:
            if self.connection:
                cursor.close()
                self.disconnect()

    def update(self, key, new_value):
        """키를 기준으로 특정 값을 수정합니다."""
        # 데이터 수정 로직 구현
        pass
