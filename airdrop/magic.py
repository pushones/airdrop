

import time
import  requests
from eth_account.messages import encode_defunct
from pop import ima
from rpc import Rpc
import threading
import web3
import random
import os
from dotenv import load_dotenv
from concurrent.futures.thread import ThreadPoolExecutor
from uitl import random_string
from faker import Faker

load_dotenv()
thread = threading.Lock()

os.environ['HTTP_PROXY'] = "http://127.0.0.1:10808"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10808"

class airdrop:
    def __init__(self, account):
        self.account = account
        self.session = requests.Session()
        self.rpc  = Rpc('https://api.mycryptoapi.com/eth', chainid=1 )# BSC 注意PRC
        veraaa =str( random.randint(96,120))

        self.pxy = "127.0.0.1:10808"
        self.proxy_pool = {'http': 'http://' + self.pxy, 'https': 'http://' + self.pxy}
        self.headers = {
            'sec-ch-ua': F'" Not A;Brand";v="99", "Chromium";v="{veraaa}", "Google Chrome";v="{veraaa}"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': F'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{veraaa}.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://magiceden.io',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://magiceden.io/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            "authorization": "Bearer null"
        }


    def get_nonce(self):

        url = f"https://api-mainnet.magiceden.io/v2/xc/login/v2/init"
        data = {
                "address": self.account.address,
                "blockchain": "ethereum"
            }

        for i in range(3):
            try:
                response = self.session.post(url, headers=self.headers, json=data,proxies=self.proxy_pool, impersonate="chrome110")
                data = response.json()

                if(data['token']):
                    return data
            except Exception as aaa:
                print(aaa)
                pass


    def _sign_message(self,msg):
        # print('钱包:' + str(self.account.address),msg)

        res = self.account.sign_message(encode_defunct(text=msg))
        return res.signature.hex()

    def wallet(self, nonce):
        token = nonce['token']
        nonce2 = nonce['nonce']
        url = f"https://api-mainnet.magiceden.io/v2/xc/login/v2/verify?chainId=ethereum"
        post1 = {
            "address": self.account.address,
            "signature": "0xed2df03439d8b5994d8d764a9d2537c080559e173e2f79172348a89278bc1d4c432c32e13a6cbe13cf3fe893e70b1e5ca4b6e02d69937a4004363b6200f6e28b1b",
            "nonce": nonce2,
            "token": token,
            "blockchain": "ethereum",
            "is_smart_wallet": False
        }
        HEX = self._sign_message(nonce['message'])
        post1["signature"] = HEX
        for i in range(3):
            try:
                response = self.session.post(url, headers=self.headers, proxies=self.proxy_pool, json=post1, impersonate="chrome110")
                # print("data", response.json())
                data = response.json()
                if(data['token']):
                    self.daily( data['token'])
                    return data['token']
            except Exception as aaa:
                print(aaa)
                pass
    def claim(self,token):
        self.headers['authorization'] = 'Bearer ' + token
        fake2 = Faker()
        fake2.pystr(min_chars=6, max_chars=10)
        namae= fake2.name().split(" ")[0]
        namae = namae+ random_string(4)
        url = f"https://api-mainnet.magiceden.io/auth/user"
        data ={"username":namae,"displayName":"","bio":"","email":"","antiPhishingCode":"",
               "preferences":{"socials":{"showDiscord":False}},"twitter":{"username":""},"discord":{"username":""},"telegram":{"username":""}}
        for i in range(3):
            try:
                response =requests.request("PUT",url, headers=self.headers,json=data, proxies=self.proxy_pool, impersonate="chrome110")
                if(response.text ==""):
                    break
            except Exception as aaa:
                time.sleep(2)
                pass
        url = f"https://api-mainnet.magiceden.io/rewards/quests/claimCompletedQuest?walletAddress={self.account.address}&questId=b5d802dc-892c-4f54-bf8d-f9de68a12e12"
        for i in range(3):
            try:
                response = self.session.post(url, headers=self.headers, proxies=self.proxy_pool, impersonate="chrome110")
                print("data", response.text)
                if(response.text!=""):
                    return
            except Exception as aaa:
                time.sleep(2)
                print(aaa)
                pass
    def daily(self, token):
        self.headers['authorization'] = 'Bearer ' + token
        # print("daily")
        url = f"https://api-mainnet.magiceden.io/rewards/quests/claimCompletedQuest?walletAddress={self.account.address}&questId=074de250-0aaa-4ece-9821-88ca04352250"
        for AAA in range(3):
            try:
                response = self.session.post(url, headers=self.headers, proxies=self.proxy_pool, impersonate="chrome110")
                if (response.text):
                    print("daily",response.text)
                    break
            except Exception as aaa:
                print(aaa)
        return

def run(acc):
    data= acc.strip()
    prikey = data.split("----")[1]
    print(prikey)
    account = web3.Account.from_key(prikey)
    op = airdrop(account)
    nonce = op.get_nonce()
    token = op.wallet(nonce)
    op.claim(token)

def read_file():
    with open('acctest.txt', 'r', encoding="utf-8") as f:
        a = f.readlines()
    return  a
def save_local(info):
        thread.acquire()
        with open("magic_cook.txt", "a+", encoding="utf-8") as f:
                f.write(info);
                f.write('\n')
        thread.release()
def strat():
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    delaytime = int(config['settings']['delaytime'])
    print("delaytime",delaytime)
    time.sleep(10*delaytime*60)
    config['settings']['delaytime'] = str(delaytime+1)
    with open('../redbrick/config.ini', 'w') as configfile:
        config.write(configfile)
    data =  read_file()
    count = len(data)
    threadPool = ThreadPoolExecutor(3)
    for num in range(0, count):
        threadPool.submit(run, data[num])
if __name__ == '__main__':
    strat()

