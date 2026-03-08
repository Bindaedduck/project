import pandas as pd
import glob
import os

class IPMProcessor:
    def __init__ (self, input_dir, split_rows=2000000, chunk_rows=100000):
        self.input_dir = input_dir
        self.output_dir = os.path.join(input_dir, "output")
        self.split_rows = split_rows
        self.chunk_rows = chunk_rows

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        print(self.output_dir)
    
    def fill_na(self, df, column_dict):
        return df.fillna(value=column_dict)

    def drop_col(self, df, col):
        print(col)
        df.drop(col, axis=1, inplace=True)

        return df
    
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
    
    def run_unified_batch(self, fill_na=None, drop_col=None, convert_timestamp=None, drop_na=None, output_extension=".csv.gz"):
        file_list = sorted(glob.glob(os.path.join(self.input_dir, "*.csv")))
        print(f" 총 {len(file_list)}개의 파일을 통합 처리합니다.")

        file_part = 1
        current_rows = 0

        for file_path in file_list:
            print(f"{os.path.basename(file_path)} 읽는 중...")

            reader = pd.read_csv(file_path, chunksize=self.chunk_rows)

            for chunk in reader:
                if fill_na:
                    chunk = self.fill_na(chunk, fill_na)
                    print("fill_na 작업 완료")
                if drop_col:
                    chunk = self.drop_col(chunk, drop_col.split(','))
                    print("drop_col 작업 완료")
                    print(chunk)
                if convert_timestamp:
                    for col, length in convert_timestamp():
                        chunk = self.convert_timestamp(chunk, col, length)
                    print("convert_timestamp 작업 완료")
                if drop_na:
                    chunk = self.drop_na(chunk, col)
                    print("drop_na 작업 완료")

                output_name = f"result_part_{file_part}"+output_extension
                output_path = os.path.join(self.output_dir, output_name)

                if output_extension == 'csv.gz':
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
            
            print(f"{output_name} 생성 완료")
            
        print("전체 작업 완료")

def main():
    INPUT_DIR = r"C:\Users\tjrwl\Desktop\Archive\01.Work\01.Project\삼성전자 AX 프로젝트 설계\Data"

    processor = IPMProcessor(input_dir=INPUT_DIR)

    processor.run_unified_batch(

        # fill_na: 컬럼 값이 빈칸이면 특정문자열로 채운다. / param 형식: {컬럼 이름: 빈칸을 채울 문자열, ...}
        # drop_col: 삭제할 컬럼  / param 형식: Ex-삭제할 컬럼 이름, ...
        # convert_timestamp: timestamp 형식 datetime으로 변경 / param 형식: {timestamp컬럼 이름, timestamp 길이}
        # output_extension: 결과파일 확장자

        fill_na={"case_id":"NA", "event_id":"NA", "server_node_name":"NA"},
        drop_col= "status_code,resource_id",
        # convert_timestamp={"time": 10},
        output_extension=".csv"
    )

if __name__ == "__main__":
    main()



    