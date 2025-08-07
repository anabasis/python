# 귀농귀촌 적응 예측 시스템

## [01] 귀농귀촌 적응 예측 시스템

1. 머신 러닝 주제: 시골 귀농, 귀촌 적응 가능성 예측하기.
2. 변수 구성
   - 영향을 많이 미칠것으로 예상이 되는 변수의 선정
   - 공학적인 지식과 함께 인문학적인 사고력이 필요함.
   - 데이터 분석가의 역량에 따라 크게 달라질 수 있음.

   1) 주당 음주 횟수: 0 ~ 3(3회 이상)
   2) 농촌에서 생활적이 있다: 0(없음), 1(있음)
   3) 가족중에 농촌에서 생활하고 있는 친척있는 여부: 0(없음), 1(있음)
   4) 1년동안의 여행 횟수(교통을 이용한 등산/캠핑, 당일, 국내, 국외 모두 해당): 0 ~ 12
   5) 집을 소유 할 수 있는 경제력: 0(없음), 1(있음)
   6) 경작 할 수 있는 토지 평수(0: 없음, 1: ~ 1000 미만, 2: ~ 3000미만, 3: 3000 이상): 0
   7) 정착: 1, 실패: 0

3. 데이터 준비
- 일부 변수의 값이 변수가 가지고 있는 중요성에 비해서 너무 큰값을 가지고 있는 경우
 정규를 해야함.
- 정규화방법: X / 최대값, X / 특정 기준값, 표준화 공식을 이용하여 z 값을 산출하여 사용
- 정규분포를 표준정규분포로 바꾸는 Z의 공식
  Z = X-μ / σ (X: 확률변수, μ: 평균, σ: 표준 편차)

  ```python
  xm = np.mean(x[:, 5])
  z = (x - xm) / np.std(x[:, 5])
  ```

  - 최대값을 이용한 방법
  
  ```python
  max_val = np.max(data[:, 5])
  print(max_val)

  for item in data:
    item[5] = item[5] / max_val
    print(data[:3, 5])
  ```

- 정상적인 정규화의 기준은 정확도가 상승하는지 그리고 손실값이 감소되는지의 여부에 따라 적용
- 대부분의 정수형 큰값은 정규화를 진행하여 학습함.

## [02] ais app, 귀농/귀촌 적응 예측, <http://127.0.0.1:8000/country/>, form.html, proc.html

1. URLconf 설계, URL과 View 매핑

|URL 패턴|View 이름|View가 처리하는 내용|
|:--:|:--:|:--:|
/                         index()             index.html 템플릿 출력
/calc/add/50/100/   add()               add.html 템플릿 출력, 더하기 연산 
/country/form/       country_form()   form.html    
/country/proc/       country_proc()    proc.html    
      
 
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
    path('country/form/', views.country_form),  # 귀농귀촌 적응 예측 시스템 예측폼
    path('country/proc/', views.country_proc),   # 귀농귀촌 적응 예측 시스템 처리
]
```

3. Model 제작, Calc 클래스의 add 메소드 선언

1) h5 model 복사
    C:/ai_201909/ws_python/machine/ais/AI_models/country2.h5

2) 처리 Model
▷ /ais/models.py 
-------------------------------------------------------------------------------------
from django.db import models

# Deep learning packages
import os
from keras.models import load_model
import numpy as np

# Create your models here.
class Calc:
    def add(self, su1, su2):
        self.res = su1 + su2
        return self.res


class Country:
    def country(self, data):  # self: 함수와 객체 연결
        print('data:', data)
        # self.res = data
        # data 형식: "0,0,0,5,1,0,0"
        data = np.array(data.split(','), dtype=float)  # or int
        # print('변환된 data:', data)

        # 2차원 배열로 변환
        x_data = np.array([
            data,
        ])

        # 절대 경로 사용
        path = os.path.dirname(os.path.abspath(__file__)) # 스크립트파일의 절대경로

        # model 이 있는 경로: C:/ai_201909/ws_python/notebook/machine/country/country2.h5
        # model = load_model("C:/ai_201909/ws_python/ai/ais/AI_models/country2.h5")
        model = load_model(os.path.join(path, 'AI_models/country2.h5'))

        yp = model.predict(x_data[0:1])  # 1건의 데이터
        # y_predict = model.predict(x_data)  # 1건의 데이터

        for i in range(len(x_data)):
            # print('적응 확률:', yp[i][0] * 100, ' %')
            pct = yp[i][0]
            print('적응 확률: {0:.3f}%'.format(pct * 100))

            if pct >= 0.8:
                print('귀농가능합니다.')
                self.res = '귀농가능합니다.'
            elif pct >= 0.5:
                print('귀촌을 권장합니다.')
                self.res ='귀촌을 권장합니다.'
            else:
                print('귀농/귀촌을 권장하지 않습니다.')
                self.res ='귀농/귀촌을 권장하지 않습니다.'

        return pct * 100, self.res  # pct, res

  
4. /ais/views.py 설정
▷ /ais/views.py
-------------------------------------------------------------------------------------
from django.shortcuts import render
from ais.models import Calc # models.py 파일(모듈)의 Calc class import 선언
from ais.models import Country # models.py 파일의 Country class import 선언

# Create your views here.
def index(request):
    # /ws_python/machine/ais/templates/index.html
    return render(request, 'index.html')

def country_form(request):
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    return render(request, 'country/form.html', {})

def country_proc(request):
    country = Country()
    data = request.GET['data']  # form get
    # print('views.py', data)
    pct, res = country.country(data)

    pct = round(pct, 1) # 소수 첫째자리까지 반올림

    return render(request, 'country/proc.html', {'data': data, 'pct':pct, 'res': res})

    
-------------------------------------------------------------------------------------
    

5. templates 생성       
1) form 파일
▷ /ais/templates/country/form.html
-------------------------------------------------------------------------------------
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Survival</title>
    {% load static %}
    <link href="{% static '/css/style.css' %}" rel="Stylesheet" type="text/css">
    <script type="text/JavaScript"
                 src="http://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    <script type="text/javascript" language="javscript">
        function send() {
          if ($.trim($('#data').val()).length == 0) {
            alert('데이터를 입력해주세요');
          } else {
            frm.submit();
          }
        }
    </script>
</head>
<body>
<DIV class="container">
<H1>귀농귀촌 적응 예측 시스템</H1>
 <form id='frm' name='frm' action='/country/proc' method='GET'>
  <br>
  데이터<br>
  <input type='text' id='data' name='data' value='1,0,1,6,1,0' style='width: 60%;'><br>
  <br>
  <button type='button' onclick="send();">실행</button>
  <button type='button' onclick="location.href='/';">HOME</button>
  <br><br>
  테스트 데이터<br>
  정착: 1,0,1,6,1,0<br>
  실패: 0,0,0,5,1,0<br>
</form>
</DIV>
</body>
</html>
 
-------------------------------------------------------------------------------------
  
2) process 파일
▷ /ais/templates/country/proc.html
-------------------------------------------------------------------------------------
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>결과</title>
    {% load static %}
    <link href="{% static '/css/style.css' %}" rel="Stylesheet" type="text/css">
    <script type="text/JavaScript"
                 src="http://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    <script type="text/javascript" language="javscript">
        function send() {
          if ($.trim($('#data').val()).length == 0) {
            alert('데이터를 입력해주세요');
            return;
          } else {
            frm.submit();
          }
        }
    </script>
</head>
<body>
<DIV class="container">
<H1>귀농귀촌 적응 예측 시스템</H1>
<br>
<UL>
  <LI  style='font-size: 26px; list-style: none;'>데이터: {{data}}</LI>
    <LI  style='font-size: 26px; list-style: none;'>귀농/귀촌 성공 확률: <span style="text-decoration: underline;">{{pct}} %</span></LI>
    <LI  style='font-size: 26px; list-style: none;'>결과: <span style="text-decoration: underline;">{{res}}</span></LI>
</UL>

 <form id='frm' name='frm' action='/country/proc' method='GET'>
  <br>
  데이터<br>
  <input type='text' id='data' name='data' value='1,0,1,6,1,0' style='width: 60%;'><br>
  <br>
  <button type='button' onclick="send();">실행</button>
  <button type='button' onclick="location.href='/';">HOME</button>
  <br><br>
  테스트 데이터<br>
  정착: 1,0,1,6,1,0<br>
  실패: 0,0,0,5,1,0<br>
</form>
</DIV>
</body>
</html>


-------------------------------------------------------------------------------------

  
   
5. 접속 테스트
C:\ai4\ws_python\ai>activate machine
(machine) F:\ai3\ws_python\machine>python manage.py runserver 0.0.0.0:8000
Django version 2.2.2, using settings 'config.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
  
2) 접속: http://127.0.0.1:8000/
 