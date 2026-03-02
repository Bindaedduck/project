import pandas as pd
import os

def csv_comma_to_semicolon():
    input_folder_path = input("폴더 경로: ")
    input_extract_col = input("특정문자를 추출할 컬럼명 입력(""안에 :뒤 문자열 추출): ")
    include_str = ".csv"
    
    for file_name in os.listdir(input_folder_path):
        if include_str in file_name:
            file_path = os.path.join(input_folder_path, file_name)
            file_name_without_ext = os.path.splitext(file_name)[0]+"_comma_to_semicolon.csv"
            csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
            
            df = pd.read_csv(file_path, quotechar='"')
            # 문자
            df[f'{input_extract_col}_extract'] = df[input_extract_col].str.extract(r'"[^"]*:\s*(\w+)"') 
            # 숫자
            # df[f'{input_extract_col}_extract'] = df[input_extract_col].str.extract(r'"[^"]*:\s*(\d+)"') 

            df.to_csv(csv_result_file_path, index=False, encoding='utf-8-sig')
            
    print("작업 완료")

if __name__ == "__main__":
    csv_comma_to_semicolon()