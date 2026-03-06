import pandas as pd
import os

def csv_chunk_combine():
    input_folder_path = input("폴더 경로: ")
    include_str = ".csv"
    chunk_list = []
    file_count = 0
    
    for file_name in os.listdir(input_folder_path):
        if include_str in file_name:
            file_path = os.path.join(input_folder_path, file_name)
            
            df = pd.read_csv(file_path)
            chunk_list.append(df)
            
            if len(pd.concat(chunk_list) >= 2000000):
                file_count += 1
                df_result = pd.concat(chunk_list)
                df_result.to_csv(f'combined_{file_count}.csv.gz', index=False, quoting=1, escapechar='\\', encoding='utf-8-sig')
                chunk_list = []
    
    if chunk_list:
        file_count += 1
        pd.concat(chunk_list).to_csv(f'combined_{file_count}.csv.gz', index=False, quoting=1, escapechar='\\', encoding='utf-8-sig')
        
    print("작업 완료")
                
if __name__ == "__main__":
    csv_chunk_combine()