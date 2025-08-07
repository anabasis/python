# [01] CNN을 이용한 영상입력을 통한 수치 예측 모델의 개발

- 난수를 이용하여 숫자를 생성하였음으로 규칙이없어 검증정확도는 정확하지 않음.
- 데이터의 규모가 작아 CPU, GPU 성능 차이는 미미함.

## 1) 활용예

- CCTV 등 촬영 영상으로부터 미세먼지 지수 예측
- 위성영상으로부터 녹조, 적조 등의 지수 예측
  
>> /ws_python/notebook/machine/cnn_image/cnn_image1.ipynb

## 데이터 로드

```python
.....
np.random.randint(0, 16 * 16) # 0 ~ 256-1 사이의 난수 발생, 최대값은 발생안됨.
.....
print(np.zeros((16, 16)))  # 16행 16열 0으로 채워진 배열 생성
.....
np.random.random((10, 2)) # 10행 2열 난수 발생
.....
for i in range(25):  # 0 ~ 24
    print(i // 5, i % 5) # //: 정수 나누기, 행열의 구성시 주로 사용
.....
width = 16
height = 16

def generate_dataset(samples):  # 1500
    ds_x = [] # 이미지를 출력할 2차원 행렬 저장
    ds_y = [] # 0 ~ 255 구간의 정수

    for it in range(samples):  # 1500: 0 ~ 1499, 1500번 처리
        num_pt = np.random.randint(0, width * height)  # 256: 0 ~ 255
        img = generate_image(num_pt)  # 7 이라면

        ds_y.append(num_pt)  # 0 ~ 255 구간의 정수, 레이블, class
        ds_x.append(img)     # 이미지를 출력할 2차원 행렬 추가

    # ds_x를 배열로 변경, ds_y를 1500행 1열로 변환
    return np.array(ds_x), np.array(ds_y).reshape(samples, 1)

def generate_image(points): # 0 ~ 255, 7이라고 가정
    img = np.zeros((width, height))  # 16 x 16의 0으로 채워진 행렬
    pts = np.random.random((points, 2)) # 7이하면 7행 2열의 난수 발생

    # pts는 2차원 배열이나 for문 때문에 하나의 행씩 추출됨. [0.26333527, 0.20043297]
    for ipt in pts:
        # int(0.26333527 * 16), int(0.20043297 * 16)] = 1
        img[int(ipt[0] * width), int(ipt[1] * height)] = 1

    return img.reshape(width, height, 1) # 16 x 16의 1: 흑백 이미지 생성
```

## 훈련용, 이미지 출력용 행렬, 1500행 1열 정수 행렬

```python
.....
# 훈련용, 이미지 출력용 행렬, 1500행 1열 정수 행렬
x_train, y_train = generate_dataset(1500)
print(x_train.shape)
print(y_train.shape)
x_val, y_val = generate_dataset(300)      # 검증용
print(x_val.shape)
x_test, y_test = generate_dataset(100)    # 시험용
print(y_val.shape)

.....
plt_row = 5
plt_col = 5

plt.rcParams["figure.figsize"] = (10,10)  # plot 크기 지정

f, axarr = plt.subplots(plt_row, plt_col)  # 5 x 5 형태의 plot

for i in range(plt_row*plt_col):  # 0 ~ 24
    sub_plt = axarr[i // plt_row][i % plt_col]  # 행열 지정
    sub_plt.axis('off') # 축의 label을 출력하지 않음.
    sub_plt.imshow(x_train[i].reshape(width, height)) # 3차원을 2차원으로 변경
    sub_plt.set_title('R ' + str(y_train[i][0])) # 0 ~ 255 출력

plt.show()
```

## 다층퍼셉트론 신경망 모델

```python
.....
# 다층퍼셉트론 신경망 모델
x_train, y_train = generate_dataset(1500)
x_val, y_val = generate_dataset(300)
x_test, y_test = generate_dataset(100)
print(x_train.shape[0], x_val.shape[0],x_test.shape[0])

x_train_1d = x_train.reshape(x_train.shape[0], width*height)  # 1500, 256
x_val_1d = x_val.reshape(x_val.shape[0], width*height)        # 300, 256
x_test_1d = x_test.reshape(x_test.shape[0], width*height)     # 100, 256
.....
model = Sequential()
model.add(Dense(256, activation='relu', input_dim = 256)) # width * height
model.add(Dense(128, activation='relu'))
model.add(Dense(64))
model.add(Dense(1))  # 예측 실수 출력
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

start=time.time()
hist = model.fit(x_train_1d, y_train, batch_size=50, epochs=50,
                 validation_data=(x_val_1d, y_val))
print("training Runtime: %0.2f 초" % ((time.time() - start)))
# CPU
# training Runtime: 3.81 초

# GPU
# training Runtime: 9.24 초

.....
loss, accuracy = model.evaluate(x_val_1d, y_val, batch_size=32)
print('손실값: ' + str(loss), ' / 정확도: ' + str(accuracy * 100),'%')
.....
yhat_test = model.predict(x_test_1d, batch_size=32)
plt_row = 5
plt_col = 5

plt.rcParams["figure.figsize"] = (10,10)

f, axarr = plt.subplots(plt_row, plt_col)

for i in range(plt_row*plt_col):
    sub_plt = axarr[i//plt_row, i%plt_col]  # //: 정수형 나누기
    sub_plt.axis('off')
    sub_plt.imshow(x_test[i].reshape(width, height))
    sub_plt.set_title('R %d P %.1f' % (y_test[i][0], yhat_test[i][0]))  # R: 실제값, P: 예측한 값

plt.show()
.....
```

## 모델링

```python
model = Sequential()
# 3행 3열의 32개 커널 사용, 입력 형식 3차원 배열
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(width, height, 1)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2))) # 벡터(변수, 노드) 차원(갯수) 50% 감소
model.add(Conv2D(16, (3, 3), activation='relu'))
model.add(Flatten()) # 평탄화, 1차원 텐서(1차원 배열)로 변경
model.add(Dense(64, activation='relu'))
model.add(Dense(1))  # 수치예측임으로 계산 결과를 그대로 출력

model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
# x_train: (1500, 16, 16, 1), y_train: (1500, 1)

start=time.time()
hist = model.fit(x_train, y_train, batch_size=50, epochs=50,
                 validation_data=(x_val, y_val))
print("training Runtime: %0.2f 초" % ((time.time() - start)))
# CPU
# training Runtime: 32.86 초

# GPU
# training Runtime: 13.56 초
.....
loss, accuracy = model.evaluate(x_val, y_val, batch_size=32)
print('손실값: ' + str(loss), ' / 정확도: ' + str(accuracy * 100),'%')
.....
```
