# Jupyter

<https://devtimes.com/bigdata/2019/02/14/jupyter/>
<https://dailyheumsi.tistory.com/37>

## Jupyter 템플릿 적용

<https://github.com/dunovank/jupyter-themes/blob/master/README.md>

```bash
pip install jupyter # 주피터 설치
pip install jupyterthemes # 주피터 테마 설치
```

### 테마 리스트 보기

>> jt -l (소문자 L)

입력하면 아래처럼 사용 가능한 테마 리스트가 나옵니다. 하나씩 적용해 보시고 맘에 드는걸로 쓰시면 됩니다.

   chesterish
   grade3
   gruvboxd
   gruvboxl
   monokai
   oceans16
   onedork
   solarizedd
   solarizedl

### 테마 적용

>> jt -t chesterish

-t 옵션을 주면 chesterish 라는 테마로 바뀝니다. 바로 안바뀔경우,브라우저를 새로고침 하거나, 처음 설치시에는 주피터 한번 종료 해주시면 됩니다.

재기동

### 적용테마 확인

>> vi ~/.jupyter/custom/custom.css
