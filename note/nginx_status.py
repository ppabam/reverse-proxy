import os
from datetime import datetime
import time

def get_nginx_status() -> str:
    import requests
    res = requests.get("http://localhost:8949/nginx_status")
    text = res.text
    return text

def pasing_status(text) -> dict:
    lines = text.split('\n')
    active_connections = int(lines[0].split(' ')[2])

    lines_3_s = lines[2].split(' ')
    # accepts, handled, requests = int(lines_3_s[1]), int(lines_3_s[2]), int(lines_3_s[3])
    accepts, handled, requests = map(int, lines_3_s[1:4])
    
    lines_4_s = lines[3].split(' ')
    # reading, writing, waiting = int(lines_4_s[1]), int(lines_4_s[3]), int(lines_4_s[5])
    reading, writing, waiting = map(int, lines_4_s[1:6:2])
    return {
        "timestamp": int(datetime.now().timestamp()),
        "active_connections": active_connections,
        "accepts": accepts,
        "handled": handled,
        "requests": requests,
        "reading": reading,
        "writing": writing,
        "waiting": waiting
    }

def write_log(v: str, file_name):
    with open(file_name, "a") as f:
        f.write(v + '\n')

previous_data = {}

def diff_data(current):
    if not previous_data:
        print("No previous data")
        return current
        
    diff_data = current.copy()  # 현재 상태를 복사하여 나머지 값을 그대로 유지
    for key in ['accepts', 'handled', 'requests']:
        diff_data[key] = current[key] - previous_data[key]  # 차이값 계산
    return diff_data

# 메인 루프
def main():
    print("Starting ...")
    while True:
        # 현재 데이터 가져오기
        text = get_nginx_status()
        current = pasing_status(text)
        
        data = diff_data(current)
        global previous_data
        previous_data = current
        
        file_name = 'nginx_status.csv'
        if not os.path.exists(file_name):
            header = ",".join(data.keys())
            write_log(header, file_name)
        
        v = ",".join(map(str, data.values()))
        write_log(v, file_name)
        print(v)
       
        # 10초 대기
        time.sleep(10)

if __name__ == "__main__":
    main()