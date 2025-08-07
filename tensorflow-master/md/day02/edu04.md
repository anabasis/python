# Pandas

## [01] 대용량 데이터 연산 package(library) Pandas 실습

- <http://pandas.pydata.org>
- Series는 numpy의 1차원 배열과 비슷한 구조이나 index와 컬럼명을 지정 할 수 있어 사용이 편리하다.
- DataFrame은 numpy의 ndArray를 기반으로한 2차원 배열의 형태를 갖는 데이터 구조이다.
- 1 차원 배열형태는 Series의 개념을 사용
- 2 차원 배열형태는 DataFrame의 개념을 사용
- Excel과 비슷한 데이터 처리 지원

1) 파일이나 데이터베이스, 금융 관련 library 지원.
2) 시각화 관련 편리한 기능 제공.
3) describe(): 기술 통계
   변수단위 요약 정보 출력
   count: 데이터수, 과목별 성적의 수
   mean: 평균, 과목별 평균
   std: 표준 편차, 값이 크면 성적이 넓게 퍼짐
   min: 최소값, 가장 낮은 성적
   25%: 25/100 지점의 값
   50%: 50/100 지점의 값, 중앙값, median
   75%: 75/100 지점의 값
   max: 100/100 지점의 값, 최대값

1. 데이터 생성, 인덱스 생성, 데이터 선별
    >> /ws_python/notebook/package/pandas_test.ipynb

    ```python
    # randn: 표준 정규 분포 난수 발생, 평균:0, 표준 편차 1
    df = pd.DataFrame(np.random.randn(10, 5), columns=['kor', 'eng', 'mat', 'python', 'ai'])
    print(df)
    .....
    df4 = pd.DataFrame([[2, 4, 6, 20]], columns=['A', 'B', 'C', 'E'])
    print(df4)
    .....
    s3 = pd.DataFrame([[1,2],[3,4]], columns=['A', 'B'])
    print(s3)
    .....
    df.loc[0:0, 'A'] = 100 # index: 0, A 열
    print(df)
    df.loc[0:1, 'A'] = 100 # index: 0~1, A 열
    print(df)
    .....
    df.loc[0:0, 0:0] = 100 # 변경 안됨
    print(df)
    df.loc[0:0, 0:1] = 100
    print(df)
    .....
    dates = pd.date_range('20190101', periods=6)  # 6일간 날짜 생성
    print(dates)
    .....
    # 평균(기댓값)이 0이고 표준편차가 1인 가우시안 표준 정규 분포를 따르는 난수생성
    # index를 날짜로 지정
    df = pd.DataFrame(np.random.randn(6,4), index=dates,columns=['A','B','C','D'])
    df
    .....
    df2 = df.copy()
    df2['E'] = ['one', 'one','two','three','four','three'] # 새로운 컬럼의 추가
    df2
    .....
    df2['E'].isin(['two','four']) # E 변수에서 two, four 값을 찾아 True를 출력  
    .....
    df2[df2['E'].isin(['two','four'])] # true인 행 출력
    .....
    ```
