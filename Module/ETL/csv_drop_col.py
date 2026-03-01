import pandas as pd
import os

def drop_col():
    input_folder_path = input("폴더 경로: ")
    input_delete_col = input("삭제할 컬럼(여러 개일 경우 ,로 구분): ")
    include_str = ".csv"
    delete_col = input_delete_col.split(',')
    
    for file_name in os.listdir(input_folder_path):
        if include_str in file_name:
            file_path = os.path.join(input_folder_path, file_name)
            file_name_without_ext = os.path.splitext(file_name)[0]+"_drop_col.csv"
            csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
            
            df = pd.read_csv(file_path)
            df.drop(delete_col, axis=1, inplace=True)
            df.to_csv(csv_result_file_path, index=False, encoding='utf-8-sig')
            
    print("작업 완료")

if __name__ == "__main__":
    drop_col()