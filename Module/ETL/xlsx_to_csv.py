import pandas as pd
import os

def xlsx_to_csv():
    input_folder_path = input("폴더 경로: ")
    include_str = ".xlsx"
    
    for file_name in os.listdir(input_folder_path):
        if include_str in file_name:
            file_path = os.path.join(input_folder_path, file_name)
            file_name_without_ext = os.path.splitext(file_name)[0]+".csv"
            csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
            
            # xlsx파일 읽기
            # header: 몇 행을 header로 읽어들일지
            df = pd.read_excel(file_path, header=2)
            
            # csv파일 생성
            df.to_csv(csv_result_file_path, index=False, encoding='utf-8-sig')
            
    print("작업 완료")

if __name__ == "__main__":
    xlsx_to_csv()