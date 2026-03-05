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