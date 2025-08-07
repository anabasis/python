from django.shortcuts import render
from ais.models import Calc      # models.py 파일의 Calc class import 선언
from ais.models import Country # models.py 파일의 Country class import 선언

# Create your views here.
# http://127.0.0.1:8000 --> /ais/templates/index.html
def index(request):
    return render(request, 'index.html')

# http://127.0.0.1:8000/calc/add/add/50/100 --> /ais/templates/calc/add.html
def add(request, su1, su2):
    calc = Calc()  # 객체 생성
    res = calc.add(su1, su2)  # 메소드 호출
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    return render(request, 'calc/add.html', {'su1': su1, 'su2': su2, 'res': res})

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



