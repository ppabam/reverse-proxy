import requests
import time
import os
from datetime import datetime

# 상태 데이터를 가져오는 함수
def fetch_nginx_status():
    try:
        res = requests.get("http://localhost:8949/nginx_status")
        text = res.text
        
        # TODO
        # ac,accepts,handled,nginx_requests,reading,writing,waiting 파싱
        ac,accepts,handled,nginx_requests,reading,writing,waiting = ""
        
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ac': ac,
            'accepts': accepts,
            'handled': handled,
            'requests': nginx_requests,
            'reading': reading,
            'writing': writing,
            'waiting': waiting
        }
    except Exception as e:
        print(f"Error fetching status: {e}")
        return None

# 파일에 데이터 저장
def save_to_file(data, filename="nginx_status.txt"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as f:
        if not file_exists:
            # 헤더 작성
            header = ','.join(data.keys()) + '\n'
            f.write(header)
        # 데이터 작성
        line = ','.join(str(value) for value in data.values()) + '\n'
        f.write(line)

# 이전 데이터 불러오기
def load_previous_data(filename="nginx_status.txt"):
    if not os.path.isfile(filename):
        return None
    with open(filename, 'r') as f:
        lines = f.readlines()
        if len(lines) < 2:  # 헤더만 있는 경우
            return None
        last_line = lines[-1].strip().split(',')
        keys = lines[0].strip().split(',')
        return dict(zip(keys, last_line))

# 차이값 계산 및 저장
def calculate_and_save_diff(current, previous, filename="nginx_status_diff.txt"):
    if previous is None:
        return
    
    diff = {
        'timestamp': current['timestamp'],
        'accepts_diff': int(current['accepts']) - int(previous['accepts']),
        'handled_diff': int(current['handled']) - int(previous['handled']),
        'requests_diff': int(current['requests']) - int(previous['requests']),
        'ac': current['ac'],  # 순간값은 그대로 저장
        'reading': current['reading'],
        'writing': current['writing'],
        'waiting': current['waiting']
    }
    
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as f:
        if not file_exists:
            header = ','.join(diff.keys()) + '\n'
            f.write(header)
        line = ','.join(str(value) for value in diff.values()) + '\n'
        f.write(line)

# 메인 루프
def main():
    print("Starting Nginx status monitoring...")
    while True:
        # 현재 데이터 가져오기
        current_data = fetch_nginx_status()
        if current_data:
            # 원본 데이터 저장
            save_to_file(current_data, "nginx_status.txt")
            print(f"Saved raw data: {current_data}")

            # 이전 데이터 불러오기
            previous_data = load_previous_data("nginx_status.txt")
            
            # 차이값 계산 및 저장
            if previous_data:
                calculate_and_save_diff(current_data, previous_data, "nginx_status_diff.txt")
                print(f"Saved diff data: {previous_data['timestamp']} -> {current_data['timestamp']}")

        # 10초 대기
        time.sleep(10)

if __name__ == "__main__":
    main()