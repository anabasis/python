# 모듈

## [01] 모듈과 패키지의 사용

- 모듈: def로 선언된 함수, class들을 모아놓은것
- 개발자가 다양한 분야의 SW를 개발할 수 있도록 미리 파이썬 언어에서 지원하는 것을
  내장 모듈(파이썬 파일, 내장 함수: 예) print(), str(), list()...)이라고합니다.
- 개발자는 자신이 필요한 모듈을 생성 할 수 있습니다.

- 모듈은 import하여 사용합니다.
   import 모듈이름     ← 파이썬 파일명
   import 패키지 이름.모듈 이름   ← 폴더.파이썬 파일명
   import 이름이 긴 패키지.모듈명 as 별명
   from 모듈 이름 import 함수 이름   ← 하나의 함수만 가져옴
   from 패키지 이름 import 모듈 이름    ← 패키지에서 파일을 가져옴.
   from 패키지 이름.모듈 이름 import 함수 이름

- 패키지: 모듈이 모이면 폴더가 생성되고 패키지라함.
  일반 폴더와 구분하기위해 패키지는 폴더안에 '__init__.py' 파일을 생성하며
  version 1.0 정도의 문자열을 내용으로 표시합니다.
  Python 3.3부터는 '__init__.py' 파일 선언이 없어도 모든 폴더가 Package로 인식됩니다.

- 하위 패키지의 생성은 계속적인 하위 폴더를 생성합니다.

- 파이썬은 자바의 main 메소드가 있는 클래스 처럼 시작 파일이 지정되지 않음(JAVA: main 메소드).
  
1. 모듈의 선언
   - Jupyter Notebook: '/ws_python/notebook/module' 폴더를 생성합니다.
   - PyCharm에서는 '/ws_python/notebook/module' 패키지를 생성합니다.(프로젝트 선택 -> New -> Python Package)
   - Jupyter Notebook은 'Lib.ipynb' 파일이 생성되어 import가 현재 지원이 안됨. 따라서 'Lib.py' 파일로 저장해서 사용해야함 ★.
   >> /ws_python/notebook/module/Lib.ipynb
   >> /ws_python/notebook/module/Lib.py

    ```python
    def absolute(su1):
        if su1 < 0:
            su1 = su1 * -1
        return su1
    ```

    >> /ws_python/notebook/module/LibUse.ipynb

   - '__name__' 시스템 변수는 현재 파이썬 파일이 참조되는 모듈이 아니라,  실행이 시작되는 파일이면  '__main__' 값을 갖게됩니다. 즉 시작파일인지 아닌지를 판단하는 기준이됩니다.

    ```python
    # 예
    # __name__이 '__main__' 값이면 시작 파일임.
    if __name__ == '__main__':
    ```

2. 패키지안의 모듈의 선언
    >> /ws_python/notebook/module/tool/Math.ipynb
    >> /ws_python/notebook/module/tool/Math.py

    ```python
    def roundsu(su1):
        su1 = su1 + 0.5
        return str(int(su1))

    def tot(*args): # 가변 인수, 전달받은 수의 합계
        tot = 0
        for su in args:
            tot = tot + su
        return tot
    .....
    if __name__ == '__main__':
        print(roundsu(10.4))
        print(roundsu(10.5))
        print(tot(10, 20, 30))
    ```

3. 패키지를 동반한 모듈의 선언

    >> /ws_python/notebook/module/tool/Tool.ipynb
    >> /ws_python/notebook/module/tool/Tool.py

    ```python
    def maxsu(su1, su2):
        if su1 > su2:
            return su1
        else:
            return su2

    def minsu(su1, su2):
        if su1 < su2:
            return su1
        else:
            return su2

    def swap(su1, su2):
        temp = su1
        su1 = su2
        su2 = temp

        return su1, su2
    ```

4. import를 이용한 모듈의 사용
   - import 선언시 실행시에 import되는 모듈이 자동으로 실행됩니다.
   - 이 문제를 방지하기 위하여 if __name__ == '__main__': 코드를 이용하여 현재 참조 상태인지 아니면 main(Run, Start)으로 시작되는지를 구분하여 코드를 실행합니다.
   - Lib.py, Math.py, Tool.py 파일에 테스트 스크립트가 실행이 안되도록 아래 처럼 코드 추가

    ```python
    ## 예)
    if __name__ == '__main__':
        print(absolute(1000))
        print(absolute(-1000))
    ```

    >> /ws_python/notebook/ModuleTest.ipynb
    - 파일 저장 폴더 'notebook'으로 지정, module안에 있으면 인식이안됨.

    ```python
    %reset
    # 변수 삭제
    # loading된 library(module, python file)는 Kernel Restart를 해야함.
    ```

   - 에러의 해결: File --> Download as --> Python 로 확장자가 py가 되도록 저장,저장시 폴더 변경하지 말것.
