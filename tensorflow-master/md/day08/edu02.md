# CNN, 이미지 인식을 통한 영화배우 정보 조회하기

## [01] CNN, 이미지 인식을 통한 영화배우 정보 조회하기

### 1. 이미지 준비, Google Crawler 제작

- 관련 패키지 설치

```bash
(base) C:\WINDOWS\system32>activate machinegpu
(machinegpu) C:\WINDOWS\system32>conda install scrapy
(machinegpu) C:\WINDOWS\system32>pip install icrawler
# (machinegpu) C:\WINDOWS\system32>pip uninstall pyopenssl
# (machinegpu) C:\WINDOWS\system32>pip install pyopenssl
```

>> /ws_python/notebook/machine/cnn_actor/google_crawler.ipynb

```python
from icrawler.builtin import GoogleImageCrawler
import requests
import urllib.request
import datetime

from scrapy.selector import Selector

count = 0
count_max = 0

# Amanda_Seyfried, Andrew_Lincoln, Anne_Hathaway, Keira_Christina_Knightley, Pierce_brosnan
inputSearch = input('배우 이름을 입력하세요: ')
count_max = int(input('저장할 이미지수를 입력하세요.')) # 충분히 다운 받음 120, 50: Train, 10: validation

base_url = "https://www.google.co.kr/search?biw=1597&bih=925&" \
             "tbm=isch&sa=1&btnG=%EA%B2%80%EC%83%89&q=" + inputSearch

# full_name = "C:/ai_201905/ws_python/notebook/machine/cnn_actor/src/"+inputSearch+"/"+inputSearch+"_"+str(count)+"_"+nowDatetime+".jpg"
full_name = "C:/ai_201905/ws_python/notebook/machine/cnn_actor/src/"+inputSearch
google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,
                 storage={'root_dir': full_name})

google_crawler.crawl(keyword=inputSearch,
                     max_num=count_max,
                     min_size=(200,200),
                     max_size=None)
```
  
### 2. 원본 이미지 저장 폴더(공백 상관 없음)

```bash
C:/ai4/ws_python/notebook/machine/cnn_actor/src
├─Amanda Seyfried
├─Andrew Lincoln
├─Anne Hathaway
├─Keira Christina Knightley
└─Pierce Brosnan
```

### 3. OpenCV haarcascades 설정

1) 다운로드

- 각종 인식 정보를 가지고 있는 스크립트
- <https://github.com/opencv/opencv>   opencv-master.zip 다운로드
- <https://github.com/opencv/opencv/tree/master/data/haarcascades>

2) 복사

```bash
C:/ai4/setup/opencv-master/data/haarcascades 폴더를 복사
C:/ai4/ws_python/notebook/machine/cnn_actor/haarcascades
```

### 4. 이미지 자르기

1) Crop 이미지 저장 폴더

```bash
C:/ai_201905/ws_python/notebook/machine/cnn_actor/src_crop
├─Amanda Seyfried
├─Andrew Lincoln
├─Anne Hathaway
├─Keira Christina Knightley
└─Pierce brosnan
```

### 5) script

▷ /ws_python/notebook/machine/cnn_actor/cropdata.ipynb

```python
# GPU는 메모리 해제가 안됨으로 CPU에서 실행
# 하나의 이미지의 얼굴을 검색하여 Crop
import cv2

face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

# img = cv2.imread('./kim.jpg')
img = cv2.imread('./lee.jpg')
# img = cv2.imread('./father.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3,5)
for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_casecade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh),(0,255,0),2)

cv2.imshow('Image view', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

```python
.....

# GPU는 메모리 해제가 안됨으로 CPU에서 실행
# 하나의 이미지의 얼굴을 검색하여 Crop
import cv2
import datetime

face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

# img = cv2.imread('./kim.jpg')
# img = cv2.imread('./lee.jpg')
img = cv2.imread('./father.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3,5)
count = 0
for (x,y,w,h) in faces:
    cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
    # 이미지를 저장

    count += 1
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d%H%M%S')

    cv2.imwrite(nowDatetime + "_" + str(count) + ".jpg", cropped)

cv2.imshow('Image view', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
.....
```

```python
# 특정 폴더의 파일을 처리
import os

path = "./src/Andrew Lincoln"
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.endswith(".jpg")]
for file in file_list_py:
    print ("file: {}".format(file))
.....
```

```python
# GPU는 메모리 해제가 안됨으로 CPU에서 실행
# 특정 폴더의 이미지의 얼굴을 검색하여 Crop
# 폴더명에 공백 가능
import os
import cv2
import datetime

face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

# Amanda Seyfried, Andrew Lincoln, Anne Hathaway,
# Keira Christina Knightley, Pierce_Brosnan
cropDir = input('배우 이름을 입력하세요: ')

path = "./src/" + cropDir
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.endswith(".jpg")]
count = 0

for file in file_list_py:
    print ("file: {}".format(file))
    img = cv2.imread("./src/" + cropDir + "/" + file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    for (x,y,w,h) in faces:
        cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
        # 이미지를 저장

        count += 1
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y%m%d%H%M%S')

        cv2.imwrite("./src_crop/" + cropDir + "/" + nowDatetime + "_" + str(count) + ".jpg", cropped)

    # cv2.imshow('Image view', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
```

### 3. 자신이 관심있는 영화배우 이미지를 선정하여 저장

- 아래와 같이 부모 폴더아래 그룹 폴더가 존재해야함.

```bash
/ws_python/notebook/machine/cnn_actor
├─train
│  ├─Amanda Seyfried   <-- 35개
│  ├─Andrew Lincoln
│  ├─Anne Hathaway
│  ├─Keira Christina Knightley
│  └─Pierce Brosnan
├─validation
│  ├─Amanda Seyfried   <-- 10개
│  ├─Andrew Lincoln
│  ├─Anne Hathaway
│  ├─Keira Christina Knightley
│  └─Pierce Brosnan
├─use1
│  └─64X64
├─use2
│  └─64X64
├─use3
│  └─64X64
├─use4
│  └─64X64
├─use5
│  └─64X64
└─use6
    └─64X64
```

## [참고] AlSee의 설치

- Altools Update 에서 설치
- [시작 메뉴 -> 알씨 실행 -> 파일 선택 -> 도구 메뉴 -> 일괄 편집
    -> '이미지 크기 변경, 이름 변경' 선택 -> 해상도로 조절하기(선택적임): 200 X 133(116)
    -> 이름 변경 규칙: [%N]_t
    -> 저장 포맷 - 변경할 파일 포맷: JPG
    -> 저장 경로: 원본 하위 폴더에 저장 선택, thumb
- 생성된 파일명: monggo01.jpg -> monggo01_t.jpg  
