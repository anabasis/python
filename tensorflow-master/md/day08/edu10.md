# 4칙연산의 기능의 제작

## [01] 4칙연산의 기능의 제작, <http://127.0.0.1:8000/calc/> 제작

1. URLconf 설계, URL과 View 매핑
|URL 패턴|View 이름|View가 처리하는 내용|
|:--:|:--:|:--:|
|/|index()|index.html 템플릿 출력|
|/calc/add/50/100/|add()|add.html 템플릿 출력, 더하기 연산|

2. URLconf 설정
▷ /config/urls.py

    ```python
    from django.contrib import admin
    from django.urls import path
    from ais import views # ais 패키지의 views.py 등록

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index), # index.html
        path('calc/add/<int:su1>/<int:su2>/', views.add), # 더하기
    ]
    ```

3. Model 제작, Calc 클래스의 add 메소드 선언
▷ /ais/models.py

    ```python
    class Calc:
        def add(self, su1, su2):
            self.res = su1 + su2
            return self.res
    ```  

4. /ais/views.py 설정
▷ /ais/views.py

    ```python
    from django.shortcuts import render
    from ais.models import Calc  # models.py 파일의 Calc class import 선언

    # http://127.0.0.1:8000 --> /ais/templates/index.html
    def index(request):
        return render(request, 'index.html')

    # http://127.0.0.1:8000/calc/add/add/50/100 --> /ais/templates/calc/add.html
    def add(request, su1, su2):
        calc = Calc()  # 객체 생성
        res = calc.add(su1, su2)  # 메소드 호출
        # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
        return render(request, 'calc/add.html', {'su1': su1, 'su2': su2, 'res': res})
    ```

5. templates 생성
▷ /ais/templates/calc/add.html
   - UTF-8로 저장

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Add</title>
        {% load static %}
        <link href="{% static '/css/style.css' %}" rel="Stylesheet" type="text/css">

    </head>
    <body>
    <DIV class="container">
    <H1 style="margin: 20px;">더하기 계산기입니다.</H1>

    <UL style="margin-left: 50px;">
    <LI  style='font-size: 26px;'>su1: {{ su1 }}</LI>
    <LI  style='font-size: 26px;'>su2: {{ su2 }}</LI>
    <LI  style='font-size: 26px;'>res: {{ res }}</LI>
    <LI  style='font-size: 26px; list-style: none; margin: 20px;'><A href='/'>HOME</A></LI>
    </UL>
    </DIV>
    </body>
    </html>
    ```

6. 접속 테스트
   1) 접속 테스트

        ```bash
        (machine) F:\ai3\ws_python\machine>python manage.py runserver
        Django version 2.2.2, using settings 'config.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CTRL-BREAK.
        ````

   2) 접속: <http://127.0.0.1:8000/>

## [과제]

1. 빼기
    URLconf 설계, URL과 View 매핑

    |URL 패턴|View 이름|View가 처리하는 내용|
    |:--:|:--:|
    |/|index()|index.html 템플릿 출력|
    |/calc/add/50/100/|add()|add.html 템플릿 출력, 더하기 연산|
    |/calc/sub/50/100/|sub()|sub.html 템플릿 출력, 빼기 연산|

2. 곱하기
    |URL 패턴|View 이름|View가 처리하는 내용|
    |:--:|:--:|
|/|index()|index.html 템플릿 출력|
|/calc/add/50/100/|add()|add.html 템플릿 출력, 더하기 연산|
|/calc/sub/50/100/|sub()|sub.html 템플릿 출력, 빼기 연산|
|/calc/mul/50/100/|mul()|mul.html 템플릿 출력, 곱하기 연산|

3. 나누기
    |URL 패턴|View 이름|View가 처리하는 내용|
    |:--:|:--:|
|/|index()|index.html 템플릿 출력
|/calc/add/50/100/|add()|add.html 템플릿 출력, 더하기 연산|
|/calc/sub/50/100/|sub()|sub.html 템플릿 출력, 빼기 연산|
|/calc/mul/50/100/|mul()|mul.html 템플릿 출력, 곱하기 연산|
|/calc/div1/50/100/|div1()|div1.html 템플릿 출력, 나누기 연산|

4. 정수나누기
    |URL 패턴|View 이름|View가 처리하는 내용|
    |:--:|:--:|
|/|index()|index.html 템플릿 출력|
|/calc/add/50/100/|add()|add.html 템플릿 출력, 더하기 연산|
|/calc/sub/50/100/|sub()|sub.html 템플릿 출력, 빼기 연산|
|/calc/mul/50/100/|mul()|mul.html 템플릿 출력, 곱하기 연산|
|/calc/div1/50/100/|div1()|div1.html 템플릿 출력, 나누기 연산|
|/calc/div2/50/100/|div2()|div2.html 템플릿 출력, 정수 나누기 연산|

5. 나머지
    |URL 패턴|View 이름|View가 처리하는 내용|
    |:--:|:--:|
|/|index()|index.html 템플릿 출력|
|/calc/add/50/100/|add()|add.html 템플릿 출력, 더하기 연산|
|/calc/sub/50/100/|sub()|sub.html 템플릿 출력, 빼기 연산|
|/calc/mul/50/100/|mul()|mul.html 템플릿 출력, 곱하기 연산|
|/calc/div1/50/100/|div1()|div1.html 템플릿 출력, 나누기 연산|
|/calc/div2/50/100/|div2()|div2.html 템플릿 출력, 정수 나누기 연산|
|/calc/mod/50/100/|mod()|mod.html 템플릿 출력, 정수 나누기 연산|
