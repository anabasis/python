#

[01] 선형회귀, 경사 하강법(gradient decent)을 이용한 사칙 연산 결과의 예측

1. 데이터
[
  [1, 12],
  [2, 14],
  [5, 20],
  [13, 36],
  [17, 44],
  [30, ???]
]
23일때의 값은?

>> /ws_python/notebook/machine/tsbasic/RegressionExam1.py

```python
import warnings
warnings.filterwarnings(action='ignore')

import tensorflow as tf

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
data = [
  [1, 12],
  [2, 14],
  [5, 20],
  [13, 36],
  [17, 44],
  [19, 48],  
  [30, 70],
  [37, 84],
  [43, 96],
  [50, 110]  
]

x = [row[0] for row in data]
print(x)

yr = [row[1] for row in data]
print(yr)
```

```python
# 테스트, 검증
test_data=[37, 43, 50]
test_data_y=[84, 96, 110]
for i in range(len(test_data)):
    y = v_a * test_data[i] + v_b  # y = ax + b, y = 2.3x + 79 가정
    print('데이터: %d 실제: %d 예측 %d' % (test_data[i], test_data_y[i], y))
```
  
## [02] 함수 기반 구현

### 1. 데이터

```json
  [1, 12],
  [2, 14],
  [5, 20],
  [13, 36],
  [17, 44],
  [19, 48],  
  [30, 70],
  [37, 84],
  [43, 96],
  [50, 110]  
```

23일때의 값은?

### 2. script

>> /ws_python/notebook/machine/tsbasic/RegressionExam2.py

첨부 파일 참고
