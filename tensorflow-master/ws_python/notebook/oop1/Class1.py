#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Class1:
    year = 0
    product = ''
    price = 0
    dc = 0;
    service = False


# In[2]:


if __name__ == '__main__':    
    Class1.year = 2017  # static 적인 방법, 클래스명으로 접근
    Class1.product = 'SSD512'
    Class1.price = 200000
    Class1.dc = 3.5
    Class1.service = False
 
    print(Class1.year)
    print(Class1.product)
    print(Class1.price)
    print(Class1.dc)
    print(Class1.service)  


# In[3]:


product1 = Class1() # 객체 생성, 새로운 메모리 할당, new 없음
print(product1.year) # year 변수 공유

product2 = Class1()
print(product2.year) # year 변수 공유


# In[4]:


class Product:
    def setData(self):    # self: 함수와 객체 연결, self == this, self 생략시 에러
        print(type(self))
 
    def setData2(self, year, product):
        self.year = year  # instance 변수, field, property, attribute, 멤버 변수, 속성...
        self.product = product
        self.price = 0
        self.dc = 0
    def printData(self):
        print('----------------------')
        print("생산 년도:", self.year)
        print("제품명:", self.product)
        print("가격:", self.price)
        print("할인 가격:", self.dc)


# In[5]:


product1 = Product()  # 객체명 = 클래스명
product2 = Product()  # 객체명 = 클래스명
    
product1.setData()      #<class '__main__.Product'>  


# In[6]:


product1.setData2(2019, 'GTX 1060')
product2.setData2(2020, 'RTX 2080')

print(product1.year, product1.product)
print(product2.year, product2.product)

product1.printData() # self: product1 
product2.printData() # self: product2 


# In[7]:


class GDP:
    def getNation(self, code):
        str1 = "미결정"  # self가 선언되지 않았음으로 지역 변수, 함수안에서만 사용 가능한 변수
        if code == "KOR":
            str1 = "한국"
        elif code == "JAP":
            str1 = "일본"
        elif code == "CHA":
            str1 = "중국"

        return str1

    def getGDP(self, code):
        gdp = 1000  # self가 선언되지 않았음으로 지역 변수
        if code == "KOR":
            gdp = 28738
        elif code == "JAP":
            gdp = 37539
        elif code == "CHA":
            gdp = 6747

        return gdp


# In[8]:


# 한국
# 28738
gdp = GDP()  # gdp 객체 생성
print(gdp.getNation("KOR"))
print(gdp.getGDP("KOR"))


# In[9]:


gdp.wc = '러시아 월드컵' # 객체 생성후 field 추가 가능
gdp.city='모스크바'
print(gdp.wc)
print(gdp.city)


# In[10]:


class Nation:
    def __init__(self, code='KOR'):  # 생성자
        self.count = 0
        self.code = code
        print('객체가 메모리에 생성되었습니다.')

    def __del__(self):  # 소멸자
        print('객체가 메모리에서 소멸되었습니다.')

    def getNation(self, code):
        self.count = self.count + 1
        str1 = ""  # 지역 변수
        if code == "KOR":
            str1 = "한국"
        elif code == "JAP":
            str1 = "일본"
        elif code == "CHA":
            str1 = "중국"

        return str1


# In[11]:


nation = Nation()
print('count:', nation.count)
print('code:', nation.code)
print('nation:', nation.getNation('KOR'))
del nation # 변수 메모리 해제


# In[ ]:




