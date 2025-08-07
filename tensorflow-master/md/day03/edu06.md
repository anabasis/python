# 선형회귀

## [01] 선형회귀

### 1) Support Vector Machine(SVM)

- 서포트 벡터 머신(support vector machine, SVM)은 기계 학습의 분야 중 하나로 패턴 인식, 자료 분석을 위한 지도 학습 모델이며, 주로 분류와 회귀 분석을 위해 사용한다.
- 두 카테고리 중 어느 하나에 속한 데이터의 집합이 주어졌을 때, SVM 알고리즘은 주어진 데이터 집합을 바탕으로 하여 새로운 데이터가 어느 카테고리에 속할지 판단하는 비확률적 이진 선형 분류 모델을 만든다.
- 만들어진 분류 모델은 데이터가 사상된 공간에서 경계로 표현되는데 SVM 알고리즘은 그 중 가장 큰 폭을 가진 경계를 찾는 알고리즘이다.
- SVM은 선형 분류와 더불어 비선형 분류에서도 사용될 수 있다.
- 비선형 분류를 하기 위해서 주어진 데이터를 고차원 특징 공간으로 사상하는 작업이 필요한데, 이를 효율적으로 하기 위해 커널 트릭을 사용하기도 한다.
- 분류에 사용되었지만 선형회귀도 적용 가능
- model = svm.SVR()
- 적은 데이터수로도 분류 가능, 속도가 느림, 기본적으로 이항 분류가 되며 여러 클래스의 분류는 SVM을 조합해야함.
- 분할 직선의 이미지
![분할직선](./images/21(3).jpg)
- 분할선으로부터 마진의 합(거리의 제곱)이 가장 많은 직선을 선택

1) Random Forest
   - 기계 학습에서의 랜덤 포레스트(영어: random forest)는 분류, 회귀 분석 등에 사용되는
     앙상블 학습 방법의 일종으로, 훈련 과정에서 구성한 다수의 결정 트리로부터 부류(분류) 또는
     평균 예측치(회귀 분석)를 출력함으로써 동작한다.
   - 분류에 사용되었지만 선형회귀도 적용 가능
   - model = ensemble.RandomForestRegressor()
   - 전체 학습 데이터 중에서 중복이나 누락을 허용해 학습 데이터셋을 여러 개 추출하며,
     그 일부속성을 이용해 약한 학습기를 생성
   - 처리 속도가 빠르고 학습 데이터의 노이즈에도 강함
   - 분류, 회귀, 클러스터링에 모두 사용 가능
   - 학습 데이터가 적으면 과적합이 발생함으로 권장하지 않음.
   - 사용: classifier = ensemble.RandomForestClassifier(n_estimators=20, max_depth=3, criterion="gini")

### 2. Script

>> /ws_python/notebook/machine/sklearn/Regression2.ipynb

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
