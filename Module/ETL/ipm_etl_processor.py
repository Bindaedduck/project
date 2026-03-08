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
    
    def run_unified_batch(self):
        file_list = sorted(glob.glob(os.path.join(self.input_dir, "*.csv")))
        print(f" 총 {len(file_list)}개의 파일을 통합 처리합니다.")

        file_part = 1
        current_rows = 0

        for file_path in file_list:
            print(f"{os.path.basename(file_path)} 읽는 중...")

            reader = pd.read_csv(file_path, chunksize=self.chunk_rows)

            for chunk in reader:
                output_name = f"result_part_{file_part}.csv.gz"
                output_path = os.path.join(self.output_dir, output_name)

                write_header = not os.path.exists(output_path)

                chunk.to_csv(output_path, mode='a', index=False,
                             header=write_header, encoding='utf-8-sig',
                             compression='gzip')

                current_rows += len(chunk)

                if current_rows >= self.split_rows:
                    print(f"{output_name} 생성 완료")
                    file_part += 1
                    current_rows = 0
            
            print(f"{output_name} 생성 완료")
            
        print("전체 작업 완료")

def main():
    INPUT_DIR = r"경로"

    processor = IPMProcessor(input_dir=INPUT_DIR)

    processor.run_unified_batch()

if __name__ == "__main__":
    main()



    