# Task of Wanted lab
* fastapi를 이용한 docker-compose API 애플리케이션 개발

# docker build
```sh
docker-compose build --no-cache
```

# docker run
```sh
# 불륨 생성
docker-compose up --build
```

# docker migration
```sh
docker-compose exec backend sh
# python manager.py db init
# python manager.py db migrate 
```

## REST API 기능
```
회사명 자동완성 (회사명의 일부만 들어가도 검색)
회사 이름으로 회사 검색 
새로운 회사 추가
```