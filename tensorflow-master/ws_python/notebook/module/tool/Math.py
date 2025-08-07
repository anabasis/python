#!/usr/bin/env python
# coding: utf-8

# In[3]:


def roundsu(su1):
    su1 = su1 + 0.5
    return str(int(su1))

def tot(*args): # 가변 인수, 전달받은 수의 합계
    tot = 0
    for su in args:
        tot = tot + su

    return tot

def maxsu(su1, su2):
    if su1 > su2:
        return su1
    else:
        return su2


def minsu(su1, su2):
    if su1 < su2:
        return su1
    else:
        return su2


def swap(su1, su2):
    temp = su1
    su1 = su2
    su2 = temp

    return su1, su2


if __name__ == '__main__':
    print(roundsu(10.4))
    print(roundsu(10.5))
    print(tot(10, 20, 30))


# In[ ]:




