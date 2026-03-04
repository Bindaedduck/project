import pandas as pd
import os

def csv_contents_modify():
    input_folder_path = input("폴더 경로: ")
    include_str = ".csv"
    
    for file_name in os.listdir(input_folder_path):
        if include_str in file_name:
            file_path = os.path.join(input_folder_path, file_name)
            file_name_without_ext = os.path.splitext(file_name)[0]+"_contents_modify.csv"
            csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
            
            df = pd.read_csv(file_path, quotechar='"')
            df['activity_name'] = 'p4_'+df['activity_name']

            df.to_csv(csv_result_file_path, index=False, encoding='utf-8-sig')
            
    print("작업 완료")

if __name__ == "__main__":
    csv_contents_modify()