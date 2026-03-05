import pandas as pd
import os

def csv_combine():
    input_folder_path = input("폴더 경로: ")
    dfs = []
    
    for file_name in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, file_name)
        
        df = pd.read_csv(file_path)
        dfs.append(df)
    
    csv_result_file_path = os.path.join(input_folder_path, 'filename_eft.csv.gz')
    
    df_result = pd.concat(dfs, ingonre_index=True)
    df_result.to_csv(csv_result_file_path, index=False, quoting=1, escapechar='\\', encoding='utf-8-sig')
    
    print("작업 완료")

if __name__ == "__main__":
    df = csv_combine()