import pandas as pd
from zipfile import ZipFile

def execute(context):
	zip_file_name = context["file_upload_name"]
	dfs= []
    
	with ZipFile(zip_file_name, 'r') as z:
		# zip파일 내 모든 파일이름 확인
		for file_name in z.namelist():
			if file_name.endwith('csv'):
				with z.open(file_name) as f:
					df = pd.read_csv(f)
					dfs.append(df)

	# 기존 인덱스를 무시하고 0부터 다시 인덱스가 만들어진다				
	df_result = pd.concat(dfs, ignore_index=True)

	return df_result

if __name__ == "__main__":
    df = execute({})
    