
# coding: utf-8

# [실습 1] 하나의 수를 정의하고 2, 3, 4의 배수인지
#           판단하는 프로그램을 제작하세요. 
# C:\ai4\ws_python\notebook\basic>python IfExam1.py 100
# 
# 파일명: IfExam1.py
# 
# 입력수: 100

# In[ ]:


# console에서의 입력
import sys
filename = sys.argv[0]
su = int(sys.argv[1])
str1 = ''

print('파일명:', filename)
print('입력수:', su)

if (su % 2 == 0 and su % 3 == 0 and su % 4 == 0):
    str1 = '2,3,4의 배수입니다.'
else:
    str1 = '2,3,4의 배수가 아닙니다.'

print(str1)    

