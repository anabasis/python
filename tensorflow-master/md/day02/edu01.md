# 함수

## [01]  함수 다루기, 함수의 인자, 지역 변수와 전역 변수, 리턴값

- 함수는 1개이상의 명령어를 그룹으로 묶어 반복 처리가 가능합니다.
- 데이터(변수)를 사칙연산(+, -, *, /, %)을 이용하여 처리하는 역활을 합니다.
- 데이터를 입출력하는 경우 사용합니다.
- 한번 만든 함수는 계속적으로 호출(재사용) 할 수 있습니다.
- SW 콤포넌트의 가장 작은 단위라고 할 수 있습니다.
- 함수는 소괄호 '()'를 선언해야합니다.
- 함수로 전달하는 데이터를 Parameter, 전달받는 쪽을 Argument라고 부릅니다.
- 파이썬은 Method Overroding을 지원하지 않습니다. 하지만 가변 인수로 어느정도 비슷한 기능을
구현 할 수 있습니다.
- 형식: def 함수이름(인자1, 이자2...):
            코드들
        return 결과값

1. 함수로 데이터 전달
   - *actors: 인수를 tuple 형태로 가변 인자로 전달 받음
   - **actors: 인수를 dictionary 형태로 가변 인자로 전달 받음
2. 지역 변수와 전역변수
   - 지역 변수: 메소드(함수) 안에 선언, 메소드(함수) 안에서만 사용 가능
   - 전역 변수: 메소드(함수) 외부에 선언, 모든 메소드(함수) 에서 사용 가능
   - global: 전역 변수의 사용 선언

### 1. Script

>> /ws_python/notebook/module/Def.ipynb

- Jupyter Notebook에서 '/ws_python/notebook/module' 폴더를 생성합니다.
- (Python3부터 폴더와 패키지의 구분이 없어짐)
- PyCharm에서는 '/ws_python/notebook/module' 패키지를 생성합니다.
  (프로젝트 선택 -> New -> Python Package)

```python
def movie1(name):  # name 인수
    print('영화명:' + name)

def movie2(name, genre):  # 인수 여러개 사용 가능
    print('영화명:' + name)
    print('장  르:' + genre)

def movie3(name, genre, score=5.0):  # 기본값 사용
    print('영화명:' + name)
    print('장  르:' + genre)  
    print('평  점:' + str(score))
.....

def movie5(*actors):  # tupe, 가변인자 처리
    print(type(actors))
    print(actors)
.....

def movie6(movie, **actors):  # 고정과 가변인자 병합 처리
    print(type(actors))
    print(movie)
    print(actors)  # Dictionary
.....

def season(month):
    season=''
    if month == 1:
        season='January'
    elif month == 2:
        season='February'
    elif month == 3:
        season="March"
    else:
        season="Only input 1 ~ 3"
    return season
```
