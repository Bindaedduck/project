import datetime
import logging
import os
import shutil
from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine

class BaseIngestion(ABC):
    def __init__(self, system_name, file_path):
        self.system_name = system_name.upper()
        # 작업할 시스템 파일 경로 - file_path/system_name
        self.system_path = os.path.join(file_path, system_name)
        self.file_path = os.path.join(self.system_path, "input")
        self.backup_path = os.path.join(self.system_path, "backup")
        self.logger = self._set_logger()

    @abstractmethod
    def _sef_file_list(self):
        pass
    
    @abstractmethod
    def _read_file(self):
        pass
    
    @abstractmethod
    def _extract(self):
        pass
    
    @abstractmethod
    def _transform(self):
        pass
        
    @abstractmethod
    def _mapping(self, df):
        pass
        
    def _set_logger(self):
        logger = logging.getLogger(self.system_name)
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            os.makedirs('logs', exist_ok=True)

            file_handler = logging.FileHandler(f”logs/{self.system_name}.log”, encoding='utf-8')
            stream_handler = logging.StreamHandler()

            formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
        
        return logger
	
    # 중복된 데이터 무시하고 DB insert
    def _insert_on_conflict_nothing(self, table, conn, keys, data_iter):
        data = [dict(zip(keys, row))] for row in data_iter]
        
        stmt = insert(table.table).values(data)
        
        on_conflict_stmt = stmt.on_conflict_do_nothing(
        	index_elements=['system_name', 'process_id', 'activity_name', 'start_time] # EVENT LOG - UNIQUE KEY
        )
        
        conn.execute(on_conflict_stmt)

	def _load(self, df):
    	try:
        	engine = create_engine()
            
            df = df.drop_duplicates(subset=['system_name', 'process_id', 'activity_name', 'start_tiem'], keep='first')
            
        	with engine.begin() as conn:
            	df.to_sql(
                	name='',
                    con=conn,
                    schema='',
                    if_exists='append',
                    index=False,
                    method=self._insert_on_conflict_nothing,
                    #method=None, # DEBUG
                    chunksize=10000
                )
         except Exception as e:
            self.logger.error(f"Error: {str(e)}", exc_info=True)
    
    def file_backup(self):
        for file_name in os.listdir(self.file_path):
            	source_path = os.path.join(self.file_path, file_name)
                target_path = os.path.join(self.backup_path, file_name)
                
                if os.path.isfile(source_path):
                    shutil.move(source_path, target_path)       

    def run(self):
        try:
            for chunk_data in self._read_file():
            	extracted_data = self._extract(chunk_data)
                trnasformed_df = self._transform(extarcted_data)
                result_df = self._mapping(transformed_df)
                self._load(result_df)
            
            self.file_backup()
                
        except Exception as e:
            self.logger.error(f'Error: {str(e)}', exc_info=True)