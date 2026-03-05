import pandas as pd
import os

def timestamp_to_datetime():
    input_folder_path = input("폴더 경로: ")
    include_str = ".csv"
    
    for file_name in os.listdir(input_folder_path):
        if include_str in file_name:
            file_path = os.path.join(input_folder_path, file_name)
            file_name_without_ext = os.path.splitext(file_name)[0]+"_eft.csv"
            csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
            
            df = pd.read_csv(file_path, quotechar='"')
            # 16자리 timestamp
            # errors='corce' 에러난 건 표시?
            df['Timestamp_etf'] = pd.to_datetime(df['Timestamp'], unit='us', erros='coerce')
            # 10자리 timestamp
            # df['time_etf'] = pd.to_datetime(df['time'], unit='s', errors='coerce')
            df = df.dropna(subset=['Timestamp_etf'])
            
            df.to_scv(csv_result_file_path, index=False, quoting=1, escapechar='\\', encoding='utf-8-sig')
        
        print("작업 완료")
    
    if __name__ == "__main__":
        timestamp_to_datetime()