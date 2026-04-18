import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://ID:비밀번호@접속주소/데이터베이스")

def db_to_csv_chunk(system_name, file_path):
    CHUNK_SIZE = 1000000
	시스템 이름과 조회가간 별로 반복해서 조회?
    query = f'''SELECT * FROM pulbic."EVENT_LOG" WHERE SYSTEM_NAME='{system_name}'  '''
    
    data_iterator = pd.read_sql(query, engine, chunksize=CHUNK_SIZE)
    
    for i, df_chunk in enumerate(data_iterator):
        file_name = f"{file_path}/{system_name}_eventlog_{i}.csv"
        
        df_chunk.to_csv(file_name, index=False, encoding='utf-8-sig')

def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument()
    
    args = parser.parse_args()
    
    output_file_path = ""
    db_to_csv_chunk(args.system_name, output_file_path)
    	