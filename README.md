# reverse-proxy
- 성능
- 부하분산(LB)
- 가상호스트 및 라우팅

## python server
```bash
$ python -m http.server --directory pyweb1 8001
$ python -m http.server --directory pyweb2 8002
$ python -m http.server 8003 --directory blog 
```
## nginx
- https://ubuntu.com/tutorials/install-and-configure-nginx#1-overview
```bash
# install
$ sudo apt install nginx

$ sudo service nginx restart
$ sudo service nginx stop 
$ sudo service nginx start
$ sudo service nginx status #-> worker 16ea
$ sudo nginx -t # syntax check
```

## nGrinder
- http://localhost:8080 (admin/admin)
```bash
$ pwd
~/app
$ tree -L 2
.
├── ngrinder-agent
│   ├── lib
│   ├── run_agent.sh
│   ├── run_agent_bg.sh
│   ├── run_agent_internal.sh
│   └── stop_agent.sh
└── ngrinder-controller
    └── ngrinder-controller-3.5.9-p1.war

# controller
$ java -jar ngrinder-controller-3.5.9-p1.war

# agent
$ run_agent.sh
```

## Docker
```bash
$ docker compose up -d  # 백그라운드에서 컨테이너 실행
$ docker compose down   # 컨테이너 중지 및 네트워크 제거
$ docker compose stop   # 컨테이너 중지
$ docker compose start  # 중지된 컨테이너 다시 시작
$ docker compose restart  # 컨테이너 재시작
$ docker compose down  # 컨테이너, 네트워크 제거
$ sudo docker compose stats # 성능 모니터링

# scale out
$ sudo docker compose up -d --scale web1=3
```

## nginx
```bash
$ sudo docker exec -it <LB_NAME> bash
$ nginx -s reload
```

## FastAPI
- https://fastapi.tiangolo.com/
```bash
$ fastapi dev main.py
```






