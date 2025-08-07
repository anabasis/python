# 제어문

## [01] 제어문 - 분기문 if

     - 조건에따라 판단을하여 코드를 실행합니다.
     - 조건에 따라 분기를 할 수 있습니다. 
     - if 조건식:
         참일 경우 실행
       else:
         거짓일 경우 실행
     - 중괄호 블럭안은 경계를 위해 들여쓰기를 2칸(2~4칸)정도해야합니다.  
      . 콜론 다음 라인부터 시작하는 코드는 들여쓰기 간격이 모두 동일해야합니다.
      . 들여쓰기 간격이 일정하지 않으면 ERROR 발생(JAVA는 상관 없음)
     - 블럭 지정후 'TAB' 키를 누르면 모두 들여쓰기가 됨.
     - 블럭 지정후 'Shift+TAB' 키를 누르면 모두 내어쓰기가 됨.  

![if](./images/08_(1).jpg)

1. If문의 기본 형태
   - 참일 경우만 실행하는 단순 if문
    ![if1](./images/09_(1).jpg)
   - 참과 거짓일 경우 각각 다르게 실행되는 if문
    ![if2](./images/10_(1).jpg)
   - 여러개의 if 조건을 나열하고 해당하는 조건에 참인 if 문을 실행하고 if 문 전체를
     종료합니다.
    ![if3](./images/11_(1).jpg)

   - if문은 if문을 포함 할 수 있습니다.
   - or: OR 연산자, 조건중 하나라도 참이면 참 처리, '또는'의 의미. 
     예) if su % 2 == 0 or su % 3 == 0:
   - and: AND 연산자, 모든 조건을 만족해야 참으로 처리, '그리고'의 의미. 
     예) if su % 2 == 0 and su % 3 == 0:

2. IF문의 다양한 사용예
- 'control'이란 폴더를 만들어 소스를 실습합니다.
  
▷ /ws_python/notebook/basic/IfTest.ipynb
-------------------------------------------------------------------------------------
 
 
 
-------------------------------------------------------------------------------------
 
 
3. 콘솔 파라미터 입력
import sys

var0 = sys.argv[0] <- 파일명
var1 = sys.argv[1]
var2 = int(sys.argv[1])

/ws_python/notebook/basic> python 파일명.py 인수1 인수2... 

 
  
[실습 1] 하나의 수를 정의하고 2, 3, 4, 5의 배수인지 판단하는 프로그램을 제작하세요. 
- Python 파일의 저장: Jupyter Notebook --> File --> Download as --> Python(.py)
- 실행
  C:\ai4\ws_python\notebook\basic>python IfExam1.py 100
  파일명: IfExam1.py
  입력수: 100
  
▷ /ws_python/notebook/basic/IfExam1.ipynb
-------------------------------------------------------------------------------------
 
 
 
-------------------------------------------------------------------------------------
 
 
* python 명령어가 실행이 안될경우 Path 확인 및 등록
C:\ai2\ws_python\python\control>echo %Path%

C:\ProgramData\Anaconda3;C:\ProgramData\Anaconda3\Library\mingw-w64\bin;C:\ProgramData\Anaconda3\Library\usr\bin;C:\ProgramData\An
aconda3\Library\bin;C:\ProgramData\Anaconda3\Scripts;C:\oraclexe\app\oracle\product\11.2.0\server\bin;C:\jdk1.8.0\bin;C:\ProgramDa
ta\Oracle\Java\javapath;C:\oraclexe\app\oracle\product\11.2.0\server\bin;C:\Program Files (x86)\AMD APP\bin\x86_64;C:\Program File
s (x86)\AMD APP\bin\x86;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Pro
gram Files (x86)\ATI Technologies\ATI.ACE\Core-Static;C:\mysql_16\mysql-5.7.17-winx64\bin;C:\spring_2017\spring-1.5.3.RELEASE\bin;
C:\spring_2017\apache-maven-3.5.0\bin;C:\Program Files\Bandizip\;C:\Program Files (x86)\ESTsoft\ALSee\x64
  
   
 
## [02] 제어문 - 반복문 While, for 문 

- switch ~ case, do ~ while문은 존재하지 않는다.

1. While 문 
   - 참일동안 실행합니다. 
   - 조건을 만족하지 않으면 한번도 실행을 하지 않습니다. 
   - 순환 횟수를 정확히 지정할 수 없을 경우 사용합니다.
   ![while](./images/06_(2).jpg)
2. for 문  
   - 반복 횟수가 지정되어 있는 경우 사용합니다. 

1) 유형 1
  for 변수 in 범위:
    반복으로 실행할 코드
 
2) 유형 2
  for 변수 in 범위:
    반복으로 실행할 코드
  else:
    for 구문이 모두 실행되었을 때 실행할 코드  
   
  
3. 실습
▷ /ws_python/notebook/basic/While_For.ipynb