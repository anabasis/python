# This Python file uses the following encoding: utf-8

import requests
import re
from bs4 import BeautifulSoup

'''
Created on 2017. 2. 16.

@author: anabasis
'''

def spider():
    print("START!!!")

    url = 'https://docs.splunk.com/Documentation/Splunk/6.5.2/Admin/Serverconf'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")   ## lxml파서, html.parser파서 비교
    #print(soup.text)
    #print(soup.contents)
    #soup.find_all("","")
    fTag = soup.find_all("span", class_="mw-headline")
    
    for ftag in fTag :
        print(ftag)
        preTag = ftag.find_parent(re.compile("^h"))
        nextTag = preTag.find_next_sibling()
        print(preTag)
        print(nextTag)
        
    print("END!!!")

spider()