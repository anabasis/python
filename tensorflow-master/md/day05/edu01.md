# KERAS

## [01] Keras를 이용한 2개이상의 입력과 2개의 출력 node 사용

1. Keras 실습

>> /ws_python/notebook/machine/keras/Basic4.ipynb

```python
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

.....
# 데이터
x_train = np.array([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9],
                    [6, 10], [7, 11], [8, 12], [9, 13], [10, 14]])
# 1 * 2 = 2, 5 * 2 = 10
y_train = np.array([[2, 10], [4, 12], [6, 14], [8, 16], [10, 18],
                    [12, 20], [14, 22], [16, 24], [18, 26], [20, 28]])
print(x_train.shape)
print(y_train.shape)
```

```python
# 모델 사용
model = load_model('./Basic4.h5')

x_use = np.array([[11, 19], [12, 20], [13, 21], [14, 22], [15, 23]])
y_use = np.array([[22, 38], [24, 40], [26, 42], [28, 44], [30, 46]])

y_predict = model.predict(x_use) # 모델 사용

for i in range(len(x_use)):
    # print('실제값: {0}, 예측값: {1}'.format(y_use[i], y_predict[i]))
    print(y_predict[i]) # 1차원 배열
    print('실제값: {0}, 예측값: {1}'.format(y_use[i], y_predict[i]))
```

```python
plt.scatter(x_use, y_use, color='g')  # 실제값: 초록색
plt.plot(x_use, y_use, color='g')
plt.scatter(x_use, y_predict, color='r')  # 예측값: 빨간색
plt.plot(x_use, y_predict, color='r')
plt.grid(True)  # 그리드 출력
plt.show()
```

```python
plt.scatter(x_use, y_use, color='g')  # 실제값: 초록색
plt.plot(x_use, y_use, color='g')
plt.scatter(x_use, y_predict, color='r')  # 예측값: 빨간색
plt.plot(x_use, y_predict, color='r')
plt.ylim(0, 50)
plt.grid(True)  # 그리드 출력
plt.show()
```
