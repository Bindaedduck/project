import pandas as pd
import glob
import json
import os

class IpmConvertCsvProcessor:
    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.output_dir = os.path.join(input_dir, "output")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def json_convert_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        
        # df = pd.json_normalize(json_data)
        df = pd.DataFrame(json_data)
        
        return df
    
    def xlsx_convert_csv(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
        
        return df
    
    def run_converted_batch(self, file_ext):
        file_list = sorted(glob.glob(os.path.jsoin(self.input_dir, "*."+file_ext)))
        print(f"총 {len(file_list)}개의 파일을 통합 처리합니다.")
        
        for file_path in file_list:
            print(f"{os.path.basename(file_path)} 읽는 중...")
            
            if file_ext == "json":
                reader = self.json_convert_csv(file_path)
            elif file_ext == "xlsx":
                reader = self.xlsx_convert_csv(file_path)
            
            output_name = f"result.csv"
            output_path = os.path.join(self.output_dir, output_name)
            
            reader.to_csv(output_path, mode='a', index=False, quoting=1, escapechar='\\', encoding='utf-8-sig')
        
        print("전체 작업 완료")
    
    def main():
        INPUT_DIR = r""
        
        processor = IpmConvertCsvProcessor(input_dir=INPUT_DIR)
        
        processor.run_converted_batch(
        	# file_ext: 변환할 파일 확장자 / param - json 또는 xlsx
            # file_ext='xlsx'
        )
        
    if __name__ == "__main__":
        main()