# Jupyter Notebook

## [01] Jupyter Notebook 커널(Conda 가상환경) 연동
 
1. [Anaconda Prompt] 관리자 권한으로 실행
(base) C:\Windows\system32> activate machine
 
 
2. ipykernel 라이브러리 설치
(machine) C:\Windows\system32>pip install ipykernel 
 
 
3.  jupyter notebook에 가상환경 kernel 추가
1) CPU 기반 커널 연동
(machine) C:\Windows\system32>python -m ipykernel install --user --name=machine
     
4. [Anaconda Prompt] 관리자 권한으로 실행
- C:\Windows\System32: 기본 작업 폴더 
(base) C:\Windows\system32>jupyter notebook
  
5. 커널 해제
(base) C:\Windows\system32>jupyter kernelspec uninstall machine
Kernel specs to remove:  machine  C:\Users\soldesk\AppData\Roaming\jupyter\kernels\machine
 
Remove 1 kernel specs [y/N]: y
   
 
## [02] Anaconda 5.1.0 Jupyter Notebook Interpreter의 사용
 
1. 기본 작업 폴더 생성
1) Command 실행
  
2) Notebook 작업 홈 폴더 생성
C:
CD \
MD ai_201909
MD ai_201909\ws_python
MD ai_201909\ws_python\notebook
MD ai_201909\ws_python\notebook\data
CD ai_201909\ws_python\notebook\data
 
폴더 PATH의 목록입니다.
볼륨 일련 번호는 C0EE-2E5F입니다.
C:\AI_201909
├─setup
└─ws_python
    └─notebook
        └─data
 
    
  
2. Jupyter Notebook 실행 파일 생성
- Jupyter Notebook을 실행하는 경로가 기본 작업 폴더로 인식됨. 
 
▷ C:/ai_201909/jupyter.cmd
  C:
  CD\
  CD ai_201909
  CD ws_python
  CD notebook
  call activate machine
  call Jupyter Notebook
 
  
   
[참고] 만약 특정 경로로 실행되면 Jupyter Notebook 기본 경로의 주석 처리
   - 여러명이 Jupyter Notebook 사용시는 폴더 충돌이 발생함으로 아래의 설정을 할것.
▷ C:/Users/soldesk/.jupyter/jupyter_notebook_config.py
    (Anaconda 4.4.0은 202번 라인, Anaconda 5.1.0 246번 라인)
.....
# c.NotebookApp.notebook_dir = 'C:/ai_201909/ws_python/notebook'
.....
 
    
   
[참고] 기본 작업 폴더의 변경
 
1) jupyter notebook --generate-config 실행 
   (base) C:\Users\user>jupyter notebook --generate-config
   Writing default config to: C:\Users\윈도우계정\.jupyter\jupyter_notebook_config.py 
  
2) C:/Users(사용자)/윈도우 로그인 계정/.jupyter/jupyter_notebook_config.py 편집
 
3) c.NotebookApp.notebook_dir = 'C:/ai_201905/ws_python/notebook' 설정 (246번 라인)
   - 폴더 구분자로 \ 사용하면 안됨 
     ERROR: c.NotebookApp.notebook_dir = 'C:\ai_201905\ws_python\notebook' 
    
4) jupyter notebook 실행
   관리자 모드: (base) C:\Windows\system32>jupyter notebook 
   또는
   관리자 모드: C:\Users\soldesk>jupyter notebook
 
[I 11:27:59.854 NotebookApp] Serving notebooks from local directory: C:/ai_201905/ws_p
ython/notebook
[I 11:27:59.855 NotebookApp] 0 active kernels
[I 11:27:59.855 NotebookApp] The Jupyter Notebook is running at: http://localhos
t:8888/?token=7f8b87761f12e45c0f0ddd1efe4d66d4441806e7df220c8a
[I 11:27:59.855 NotebookApp] Use Control-C to stop this server and shut down all
 kernels (twice to skip confirmation).
[C 11:27:59.857 NotebookApp]

## [03] 실습

1. Script 생성 및 저장
▷ /ws_python/notebook/basic/Test.ipynb
-------------------------------------------------------------------------------------
import tensorflow as tf

print(tf.__version__)
print("Hello 파이썬")

-------------------------------------------------------------------------------------

2. Script 실행
   Shift + Enter: 실행후 focus가 다음셀로 이동함.
   Ctrl + Enter: 실행후 focus가 다음셀로 이동하지 않음.
  
3. 코드 입력후 Tab을 누르면 자동으로 Assist 목록이 출력됨.
   np.TAB 클릭
