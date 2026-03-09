import pandas as pd
import glob
import os

class IPMProcessor:
    def __init__ (self, input_dir, split_rows=2000000, chunk_rows=100000):
        self.input_dir = input_dir
        self.output_dir = os.path.join(input_dir, "output")
        self.split_rows = split_rows
        
        if chunk_rows > split_rows:
            self.chunk_rows = split_rows
        else:
            self.chunk_rows = chunk_rows

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def common_tasks(self, df):
        #이름 없는 컬럼 삭제
        df.drop(df.columns[df.columns.str.contains('Unnamed')], axis=1, inplace=True)
        
        # 컬럼 이름의 '.' -> ''로 변경
        df.columns = df.columns.str.replace('.', '', regex=False)
 		
        return df
        
    def drop_duplicate_key(self, col):
   		df = df.drop_dupliactes(subset=[col])
        
        return df
        
    def drop_col(self, df, col):
        df.drop(col, axis=1, inplace=True)

        return df
    
    def replace_data(self, df, col, find_date, mod_date):
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(find_date, mod_date, regex=False)
        
        return df
    
    def fill_na(self, df, column_dict):
        return df.fillna(value=column_dict)
    
    def convert_timestamp(self, df, col, length):
        time_unit = {10:'s', 13:'ms', 16:'us', 19:'ns'}
        work_time_unit = time_unit.get(length, 'us')
        
        # 유령값 제거
        ghost_value = -9223372036854775808
        df = df[df[col] != ghost_value].copy()

        df[col] = pd.to_datetime(df[col], unit=work_time_unit, errors='coerce')
        self.drop_na(col)
        
        return df

    def drop_na(self, df, col):
        return df.dropna(subset=[col])
    
    def run_unified_batch(self, drop_dupliacte_key=None, drop_col=None, replace_data=None, fill_na=None, convert_timestamp=None, drop_na=None, output_extension=".csv.gz"):
        file_list = sorted(glob.glob(os.path.join(self.input_dir, "*.csv")))
        print(f" 총 {len(file_list)}개의 파일을 통합 처리합니다.")

        file_part = 1
        current_rows = 0

        for file_path in file_list:
            print(f"{os.path.basename(file_path)} 읽는 중...")

            reader = pd.read_csv(file_path, chunksize=self.chunk_rows)

            for chunk in reader:
                
                if drop_dupliacte_key:
                    chunk = self.drop_duplicate_key(chunk, drop_duplicate_key)
                if drop_col:
                    chunk = self.drop_col(chunk, drop_col.split(','))
                if replace_data:
                    for col, find_data, mod_data in replace_data:
                        chunk = self.replace_data(chunk, col, find_data, mod_data)
                if fill_na:
                    chunk = self.fill_na(chunk, fill_na)
                if convert_timestamp:
                    for col, length in convert_timestamp():
                        chunk = self.convert_timestamp(chunk, col, length)
                if drop_na:
                    chunk = self.drop_na(chunk, drop_na)
                
                chunk = self.common_tasks(chunk)    

                output_name = f"result_part_{file_part}"+output_extension
                output_path = os.path.join(self.output_dir, output_name)

                if output_extension == '.csv.gz':
                    write_compression = 'gzip'
                else:
                    write_compression = None

                write_header = not os.path.exists(output_path)
                
                chunk.to_csv(output_path, mode='a', index=False,
                             header=write_header, quoting=1,
                             escapechar='\\', encoding='utf-8-sig',
                             compression=write_compression)

                current_rows += len(chunk)

                if current_rows >= self.split_rows:
                    print(f"{output_name} 생성 완료")
                    file_part += 1
                    current_rows = 0
            
            if os.path.exists(output_path):
            	print(f"{output_name} 생성 완료")
            
        print("전체 작업 완료")

def main():
    INPUT_DIR = r"C:\Users\tjrwl\Desktop\Archive\01.Work\01.Project\삼성전자 AX 프로젝트 설계\Data"

    processor = IPMProcessor(input_dir=INPUT_DIR)

    processor.run_unified_batch(
		# chunk_size: 결과파일에 저장할 엑셀 row / param - row 수
        # drop_duplicate_key: key값 중복 제거 / param - "key컬럼 이름"
        # drop_col: 삭제할 컬럼  / param 형식: param - "삭제할 컬럼 이름, ..."
        # replace_data: 특정 컬럼 값을 다른 값으로 변경한다. / param - {col:변경할 컬럼 이름, find_data:변경할 값, mod_data:수정할 값}
        # fill_na: 컬럼 값이 빈칸이면 특정문자열로 채운다. / param - {컬럼 이름: 빈칸을 채울 문자열, ...}
        # convert_timestamp: timestamp 형식 datetime으로 변경 / param - {col:timestamp컬럼 이름, len:timestamp 길이}
        # drop_na: 데이터가 없는 컬럼에 해당하는 열 삭제 / param - "컬럼 이름" 
        # output_extension: 결과파일 확장자
		
        chunk_size = 0,
        drop_duplicate_key = "",
        drop_col = "",
        replace_data = {},
        fill_na = {},
        convert_timestamp = {},
        drop_na = "",
        output_extension = ""
    )

if __name__ == "__main__":
    main()



    