# -*-encoding=utf-8 -*-
#/usr/bin/env python

import requests
import urllib

theurl = "http://www.iteye.com/login/"

header = {"User-Agent":"Mozilla/5.0 (indows NT 6.2; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43"}

datas = {"authenticity_token":"Y/cTDEBcgE+NzvQxYB38RMsg8Hl7590Eb0KoaX2WUx0=",
        "name":"lantian_123",
        "password":"****"
        }

datas = urllib.urlencode(datas)

r = requests.post(theurl,data=datas,headers=header)
print "login....."
print r.url
print r.status_code

cookie =r.cookies

datas = {
            "authenticity_token":"Y/cTDEBcgE+NzvQxYB38RMsg8Hl7590Eb0KoaX2WUx0=",
            "blog[blog_type]":"0",
            "blog[whole_category_id]":"4",
            "blog[title]":"helloworld",
            "blog[category_list]":"Java",
            "blog[body]":"hello,iteye,just a test",
            "blog[diggable]":"1",
        }
theurl = "http://liuzhijun.iteye.com/admin/blogs"

datas = urllib.urlencode(datas)
r2 = requests.post(theurl,data=datas,headers=header,cookies=cookie)
print "post...."
print r2.url
print r2.status_code
print r2.text

