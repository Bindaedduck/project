import pandas as pd
import json
import os

def execute():
    input_folder_path = ''
    
    for file_name in os.listdir(input_folder_path)
     	# 폴더 안 각각의 파일 경로
        input_json_file_path = os.path.join(input_folder_path, file_name)
        
        # 확장자를 제외한 파일 이름
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # 저장할 csv파일 이름
        csv_file_path = ''
        
        # 파일 읽기
        with open(input_json_file_path, 'r', encoding='utf-8') as input_json_files:
        	json_data = json.load(input_json_file)
        
        # csv파일 형식으로 맞추기
        df = pd.json_normalize(json_data)
        
        # csv파일 생성
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        
    print("Csv create!!!")
    
if __name__ == "__main__":
    df = execute()