import os
import glob
import subprocess
import json
import logging
import time
from datetime import date
from dotenv import load_dotenv

load_dotenv()

domain_url = os.getenv("DOMAIN_URL")
uid = os.getenv("UID")
api_key = os.getenv("API_KEY")
target_dir = os.getenv("TARGET_DIR")
project_key = os.getenv("PROJECT_KEY")
org_key = os.getenv("ORG_KEY")

ACCESS_TOKEN = ""

def set_access_token(token):
    global ACCESS_TOKEN
    ACCESS_TOKEN = token

    today = date.today()
    log_today = today.strftime('%Y%m%d')
    log_path = f"{target_dir}/logs"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(name)s] - %(levelName)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{log_path}/upload_csv_{today}.log", encoding='utf-8')
        ]
    )

def set_token():
    get_token_url = f"{domain_url}/integration/sign"
    
    payload = {
    	"uid":uid,
        "apikey":api_key
    }
    
    cmd = [
    	"curl",
        "-k",
        "-w",
        "%{http_code}",
        "-X", "POST",
        get_token_url,
        "-H", "Accept: application/json",
        "-H", "Content-Type: application/josn",
        "--data-raw", json.dumps(payload)
    ]
    
    try:
        response = subprocess.run(cmd, check=True, capture_ouptut=True, text=True)
    except subprocess.CalledProcessError as e:
        logging.error()
    except Exception as e:
        logging.critical()
    
    status_code = int(response.stdout[-3:])
    response_body = response.stdout[:-3]
    
    if status_code == 200:
        token = response_body.get("sign")
        
        try:
            if not token:
                raise ValueError()
        except ValueError as e:
            logging.error()
        
        logging.info()
        
        set_access_token(token)
    else:
        logging.error()
        
    return status_code

def upload_all_csv_in_folder(file_name, max_retries=5):
    upload_csv_url = f"{domain_url}/integration/csv/{project_key}/upload?org={org_key}"

    retry_count = 0
    wait_time = 5

    while retry_count < max_retries:
        try:
            cmd = [
                "cur",
                "-k",
                "-w",
                "%{http_code}",
                "-X", "POST",
                upload_csv_url,
                "-H", f"Authorization: Bearer {ACCESS_TOKEN}",
                "-H", "Content-Type: multipart/form-data",
                "-F", f"file=@{file_name}"
            ]
            
            try:
                response = subprocess.run(cmd, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                logging.error()
                return False
            except Exception as e:
                logging.critical()
                return False
            
            status_code = int(response.stdout[-3:])
            response_body = response.stdout[:-3]
            
            if status_code == 200:
                logging.info()
                return True
            
            if "is running." in response_body.lower():
                retry_count += 1
                time.sleep(wait_time)
                
                wait_time += 5
            else:
                logging.error()
                return False
        except Exception as e:
            logging.error()
            return False
    return False

def map_csv():
    csv_mapping_url = f"{domain_url}/integration/csv/{project_key}/create_log?org={org_key}"
    
    cmd = [
    	"curl",
        "-k",
        "-w",
        "%{http_code}",
        "-X", "POST",
        csv_mapping_url,
        "-H", f"Authorization: Bearer {ACCESS_TOKEN}"
    ]
	
    try:
        response = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        loggig.error()
    except Exception as e:
        logging.critical()
    
    status_code = int(response.stdout[-3:])
    response_body = response.stdout[:-3]
    
    if status_code == 200:
        logging.info()
    else:
        logging.info()

def main():
    set_token_response = set_token()
    
    if set_token_response == 200:
        csv_files = glob.glob(os.path.join(target_dir, '*.csv'))
        
        for csv_file in csv_files:
            success = upload_all_csv_in_folder(csv_file)
            
            if not success:
                logging.error()
            
            time.sleep(10)
        
    time.sleep(20)
    map_csv()