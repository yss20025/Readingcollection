"""

time: 2023。7.28
new Env('花花阅读');
地址：
http://mr1690765364827.xdxgiqh.cn/user/index.html?mid=TB6T7ENWA 
【花花阅读】看文章赚零花钱，全新玩法，提现秒到(若链接打不开，可复制到手机浏览器里打开)
进入app-我的-抢红包或者在我的钱包-提现进去之后抓包
提前在我的钱包里面绑定zfb号
抓包域名: http://u.cocozx.cn
抓包请求体里面: un和token
变量填在文本末尾 


"""

import requests
import time


class HHYD:
    def __init__(self, un, token):
        self.un = un
        self.token = token
        self.txje = 0
        self.headers = {
            'Host': 'u.cocozx.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5169 MMWEBSDK/20230604 MMWEBID/9516 MicroMessenger/8.0.38.2400(0x28002658) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'com.tencent.mm',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.data = {
            'un': f'{self.un}',
            'token': f'{self.token}',
            'pageSize': 20
        }

    def read(self):
        r = requests.post('http://u.cocozx.cn/api/user/read', headers=self.headers, json=self.data)
        # print(r.json())
        if r.json()['result'] is not None:
            if r.json()['result']['status'] == 10:
                print("获取文章成功！开始阅读！")
                time.sleep(5)
                run.submit()
            elif r.json()['result']['status'] == 50:
                print('获取文章失败，可能阅读已经失效！')
                run.info()
            elif r.json()['result']['status'] == 70:
                print('下一轮还未开始')
        else:
            print('获取文章失败！')
            print(r.json())
            run.info()

    def submit(self):
        r = requests.post('http://u.cocozx.cn/api/user/submit', headers=self.headers, json=self.data)
        # print(r.json())
        if r.json()['result'] is not None:
            print(f'获得：{r.json()["result"]["val"]},剩余阅读数：{r.json()["result"]["progress"]}')
            if r.json()["result"]["progress"] == 0:
                print("阅读完成！！！")
                run.info()
            else:
                print(f"准备阅读下一篇文章")
                time.sleep(5)
                run.read()
        else:
            print(f'阅读失败！')
            print(r.json())

    def info(self):
        r = requests.post('http://u.cocozx.cn/api/user/info', headers=self.headers, json=self.data)
        print(f"当前积分：{r.json()['result']['moneyCurrent']}")
        if int(r.json()['result']['moneyCurrent']) > 50000:
            self.txje = 50000
            print(f'准备提现5元')
            run.tx()
        elif 10000 < int(r.json()['result']['moneyCurrent']) < 50000:
            self.txje = 10000
            print(f'准备提现1元')
            run.tx()
        elif 5000 < int(r.json()['result']['moneyCurrent']) < 10000:
            self.txje = 5000
            print(f'准备提现0.5元')
            run.tx()
        elif 3000 < int(r.json()['result']['moneyCurrent']) < 5000:
            self.txje = 3000
            print(f'准备提现0.3元')
            run.tx()
        else:
            print("积分不足兑换")

    def tx(self):
        data = {
            'val': f'{self.txje}',
            'un': f'{self.un}',
            'token': f'{self.token}',
            'pageSize': 20
        }
        response = requests.post('http://u.cocozx.cn/api/user/wd', headers=self.headers, json=data)
        print(f"提现：{response.json()['msg']}")
        time.sleep(5)
        run.info()


if __name__ == '__main__':
    # 运行前前手动进去一下页面和提现页面
    un = '这里'
    token = '这里'
    run = HHYD(un, token)
    run.read()
