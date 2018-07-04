#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：GWN76xx设置向导的业务层

from setupwizard_control import SWControl
import time
from connect.ssh import SSH
from data import data



class SWBusiness(SWControl):

    def __init__(self,driver):
        #继承SWControl类的属性和方法
        SWControl.__init__(self,driver)

    #取出ap的PN值来判断ap是USA还是WORLD，并给出设置向导中两种型号的是否有国家代码页面
    def get_country_code(self):
        #登录web页面获取DUT的hostname
        DUT_hostname = SWControl.get_DUT_hostname(self)
        data_basic = data.data_basic()
        data_login = data.data_login()
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        tmp1 = ssh.ssh_cmd(data_basic['sshUser'],"ubus call controller.core status | grep part_number")
        tmp = tmp1.split("\"")[3][-4]
        if DUT_hostname == "GWN7610":
            #如果是USA，返回1
            if tmp == "1":
                print "The AP is USA product!"
                return 1
            #如果是WORLD，返回0
            elif tmp == "6":
                print "The AP is WORLD product!"
                return 0
            else:
                print "PN value is not correct!"
                return None
        elif DUT_hostname == "GWN7600":
            #如果是USA，返回1
            if tmp == "5":
                print "The AP is USA product!"
                return 1
            #如果是WORLD，返回0
            elif tmp == "7":
                print "The AP is WORLD product!"
                return 0
            else:
                print "PN value is not correct!"
                return None
        elif DUT_hostname == "GWN7600LR":
            #如果是USA，返回1
            if tmp == "1":
                print "The AP is USA product!"
                return 1
            #如果是WORLD，返回0
            elif tmp == "2":
                print "The AP is WORLD product!"
                return 0
            else:
                print "PN value is not correct!"
                return None
        elif DUT_hostname == "GWN7002W":
            #如果是USA，返回1
            if tmp == "8":
                print "The AP is USA product!"
                return 1
            #如果是WORLD，返回0
            elif tmp == "9":
                print "The AP is WORLD product!"
                return 0
            else:
                print "PN value is not correct!"
                return None



    #关闭设置向导，点击其他页面判断是否有无设置向导窗口
    def close_wizard_click_othermenu(self):
        #点击关闭按钮
        SWControl.close_wizard(self)
        #进入接入点确定没有设置向导窗口
        SWControl.menu_css(self,u"接入点","Access Points")
        result = SWControl.check_wizard(self)
        return result


    #尝试在浏览其他页面时，点击设置向导，并检查向导是否正常使用
    def othermenu_click(self):
        result = []

        #进入接入点
        SWControl.menu_css(self,u"接入点","Access Points")
        ##点击页面上的问号开启设置向导
        SWControl.SW_menu(self)
        #检查登录web界面，判断是否会显示向导页面
        result11 = SWControl.check_wizard(self)
        #下次不再显示是否被选中
        result12 = SWControl.get_hidenexttime(self)
        SWControl.close_wizard(self)
        if result11 == True and result12 =="true":
            result.append(True)
        else:
            result.append(False)

        #进入SSIDs
        SWControl.menu_css(self,u"SSIDs","SSIDs")
        ##点击页面上的问号开启设置向导
        SWControl.SW_menu(self)
        result21 = SWControl.check_wizard(self)
        #下次不再显示是否被选中
        result22 = SWControl.get_hidenexttime(self)
        SWControl.close_wizard(self)
        if result21 == True and result22 =="true":
            result.append(True)
        else:
            result.append(False)
        #进入客户端
        SWControl.menu_css(self,u"客户端","Clients")
        ##点击页面上的问号开启设置向导
        SWControl.SW_menu(self)
        result31 = SWControl.check_wizard(self)
        #下次不再显示是否被选中
        result32 = SWControl.get_hidenexttime(self)
        SWControl.close_wizard(self)
        if result31 == True and result32 =="true":
            result.append(True)
        else:
            result.append(False)
        #进入系统设置
        SWControl.menu_css(self,u"系统设置","System Settings")
        ##点击页面上的问号开启设置向导
        SWControl.SW_menu(self)
        result41 = SWControl.check_wizard(self)
        #下次不再显示是否被选中
        result42 = SWControl.get_hidenexttime(self)
        SWControl.close_wizard(self)
        if result41 == True and result42 =="true":
            result.append(True)
        else:
            result.append(False)
        return result

    #AP发现AP状态
    def AP_status(self,master_ap,slave_ap1,slave_ap2):
        result = []
        n = SWBusiness.get_country_code(self)
        #点击页面上的问号开启设置向导
        SWControl.SW_menu(self)
        #点击两次下一步
        for i in range(2-n):
            SWControl.nextstep(self)
        time.sleep(30)
        result1 = SWControl.get_APs_text(self)
        Master_AP = master_ap.upper()
        Slave_ap1 = slave_ap1.upper()
        Slave_ap2 = slave_ap2.upper()
        print Master_AP,result1
        if (Master_AP in result1) and (Slave_ap1 in result1) and (Slave_ap2 in result1):
            result.append(True)
        else:
            result.append(False)

        #获取APs页面中没有配对的元素的disabled属性
        result2 = SWControl.get_APs_unpair(self)
        #如果有disable属性为true的，则返回True
        if 'true' in result2:
            result.append(True)
        else:
            result.append(False)

        return result



    #登录web界面，运行设置向导，配对slave ap
    #只有一个设备时,只添加一个设备到网络组
    def pair_slaveAP(self,mac):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击两次下一步
        for i in range(2-n):
            SWControl.nextstep(self)
        #点击配对
        SWControl.pair(self,mac)
        time.sleep(80)
        #获取APs页面的状态信息
        result1 = SWControl.get_APs_status(self)
        print result1
        if (u"在线" or 'Online') in result1:
            return True
        else:
            return False

    #网络组中，wifi的状态
    def wifi_status(self):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        #获取wifi的状态
        #输出：true：被选中，None：没被选中
        result = SWControl.get_wifi_status(self)
        return result

    #取得应该的ssid
    def default_ssid(self,master_ap):
        #小写转换为大写
        Master_ap = master_ap.upper()
        #按：号分成列表
        tmp1 = Master_ap.split(":")
        #取第4个元素到最后一个元素
        tmp2 = tmp1[3:]
        #组合成字符串
        tmp3 = ''.join(tmp2)
        tmp = 'GWN%s'%tmp3
        return tmp

    #判断默认ssid正确与否
    def check_default_ssid(self,master_ap):
        n = SWBusiness.get_country_code(self)
        #取得应该的ssid
        tmp = SWBusiness.default_ssid(self,master_ap)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        #获取SSID
        result = SWControl.get_ssid(self)
        print tmp,result
        if result == tmp:
            return True
        else:
            return False


    #新添加的AP在可添加设备中,默认DUT会被放入已添加设备中
    def default_devices(self,slave_ap,master_ap):
        n = SWBusiness.get_country_code(self)
        #小写转换为大写
        Slave_ap = slave_ap.upper()
        Master_ap =master_ap.upper()
        #打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        #获取可添加设备的mac
        #result1 = SWControl.get_available_devices(self)
        #获取已添加设备的mac----1.0.2.94已调整到每次配对后，设备自动在已添加的设备中
        result2 = SWControl.get_member_devices(self)
        print Slave_ap,Master_ap,result2
        if (Slave_ap and Master_ap) in result2:
            return True
        else:
            return False


    #添加AP
    #设备管理，只有一个设备时,只添加一个设备
    def add_slave_ap(self,slave_ap):
        n = SWBusiness.get_country_code(self)
        #小写转换为大写
        Slave_ap = slave_ap.upper()
        #打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        #1.0.2.94已调整到每次配对后，设备自动在已添加的设备中
        #SWControl.add_NG(self)
        #获取已添加设备的mac
        result2 = SWControl.get_member_devices(self)
        print Slave_ap,result2
        if Slave_ap in result2:
            return True
        else:
            return False


    #网络组-disable wifi
    def disable_wifi(self,ssid,wlan):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        ##设置wifi的状态:disalbe/enable
        SWControl.set_wifi_status(self)
        #设置SSID
        #SWControl.ssid(self,ssid)
        #设置wpa的密码
        #SWControl.wpa_key(self,key)
        SWControl.nextstep(self)
        time.sleep(120)
        print "disable wifi in setupwizard successfully!"
        #扫描到ssid返回True
        result = SWControl.ssid_scan_result(self,ssid,wlan)
        print result
        return result

    #网络组-enable wifi
    def enable_wifi(self,ssid,key,wlan):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        ##设置wifi的状态:disalbe/enable
        SWControl.set_wifi_status(self)
        #设置SSID
        SWControl.ssid(self,ssid)
        #设置wpa的密码
        SWControl.wpa_key(self,key)
        SWControl.nextstep(self)
        time.sleep(180)
        #扫描到ssid返回True
        result = SWControl.ssid_scan_result_backup(self,ssid,wlan)
        print result
        return result

    #网络组-移除AP
    def del_ap(self,slave_ap,host,user,pwd):
        n = SWBusiness.get_country_code(self)
        #再次打开设置向导
        SWControl.SW_menu(self)
        #点击三次下一步
        for i in range(3-n):
            SWControl.nextstep(self)
        #设备管理，在已添加的设备中删除特定的设备
        SWControl.del_NG_special(self,slave_ap)
        SWControl.nextstep(self)
        time.sleep(80)
        #登录slave ap确认没有wifi接口
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"ifconfig")
        if 'wifi0' in result:
            return False
        else:
            return True

    def unpair_slave_ap(self,host,user,pwd):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击两次下一步
        for i in range(2-n):
            SWControl.nextstep(self)
        #只有一个slave时，解除配对的设备
        SWControl.unpair(self)
        SWControl.notice_ok(self)
        time.sleep(200)
        #登录AP后台取出管理员密码,判断slave ap是否恢复出厂设置
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show grandstream.general.admin_password")
        if "='admin'" in result:
            return True
        else:
            return False

    #完全操作：登录web界面，运行设置向导，配对slave ap，并加入默认网络组
    #只有一个设备时,只添加一个设备到网络组
    def complete(self,ssid,key,wlan,slave_mac1,slave_mac2):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击两次下一步
        for i in range(2-n):
            SWControl.nextstep(self)
         #点击配对
        SWControl.pair(self,slave_mac1)
        #点击配对
        SWControl.pair(self,slave_mac2)
        time.sleep(20)
        #点击下一步
        SWControl.nextstep(self)
        #设置SSID
        SWControl.ssid(self,ssid)
        #设置wpa的密码
        SWControl.wpa_key(self,key)
        #1.0.2.94已调整到每次配对后，设备自动在已添加的设备中
        #设备管理，只有一个设备时,只添加一个设备
        #SWControl.add_NG(self)
        SWControl.nextstep(self)
        time.sleep(120)
        print "run setupwizard,pair slave ap,set ssid and key successfully!"
        #无线网卡连接该ssid，返回连接的结果
        result = SWControl.connect_WPA_AP(self,ssid,key,wlan)
        #使无线网卡获取IP地址
        #SWControl.dhcp_wlan(self,wlan)
        if ssid in result:
            return True
        else:
            return False

    #完全操作：登录web界面，运行设置向导，配对slave ap，并加入默认网络组
    #只有一个设备时,只添加一个设备到网络组
    def complete_backup(self,ssid,key,wlan,slave_mac2):
        n = SWBusiness.get_country_code(self)
        #打开设置向导
        SWControl.SW_menu(self)
        #点击两次下一步
        for i in range(2-n):
            SWControl.nextstep(self)
        #点击配对
        SWControl.pair(self,slave_mac2)
        time.sleep(20)
        #点击下一步
        SWControl.nextstep(self)
        #设置SSID
        SWControl.ssid(self,ssid)
        #设置wpa的密码
        SWControl.wpa_key(self,key)
        #1.0.2.94已调整到每次配对后，设备自动在已添加的设备中
        #设备管理，只有一个设备时,只添加一个设备
        #SWControl.add_NG(self)
        SWControl.nextstep(self)
        time.sleep(120)
        print "run setupwizard,pair slave ap,set ssid and key successfully!"
        #无线网卡连接该ssid，返回连接的结果
        result = SWControl.connect_WPA_AP(self,ssid,key,wlan)
        #使无线网卡获取IP地址
        #SWControl.dhcp_wlan(self,wlan)
        if ssid in result:
            return True
        else:
            return False