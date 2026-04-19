import os
import glob
import json
import time
import logging
import argparse
import subprocess
import pandas as pd
from datetime import date, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class EventLogToIpm:
    def __init__(self):
        self.target_dir = os.getenv("TARGET_DIR")
        self.log_path = f"{self.target_dir}/logs"
        self.domain_url = os.getenv("DOMAIN_URL")
        self.project_key = os.getenv("PROJECT_KEY")
        self.org_key = os.getenv("ORG_KEY")
        self.access_token = None
        
        # DB 접속 설정
        db_url = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getnev("DB_POSRT")}/{os.getenv("DB_NAME")}"
        self.engine = create_engine(db_url)
        
        self.logger = self._set_logger("uploader")

    def _set_logger(self):
        # 수정필요
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path, exist_ok=True)
        logger = logging.getLogger(f"uploader")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            log_today = date.today().strftime('%Y%m%d')
            handler = logging.FileHandler(f"{self.log_path}/upload_ipm_{log_today}.log", encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
        return logger
   
    # EVENT_LOG에서 CSV파일 추출
    def extract_db_to_csv(self, system_name, chunk_size=1000000):
        end_date = date.today()
        start_date = end_date - timedelta(days=7)

        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        self.logger.info(f"[*] DB 추출 시작: {system_name} ({start_str} ~ {end_str})")
        query = f"""
            SELECT * FROM public.\"EVENT_LOG\" 
            WHERE SYSTEM_NAME='{system_name}'
            AND START_TIME BETWEEN '{start_str}' and '{end_str}'
        """
        try:
            data_iterator = pd.read_sql(query, self.engine, chunksize=chunk_size)
            for i, df_chunk in enumerate(data_iterator):
                file_name = f"{self.target_dir}/{self.system_name}_eventlog_{i}.csv"
                df_chunk.to_csv(file_name, index=False, encoding='utf-8-sig')
                self.logger.info(f"[+] CSV 생성: {file_name}")
        except Exception as e:
            self.logger.error(f"[-] DB 추출 에러: {e}")

    # subprocess 공통 호출
    def _run_curl(self, cmd_args, description="API 호출"):
        base_cmd = ["curl", "-k", "-s", "-w", "%{http_code}"]
        full_cmd = base_cmd + cmd_args
        
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
            status_code = int(result.stdout[-3:])
            response_body = result.stdout[:-3]
            return status_code, response_body
        except Exception as e:
            self.logger.error(f"[-] {description} 중 시스템 오류: {str(e)}")
            return 500, None

    # 토큰 발급
    def authenticate(self):
        url = f"{self.domain_url}/integration/sign"
        payload = {"uid": os.getenv("UID"), "apikey": os.getenv("API_KEY")}
        
        cmd = ["-X", "POST", url, 
               "-H", "Content-Type: application/json", 
               "--data-raw", json.dumps(payload)]
        
        status, body = self._run_curl(cmd, "인증 토큰 요청")
        if status == 200:
            try:
                self.access_token = json.loads(body).get("sign")
                self.logger.info(f"[+] 인증 토큰 요청 성공: {self.access_token}")
                return True
            except:
                self.logger.error("[-] 응답 데이터 파싱 실패")
        return False

    # CSV파일 IPM 업로드
    def upload_csv_files(self, max_retries=5):
        url = f"{self.domain_url}/integration/csv/{self.project_key}/upload?org={self.org_key}"
        csv_files = glob.glob(os.path.join(self.target_dir, "*.csv"))
        
        for csv_file in csv_files:
            retry_count = 0
            wait_time = 5

            self.logger.info(f"[*] 업로드 시도: {os.path.basename(csv_file)}")

            while retry_count < max_retries:
                cmd = ["-X", "POST", url, 
                    "-H", f"Authorization: Bearer {self.access_token}",
                    "-F", f"file=@{csv_file}"]
                
                status, body = self._run_curl(cmd, f"파일 업로드({os.path.basename(csv_file)})")
                if status == 200:
                    self.logger.info(f"[+] 업로드 성공: {csv_file}")
                    break
                if body and "is running." in body.lower():
                    retry_count += 1
                    if retry_count >= max_retries:
                        self.logger.error(f"[-] 최대 재시도 횟수({max_retries}) 초과: {csv_file}")
                        break
                    
                    self.logger.warning(f"[!] is running. 감지 {retry_count}차 재시도 대기 ({wait_time}초)...")
                    time.sleep(wait_time)

                    wait_time += 5

                else:
                    self.logger.error(f"[-] 업로드 실패: {csv_file}")
                    break

            time.sleep(10)

    # IPM EVENT LOG 매핑
    def map_csv(self):
        url = f"{self.domain_url}/integration/csv/{self.project_key}/create_log?org={self.org_key}"
        cmd = ["-X", "POST", url, "-H", f"Authorization: Bearer {self.access_token}"]
        
        time.sleep(20) # 서버 처리 대기
        status, _ = self._run_curl(cmd, "매핑 요청")
        if status == 200:
            self.logger.info("[+] 최종 매핑 완료")
        else:
            self.logger.error(f"[-] 매핑 실패: {status}")

def main():
    SYSTEM_LIST = os.getenv("SYSTEM_LIST")

    uploader = EventLogToIpm()

    for system in SYSTEM_LIST:
        uploader.extract_db_to_csv(system)
    
    if uploader.authenticate():
        uploader.upload_csv_files()
        uploader.map_csv()

if __name__ == "__main__":
    main()