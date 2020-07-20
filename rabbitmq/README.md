# PYTHON

## 가상환경 구성

```bash
cd E:\REPO\GIT_REPO\python>
python -m venv rabbitmq
cd rabbitmq
.\Scripts\activate
python -m pip install --upgrade pip
pip install pika

# 라이브러리 리스트 작성
pip freeze > requirements.txt
```

## 아나콘다 가상환경 구성

```bash
# example 가상환경 구성
C:\project>C:\Users\dojang\Anaconda3\Scripts\conda.exe create --name example

# example python3.5 가상환경 구성
C:\project>C:\Users\dojang\Anaconda3\Scripts\conda.exe --name example python=3.5

# example python3.5 32Bit 가상환경 구성
C:\project>set CONDA_FORCE_32BIT=1
C:\project>C:\Users\dojang\Anaconda3\Scripts\conda.exe --name example python=3.5

```

conda는 venv와는 달리 가상 환경을 현재 폴더에 생성하지 않고 아나콘다 설치 폴더의 envs 안에 생성합니다.
예) C:\Users\dojang\Anaconda3\envs\example

### activate 가상환경이름

```bash
C:\project>C:\Users\dojang\Anaconda3\Scripts\activate example
(example) C:\project>
```

아나콘다 가상 환경에 패키지를 설치할 때는 pip 대신 conda를 사용해야 합니다. 만약 pip를 사용하면 아나콘다 설치 폴더의 Lib/site-packages 안에 패키지가 저장되므로 주의해야 합니다.

### conda install 패키지

```bash
(example) C:\project>conda install numpy
```

### 주요 명령어

- conda info: 현재 환경 정보 출력
- conda search 패키지: 패키지 검색
- conda install 패키지=버전: 특정 버전의 패키지를 설치(예: conda install numpy=1.11.3)
- conda install 패키지=버전=파이썬버전: 파이썬 버전을 지정하여 특정 버전의 패키지를 설치(예: conda install numpy=1.11.3=py36_0)
- conda update 패키지: 패키지 업데이트
- conda list: 패키지 목록 출력
- conda remove 패키지: 패키지 삭제
- conda list --export > package-list.txt: 패키지 목록 및 버전 정보 저장:
- conda install --file package-list.txt: 패키지 목록으로 설치

### ATOM 반드시 설치해야 하는 패키지

- 반드시 설치해야하는 패키지 : Script, autocomplete-python
- 기본명령어를 설명해주는 패키지 : kite
- 같은 변수명 전체 변경 등 실제 작업에 편리한 패키지 : python-tools
- 같은 용어(변수명, 함수명 등)를 한번에 알게 해주는 패키지 : highlight-selected
- 전체 라인을 간단히 보여주는 패키지 : minimap
- 전체 라인에서도 같은 용어를 표시해주는 패키지 : minimap-highlight-selected
- 가상환경작업에 편리한 패키지 : auto-python-virtualenv
