
# Django REST API

## 앱 실행
```
docker-compose up db
docker-compose up -d
python3 manage.py migrate 
```

# REST API

근태 관리 API
  * 특이사항
   > 직원들이 출입게이트에서 태그를 찍지않고 지나가는 경우가 있기때문에 연속으로 동일 태그 찍히는 경우는 무시하고 로그만 쌓음

## 출입 태그 기록

### Request

`POST /worktime/record/`

    curl -X POST http://localhost:8083/worktime/record/ -H "Content-Type: application/json"   -d '{"user_id": 1002, "tag": "IN"}'

### Response

    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "user_id": 1001,
        "date": "2023-01-17",
        "tag": "IN",
        "created": "2023-01-17T09:00:17.186199"
    }
    
## 일별 근무 기록 조회

### Request

`GET /worktime/list/<user_id>`

    curl -i -H 'Accept: application/json' http://localhost:8083/worktime/list/<user_id>

### Response

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 13,
            "user_id": 1001,
            "date": "2023-01-17",
            "in_time": "2023-01-17T09:00:17.186199",
            "out_time": "2023-01-17T18:00:57.704602",
            "total_work_time": 500,
            "total_rest_time": 40,
            "updated": "2023-01-17T15:35:17.192901"
        }
    ]
    
## 근무 기록 수정

### Request

`PUT /worktime/detail/<pk>`

    curl -i -H 'Accept: application/json' http://localhost:8083/worktime/detail/<pk>

### Response

    HTTP 200 OK
    Allow: PUT, DELETE, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "id": 13,
        "user_id": 1001,
        "date": "2023-01-17",
        "in_time": "2023-01-17T09:00:17.186199",
        "out_time": "2023-01-17T18:00:57.704602",
        "total_work_time": 480,
        "total_rest_time": 60,
        "updated": "2023-01-17T16:22:25.895739"
    }
    
## 근무 기록 삭제

### Request

`DELETE /worktime/detail/<pk>`

    curl -i -H 'Accept: application/json' http://localhost:8083/worktime/detail/<pk>

### Response

    HTTP 200 OK
    Allow: GET, PUT, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    "delete ok"
