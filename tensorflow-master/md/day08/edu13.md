# Django 외부 IP 접속

## [참고] Django 외부 IP 접속

### 1. 외부 접속 테스트

1) /config/settings.py 설정 파일 변경

    ```python
    # 모든 ip 에서의 접속
    ALLOWED_HOSTS = ['*']
    ```

2) OS에서 8000번 포트 방화벽 열기

3) IP 지정 실행

    ```bash
    (machine) F:\ai3\ws_python\machine>python manage.py runserver 172.16.12.100:8000
    Django version 2.2.2, using settings 'config.settings'
    Starting development server at http://172.16.12.100:8000/
    Quit the server with CTRL-BREAK.
    ```

4) 접속: <http://127.0.0.1:8000/>       <-- Fail
   접속: <http://172.16.12.100:8000/> <-- Success

5) 모든 서버 IP의 접속

    ```python
    (machine) F:\ai3\ws_python\machine>python manage.py runserver 0.0.0.0:8000
    Django version 2.2.2, using settings 'config.settings'
    Starting development server at http://0.0.0.0:8000/
    Quit the server with CTRL-BREAK.
    ```

6) 접속: <http://127.0.0.1:8000/>     <-- Success
   접속: <http://172.16.12.100:8000/> <-- Success
