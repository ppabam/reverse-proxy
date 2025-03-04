#!/bin/bash

# 출력 파일 지정
OUTPUT_FILE="docker_stats.csv"

# 파일이 처음 생성될 때 헤더 추가
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Timestamp,HostCPU,HostMemUsage,HostMemTotal,HostMemPerc,Container,Name,ID,CPUPerc,MemUsage,MemPerc,NetIO,BlockIO,PIDs" > "$OUTPUT_FILE"
fi

# CPU 사용량 계산 함수 (host)
get_host_cpu_usage() {
    # /proc/stat에서 CPU 사용량 가져오기
    CPU1=($(head -n1 /proc/stat))
    sleep 1
    CPU2=($(head -n1 /proc/stat))

    # 각 필드 추출
    IDLE1=${CPU1[4]}
    IDLE2=${CPU2[4]}
    TOTAL1=0
    TOTAL2=0

    for value in "${CPU1[@]:1}"; do
        TOTAL1=$((TOTAL1 + value))
    done

    for value in "${CPU2[@]:1}"; do
        TOTAL2=$((TOTAL2 + value))
    done

    # 사용된 CPU 시간 계산
    DIFF_IDLE=$((IDLE2 - IDLE1))
    DIFF_TOTAL=$((TOTAL2 - TOTAL1))
    DIFF_USAGE=$((100 * (DIFF_TOTAL - DIFF_IDLE) / DIFF_TOTAL))

    echo "$DIFF_USAGE"
}

# 메모리 사용량 계산 함수 (host)
get_host_memory_usage() {
    MEM_TOTAL=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    MEM_FREE=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    MEM_USED=$((MEM_TOTAL - MEM_FREE))
    MEM_PERCENTAGE=$(awk "BEGIN {printf \"%.2f\", ($MEM_USED/$MEM_TOTAL)*100}")

    echo "$MEM_USED,$MEM_TOTAL,$MEM_PERCENTAGE"
}

# 무한 루프 실행
while true; do
    # 현재 타임스탬프 (초 단위)
    TIMESTAMP=$(date +%s)

    # 호스트 CPU 및 메모리 사용량 가져오기
    HOST_CPU=$(get_host_cpu_usage)
    read HOST_MEM_USED HOST_MEM_TOTAL HOST_MEM_PERC <<< $(get_host_memory_usage)

    # docker stats 실행 및 JSON 파싱
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

        # CSV 형식으로 타임스탬프, 호스트 리소스, 컨테이너 리소스 출력
        echo "$TIMESTAMP,$HOST_CPU,$HOST_MEM_USED,$HOST_MEM_TOTAL,$HOST_MEM_PERC,$CONTAINER,$NAME,$ID,$CPU_PERC,\"$MEM_USAGE\",$MEM_PERC,\"$NET_IO\",\"$BLOCK_IO\",$PIDS" >> "$OUTPUT_FILE"
    done

    # 10초 대기
    sleep 10
done

