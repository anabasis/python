# [01] 머신러닝과정 주말반 OT

WIFI 설정
AP: soldesk~, Password: soldesklove

윈도우 id: soldesk
password: soldesklove12, soldesk or soldesklove
<http://www.nulunggi.pe.kr>

1. 출석 확인
2. 강사 소개
3. 수강생 출석 유의 사항 전달
   - 재직자 안내
     . 토요일: 12:10 이전 입실 체크, 19:50이후 퇴실
     . 일요일: 10:10 이전 입실 체크, 17:50이후 퇴실, 점식 식사(1:00 ~ 2:00)  
   - 60 시간: 48시간 이상 수강해야 환급, 1일 결석만 해당, 1일 결석일 경우 지각 안됨(최악의 경우 4시간 안으로 지각 가능).
4. 교재 배포
   - 수업 내용은 전부 인터넷에서 확인 가능
5. 교재비 환불 불가 동의서 사인
6. 교재 대장 사인
7. 개발 장비의 기준
   - Intel i5와 비슷하거나 그이상의 고성능 CPU 성능를 갖는 14 ~ 15.1인치이상 노트북,
     26'이상의 모니터(width: 2048 x height: 1024 이상)
   - 2개 이상의 GPU 설치시에는 케이스가 큰 ATX 데스크탑을 추천
   - RAM 8GB 이상을 권장합니다.
   - HDD 사용보다 SSD 사용을 권장합니다.
   - NVIDIA RTX 2070 8G 이상의 그래픽 카드

## 수업 흐름

1. 파이썬 기초 문법
2. 파이썬 데이터분석 패키지
3. 머신러닝
4. 딥러닝
5. Django 웹 서비스 project

## 원격툴

<https://remotedesktop.google.com/support>

## [04] cx_freeze로 EXE 만들기

### 1. <http://cx-freeze.sourceforge.net>
### 2. install

  ```bash
  pip install cx_freeze
  ```

### 3. script 생성

  ```python
  # /reexam/Setup.py
  # -*- coding: utf-8 -*-
  import sys
  from cx_Freeze import setup, Executable

  setup(name = "Pyperclip",
        version = "1.0",
        description = "Pyperclip phone email filter",
        author = "dev",
        executables = [Executable("re09.py")])
        # executables = [Executable("re09.py", base="Win32GUI")])
  ```

### 4. 실행

  ```bash
  setup.py build
  build/exe.win-amd64-3.6/re09.exe
  ```
  
  실행
