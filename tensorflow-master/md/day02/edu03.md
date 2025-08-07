# 객체지향 언어

## [01] 클래스(CLASS:반, 학급, 그룹)

- 데이터 표현 방법의 변화
  - OOP 이전 시대: 문자 숫자 기반의 단순한 데이터 처리
    >> 예) String 성명, String 기술력, String 프로젝트, int 경력, String 자격증, int salary, int tax C언어의 구조체는 데이터를 묶어서 처리 지원
  - OOP 이후 시대: 의미 있는 데이터의 집합, 개발자가 새로운 데이터 타입을 생성하는 구조
    >> 예)
        - 개발자{String 성명, String 기술력, String 프로젝트, int 경력, String 자격증}
        - 노트북{String brand, float cpu, int hdd, float lcd, boolean wifi, boolean bluetooth}
        - 리조트{String 객실, Date 입실, Date 퇴실, Option 바베큐, Option 요트}
        - 영화{String 제목, int 년도, String  장르, int 상영 시간, String 국가...}
        - 배우{....}

- 데이터 처리 방법의 변화
   전통적인 프로그램은 순차식으로 구현되어 간결한 문법과 이해가 쉬웠습니다. 예) GW-BASIC...
   하지만 코드 라인수가 100라인만 지나가도 이해하기 어려워,
   소스 변경이 매우 힘들었습니다.
   순차 처리보다 발전된 프로그래밍 모델이 있는데 그것은 함수 기반 언어인
   C언어가 대표적입니다. 예) Fortran, C, COBOL, Pascal...
   C언어는 함수기반언어로 반복되는 코드를 그룹화해서 실행 할 수
   있었으나 같은 메모리의 데이터가 여러 함수들에 의해서 접근되어
   로직의 구분이 명확하지 않게되어 대규모 프로젝트를 진행하는데
   어려움이 많았습니다. 메모리 에러를 잡기 어려운 문제 발생.
   메모리 관련 코드의 분석이 어렵습니다.

   이를 개선한 OOP 모델은 각각의 기능과 데이터를 클래스라고 하는
   독립적인 코드 파일로 나누어, 서로간의 간섭을 줄이고,
   마치 레고블럭처럼 SW를 개발하는 모델을 말합니다.
   SW를 포함하여 이미 대부분의 산업이 레고처럼 블럭 구조기반으로 변경되고 있습니다.
   예) JAVA, Python, C++, Win32 API, MFC, .NET....
   예) 타이어 23560R17: 한국 타이어 HL3, 금호 크루젠 프리미엄, 넥센 RU50.....

1. 클래스 멤버: 클래스명으로 사용되는 변수, 모든 객체들이 공유함
   - 변수 선언시 초기값을 선언해야합니다.
    >> /ws_python/notebook/oop1/Class1.ipynb ← 클래스 선언은 첫자를 대문자 권장, 대소문자 error 발생 안함.

    ```python
    class Class1:
        year = 0
        product = ''
        price = 0
        dc = 0;
        service = False

    if __name__ == '__main__':
        Class1.year = 2017  # static적인 방법, 클래스명으로 접근
        Class1.product = 'SSD512'
        Class1.price = 200000
        Class1.dc = 3.5
        Class1.service = False

        print(Class1.year)
        print(Class1.product)
        print(Class1.price)
        print(Class1.dc)
        print(Class1.service)
    ```
  
2. 인스턴스 멤버: 객체를 생성하면 객체생성시 마다 새롭게 변수가 할당됨
    - self: 클래스의 객체 참조
    >> /ws_python/notebook/oop1/Class1.ipynb 에 추가

    ```python
    class Product:
    def setData(self):    # self: 함수와 객체 연결
        print(type(self))

    def setData2(self, year, product):
        self.year = year  # instance 변수, field, property, attribute, 멤버 변수, 속성...
        self.product = product
        self.price = 0
        self.dc = 0
    def printData(self):
        print('----------------------')
        print("생산 년도:", self.year)
        print("제품명:", self.product)
        print("가격:", self.price)
        print("할인 가격:", self.dc)
    ```

3. 메소드(함수)
   - 데이터를 전달 받은 메소드는 print('')를 이용하여 처리 결과를 출력 할 수 있지만, 처리된 값을 다양한 형태로 이용하기 위하여 메소드를 호출한 곳으로 처리값을 리턴 할 수도 있으며, 자주 이용됩니다.

   - 지역 변수: 메소드안에서만 사용가능한 변수
    >> /ws_python/notebook/oop1/Class1.ipynb 에 추가

    ```python
    class GDP:
        def getNation(self, code):
            str1 = "미결정"  # self가 선언되지 않았음으로 지역 변수
            if code == "KOR":
                str1 = "한국"
            elif code == "JAP":
                str1 = "일본"
            elif code == "CHA":
                str1 = "중국"

            return str1

        def getGDP(self, code):
            gdp = 1000  # self가 선언되지 않았음으로 지역 변수
            if code == "KOR":
                gdp = 28738
            elif code == "JAP":
                gdp = 37539
            elif code == "CHA":
                gdp = 6747

            return gdp

    .....
    # 한국
    # 28738
    ```

## [02] Class의 import

- 'oop1' 패키지를 추가하고 클래스를 생성 할 것
- class 이름과 저장 파일명(모듈명)이 달라도 상관없음.
- 클래스명과 대소문자 달라도 상관 없음.

>> /ws_python/notebook/oop1/GDPData.ipynb
>> /ws_python/notebook/oop1/GDPData.py

```python
class GDPData:
    def __init__(self):
        self.count = 0
        print('객체가 메모리에 생성되었습니다.')

    def __del__(self):
        print('객체가 메모리에서 소멸되었습니다.')

    def getNation(self, code):
        self.count = self.count + 1
        str1 = ""  # 지역 변수
        if code == "KOR":
            str1 = "한국"
        elif code == "JAP":
            str1 = "일본"
        elif code == "CHA":
            str1 = "중국"

        return str1

    def getGDP(self, code):
        self.count = self.count + 1
        gdp = 0   # 지역 변수
        if code == "KOR":
            gdp = 28738
        elif code == "JAP":
            gdp = 37539
        elif code == "CHA":
            gdp = 6747

        return gdp
```

>> 클래스 사용

- /ws_python/notebook/GDPDataUse.ipynb  <-- 패키지 외부에 선언해야 인식됨.
- ERROR: /ws_python/notebook/oop1/GDPDataUse.ipynb  
