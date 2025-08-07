# 예제

## [01] 다항식을 갖는 단순 선형회귀를 이용한 광고에 소요되는 비용으로 클릭수 예측하기

- 선형 대수: 전치 행렬 위키 검색
- 결과는 곡선이됨.

1. Data
    >> /ws_python/notebook/machine/basic/click.csv

    x: 비용, y: 클릭수

    ```csv
    x,y
    235,591
    216,539
    148,413
    35,310
    85,308
    204,519
    49,325
    25,332
    173,498
    191,498
    134,392
    99,334
    117,385
    112,387
    162,425
    272,659
    159,400
    159,427
    59,319
    198,522
    ```

2. Script

    >> /ws_python/notebook/machine/basic/Regression2.ipynb

```python
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()
# windows 10
# font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/malgunsl.ttf").get_name()
rc('font', family=font_name)           # 맑은 고딕 폰트 지정
plt.rcParams["font.size"] = 12         # 글자 크기
# plt.rcParams["figure.figsize"] = (10, 4) # 10:4의 그래프 비율
plt.rcParams['axes.unicode_minus'] = False  # minus 부호는 unicode 적용시 한글이 깨짐으로 설정

# Jupyter에게 matplotlib 그래프를 출력 영역에 표시할 것을 지시하는 명령
%matplotlib inline  
```

```python
print(train_z.size)
print(np.ones(train_z.size))
print(train_z)
print(train_z**2)
print(1.39433428 * 1.39433428)
```

```python
# 학습 데이터 행렬을 만든다. 전치행렬, 변수가 3개가 되도록 생성
# vstack: 열 방향 결합
# T: 배열의 열을 행으로 변환, 전치 행렬로 변환
def to_matrix(x):
    # return np.vstack([np.ones(x.size), x, x ** 2]) # 열방향으로 데이터가 발생함, 3행.
    return np.vstack([np.ones(x.size), x, x ** 2]).T # 행방향으로 데이터 나열
```

```python
.....
print('f(x)={0:.2f}x1 + {1:.2f}x2 + {2:.2f}x3'.format(cust[0], cust[1], cust[2]))
```

```python
.....
# 표준화된 데이터를 학습했음으로 표준화된 데이터를 사용해서 테스트 해야함.
for i in range(len(train_z)):
    predict = cust[0]*x[i][0] + cust[1] * x[i][1] + cust[2] * x[i][2]
    print('클릭수: {0}, 실제 비용:{1}, 예상 비용: {2:.1f}, 차이: {3:.1f}'.format(train_x[i], train_y[i], predict, (train_y[i]-predict)))
```
