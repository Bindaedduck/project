import pandas as pd
from sqlalchemy import create_engine
import os
import glob
import logging

def execute(input_dir):
    
    logging.basicConfig(
        filename='app.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    try:
        file_list = sorted(glob.glob(os.path.join(input_dir, "*.csv")))
        
        engine = create_engine()

        for file_path in file_list:
            reader = pd.read_csv(file_path, chunksize=100000, usecols=['system_name','process_id'])
            
            for chunk in reader:
                chunk = chunk.drop_duplicates(subset=['process_id'], keep='first')
                
                with engine.begin() as conn:
                    process_id = pd.read_sql("SELECT process_id FROM \"SAMPLE\"", conn)
                    
                    merged = pd.merge(chunk, process_id, on='process_id', how='left', indicator=True)
                    
                    insert_value = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
                        
                    if not insert_value.empty:
                        insert_value['ref_id'] = insert_value['process_id'] 
                        insert_value.to_sql(
                            name='EVENT_LOG',
                            con=conn,
                            if_exists='append',
                            index=False,
                            method='multi',
                            chunksize=10000
                        )
                    
    except Exception as e:
        logging.exception("Exception occured: %s", e)

if __name__ == "__main__":
    input_dir = r''
    df = execute(input_dir)