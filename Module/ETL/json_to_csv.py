import pandas as pd
import json
import os

def execute():
	input_folder_path = input("폴더 경로: ")
	inclue_str = ".json"

	for file_name in os.listdir(input_folder_path):
		if inclue_str in file_name:
			file_path = os.path.join(input_folder_path, file_name)
			file_name_without_ext = os.path.splitext(file_name)[0]+".csv"
			csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
			
			with open(file_path, 'r', encoding='utf-8') as json_file:
				json_data = json.load(json_file)
		
			# df = pd.json_normalize(json_data)
			df = pd.DataFrame(json_data)
			# 100개의 데이터만 가져와라
			# df = df.head(100)
			
			df.to_csv(csv_result_file_path, index=False, encoding='utf-8-sig')
		
	print("작업 완료")
    
if __name__ == "__main__":
    df = execute()