#!/usr/bin/env python
#! -*- encoding:utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup

url = 'http://news.dbanotes.net'
r = requests.get(url)
soup = BeautifulSoup(r.text)

tag_url = soup.find_all('a',text="Login/Register")[0]

login_url = url + tag_url['href']

r = requests.get(login_url)

soup = BeautifulSoup(r.text)

fnid = soup.find_all(attrs={'type':'hidden'})[0]['value']

param = {'fnid':fnid,'u':'qwerty','p':'qwerty'}

r = requests.post('http://news.dbanotes.net/y',data = param)

soup = BeautifulSoup(r.text)


centers = soup.find_all('center')[1:]

for center in centers:
    print center
    try:
        url1 = url + "/" + center.a['href']
        cookies = {'user':'igbj8JwX'}
        r = requests.get(url1,cookies = cookies)
        print r.text
        #time.sleep(1)
        #break
    except :
        pass

