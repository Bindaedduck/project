import pandas as pd
import os

def drop_col():
    input_delete_col = input("삭제할 컬럼: ")
    input_processing = input("1.단건 처리 / 2.복수건 처리: ")
    input_folder_path = input("폴더 경로: ")
    include_str = ""
    processing_flas = True
    
    if input_processing == "1":
        include_str = input("파일 이름: ")
        
        if include_str == "":
            processing_flag = False
        
    elif input_processing == "2":
        include_str = input("작업 파일의 확장자(입력 안할 시 폴더 안 파일 전체 작업): ")
        
    if processing_flag:
        for file_name in os.listdir(input_folder_path):
            if include_str in file_name:
                file_path = os.path.join(input_folder_path, file_name)
                file_name_without_ext = os.path.splitext(file_name)[0]+"_etf.csv"
                csv_result_file_path = os.path.join(input_folder_path, file_name_without_ext)
                
                df = pd.read_csv(file_path)
                df.drop(input_delete_col, axis=1, inplace=True)
                df.to_csv(csv_result_file_path, index=False)
            
        print("작업 정상 완료")
    else:
        print("작업 비정상 종료")
    
def select_work():
    print("=== 작업 목록 ===")
    print("1. 특정 컬럼 삭제")
 	print("2. ""문자열에서 ,문자 ;문자로 변환")
    print("================")
    input_work = input("수행 할 작업을 입력하세요: ")
    return input_work

def main():
    work = select_work()
    
    if work == "1":
        drop_col()

if __name__ == "__main__":
    main()