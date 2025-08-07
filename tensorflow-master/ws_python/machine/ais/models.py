from django.db import models

import numpy as np
import os
from keras.models import load_model

# Create your models here.
class Calc:
    def add(self, su1, su2):
        self.res = su1 + su2
        return self.res

class Country:
    def country(self, data):  # self: 함수와 객체 연결
        print('data:', data)
        # self.res = data
        # data 형식: "0,0,0,5,1,0,0"
        data = np.array(data.split(','), dtype=float)  # or int
        # print('변환된 data:', data)

        # 2차원 배열로 변환
        x_data = np.array([
            data,
        ])

        # 절대 경로 사용
        path = os.path.dirname(os.path.abspath(__file__)) # 스크립트파일의 절대경로

        # model 이 있는 경로: C:/ai_201909/ws_python/notebook/machine/country/country2.h5
        # model = load_model("C:/ai_201909/ws_python/ai/ais/AI_models/country2.h5")
        model = load_model(os.path.join(path, 'AI_models/country2.h5'))

        yp = model.predict(x_data[0:1])  # 1건의 데이터
        # y_predict = model.predict(x_data)  # 1건의 데이터

        for i in range(len(x_data)):
            # print('적응 확률:', yp[i][0] * 100, ' %')
            pct = yp[i][0]
            print('적응 확률: {0:.3f}%'.format(pct * 100))

            if pct >= 0.8:
                print('귀농가능합니다.')
                self.res = '귀농가능합니다.'
            elif pct >= 0.5:
                print('귀촌을 권장합니다.')
                self.res ='귀촌을 권장합니다.'
            else:
                print('귀농/귀촌을 권장하지 않습니다.')
                self.res ='귀농/귀촌을 권장하지 않습니다.'

        return pct * 100, self.res  # pct, res


