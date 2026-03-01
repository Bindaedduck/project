import pandas as pd
from sqlalchemy import create_engine
import os

def execute():
	input_folder_path = ''
	dfs = []

	for file_name in os.listdir(input_folder_path):
		# 폴더 안 각각의 파일 경로
		csv_file_path = os.path.join(input_folder_path, file_name)
		
		df = pd.read_csv(csv_file_path)
		dfs.append(df)

	df_result = pd.concat(dfs, ignore_index=True)

	engine = create_engine("postgresql://")

	# db insert
	with engine.begin() as conn:
		df_result.to_sql(name='jira_ticketing', con=conn, if_exists='append', index=False)
		
	print("Csv to db complete!!!") 
    
if __name__ == "__main__":
    df = execute()