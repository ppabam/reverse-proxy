#!/bin/bash

# 출력 파일 지정
OUTPUT_FILE="docker_stats.csv"

# 파일이 처음 생성될 때 헤더 추가
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Timestamp,Container,Name,ID,CPUPerc,MemUsage,MemPerc,NetIO,BlockIO,PIDs" > "$OUTPUT_FILE"
fi

# 무한 루프 실행
while true; do
    # 현재 타임스탬프 (초 단위)
    TIMESTAMP=$(date +%s)

    # docker stats 명령어 실행 및 JSON 파싱
    sudo docker stats --no-stream --format "{{ json . }}" | while read -r line; do
        # JSON에서 필요한 필드 추출 (jq 필요, 설치 필요 시: sudo apt-get install jq)
        CONTAINER=$(echo "$line" | jq -r '.Container')
        NAME=$(echo "$line" | jq -r '.Name')
        ID=$(echo "$line" | jq -r '.ID')
        CPU_PERC=$(echo "$line" | jq -r '.CPUPerc')
        MEM_USAGE=$(echo "$line" | jq -r '.MemUsage')
        MEM_PERC=$(echo "$line" | jq -r '.MemPerc')
        NET_IO=$(echo "$line" | jq -r '.NetIO')
        BLOCK_IO=$(echo "$line" | jq -r '.BlockIO')
        PIDS=$(echo "$line" | jq -r '.PIDs')

        # CSV 형식으로 타임스탬프와 함께 출력
        echo "$TIMESTAMP,$CONTAINER,$NAME,$ID,$CPU_PERC,\"$MEM_USAGE\",$MEM_PERC,\"$NET_IO\",\"$BLOCK_IO\",$PIDS" >> "$OUTPUT_FILE"
    done

    # 10초 대기
    sleep 10
done
