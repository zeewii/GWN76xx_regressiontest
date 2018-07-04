#coding=utf-8
#作者：曾祥卫
#时间：2017.03.09
#描述：GWN76xx进行ssh登录

import pexpect,subprocess,codecs
import datetime,time


class SSH:

    #自己SSH类的属性:host-远程登录主机名，pwd-密码
    def __init__(self,host,pwd):
        self.host = host
        self.pwd = pwd

    #描述:首先使用 dbclient host -l user -i dropbear_rsa_client_key cmd登录ssh,在确定是否是首次登录，再输出结果
    #输入：user-登录用户名,cmd-命令
    #输出:命令返回的结果，同时将结果存放在同目录的log.txt文件中
    def ssh_cmd(self,user,cmd):
        try:
            #远程主机输入后出现的字符串
            ssh_newkey = "(?i)Do you want to continue connecting? (y/n)"
            # 为 ssh 命令生成一个 spawn 类的子程序对象.
            child = pexpect.spawn('dbclient %s -l %s -i ./connect/dropbear_rsa_client_key %s' \
                                  %(self.host, user, cmd), timeout=8)
            i = child.expect(['password: ',pexpect.TIMEOUT,pexpect.EOF, ssh_newkey])
            # 如果登录超时，打印出错信息，并退出.
            # if i == 0:
            #     print u"1错误，ssh 登录超时:"
            #     print child.before, child.after
            #     return None
            # 如果 登录超时或ssh 没有 public key，接受它.
            # 这里有问题：第一次登录ssh时是超时，但实际上是能响应的，这里先这样处理，后面再研究
            if i != 0:
                child.sendline('y')
                child.expect(['password: ',pexpect.TIMEOUT,pexpect.EOF])
                # if i != 0:
                #     print u"2错误，ssh 登录超时:"
                #     print child.before, child.after
                #     return None
            # 输入密码.
            child.sendline(self.pwd)

            # 列出输入密码后期望出现的字符串，'password',EOF，超时
            i = child.expect(['password: ', pexpect.EOF, pexpect.TIMEOUT])
            # 匹配到字符'password: '，打印密码错误
            if i == 0:
                print u'密码输入错误！'
            # 匹配到了EOF，打印ssh登录成功，并输入命令后成功退出
            elif i == 1:
                print u'恭喜,ssh登录输入%s命令成功！' %cmd
            # 匹配到了超时，打印超时
            else:
                print u'输入命令后等待超时！'

            # 将执行命令的时间和结果以追加的形式保存到log.txt文件中备份文件
            f = codecs.open('./data/testresultdata/ssh_log.txt', 'a',encoding='utf-8')
            str1 = str(datetime.datetime.now()) + ' command:' + cmd
            f.writelines(str1 + child.before)
            f.close()

            result = child.before
            print result
            return result
        except pexpect.ExceptionPexpect, e:
            print u"ssh连接失败，正在重启进程"
            result2 = subprocess.call("rm -rf ~/.ssh",shell=True)
            print result2

            time.sleep(10)
            print "delete ssh"
            print e

    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点频率
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改频率,mode:2.4GHz,5GHz,Dual-Band
    def ssh_menu_APs_Freq(self,user,n,mode):
        try:
            #远程主机登录后出现的字符串
            finish = ""
            # 为ssh命令生成一个spawn类的子程序对象
            child = pexpect.spawn("ssh %s@%s"%(user,self.host))
            #列出期望出现的字符串，'password',EOF,超时
            i = child.expect(["(?i)password: ", pexpect.EOF, pexpect.TIMEOUT])
            #如果匹配EOF,超时,打印信息并退出
            if i != 0:
                print u"ssh登录失败，由于输入密码时超时或EOF"
                #强制退出
                child.close(force=True)
            #匹配到了password，输入password
            child.sendline(self.pwd)
            #期待远程主机的命令提示符出现
            child.expect(finish)
            #如果匹配提示符成功，输入2进入接入点菜单
            child.sendline("2")
            child.expect(finish)
            #输入1进入已配对的设备
            child.sendline("1")
            child.expect(finish)
            #输入n来选择第n个设备
            child.sendline(n)
            child.expect(finish)
            #输入1来修改参数
            child.sendline("1")
            child.expect(finish)
            #输入4进入频率选择项
            child.sendline("4")
            child.expect(finish)
            if mode == "2.4GHz":
                #输入1进入频率2.4g
                child.sendline("1")
            elif mode == "5GHz":
                #输入2进入频率5g
                child.sendline("2")
            elif mode == "Dual-Band":
                #输入3进入频率Dual-Band
                child.sendline("3")
            else:
                #输入其他值终止
                print u"输入值错误，退出！"
                return
            #输入s保存配置
            child.expect(finish)
            child.sendline("s")
            time.sleep(180)
            print u'恭喜,ssh登录修改APs的频率%s成功！'%mode
            child.expect(finish)
            #退出telent子程序
            child.close(force=True)
            #使用admin用户通过ssh来登录路由，通过菜单来重启AP
            #SSH.ssh_menu_APs_reboot(self,user)
        #异常打印原因
        except pexpect.ExceptionPexpect, e:
            print u"ssh连接失败，正在重启进程"
            result2 = subprocess.call("rm -rf ~/.ssh",shell=True)
            print result2
            time.sleep(10)
            print "delete ssh"
            print e

    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点2.4G的配置
    #输入：user-登录用户名,menu-修改哪项参数，n-选择已配对的第几个设备来修改模式
    def ssh_menu_APs_2g4_config(self,user,n,menu,value):
        try:
            #远程主机登录后出现的字符串
            finish = ""
            # 为ssh命令生成一个spawn类的子程序对象
            child = pexpect.spawn("ssh %s@%s"%(user,self.host))
            #列出期望出现的字符串，'password',EOF,超时
            i = child.expect(["(?i)password: ", pexpect.EOF, pexpect.TIMEOUT])
            #如果匹配EOF,超时,打印信息并退出
            if i != 0:
                print u"ssh登录失败，由于输入密码时超时或EOF"
                #强制退出
                child.close(force=True)
            #匹配到了password，输入password
            child.sendline(self.pwd)
            #期待远程主机的命令提示符出现
            child.expect(finish)
            #如果匹配提示符成功，输入2进入接入点菜单
            child.sendline("2")
            child.expect(finish)
            #输入1进入已配对的设备
            child.sendline("1")
            child.expect(finish)
            #输入n来选择第n个设备
            child.sendline(n)
            child.expect(finish)
            #输入1来修改参数
            child.sendline("1")
            child.expect(finish)
            #输入6进入2.4G选择项
            child.sendline("6")
            child.expect(finish)
            #输入1进入模式选择项
            child.sendline(menu)
            child.expect(finish)
            child.sendline(value)
            #输入s保存配置
            child.expect(finish)
            child.sendline("s")
            time.sleep(80)
            print u'恭喜,ssh登录修改APs的2.4G配置成功！'
            child.expect(finish)
            #退出telent子程序
            child.close(force=True)
            #异常打印原因
        except pexpect.ExceptionPexpect, e:
            print u"ssh连接失败，正在重启进程"
            result2 = subprocess.call("rm -rf ~/.ssh",shell=True)
            print result2
            time.sleep(10)
            print "delete ssh"
            print e

    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点5g的配置
    #输入：user-登录用户名,menu-修改哪项参数,n-选择已配对的第几个设备来修改
    def ssh_menu_APs_5g_config(self,user,n,menu,value):
        try:
            #远程主机登录后出现的字符串
            finish = ""
            # 为ssh命令生成一个spawn类的子程序对象
            child = pexpect.spawn("ssh %s@%s"%(user,self.host))
            #列出期望出现的字符串，'password',EOF,超时
            i = child.expect(["(?i)password: ", pexpect.EOF, pexpect.TIMEOUT])
            #如果匹配EOF,超时,打印信息并退出
            if i != 0:
                print u"ssh登录失败，由于输入密码时超时或EOF"
                #强制退出
                child.close(force=True)
            #匹配到了password，输入password
            child.sendline(self.pwd)
            #期待远程主机的命令提示符出现
            child.expect(finish)
            #如果匹配提示符成功，输入2进入接入点菜单
            child.sendline("2")
            child.expect(finish)
            #输入1进入已配对的设备
            child.sendline("1")
            child.expect(finish)
            #输入n来选择第n个设备
            child.sendline(n)
            child.expect(finish)
            #输入1来修改参数
            child.sendline("1")
            child.expect(finish)
            #输入7进入5G选择项
            child.sendline("7")
            child.expect(finish)
            #输入数字进入5G的菜单选择项
            child.sendline(menu)
            child.expect(finish)
            #直接输入信道值
            child.sendline(value)
            #输入s保存配置
            child.expect(finish)
            child.sendline("s")
            time.sleep(180)
            print u'恭喜,ssh登录修改APs的5G配置成功！'
            child.expect(finish)
            #退出telent子程序
            child.close(force=True)
            #使用admin用户通过ssh来登录路由，通过菜单来重启AP
            #SSH.ssh_menu_APs_reboot(self,user)
        #异常打印原因
        except pexpect.ExceptionPexpect, e:
            print u"ssh连接失败，正在重启进程"
            result2 = subprocess.call("rm -rf ~/.ssh",shell=True)
            print result2
            time.sleep(10)
            print "delete ssh"
            print e

    #使用admin用户通过ssh来登录路由，通过菜单来重启AP
    #输入：user-登录用户名
    def ssh_menu_APs_reboot(self,user):
        try:
            #远程主机登录后出现的字符串
            finish = ""
            # 为ssh命令生成一个spawn类的子程序对象
            child = pexpect.spawn("ssh %s@%s"%(user,self.host))
            #列出期望出现的字符串，'password',EOF,超时
            i = child.expect(["(?i)password: ", pexpect.EOF, pexpect.TIMEOUT])
            #如果匹配EOF,超时,打印信息并退出
            if i != 0:
                print u"ssh登录失败，由于输入密码时超时或EOF"
                #强制退出
                child.close(force=True)
            #匹配到了password，输入password
            child.sendline(self.pwd)
            #期待远程主机的命令提示符出现
            child.expect(finish)
            #如果匹配提示符成功，输入9进入维护菜单
            child.sendline("9")
            child.expect(finish)
            #输入b重启ap
            child.sendline("b")
            child.expect(finish)
            time.sleep(180)
            print u'恭喜,通过菜单模式重启AP成功！'
            #退出telent子程序
            child.close(force=True)
            #异常打印原因
        except pexpect.ExceptionPexpect, e:
            print u"ssh连接失败，正在重启进程"
            result2 = subprocess.call("rm -rf ~/.ssh",shell=True)
            print result2
            time.sleep(10)
            print "delete ssh"
            print e


    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点2.4G模式
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改模式,mode:11b,11g,11n
    def ssh_menu_APs_2g4_mode(self,user,n,mode):
        if mode == "11b":
            SSH.ssh_menu_APs_2g4_config(self,user,n,"1","1")
        elif mode == "11g":
            SSH.ssh_menu_APs_2g4_config(self,user,n,"1","2")
        elif mode == "11n":
            SSH.ssh_menu_APs_2g4_config(self,user,n,"1","3")
        else:
            #输入其他值终止
            return


    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点5g的信道
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改,channel:36,40,44,48,149,153,157,161
    def ssh_menu_APs_5g_channel(self,user,n,channel):
        SSH.ssh_menu_APs_5g_config(self,user,n,"7",channel)

    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点5g的shortGI
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改,mode为1:enable，3:disable
    def ssh_menu_APs_5g_shortGI(self,user,n,mode):
        if mode == "enable":
            SSH.ssh_menu_APs_5g_config(self,user,n,"3","1")
        elif mode == "disable":
            SSH.ssh_menu_APs_5g_config(self,user,n,"3","2")
        else:
            #输入其他值终止
            return


    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点5g的active stream
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改,stream为0,1,2,3
    def ssh_menu_APs_5g_active_stream(self,user,n,stream):
        SSH.ssh_menu_APs_5g_config(self,user,n,"2",stream)

    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点5g的带宽
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改,mode为1：20,2：40,3：80
    def ssh_menu_APs_5g_width(self,user,n,mode):
        if mode == "20MHz":
            SSH.ssh_menu_APs_5g_config(self,user,n,"5","1")
        elif mode == "40MHz":
            SSH.ssh_menu_APs_5g_config(self,user,n,"5","2")
        elif mode == "80MHz":
            SSH.ssh_menu_APs_5g_config(self,user,n,"5","3")
        else:
            #输入其他值终止
            return

    #使用admin用户通过ssh来登录路由，通过菜单来修改接入点5g的发生功率强度
    #输入：user-登录用户名,n-选择已配对的第几个设备来修改,mode为1,2,3
    def ssh_menu_APs_5g_power(self,user,n,mode):
        SSH.ssh_menu_APs_5g_config(self,user,n,"4",mode)

    #使用admin用户通过ssh来登录路由，通过进入隐藏模式,并输入对应key，输入国家代码
    #输入：user-登录用户名
    def ssh_menu_APs_hidden_menu(self,user,key,ccode):
        try:
            #远程主机登录后出现的字符串
            finish = ""
            # 为ssh命令生成一个spawn类的子程序对象
            child = pexpect.spawn("ssh %s@%s"%(user,self.host))
            #列出期望出现的字符串，'password',EOF,超时
            i = child.expect(["(?i)password: ", pexpect.EOF, pexpect.TIMEOUT])
            #如果匹配EOF,超时,打印信息并退出
            if i != 0:
                print u"ssh登录失败，由于输入密码时超时或EOF"
                #强制退出
                child.close(force=True)
            #匹配到了password，输入password
            child.sendline(self.pwd)
            #期待远程主机的命令提示符出现
            child.expect(finish)
            time.sleep(3)
            #输入隐藏模式的code102010
            child.sendline("102010")
            child.expect(finish)
            time.sleep(3)
            print "go in hidden mode"
            #输入ap对应的key
            child.sendline(key)
            child.expect(finish)
            print "input ap's key"
            #输入国家代码
            child.sendline(ccode)
            child.expect(finish)
            print "input country code"
            time.sleep(3)
            #退出telent子程序
            child.close(force=True)
            #异常打印原因
        except pexpect.ExceptionPexpect, e:
            print u"ssh连接失败，正在重启进程"
            result2 = subprocess.call("rm -rf ~/.ssh",shell=True)
            print result2
            time.sleep(10)
            print "delete ssh"
            print e