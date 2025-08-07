# [01] 컨볼루션 신경망(CNN)을 이용한 도형의 인식, PILLOW 사용

1) pillow 설치
   - StopIteration: Could not import PIL.Image. The use of `array_to_img` requires PIL. 에러 처리

   ```bash
   (base) C:\Windows\system32>activate ai
   (ai) C:\Users\user>pip install pillow
   ERROR: (ai) C:\Users\user>conda install pillow

   (ai) C:\Users\user>deactivate

   (base) C:\Windows\system32>activate aigpu
   (aigpu) C:\Users\user>pip install pillow
   ERROR:(aigpu) C:\Users\user>conda install pillow
   ```

## 1. 문제 정의

- 문제 형태: 다중 클래스 분류
- 입력: 손으로 그린 삼각형, 사각형, 원 이미지
- 출력: 삼각형, 사각형, 원일 확률을 나타내는 벡터

## 2. 데이터 준비하기

- /machine/cnn_shape
- 훈련: 폴더명이 분류의 기준, 폴더의 갯수는 분류 갯수가됨.

    ```bash
    md circle
    md rectangle
    md triangle
    ```

    ```bash
    train
        ├─ circle   ◀─ 훈련데이터 폴더를 2단으로 구성, 폴더명이 분류 되는 class 값이 됨.
        ├─ rectangle
        └─ triangle
    - 검증
    validation
        ├─ circle   ◀─ 검증데이터 폴더를 2단으로 구성, 폴더명이 분류 되는 class 값이 됨.
        ├─ rectangle
        └─ triangle
    ```

- 최종 폴더의 형태는 부모 자식의 형태로 구성되어야함.

```bash
C:/AI4/WS_PYTHON/NOTEBOOK/MACHINE/CNN_SHAPE
├─.ipynb_checkpoints
├─validation
│  ├─circle
│  ├─rectangle
│  └─triangle
├─train
│  ├─circle
│  ├─rectangle
│  └─triangle
├─use1       ◀─ 모델 사용 폴더는 자식 폴더를 가지고 있어야함, 그렇지 않으면 인식이 안됨.
│  └─24X24   ◀─ 모델 사용시 이용할 이미지 폴더, 폴더명은 의미 없음.
├─use2
│  └─24X24
├─use3
│  └─24X24
├─use4
│  └─64X64
├─use5
│  └─128X128
└─use6
    └─256X256
```

## 3. 데이터셋 생성

- 케라스에서는 이미지 파일을 쉽게 학습시킬 수 있도록 ImageDataGenerator 클래스를 제공,
- ImageDataGenerator 클래스는 데이터 증강 (data augmentation)을 위해 막강한 기능을 제공
- ImageDataGenerator 클래스를 이용하여 객체를 생성한 뒤 flow_from_directory() 함수를 호출하여 제네레이터(generator)를 생성
- flow_from_directory() 함수의 주요인자
    첫번재 인자 : 이미지 경로 지정
    target_size : 패치 이미지 크기를 지정, 폴더에 있는 원본 이미지 크기가 다르더라도 target_size에 지정된 크기로 자동 조절됨
    batch_size : 배치 크기를 지정
    class_mode : 분류 방식에 대해서 지정
        . categorical : 2D one-hot 부호화된 라벨로 변환
        . binary : 1D 이진 라벨로 변환
        . sparse : 1D 정수 라벨로 변환  . None : 라벨이 변환되지 않음

```python
train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        'warehouse/handwriting_shape/train',
        target_size=(24, 24),
        batch_size=3,
        class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        'warehouse/handwriting_shape/test',
        target_size=(24, 24),
        batch_size=3,
        class_mode='categorical')
```  

## 4. 모델 구성

- 컨볼루션 레이어 : 입력 이미지 크기 24 x 24, 입력 이미지 채널 3개, 필터 크기 3 x 3, 필터 수 32개, 활성화 함수 ‘relu’
- 컨볼루션 레이어 : 필터 크기 3 x 3, 필터 수 64개, 활성화 함수 ‘relu’
- 맥스풀링 레이어 : 풀 크기 2 x 2
- 플래튼 레이어
- 댄스 레이어 : 출력 뉴런 수 128개, 활성화 함수 ‘relu’
- 댄스 레이어 : 출력 뉴런 수 3개, 활성화 함수 ‘softmax’

```python
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(24,24,3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))
```

1) 에러 메시지:  Input 0 is incompatible with layer conv2d_13: expected ndim=4, found ndim=2

    ```python
    model.add(Dense(128, activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    ```

    순서를 변경 할것

    ```python
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    ```

2) 에러 메시지: Negative dimension size caused by subtracting 3 from 1 for 'conv2d_36/ convolution' (op: 'Conv2D') with input shapes: [?,1,1,128], [3,3,128,64].

    ```python
    model.add(Conv2D(128, (3, 3), activation='relu'))  
    ```

    경계를 padding='same'으로 지정하여 축소되는 것을 방지할 것, 외곽에 하나의 행과 1개의 열을 추가하고 값을 0을 지정하여 차원 축소를 방지.

    ```python
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    ```

## 5. 모델 학습 과정 설정

- loss : 현재 가중치 세트를 평가하는 데 사용한 손실 함수, 다중 클래스 문제이므로 ‘categorical_crossentropy’로 지정
- optimizer : 최적의 가중치를 검색하는 데 사용되는 최적화 알고리즘으로 효율적인 경사 하강법 알고리즘 중 하나인 ‘adam’을 사용
- metrics : 평가 척도를 나타내며 분류 문제에서는 일반적으로 ‘accuracy’로 지정

```python
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  
```

## 6. 모델 학습

- 케라스에서는 모델을 학습시킬 때 주로 fit() 함수를 사용하지만 제네레이터로 생성된 배치로 학습시킬 경우에는 fit_generator() 함수를 사용함.
- 첫번째 인자: 훈련데이터셋을 제공할 제네레이터를 지정
- epochs: 전체 훈련 데이터셋에 대해 학습 반복 횟수를 지정
- validation_data: 검증 데이터셋을 제공할 제네레이터를 지정

```python
model.fit_generator(
        train_generator,
        epochs=50,
        validation_data=test_generator)
```

## 7. 모델 평가

- 제네레이터에서 제공되는 샘플로 평가할 때는 evaluate_generator 함수를 사용합니다.

```python
print("-- Evaluate --")
scores = model.evaluate_generator(test_generator)
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
```

## 8. 모델 사용

- 모델 사용 시에 제네레이터에서 제공되는 샘플을 입력할 때는 predict_generator 함수를 사용해야함
- 예측 결과는 클래스별 확률 벡터로 출력되며, 클래스에 해당하는 열을 알기 위해서는 제네레이터의 ‘class_indices’를 출력하면 해당 열의 클래스명을 알려줌

```python
print("-- Predict --")
output = model.predict_generator(test_generator)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(test_generator.class_indices)
print(output)
```

## 9. script

>> /ws_python/notebook/machine/cnn_shape/cnn_shape.ipynb

```python
# 훈련용 데이터 생성기, 이미지를 데이터로 바로 사용
# rescale=1./255: 정수를 실수로 변경하기위해 픽셀값을 255로 나눔
# 이미지를 수치로 바꾸는 vector 및 정수를 실수로 변경하는 정규화 자동 지원
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
        './train',
        target_size=(24, 24),     # 24 x 24로 자동으로 픽셀을 줄임.
        batch_size=1,             # 이미지를 1건씩 처리
        class_mode='categorical') # 다중 분류

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        './test',
        target_size=(24, 24),
        batch_size=1,
        class_mode='categorical')

.....
print("-- Predict --")
output = model.predict_generator(test_generator)
# 실수를 소수점 3자리까지 출력 설정
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(test_generator.class_indices)
print(output)
print(type(output))
print(output.shape)

for item in output:
    print('-----------------------')
    if (item[0] > 0.5):
        print('%6s %6s %6s' %('원','',''))     # 4
    elif (item[1] > 0.5):
        print('%6s %6s %6s' %('','사각형','')) # 5
    elif (item[2] > 0.5):
        print('%6s %6s %6s' %('','','삼각형')) # 3
    else:
        print('알수 없는 도형입니다.')
```

```python
.....
for item in output:
    print('-----------------------')
    idx = np.argmax(item) # 0 ~ 2

    if (idx == 0):
        print('%6s %6s %6s' %('원','',''))     # 4
    elif (idx == 1):
        print('%6s %6s %6s' %('','사각형','')) # 5
    elif (idx == 2):
        print('%6s %6s %6s' %('','','삼각형')) # 3

.....
def display1(data): # 2차원 배열(2차원 텐서)
    print(data)
    print(type(data))
    sw = 0
    if data[0][0] > 0.5:
        sw = '원'
    elif data[0][1] > 0.5:
        sw = '사각형'
    elif data[0][2] > 0.5:
        sw = '삼각형'
    else:
        sw = '알수없는 도형'

    return sw

def display2(data):   # argmax를 사용하는 2차원 배열(2차원 텐서)
    # print(data.shape)
    # print(data[0])
    # print(type(data[0]))
    sw= np.argmax(data[0], axis=0) # 0:열, 1: 행
    # print('sw:', sw)

    if sw == 0:
        sw = '원'
    elif sw == 1:
        sw = '사각형'
    elif sw == 2:
        sw = '삼각형'

    return sw

def display3(data):  # argmax를 사용하는 1차원 배열(1차원 텐서)
    # print(data.shape)
    # print(data)
    # print(type(data))
    sw= np.argmax(data, axis=0) # 0:열, 1: 행
    # print('sw:', sw)

    if sw == 0:
        sw = '원'
    elif sw == 1:
        sw = '사각형'
    elif sw == 2:
        sw = '삼각형'

    return sw
```

```python
.....
# 테스트
use_datagen = ImageDataGenerator(rescale=1./255)
use_generator = use_datagen.flow_from_directory('./use1', target_size=(24, 24),
        batch_size=1,
        class_mode='categorical')
output = model.predict_generator(use_generator)
print(output.shape)
print('원', display1(output))
print('원', display2(output))
```
