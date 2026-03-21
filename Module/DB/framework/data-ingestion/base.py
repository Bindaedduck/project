import logging
import os
from abc import ABC, abstractmethod

class BaseIngestion(ABC):
    def __init__(self, system_name, file_path):
        self.system_name = system_name
        # file_path = file_path/system_name
        self.file_path = os.path.join(file_path, system_name)
        self.logger = self._set_logger()

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

    @abstractmethod
    def ingestion_logic(self):
        pass

    @abstractmethod
    def col_sync_logic(self):
        pass

    def run(self):
        try:
            self.col_syncc_logic(self)
            self.ingestion_logic(self)
        except Exception as e:
            self.logger.error(f'Error: {str(e)}', exc_info=True)