import os

file_path_data = r"C:\Users\toosm\AppData\Local\Temp\scp59490\home\toomstar\KGPT\dataset\wikidata\train.json"
file_path_kb = r"C:\Users\toosm\Downloads\preprocess\preprocess\knowledge-full.json"

file_path = file_path_kb

try:
    # 파일 존재 여부 확인
    if os.path.exists(file_path):
        print("파일이 존재합니다.")
        # 파일 크기 확인
        file_size = os.path.getsize(file_path)
        print(f"파일 크기: {file_size / (1024 * 1024):.2f} MB")
        
        # 파일의 처음 몇 바이트만 읽기
        with open(file_path, 'rb') as file:
            first_bytes = file.read(10000)
            print("파일의 처음 100바이트:")
            print(first_bytes)
    else:
        print("파일을 찾을 수 없습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

print("확인 완료")