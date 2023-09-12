import requests
import time
import random
import re
import threading
import getWxInfo
import JhWxPusher
import config
import datetime

checkDict = {
    'Mzg2Mzk3Mjk5NQ==': ['wz', ''],
}


def getmsg():
    lvsion = 'v1.2_a'
    r = ''
    try:
        u = 'http://175.24.153.42:8881/getmsg'
        p = {'type': 'yuanbao'}
        r = requests.get(u, params=p)
        rj = r.json()
        version = rj.get('version')
        gdict = rj.get('gdict')
        gmmsg = rj.get('gmmsg')
        print('系统公告:', gmmsg)
        print(f'最新版本{version}当前版本{lvsion}')
        print(f'系统的公众号字典{len(gdict)}个:{gdict}')
        print(f'本脚本公众号字典{len(checkDict.values())}个:{list(checkDict.keys())}')
        print('=' * 50)
    except Exception as e:
        print(r.text)
        print(e)
        print('公告服务器异常')


class WXYD:
    def __init__(self, cg, bz):
        self.bz = bz
        self.cg = cg
        self.key = cg.get('key')
        self.un = cg.get('un')
        self.token = cg.get('token')
        self.name = cg.get('name')
        self.headers = {
            'Host': 'u.cocozx.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
        }

    def setstatus(self):
        try:
            u = 'http://175.24.153.42:8882/setstatus'
            p = {'key': self.key, 'type': 'yuanbao', 'val': '1'}
            r = requests.get(u, params=p,timeout=10)
            print(self.name, r.text)
        except Exception as e:
            print('设置状态异常')
            print(e)

    def getstatus(self):
        try:
            u = 'http://175.24.153.42:8882/getstatus'
            p = {'key': self.key, 'type': 'yuanbao'}
            r = requests.get(u, params=p,timeout=3)
            return r.text
        except Exception as e:
            print('查询状态异常',e)
            return False
    def printjson(self, text):
        if printf == 0:
            return
        print(self.name, text)

    def info(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/info'
        p = {"code": "RG5RC7LDU", "un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name, r.text)
        rj = r.json()
        if rj.get('code') == 0:
            resul = rj.get('result')
            self.moneyCurrent = int(resul.get('moneyCurrent'))
            dayCount = resul.get('dayCount')
            agreementStatus = resul.get('agreementStatus')
            if agreementStatus != 1:
                print(self.name, '你还没有同意阅读协议，必须先手动阅读一下')
                return False
            hopeNull = resul.get('hopeNull')
            if hopeNull:
                if hopeNull.get('status') == 60:
                    print(self.name, '今日文章全部读完,请明天再来')
                if hopeNull.get('status') == 70:
                    tss = hopeNull.get('ts')
                    val = hopeNull.get('val')
                    stime = datetime.datetime.strptime(tss, "%Y-%m-%d %H:%M:%S").timestamp()
                    mm = val - int((int(time.time()) - int(stime)) / 60)
                    print(self.name, '下一批文章' + str(mm) + '分钟后到来')
                if hopeNull.get('status') == 50 or hopeNull.get('status') == 80:
                    print(self.name, '您的阅读暂时失效，请明天再来')
                print(self.name, f'当前账号今日已经阅读{dayCount}篇文章，剩余金币{self.moneyCurrent}')
                return False
            print(self.name, f'当前账号今日已经阅读{dayCount}篇文章，剩余金币{self.moneyCurrent}')
            self.statAccess()
            print(self.name, '-' * 50)
            return True
        else:
            print(self.name, '可能是账号异常，ck无效，没填ck')
            print(self.name, '-' * 50)
            return False

    def statAccess(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/statAccess'
        p = {"code": "RG5RC7LDU", "un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name, r.text)

    def agreement(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/agreement'
        p = {"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name, r.text)

    def psmoneyc(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/psmoneyc'
        p = {"mid": "QS5PQAEZH", "un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        self.printjson(r.text)

    def getReadHost(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/getReadHost'
        p = {"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name, r.text)
        rj = r.json()
        if rj.get('code') == 0:
            host = rj.get('result').get('host')
            hostid = re.findall('mr(.*?)\.', host)[0]
            print(self.name, hostid)
            return hostid
        else:
            print(self.name, 'get read host err')
            return False

    def read(self):
        while True:
            print(self.name, '-' * 50)
            u = f'http://u.cocozx.cn/api/{self.bz}/read'
            p = {"un": self.un, "token": self.token, "pageSize": 20}
            r = requests.post(u, headers=self.headers, json=p)
            print(self.name, r.text)
            rj = r.json()
            if rj.get('code') == 0:
                status = rj.get('result').get('status')
                if status == 10:
                    url = rj.get('result').get('url')
                    a = getWxInfo.getinfo(url)
                    if self.testCheck(a, url) == False:
                        return False
                    print(self.name, '获取文章成功，准备阅读')
                    ts = random.randint(7, 10)
                    print(self.name, f'本次模拟读{ts}秒')
                    time.sleep(ts)
                    sub = self.submit()
                    if sub == True: return True
                    if sub == False: return False
                elif status == 30:
                    print(self.name, '未知情况')
                    time.sleep(2)
                    continue
                elif status == 50 or status == 80:
                    print(self.name, '您的阅读暂时失效，请明天再来')
                    return False
                else:
                    print(self.name, '本次推荐文章已全部读完')
                    return True
            else:
                print(self.name, 'read err')
                return False

    def testCheck(self, a, url):
        if checkDict.get(a[4]) != None:
            self.setstatus()
            for i in range(60):
                if i % 30 == 0:
                    JhWxPusher.push(self.cg['name'], url, a[3], 'yuanbao', self.cg['uids'],self.key)
                getstatusinfo = self.getstatus()
                if getstatusinfo == '0':
                    print(self.name, '过检测文章已经阅读')
                    return True
                elif getstatusinfo == '1':
                    print(self.name, f'正在等待过检测文章阅读结果{i}秒。。。')
                    time.sleep(1)
                else:
                    print(self.name, f'回调服务器请求超时，等待中{i}秒。。。')
                    time.sleep(1)
            print(self.name, '过检测超时中止脚本防止黑号')
            return False
        else:
            return True

    def submit(self):
        u = f'http://u.cocozx.cn/api/{self.bz}/submit'
        p = {"un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name, r.text)
        rj = r.json()
        if rj.get('code') == 0:
            result = rj.get('result')
            print(self.name, f'获得{result.get("val")}元宝')
            progress = result.get('progress')
            if progress > 0:
                print(self.name, f'本轮剩余{progress - 1}篇文章，继续阅读阅读')
            else:
                print(self.name, '阅读已完成')
                print(self.name, '-' * 50)
                return True
        else:
            print(self.name, '异常')
            return False

    def wdmoney(self):
        if self.moneyCurrent < config.ybtxbz:
            print(self.name, '没有达到提现标准')
            return False
        elif 3000 <= self.moneyCurrent < 10000:
            txm = 3000
        elif 10000 <= self.moneyCurrent < 50000:
            txm = 10000
        elif 50000 <= self.moneyCurrent < 100000:
            txm = 50000
        else:
            txm = 100000
        u = f'http://u.cocozx.cn/api/{self.bz}/wdmoney'
        if self.bz == 'user':
            u = f'http://u.cocozx.cn/api/{self.bz}/wd'
        p = {"val": txm, "un": self.un, "token": self.token, "pageSize": 20}
        r = requests.post(u, headers=self.headers, json=p)
        print(self.name, '提现结果', r.text)
        if '请刷新页面重试' in r.text:
            print(self.name, '提现异常，请手动提现页面提现一次，确认下一次是否正常。')

    def run(self):
        if self.info():
            if self.bz == 'user':
                self.psmoneyc()
            time.sleep(1)
            self.read()
        time.sleep(2)
        self.info()
        time.sleep(2)
        self.wdmoney()


if __name__ == '__main__':
    printf = config.printf
    getmsg()
    bzl = ['coin']
    for bz in bzl:
        print('=' * 50)
        print(bz)
        tl = []
        if config.threadingf == 1:
            for cg in config.xkybconfig:
                print('*' * 50)
                print(f'开始执行{cg["name"]}')
                api = WXYD(cg, bz)
                t = threading.Thread(target=api.run, args=())
                tl.append(t)
                t.start()
                time.sleep(0.5)
            for t in tl:
                t.join()
        elif config.threadingf == 0:
            for cg in config.xkybconfig:
                print('*' * 50)
                print(f'开始执行{cg["name"]}')
                api = WXYD(cg, bz)
                api.run()
                print(f'{cg["name"]}执行完毕')
                time.sleep(3)
        else:
            print('请确定config配置文件中threadingf参数是否正确')
        print('全部账号执行完成')
