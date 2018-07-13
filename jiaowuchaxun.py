# -*- coding: UTF-8 -*-
from tkinter.messagebox import *
import webbrowser
from bs4 import BeautifulSoup
import io,os,time
import urllib.request
import http.cookiejar
from tkinter import *

root = Tk()
fm = []
root.title("课程表查询")
userid = StringVar()
userpassword = StringVar()
width ,height= 310, 300#窗口大小

for color in [0,1,2,3,4,5,6,7,8,9]:
    #注意这个创建Frame的方法与其它创建控件的方法不同，第一个参数不是root
    fm.append(Frame(height =height,width = width))

root.geometry('%dx%d+%d+%d' % (width,height,(root.winfo_screenwidth() - width ) / 2, (root.winfo_screenheight() - height) / 2))#窗口居中显示

root.maxsize(width,height)#窗口最大值

root.minsize(width,height)#窗口最小值

def tk_login():
        lableSign_inputName = Label(fm[1], text="学号：").place(x=50, y=20)
        entryInputName = Entry(fm[1], textvariable=userid)
        entryInputName.place(x=50, y=50)

        lableSign_inputPassword = Label(fm[1], text="密码：").place(x=50, y=100)

        ycPassword = Entry(fm[1], textvariable=userpassword,show= "*")
        #xsPassword.place(x=50,y=130)
        ycPassword.place(x=50,y=130)

        bottonchabj = Button(fm[1], text="查询班级课表", command=cha_BJ).place(x=40, y=200)
        bottonchagr = Button(fm[1], text="查询个人课表", command=cha_GR).place(x=150, y=200)
        bottondelete=Button(fm[1],text = "网络测试",command = inter_test).place(x= 240,y = 10)
        bottonexit = Button(fm[1], text="退出", command=exit_exe).place(x=260, y=260)
        fm[1].pack()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#登录时需要POST的数据
def exit_exe():
        sys.exit()
def inter_test():
        showinfo(title="233", message="先等几秒，可能有点慢")
        url = urllib.request.Request('http://61.181.145.1:88')
        try:
                resp = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
                showerror(title="咕咕咕", message="盯~~~你没连上学校的网")
        else:
                time.sleep(1)
                showinfo(title="喵喵喵", message="没毛病")

def cha_BJ():
        user_id = userid.get()
        user_password = userpassword.get()
        data = {'uid': user_id,
                'pwd': user_password,
                'goto:http': '//61.181.145.1:88/login.jsp',
                'gotoOnFail:http': '//61.181.145.1:88'
                 }
        post_data = urllib.parse.urlencode(data).encode('utf-8')

        # 设置请求头
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        # 登录时表单提交到的地址（用开发者工具可以看到）
        login_url = 'http://61.181.145.1:88/check.jsp'

        # 构造登录请求
        req = urllib.request.Request(login_url, data=post_data, headers=headers)

        # 构造cookie
        cookie = http.cookiejar.CookieJar()

        # 由cookie构造opener
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

        # 发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
        resp = opener.open(req)
        #登录后才能访问的网页
        url = 'http://61.181.145.1:88/studentKBCX/index_KBCX.jsp'
        #构造访问请求
        req = urllib.request.Request(url, headers = headers)

        resp = opener.open(req)
        str1=resp.read().decode('gb2312')
        filename = str(user_id)

        web=open("./"+filename+"班级课表.html" ,"w+")
        filename_all=filename+"班级课表.html"
        web.write(str1)
        web.close()
        print_file(str1,filename_all)


def cha_GR():
        user_id = userid.get()
        user_password = userpassword.get()
        data = {'uid': user_id,
                'pwd': user_password,
                'goto:http': '//61.181.145.1:88/login.jsp',
                'gotoOnFail:http': '//61.181.145.1:88'}
        post_data = urllib.parse.urlencode(data).encode('utf-8')

        # 设置请求头
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        # 登录时表单提交到的地址（用开发者工具可以看到）
        login_url = 'http://61.181.145.1:88/check.jsp'

        # 构造登录请求
        req = urllib.request.Request(login_url, data=post_data, headers=headers)

        # 构造cookie
        cookie = http.cookiejar.CookieJar()

        # 由cookie构造opener
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

        # 发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
        resp = opener.open(req)
        # 登录后才能访问的网页
        url = 'http://61.181.145.1:88/studentKBCX/grkb.jsp'

        # 构造访问请求
        req = urllib.request.Request(url, headers=headers)
        try:
                resp = opener.open(req)
        except:
                pass
        try:
                str1 = resp.read().decode('gb2312')
        except:
                str1=""
        filename = str(user_id)

        web = open("./" + filename + "个人课表.html", "w+")
        filename_all=filename + "个人课表.html"
        web.write(str1)
        web.close()
        print_file(str1,filename_all)


# def cha_delete():
#         path = "./"
#         mode = ".html"
#         if os.path.isfile(path):
#                 if path.endswith(mode):
#                         os.remove(path)

def print_file(str1,filename_all):
        user_id=userid.get()
        filename=str(user_id)
        #target = filepath+"\\"+filename+"课表.html"
        #req = requests.get(url = target)
        html = str1
        bf = BeautifulSoup(html,"lxml")
        texts = bf.find_all('table', width = '700')
        t123 = str(texts)

      #  print(t123)
        if(t123=='[]'):
                showerror(title="错误", message="用户名或密码错误")
                os.remove("./"+filename_all)
        else:
                '''web=open("./"+filename+"_课表.html" ,"w+",encoding='utf-8')
                web.write(t123)
                web.close()'''
                webbrowser.open(filename_all)
tk_login()

root.mainloop()
