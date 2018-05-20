# -*- coding: UTF-8 -*-
import sys
from bs4 import BeautifulSoup
import io,os
import urllib.request
import http.cookiejar
from tkinter import *
import requests
root = Tk()
fm = []
root.title("课程表查询")
userid = StringVar()
userpassword = StringVar()
for color in [0,1,2,3,4,5,6,7,8,9]:
    #注意这个创建Frame的方法与其它创建控件的方法不同，第一个参数不是root
    fm.append(Frame(height = 600,width = 600))
width ,height= 600, 600#窗口大小

root.geometry('%dx%d+%d+%d' % (width,height,(root.winfo_screenwidth() - width ) / 2, (root.winfo_screenheight() - height) / 2))#窗口居中显示

root.maxsize(300,300)#窗口最大值

root.minsize(300,300)#窗口最小值
def tk_login():
        lableSign_inputName = Label(fm[1], text="学号：").place(x=50, y=20)
        entryInputName = Entry(fm[1], textvariable=userid)
        entryInputName.place(x=50, y=50)

        lableSign_inputPassword = Label(fm[1], text="密码：").place(x=50, y=100)
        entryInputPassword = Entry(fm[1], textvariable=userpassword)
        entryInputPassword.place(x=50, y=130)

        bottonSign = Button(fm[1], text="查询", command=cha).place(x=125, y=200)
        fm[1].pack()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
#user_id=165150221
#user_password=19980423
#登录时需要POST的数据
def cha():
        user_id = userid.get()
        user_password = userpassword.get()
        data = {'uid':user_id,
                'pwd':user_password,
                'goto:http':'//61.181.145.1:88/login.jsp',
                'gotoOnFail:http':'//61.181.145.1:88'}
        post_data = urllib.parse.urlencode(data).encode('utf-8')

        #设置请求头
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        #登录时表单提交到的地址（用开发者工具可以看到）
        login_url = ' http://61.181.145.1:88/check.jsp'

        #构造登录请求
        req = urllib.request.Request(login_url, data = post_data, headers = headers)

        #构造cookie
        cookie = http.cookiejar.CookieJar()

        #由cookie构造opener
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

        #发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
        resp = opener.open(req)

        #登录后才能访问的网页
        url = 'http://61.181.145.1:88/studentKBCX/index_KBCX.jsp'

        #构造访问请求
        req = urllib.request.Request(url, headers = headers)

        resp = opener.open(req)

        str1=resp.read().decode('gb2312')
        filename = str(user_id)



        web=open("./"+filename+"课表.html" ,"w+")

        web.write(str1)
        web.close()
        filepath=os.getcwd()
        print_file(str1)

def print_file(str1):
        user_id=userid.get()
        filename=str(user_id)
        #target = filepath+"\\"+filename+"课表.html"
        #req = requests.get(url = target)
        html = str1
        bf = BeautifulSoup(html,"lxml")
        texts = bf.find_all('table', width = '700')
        t123 = str(texts)
      #  print(t123)
        web=open("./"+filename+"_课表.html" ,"w+",encoding='utf-8')
        web.write(t123)
        web.close()
tk_login()

root.mainloop()