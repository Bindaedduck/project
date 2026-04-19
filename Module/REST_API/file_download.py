import glob
import logging
import os
import subprocess
from dotenv import load_dotenv
from datetime import date, datetime, timedelta

log_dir = "로그파일경로"

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

today = date.today()
log_today = today.strftime('%Y%m$d')
logging.basicConfig(
	level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levlename)s - %(message)s',
    handlers=[
    	logging.FileHandler(f"{log_dir}/log_{log_today}.log", encoding='utf-8')
    ] 
)

load_dotenv()

wget_user = os.getenv("WGET_USER")
wget_password = os.getenv("WGET_PASSWORD")
base_repo_url = os.getenv("BASE_REPO_URL")
targe_dir = os.getenv("TARGET_DIR")

def file_classification(path):
    zip_file_list = sorted(glob.glob(os.path.join(path, "*.zip*")))
    
    for zip_file in zip_file_list:
        os.remove(zip_file)
    
def get_current_week(date):
    iso_year, iso_week, _ = date.isocalendar()
    
    year_str = str(iso_year)[2:]
    week_str = f"{iso_week:02d}"
    
    return f"w{year_str}{week_str}"
    
def run_file_download_week(start_date, end_date=None):
	if end_date:
        if start_date > end_date:
            return
    else:
    	if start_date > today:
        	return
    
    start_week = get_current_week(start_date)
    run_file_downlaod(start_week)
    
    next_date = start_date + timedelta(days=7)
    
    if end_date:
        run_file_download_week(next_date, end_date)
    else:
        run_file_downlaod_week(next_date)

def fun_file_download(week):
    repo_download_url = os.path.join(base_repo_url, week, "")
    
    command = [
    	"wget",
        f"--user={wget_user}",
        f"--password={wget_password}",
        "-r",
        "-np",
        "-nd",
        "-P", target_dir,
        "-R", "index.html*",
    	repo_download_url
    ]
    
    try: 
    	result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"실패: {week} 다운로드 중 오류 발생 (Exit Code: {e.returncode})")
        logging.error(f"상세 에러 내용:\n{e.stderr}")
    except Exception as e:
        logging.critical(f"시스템 예외 발생: {str(e)}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="파일다운로드")
    parser.add_argument('--start', required=False, help="시작 날짜 (Ex: 2026-01-01)")
    parser.add_argument('--end', required=False, help="종료 날짜 (Ex: 2026-01-01)")
    
    args = parser.parse_args()
    
    file_classification(target_dir)
    
    if args.start:
        start_date = datetime.strptime(args.start, '%Y-%m-%d').date()
        
        if args.end:
            end_date = datetime.strptime(args.end, '%Y-%m-%d').date()
            run_file_download_week(start_date, end_date)
        else:
            run_file_download_week(start_date)
    
    elif args.end:
    	print()
    
    else:
        today_week = get_current_week(today)
        run_file_download(today_week)
        
    