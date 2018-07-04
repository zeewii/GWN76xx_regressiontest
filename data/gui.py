#coding=utf-8
#作者：曾祥卫
#描述：执行测试用例前的准备工作
#时间：2017.3.16

import easygui,sys,time,subprocess


#开始欢迎确认框
def welcome():
    msg1="请先把路由和PC按以下拓扑图连接好"
    msg2='请确定data.xlsx的数据是否正确'
    msg3='即将要开始GWN76xx的自动化测试\n\n'\
         '1.修改该PC的rsyslog服务器配置(/etc/rsyslog.conf)，使其作为AP的syslog服务器，并以AP的ip地址来命名log文件(如:/var/log/ip.log)。\n\n'\
         '2.请将AP的串口接入到该测试机中，安装minicom(或securecrt)，并保存串口打印信息为/home/test/minicom.log。\n\n'\
         '3.请先将配置7000的admin用户的密码为GWN@autotest123\n\n'\
         '4.请先将76xx恢复出厂设置，或者配置76xx的admin用户的密码为GWN@autotest123。\n\n'\
         '5.在该PC上安装iperf3,然后在7000的WAN端网络中安装iperf3，并运行iperf3 -s(深圳是192.168.80.5,已安装并运行)。'
    title = '欢迎进行GWN76xx的自动化测试'
    image="./data/topological_map.gif"
    choice=["正确并继续","点击该按钮先去设置"]
    #欢迎页面拓扑图
    easygui.msgbox(msg3,title)
    easygui.msgbox(msg1,title,image=image)
    #欢迎页面确定data.xlsx数据正确
    welcome = easygui.ccbox(msg2,title,choices=choice)
    #点击"先去设置"，打开data.xlsx
    if welcome == 0:
        subprocess.call("xdg-open ./data/data.xlsx",shell=True)
        print "退出自动化测试"
        sys.exit(0)

#选择GWN型号,并替换accesspoints的用例集
def GWN_name():
    title="请选择GWN产品型号"
    msg="开始测试前请选择你将要测试的产品型号"
    choices = ['GWN7610', 'GWN7600', 'GWN7600LR']
    name = easygui.buttonbox(msg=msg,title=title,choices=choices)
    print name
    return name



#选择测试用例框
def choice_case(GWN_name):
    case = []
    msg="请先选择需要执行的测试用例集"
    title="选择用例集"
    choices=['A_maintenance',
             'B_login',
             'C_setupwizard',
             'D_navbar',
             'E_overview',
             'F_accesspoints',
             'G_ssid',
             'H_clients',
             'I_clientaccess',
             'J_clienttimepolicy',
             'K_captiveportal',
             'L_debug',
             'M_failover',
             'N_countrycode_timezone',
             'O_bandwidth_rules'
             ]

    while True:
        #测试用例选择框
        case=easygui.multchoicebox(msg,title,choices)
        #点击取消退出测试
        if case == None :
            print "退出自动化测试"
            sys.exit(0)
        #不选择任何一个用例，提示
        elif len(case) ==0:
            easygui.msgbox("你没有选择任何一个测试用例集，请必须选择一个！","错误")
            continue
        else:
            msg1 = ""
            for i in range(len(case)):
                msg1 += ('%s\n'%case[i])
            #显示所选择的测试用例，并再次确认
            confirm_again=easygui.ccbox(msg=msg1,title="请确认所需测试集的用例是否正确：",\
                                        choices=("正确并继续","再去选择"))
            #点击再去选择，重新选择用例
            if confirm_again == 0:
                continue

            #如果选择的accesspoints用例集
            if 'F_accesspoints' in case:
                #按照产品型号替换相对应的用例集
                case.remove('F_accesspoints')
                if GWN_name == 'GWN7610':
                    case.append('F_accesspoints_7610')
                elif GWN_name == 'GWN7600':
                    case.append('F_accesspoints_7600')
                elif GWN_name == 'GWN7600LR':
                    case.append('F_accesspoints_7600lr')
                #最后再重新排序
                case.sort()

            #如果选择了clientaccess用例集
            if 'I_clientaccess' in case:
                #按照产品型号替换相对应的用例集
                case.remove('I_clientaccess')
                if GWN_name == 'GWN7610':
                    case.append('I_clientaccess_7610')
                elif GWN_name == 'GWN7600':
                    case.append('I_clientaccess_7600')
                elif GWN_name == 'GWN7600LR':
                    case.append('I_clientaccess_7600')
                #最后再重新排序
                case.sort()

            #如果选择了国家代码和时区菜单，弹出窗口提示
            if 'N_countrycode_timezone' in case:
                msg3 = "由于测试国家代码和时区功能需要长达9小时，请再次确认是否选择测试该两项功能！\n\n如果需要，master ap请使用World版！"
                CCTZ = easygui.ccbox(msg=msg3,title="请再次确认是否需要测试国家代码和时区", \
                                        choices=("不需要","确定需要测试"))
                #如果选择“不需要”，则从case列表中删除
                if CCTZ == 1:
                    case.remove('N_countrycode_timezone')
            #如果选择的维护菜单，确认是否需要测试国家代码的功能
            if 'A_maintenance' in case:
                msg2 = "由于测试一次升降级的功能需要多3小时以上，为了提高测试效率，所以提供该选择项!"
                case_countrycode = easygui.ccbox(msg=msg2,title="是否需要测试升降级的功能",\
                                        choices=("不需要","需要"))

                #如果选择“不需要”
                if case_countrycode == 1:
                    case[0] = 'A_maintenance_noupgrade'
                #如果选择“需要”
                elif case_countrycode == 0:
                    case[0] = 'A_maintenance_haveupgrade'
            break
    return case




#输入发送测试报告的email地址和密码
def send_email():
    send_email = []
    msg='请输入你的eamil地址和密码'
    title="你的email"
    field = ["*email地址", "*密码"]
    while True:
        #输入用户名和密码框，密码为不显示明文
        send_email=easygui.multpasswordbox(msg, title,field)
        #点击取消退出测试
        if send_email == None :
            print "退出自动化测试"
            sys.exit(0)
        #地址和密码都不输入，提示
        elif send_email == ["",""]:
            easygui.msgbox("你必须输入email地址和密码！","错误")
            continue
        #地址为空，提示
        elif send_email[0].strip()=="":
            easygui.msgbox("你必须输入email地址！","错误")
            continue
        #密码为空，提示
        elif send_email[1].strip()=="":
            easygui.msgbox("你必须输入密码！","错误")
        else:
            break
    return send_email


#输入接收测试报告的email地址
def receive_email():
    receive_email = []
    msg="至少必须输入一个emai地址，多个email地址用逗号隔开"
    title="接收测试报告的email地址"
    fields=["email地址1","email地址2","email地址3","email地址4","email地址5","email地址6","email地址7","email地址8"]
    values = ["sz_gwntest@grandstream.cn",\
              "wliu@grandstream.cn","xwzeng@grandstream.cn","tjiang@grandstream.cn"]
    values_self = ["xwzeng@grandstream.cn"]
    while True:
        #email地址输入框
        receive_email=easygui.multenterbox(msg,title,fields,values)
        #点击取消退出测试
        if receive_email == None:
            print "退出自动化测试"
            sys.exit(0)
        msg1 =""
        for i in range(len(fields)):
            msg1 +=(receive_email[i])
        #一个地址都不输入，提示
        if msg1 == '':
            easygui.msgbox("请至少必须输入一个emai地址！","错误")
            continue
        else:
            break
    return receive_email

#设置用例执行的次数
def loop_times():
    loop = easygui.ccbox('是否需要循环多次执行？','循环执行测试',choices=['否','是'])
    if loop == 0:
        times = easygui.enterbox(msg='格式如：5',title='请输入循环执行的次数')
        print "Run loop times is %s"%times
        return times
    return loop

#设置自动化执行人
def test_executor():
    while True:
        test_executor = easygui.enterbox(msg='中文英文皆可',title='请输入自动化执行人姓名')
        if (test_executor == "") or (test_executor == None):
            easygui.msgbox('必须要输入自动化执行人姓名才能继续开始测试','请输入自动化执行人姓名')
            continue
        else:
            return test_executor


#设置开始时间
def start_time():
    YN = easygui.ccbox('是否立刻开始测试？','开始测试',choices=['是','设置开始时间'])
    if YN == 0:
        start_time = easygui.enterbox(msg='格式如：18:30',title='请输入自动化测试开始的时间')
        timing=time.strftime('%H:%M',time.localtime(time.time()))
        print u"目前时间是：%s\n开始测试时间是：%s"%(timing,start_time)
        #是否需要从Internet上下载固件后，然后再进行测试
        #########控制什么时间脚本执行######
        while True:
            timing=time.strftime('%H:%M',time.localtime(time.time()))
            if timing != start_time:
                time.sleep(30)
                print u"目前时间是：%s，请等待..."%timing
            else:
                print u"开始执行自动化测试！"
                break

#是选择定时开始测试，还是选择需要检查Internet上有固件后才进行测试
def choose_timing_or_download_FW():
    download = easygui.ccbox('是否需要检查Internet上有固件后才进行测试？','检查并下载固件',choices=['否','是'])
    if download == 0:
        web_address = easygui.enterbox(msg='格式如：http://www.grandstream.cn/gwn7610fw.bin',\
                                       title='请输入固件的网站地址')
        easygui.msgbox('点击OK开始测试','即将开始测试')
        while True:
            #首先删除先前的固件
            subprocess.call("rm -rf ~/FW/7610_FW/new/*",shell=True)
            result = subprocess.call("wget --http-user=guest --http-passwd=grandstream -O ~/FW/7610_FW/new/gwn7610fw.bin %s"%web_address,shell=True)
            if result == 0:
                print "Download FW successful!\nStart running auto test..."
                break
            else:
                print "Download FW failed! Wait 20mins and go on..."
                time.sleep(1200)
    else:
        easygui.msgbox('点击OK去设置开始的时间','即将开始测试')
        start_time()



#设置每个用例集是否需要逐个测试并发送邮件
#输出：1：不需要;0：需要
def testcase_onebyone():
    msg='是否需要逐个测试并生成单独的测试报告'
    title='请确定每个用例集是否需要逐个测试并生成单独的测试报告'
    choice=["不需要","需要"]
    onebyone = easygui.ccbox(msg,title,choices=choice)
    return onebyone


__author__ = 'zeng'

