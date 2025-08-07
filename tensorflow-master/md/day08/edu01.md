# 80 Million Tiny Images CIFAR-10을 이용한 이미지 인식 모델 개발

## [01] 80 Million Tiny Images CIFAR-10을 이용한 이미지 인식 모델 개발

- <https://www.cs.toronto.edu/~kriz/cifar.html>
- <https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz>
- 8000 만장의 32X32 pixel 이미지 제공 여기에서 60,000 장의 이미지를 선별하여 레이블을 붙인것이 'CIFAR-10'임
- 학습용 50,000장의 이미지
- 테스트용 10,000장으로 구성
- 이미지 크기는 32 X 32 pixel, RGB로 채널이 3개인 color 이미지

### 1. OpenCV 설치

- OpenCV(Open Source Computer Vision)은 주로 실시간 컴퓨터 비전을 목적으로 한 프로그래밍 라이브러리임
- 원래는 인텔이 개발함
- 실시간 이미지 프로세싱에 중점을 둔 라이브러리, 인텔 CPU에서 사용되는 경우 속도의 향상을 볼 수 있는
   IPP(Intel Performance Primitives)를 지원한다.
- 이 라이브러리는 윈도, 리눅스 등에서 사용 가능한 크로스 플랫폼이며 오픈소스 BSD 허가서 하에서
  무료로 사용할 수 있다.
- OpenCV는 TensorFlow , Torch / PyTorch 및 Caffe의 딥러닝 프레임워크를 지원한다.
- Python 3.6의 경우 OpenCV 3.2.0 설치(OpenCV 4.0 버전은 에러남)

```bash
(base) C:\Windows\system32>activate machine
(machine) C:\Windows\system32>pip install opencv-python==3.2.0.6
ERROR: (machine) C:\Windows\system32>conda install -c conda-forge opencv=3.2.0

(base) C:\Windows\system32>activate machinegpu
(machinegpu) C:\Windows\system32>pip install opencv-python==3.2.0.6
ERROR: (machinegpu) C:\Windows\system32>conda install -c conda-forge opencv=3.2.0
```

- pillow ERROR

```bash
  (machine) C:\Users\user>pip install pillow
  (machinegpu) C:\Users\user>pip install pillow
```

### 2. script

>> /ws_python/notebook/machine/cifar/cifar10_mlp.ipynb

#### IMPORT

```python
.....
from keras.datasets import cifar10
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

.....
import matplotlib.pyplot as plt
from PIL import Image

plt.figure(figsize=(10, 10))
labels = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
for i in range(0, 40):
    im = Image.fromarray(X_train[i])  # NumPy 배열을 Image 객체로 변환
    plt.subplot(5, 8, i + 1)
    plt.title(labels[y_train[i][0]])
    plt.tick_params(labelbottom="off",bottom="off") # x축 제거
    plt.tick_params(labelleft="off",left="off") # y축 제거
    plt.imshow(im)

plt.show()
```

```python
.....
num_classes = 10 # class 10 사용
im_rows = 32
im_cols = 32
im_size = im_rows * im_cols * 3  # 3072

# 데이터 읽어 들이기
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# 데이터를 1차원 배열로 변환하기
X_train = X_train.reshape(-1, im_size).astype('float32') / 255
X_test = X_test.reshape(-1, im_size).astype('float32') / 255

# 레이블 데이터를 One-hot 형식으로 변환하기
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print(y_train[0])
```

#### 모델 정의하기

```python
.....
# 모델 정의하기
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(im_size,)))
model.add(Dense(num_classes, activation='softmax'))
```

#### 모델 컴파일하기

```python
# 모델 컴파일하기
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])
```

#### 학습하기

```python
# 학습 실행하기, verbose=1 진행 사항 출력, 0은 출력 안함.
hist = model.fit(x_train, y_train,
    batch_size=32, epochs=10,
    verbose=1,
    validation_data=(x_test, y_test))
```

#### 이미지 읽어 들이기

```python
.....
import numpy as np
print(np.array([1, 0, 9, 3]).argmax()) # 결과 → 2
print(np.array([1, 3, 2, 9]).argmax()) # 결과 → 3
print(np.array([9, 0, 2, 3]).argmax()) # 결과 → 0

.....
# OpenCV를 사용해서 이미지 읽어 들이기
from keras.models import load_model
import cv2
import matplotlib.pyplot as plt
import numpy as np

model = load_model('./cifar10_mlp.h5')

labels = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
num_classes = 10 # class 10 사용
im_rows = 32
im_cols = 32
im_size = im_rows * im_cols * 3  

# local gpu
# im = cv2.imread('./k3.jpg')    # automobile

# gcp, 절대 경로 사용
# im = cv2.imread('./drive/My Drive/Colab Notebooks/k3.jpg')    # truck 으로 인식

# local gpu
# im = cv2.imread('./venue.jpg')   # Truck

# gcp, 절대 경로 사용
# im = cv2.imread('./drive/My Drive/Colab Notebooks/venue.jpg')     # automobile

# local gpu
# im = cv2.imread('./sonata.jpg')   # automobile

# gcp, 절대 경로 사용
# im = cv2.imread('./drive/My Drive/Colab Notebooks/sonata.jpg')     # automobile

im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) # BGR --> RGB로 변환
im = cv2.resize(im, (32, 32))
plt.imshow(im) # 이미지 출력하기
plt.show()
```

#### 예측하고 결과 출력하기

```python
# MLP로 학습한 이미지 데이터에 형태 맞추기
im = im.reshape(im_size).astype('float32') / 255
# 예측하기
r = model.predict(np.array([im]), batch_size=32, verbose=1)
res = r[0]
# 결과 출력하기
for i, acc in enumerate(res):
    print(labels[i], "=", int(acc * 100))
print("-------------")
print(res)
print("-------------")
print("예측한 결과=", labels[res.argmax()])
```

>> /ws_python/notebook/machine/cifar/cifar10_cnn.ipynb

```python
.....
from keras.datasets import cifar10
num_classes = 10
im_rows = 32
im_cols = 32

# 데이터 읽어 들이기
(X_train, Y_train), (X_test, Y_test) = cifar10.load_data()

# 데이터를 정규화하기
x_train = X_train[0:50000].astype('float32') / 255
x_test = X_test[0:10000].astype('float32') / 255
# 레이블 데이터를 One-hot 형식으로 변환하기
y_train = to_categorical(Y_train[0:50000], num_classes)
y_test = to_categorical(Y_test[0:10000], num_classes)

# 모델 정의하기
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), activation='relu'))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2))) # 50% 감소
model.add(Dropout(0.25))                        # 25% 감소

model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation = 'softmax'))

# 모델 컴파일하기
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 학습 실행하기
hist = model.fit(x_train, y_train, batch_size=50, epochs=10, verbose=1,
    validation_data=(x_test, y_test))

.....
# OpenCV를 사용해서 이미지 읽어 들이기
labels = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

# local gpu
# im = cv2.imread('./seltos.jpg')    # automobile

# gcp, 절대 경로 사용
# im = cv2.imread('./drive/My Drive/Colab Notebooks/seltos.jpg')    # truck 으로 인식

# local gpu
# im = cv2.imread('./venue.jpg')   # truck

# gcp, 절대 경로 사용
# im = cv2.imread('./drive/My Drive/Colab Notebooks/venue.jpg')     # automobile

# local gpu
im = cv2.imread('./sonata.jpg')   # automobile

# gcp, 절대 경로 사용
# im = cv2.imread('./drive/My Drive/Colab Notebooks/sonata.jpg')     # automobile

im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) # OpenCV BGR --> 일반적인 RGB로 변환
im = cv2.resize(im, (32, 32))
plt.imshow(im) # 이미지 출력하기
plt.show()

# 예측하기
r = model.predict(np.array([im]), batch_size=1, verbose=1)
res = r[0]
# 결과 출력하기, enumerate: index 지원
for i, acc in enumerate(res):
    print(labels[i], "=", int(acc * 100))

print("-------------")
print(res)
print(type(res))
print("-------------")
print("예측한 결과=", labels[res.argmax()])
```
