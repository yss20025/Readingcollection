'''
cron: 30 */15 8-22 * * *
new Env('f智慧阅读');
活动入口微信打开：http://mr1694387464645.vdpckoa.cn/oz/index.html?mid=3Q3R692PT
下载地址：https://www.123pan.com/s/xzeSVv-IHpfv.html
公告地址：http://175.24.153.42:8881/getmsg?type=zhyd

使用方法：
1.活动入口,微信打开：http://mr1694387464645.vdpckoa.cn/oz/index.html?mid=3Q3R692PT
2.打开活动链接，抓包接口http://u.cocozx.cn/api/oz/info接口的请求体中的un和token参数
3.青龙环境变量菜单，添加本脚本环境变量
名称 ：zhyd_config
单个账户参数： ['name|un|token|key|uids']
例如：['账户1|150xxxx1234|dxxxxx|xxxxx|UID_xxxx']
多个账户['name|un|token|key|uids','name|un|token|key|uids']
例如：['账户1|150xxxx1234|dxxxxx|xxxxx|UID_xxxx','账户2|151xxxx1234|dxxxxx|xxxxx|UID_xxxx']
参数说明与获取：
ck:打开活动链接，抓包接口http://u.cocozx.cn/api/oz/info接口的请求体中的un和token参数
key:每个账号的推送标准，每个账号全阅读只需要一个key,多个账号需要多个key,key永不过期。
为了防止恶意调用key接口，限制每个ip每天只能获取一个key。手机开飞行模式10s左右可以变更ip重新获取key
通过浏览器打开链接获取:http://175.24.153.42:8882/getkey
uids:wxpusher的参数，当一个微信关注了一个wxpusher的推送应用后，会在推送管理后台(https://wxpusher.zjiecode.com/admin/main)的'用户管理-->用户列表'中显示
用户在推送页面点击’我的-->我的UID‘也可以获取

4.青龙环境变量菜单，添加本脚wxpusher环境变量(不需要重复添加)
青名称 ：push_config
参数 ：{"printf":0,"threadingf":1,"appToken":"xxxx"}
例如：{"printf":0,"threadingf":1,"appToken":"AT_r1vNXQdfgxxxxxscPyoORYg"}
参数说明：
printf 0是不打印调试日志，1是打印调试日志
threadingf:并行运行账号参数 1并行执行，0顺序执行，并行执行优点，能够并行跑所以账号，加快完成时间，缺点日志打印混乱。
appToken 这个是填wxpusher的appToken

5.提现标准默认是3000，与需要修改，请在本脚本最下方，按照提示修改
'''

import requests
import time
import random
import re
import json
import os
import threading
import datetime
checkDict={
'Mzg2Mzk3Mjk5NQ==':['wz',''],
}
def getmsg():
    lvsion = 'v1.0f'
    r=''
    try:
        u='http://175.24.153.42:8881/getmsg'
        p={'type':'zhyd'}
        r=requests.get(u,params=p)
        rj=r.json()
        version=rj.get('version')
        gdict = rj.get('gdict')
        gmmsg = rj.get('gmmsg')
        print('系统公告:',gmmsg)
        print(f'最新版本{version}当前版本{lvsion}')
        print(f'系统的公众号字典{len(gdict)}个:{gdict}')
        print(f'本脚本公众号字典{len(checkDict.values())}个:{list(checkDict.keys())}')
        print('='*50)
    except Exception as e:
        print(r.text)
        print(e)
        print('公告服务器异常')
def push(title,link,text,type1,uids,key):
    str1='''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>TITLE</title>
<style type=text/css>
   body {
   	background-image: linear-gradient(120deg, #fdfbfb 0%, #a5d0e5 100%);
    background-size: 300%;
    animation: bgAnimation 6s linear infinite;
}
@keyframes bgAnimation {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
</style>
</head>
<body>
<p>TEXT</p><br>
<p><a href="http://175.24.153.42:8882/lookstatus?key=KEY&type=TYPE">查看状态</a></p><br>
<p><a href="http://175.24.153.42:8882/lookwxarticle?key=KEY&type=TYPE&wxurl=LINK">点击阅读检测文章</a></p><br>
</body>
</html>
    '''
    content=str1.replace('TITTLE',title).replace('LINK',link).replace('TEXT',text).replace('TYPE',type1).replace('KEY',key)
    datapust = {
      "appToken":appToken,
      "content":content,
      "summary":title,
      "contentType":2,
      "uids": [uids]
    }
    urlpust = 'http://wxpusher.zjiecode.com/api/send/message'
    try:
        p = requests.post(url=urlpust, json=datapust).text
        print(p)
        print('推送成功')
        return True
    except:
        print('推送失败！')
        return False

def getinfo(link):
    try:
        r=requests.get(link)
        #print(r.text)
        html = re.sub('\s', '', r.text)
        biz=re.findall('varbiz="(.*?)"\|\|', html)
        if biz!=[]:
            biz=biz[0]
        if biz=='' or biz==[]:
            if '__biz' in link:
                biz = re.findall('__biz=(.*?)&', link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname!=[]:
            nickname=nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name!=[]:
            user_name=user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title!=[]:
            msg_title=msg_title[0]
        text=f'公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}'
        print(text)
        return nickname,user_name,msg_title,text,biz
    except Exception as e:
        print(e)
        print('异常')
        return False
class WXYD:
    def __init__(self,cg,bz):
        print(cg,bz)
        self.name = cg[0]
        self.un = cg[1]
        self.token=cg[2]
        self.key = cg[3]
        self.uids = cg[4]
        self.bz=bz
        self.headers = {
            'Host': 'u.cocozx.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
        }
    def printjson(self, text):
        if printf == 0:
            return
        print(self.name, text)

    def setstatus(self):
        try:
            u = 'http://175.24.153.42:8882/setstatus'
            p = {'key': self.key, 'type': 'zhyd', 'val': '1'}
            r = requests.get(u, params=p,timeout=10)
            print(self.name, r.text)
        except Exception as e:
            print(self.name,'设置状态异常')
            print(self.name,e)

    def getstatus(self):
        try:
            u = 'http://175.24.153.42:8882/getstatus'
            p = {'key': self.key, 'type': 'zhyd'}
            r = requests.get(u, params=p,timeout=3)
            return r.text
        except Exception as e:
            print(self.name,'查询状态异常',e)
            return False

    def info(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/info'
        p = {"code": "3Q3R692PT", "un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        self.printjson(r.text)
        rj = r.json()
        if rj.get('code') == 0:
            resul = rj.get('result')
            self.moneyCurrent = int(resul.get('moneyCurrent'))
            dayCount = resul.get('dayCount')
            agreementStatus = resul.get('agreementStatus')
            if agreementStatus != 1:
                print(self.name,'你还没有同意阅读协议，必须先手动阅读一下')
                return False
            hopeNull = resul.get('hopeNull')
            if hopeNull:
                if hopeNull.get('status') == 60:
                    print(self.name,'今日文章全部读完,请明天再来')
                if hopeNull.get('status') == 70:
                    tss = hopeNull.get('ts')
                    val = hopeNull.get('val')
                    stime = datetime.datetime.strptime(tss, "%Y-%m-%d %H:%M:%S").timestamp()
                    mm = val - int((int(time.time()) - int(stime)) / 60)
                    print(self.name,'下一批文章' + str(mm) + '分钟后到来')
                if hopeNull.get('status') == 50 or hopeNull.get('status') == 80:
                    print(self.name,'您的阅读暂时失效，请明天再来')
                print(self.name,f'当前账号今日已经阅读{dayCount}篇文章，剩余智慧{self.moneyCurrent}')
                return False
            print(self.name,f'当前账号今日已经阅读{dayCount}篇文章，剩余智慧{self.moneyCurrent}')
            self.statAccess()
            print(self.name,'-' * 50)
            return True
        else:
            print(self.name,'可能是账号异常，ck无效，没填ck')
            print(self.name,'-' * 50)
            return False

    def statAccess(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/statAccess'
        p = {"code": "3Q3R692PT", "un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        self.printjson(r.text)

    def agreement(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/agreement'
        p = {"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        self.printjson(r.text)
    def getReadHost(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/getReadHost'
        p = {"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        self.printjson(r.text)
        rj = r.json()
        if rj.get('code') == 0:
            host = rj.get('result').get('host')
            hostid = re.findall('mr(.*?)\.', host)[0]
            print(self.name,hostid)
            return hostid
        else:
            print(self.name,'get read host err')
            return False

    def read(self):
        while True:
            print(self.name,'-'*50)
            u = f'http://u.cocozx.cn/api/{self.bz}/read'
            p = {"un": self.un, "token": self.token, "pageSize": 20}
            r = requests.post(u, headers=self.headers, json=p)
            self.printjson(r.text)
            rj = r.json()
            if rj.get('code') == 0:
                status = rj.get('result').get('status')
                if status == 10:
                    url=rj.get('result').get('url')
                    a=getinfo(url)
                    if self.testCheck(a,url)==False:
                        return False
                    print(self.name,'获取文章成功，准备阅读')
                    ts = random.randint(7, 10)
                    print(self.name,f'本次模拟读{ts}秒')
                    time.sleep(ts)
                    sub = self.submit()
                    if sub == True: return True
                    if sub == False: return False
                elif status==30:
                    print(self.name,'未知情况')
                    time.sleep(2)
                    continue
                elif status==50 or status==80:
                    print(self.name,'您的阅读暂时失效，请明天再来')
                    return False
                else:
                    print(self.name,'本次推荐文章已全部读完')
                    return True
            else:
                print(self.name,'read err')
                return False
    def testCheck(self,a,url):
        if checkDict.get(a[4]) != None:
            self.setstatus()
            for i in range(60):
                if i % 30 == 0:
                    push('智慧阅读过检测', url, a[3], 'zhyd',self.uids,self.key)
                getstatusinfo = self.getstatus()
                if getstatusinfo == '0':
                    print(self.name,'过检测文章已经阅读')
                    return True
                elif getstatusinfo == '1':
                    print(self.name,f'正在等待过检测文章阅读结果{i}秒。。。')
                    time.sleep(1)
                else:
                    print(self.name,'服务器异常')
                    return False
            print(self.name,'过检测超时中止脚本防止黑号')
            return False
        else:return True
    def submit(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/submit'
        p = {"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name,r.text)
        rj = r.json()
        if rj.get('code') == 0:
            result = rj.get('result')
            print(self.name,f'获得{result.get("val")}智慧')
            progress = result.get('progress')
            if progress > 0:
                print(self.name,f'本轮剩余{progress}篇文章，继续阅读阅读')
            else:
                print(self.name,'阅读已完成')
                print(self.name,'-' * 50)
                return True
        else:
            print(self.name,'异常')
            return False

    def wdmoney(self):
        if self.moneyCurrent < 10000:
            print(self.name,'你的智慧剩余不多了，不能提现')
            return False
        elif 3000 <= self.moneyCurrent < 10000:
            txm = 3000
        elif 10000 <= self.moneyCurrent < 50000:
            txm = 10000
        elif 50000 <= self.moneyCurrent < 100000:
            txm = 50000
        else:
            txm = 100000
        u=f'http://u.cocozx.cn/api/{self.bz}/wdmoney'
        if self.bz == 'user':
            u=f'http://u.cocozx.cn/api/{self.bz}/wd'
        p = {"val":txm,"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name,'提现结果',r.text)
    def run(self):
        if self.info():
            time.sleep(1)
            self.read()
        time.sleep(2)
        self.info()
        time.sleep(2)
        self.wdmoney()

if __name__ == '__main__':
    pushconfig = os.getenv('push_config')
    if pushconfig == None:
        print('请检查你的推送变量名称是否填写正确')
        exit(0)
    try:
        pushconfig = json.loads(pushconfig.replace("'", '"'))
    except Exception as e:
        print(e)
        print(pushconfig)
        print('请检查你的推送变量参数是否填写正确')
        exit(0)
    zhconfig = os.getenv('zhyd_config')
    if zhconfig == None:
        print('请检查你的智慧阅读脚本变量名称是否填写正确')
        exit(0)
    try:
        zhconfig = json.loads(zhconfig.replace("'", '"'))
    except Exception as e:
        print(e)
        print(zhconfig)
        print('请检查你的智慧阅读变量参数是否填写正确')
        exit(0)
    printf = pushconfig['printf']
    appToken = pushconfig['appToken']
    threadingf = pushconfig['threadingf']
    getmsg()
    txbz = 3000  # 这里是提现标志3000代表3毛
    tl = []
    if threadingf == 1:
        for i in zhconfig:
            cg = i.split('|')
            print('*' * 50)
            print(f'开始执行{i[0]}')
            api = WXYD(cg,'oz')
            t = threading.Thread(target=api.run, args=())
            tl.append(t)
            t.start()
            time.sleep(0.5)
        for t in tl:
            t.join()
    elif threadingf == 0:
        for i in zhconfig:
            cg = i.split('|')
            print('*' * 50)
            print(f'开始执行{cg[0]}')
            api = WXYD(cg,'oz')
            api.run()
            print(f'{cg[0]}执行完毕')
            time.sleep(3)
    else:
        print('请确定推送变量中threadingf参数是否正确')
    print('全部账号执行完成')
