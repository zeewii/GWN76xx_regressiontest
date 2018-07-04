#coding=utf-8
#作者：曾祥卫
#时间：2017.03.15
#描述：GWN76xx接入点的业务层


import time
import subprocess
from selenium.webdriver.common.keys import Keys
from login.login_business import LoginBusiness
from aps_control import APSControl
from setupwizard.setupwizard_business import SWBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from clients.clients_business import ClientsBusiness
from overview.overview_business import OVBusiness
from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from connect.ssh import SSH
from data import data

data_AP = data.data_AP()
data_basic = data.data_basic()
data_login = data.data_login()

class APSBusiness(APSControl):

    def __init__(self,driver):
        #继承APSControl类的属性和方法
        APSControl.__init__(self,driver)

    #登录ssh，输入cat /etc/config/grandstream查看配置
    def check_AP_config(self,host,user,pwd):
        tmp = SSH(host,pwd,)
        result = tmp.ssh_cmd(user,"cat /etc/config/grandstream")
        return result

    #在页面上把AP恢复出厂设置
    def web_factory_reset(self,host,user,pwd):
        tmp = UpgradeBusiness(self.driver)
        result = tmp.web_factory_reset(host,user,pwd)
        time.sleep(60)
        #关掉下次显示，并关闭设置向导
        tmp1 = SWBusiness(self.driver)
        tmp1.hidenexttime()
        tmp1.close_wizard()
        #设置系统系统日志的地址
        tmp.syslog_uri()
        return result

    #解除最后n个slave AP的配对
    def unpair_last_slave_ap(self,n):
        ##解除最后一个slave AP的配对
        unpair = APSBusiness(self.driver)
        #点击接入点
        unpair.APS_menu()
        for i in range(n):
            #点击最后一个设备的删除配对
            unpair.delete_last_paired_device()
            #弹出的提示窗口中，点击确认
            unpair.notice_ok()
            time.sleep(180)
        print "unpair the last %s slave ap successfully!"%n


    #解除特定slave AP的配对
    def unpair_special_slave_AP(self,slave_mac):
        #unpair特定的设备
        unpair = APSBusiness(self.driver)
        #点击接入点
        unpair.APS_menu()
        unpair.unpair_special_AP(slave_mac)
        #弹出的提示窗口中，点击确认
        unpair.notice_ok()
        time.sleep(180)
        print "unpair the slave ap:%s successfully!"%slave_mac

    #解除特定slave AP的配对
    def unpair_special_slave_AP_backup(self,slave_mac):
        #unpair特定的设备
        unpair = APSBusiness(self.driver)
        #点击接入点
        unpair.APS_menu()
        unpair.unpair_special_AP_backup3(slave_mac)
        #弹出的提示窗口中，点击确认
        unpair.notice_ok()
        time.sleep(180)
        print "unpair the slave ap:%s successfully!"%slave_mac

    #解除一个slave AP的配对,并登录路由后台去判断是否解除成功！
    def step_001_unpair_last(self,host,user,pwd,slave_mac):
        #解除特定slave AP的配对
        APSBusiness.unpair_special_slave_AP(self,slave_mac)
        #调用ssh登录ap后台，输入ubus call controller.discovery get_paired_devices
        #判断是否还有slave ap的mac
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"ubus call controller.discovery get_paired_devices")
        #mac地址去冒号
        sm1 = slave_mac.lower()
        m1 = APSControl.mac_drop(self,sm1)
        print result,m1
        if m1 in result :
            return False
        else:
            return True

    #搜索AP并判断，是否正确
    def search_AP(self,slave_mac1,slave_mac2):
        #点击接入点
        APSControl.APS_menu(self)
        #点击搜索
        APSControl.discover_AP(self)
        #获取搜索到的设备的mac
        result = APSControl.get_slave_mac(self)
        #slave ap的mac转换为大写
        MAC1 = slave_mac1.upper()
        MAC2 = slave_mac2.upper()
        print MAC1,MAC2,result
        if (MAC1 in result) and (MAC2 in result):
            return True
        else:
            return False

    #搜索AP并判断，是否正确--backup
    def search_AP_backup(self,slave_mac):
        #点击接入点
        APSControl.APS_menu(self)
        #点击搜索
        APSControl.discover_AP(self)
        time.sleep(60)
        #获取搜索到的设备的mac
        result = APSControl.get_slave_mac(self)
        #关闭搜索设备窗口
        APSControl.close_search_AP(self)
        #slave ap的mac转换为大写
        MAC1 = slave_mac.upper()
        print MAC1,result
        if MAC1 in result:
            return True
        else:
            return False


    #两个slave ap时，搜索AP并配对
    def search_pair_AP(self,slave_mac1,slave_mac2):
        #点击接入点
        APSControl.APS_menu(self)
        #点击搜索
        APSControl.discover_AP(self)
        #只发现的两个设备时，点击配对
        APSControl.pair_AP(self,slave_mac1)
        time.sleep(60)
        APSControl.pair_AP(self,slave_mac2)
        time.sleep(60)
        #关闭搜索设备窗口
        APSControl.close_search_AP(self)
        print "search and pair slave ap successfully!"

    #两个slave ap时，搜索AP并配对并判断是否配对成功
    def check_search_pair_AP(self,host,user,pwd,slave_mac1,slave_mac2):
        #两个slave ap时，搜索AP并配对
        APSBusiness.search_pair_AP(self,slave_mac1,slave_mac2)
        #调用ssh登录ap后台，输入ubus call controller.discovery get_paired_devices
        #判断是否还有slave ap的mac
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"ubus call controller.discovery get_paired_devices")
        #mac地址去冒号
        sm1 = slave_mac1.lower()
        sm2 = slave_mac2.lower()
        m1 = APSControl.mac_drop(self,sm1)
        m2 = APSControl.mac_drop(self,sm2)
        print result,m1,m2
        if (m1 in result) and (m2 in result):
            return True
        else:
            return False

    #多个slave ap时，搜索并配对特定的ap
    def search_pair_special_AP(self,slave_mac):
        #点击接入点
        APSControl.APS_menu(self)
        #点击搜索
        APSControl.discover_AP(self)
        APSControl.pair_AP(self,slave_mac)
        time.sleep(60)
        #关闭搜索设备窗口
        APSControl.close_search_AP(self)
        print "search and pair slave ap successfully!"

    #登录后台，判断slave ap是否配对成功
    def check_slave_ap_pair(self,host,user,pwd,slave_mac):
        #调用ssh登录ap后台，输入ubus call controller.discovery get_paired_devices
        #判断是否还有slave ap的mac
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"ubus call controller.discovery get_paired_devices")
        #mac地址去冒号
        sm1 = slave_mac.lower()
        m1 = APSControl.mac_drop(self,sm1)
        print result,m1
        if m1 in result:
            return True
        else:
            return False

    #多个slave ap时，搜索AP并配对并判断是否配对成功
    def check_search_pair_special_AP(self,host,user,pwd,slave_mac):
        #多个slave ap时，搜索并配对特定的ap
        APSBusiness.search_pair_special_AP(self,slave_mac)
        #登录后台，判断slave ap是否配对成功
        result = APSBusiness.check_slave_ap_pair(self,host,user,pwd,slave_mac)
        return result



    #搜索-配对-加入网络组
    def search_pair_add_default(self,mac):
        pair = APSBusiness(self.driver)
        #点击接入点
        pair.APS_menu()
        #点击搜索
        pair.discover_AP()
        #点击配对
        pair.pair_AP(mac)
        time.sleep(60)
        #关闭搜索设备窗口
        pair.close_search_AP()
        print "search,pair ap:%s successfully!"%mac


    #多个网络组时，搜索-配对-加入SSIDs
    def search_pair_add(self,n,mac):
        pair = APSBusiness(self.driver)
        #点击接入点
        pair.APS_menu()
        #点击搜索
        pair.discover_AP()
        #只发现的一个设备时，点击配对
        pair.pair_AP(mac)
        time.sleep(60)
        #关闭搜索设备窗口
        pair.close_search_AP()
        #选中最后一个设备
        pair.check_last_AP()
        #点击添加到SSIDs按钮
        pair.add_Networks_Groups()
        #添加网络组中，有多个网络组时，选择特定的一个网络组
        pair.check_special_group(n)
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()
        print "ap:%s search,pair and add to SSID:%s successfully!"%(mac,n)


    #多个网络组时，搜索-配对-所有ap加入特定网络组
    def search_pair_add_manyap(self,n,mac):
        pair = APSBusiness(self.driver)
        #点击接入点
        pair.APS_menu()
        #点击搜索
        pair.discover_AP()
        #只发现的一个设备时，点击配对
        pair.pair_AP(mac)
        time.sleep(60)
        #关闭搜索设备窗口
        pair.close_search_AP()
        #选中所有设备
        pair.check_all_AP()
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，有多个网络组时，选择特定的一个网络组
        pair.check_special_group(n)
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()



    #多个网络组时，所有ap加入所有网络组，然后加入默认的网络组
    def add_manyap_to_allNG(self,n):
        pair = APSBusiness(self.driver)
        #点击接入点
        pair.APS_menu()
        #选中所有设备
        pair.check_all_AP()
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，有多个网络组时，选择所有网络组
        pair.check_all_Networks_Groups()
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()
        #time.sleep(60)
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，有多个网络组时，选择特定的一个网络组
        pair.check_special_group(n)
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()


    #将master ap加入特定的网络组
    def add_master_to_n_NG(self,n):
        #点击接入点
        APSControl.APS_menu(self)
        #选中master
        APSControl.check_special_AP(self,data_AP['master:mac'])
        #点击添加到网络组按钮
        APSControl.add_Networks_Groups(self)
        #添加网络组中，有多个网络组时，选择特定的一个网络组
        APSControl.check_special_group(self,n)
        #添加网络组中，点击保存
        APSControl.save_Networks_Groups(self)
        #弹出窗口中，点击应用
        APSControl.apply(self)



    #将master ap加入所有的网络组
    def add_master_to_all_NG(self):
        #点击接入点
        APSControl.APS_menu(self)
        #选中master
        APSControl.check_special_AP(self,data_AP['master:mac'])
        #点击添加到网络组按钮
        APSControl.add_Networks_Groups(self)
        #添加网络组中，点击全选
        APSControl.check_all_Networks_Groups(self)
        #添加网络组中，点击保存
        APSControl.save_Networks_Groups(self)
        #弹出窗口中，点击应用
        APSControl.apply(self)





    #将master ap加入默认网络组--不点击选择
    def add_master_to_gourp0(self):
        #点击添加到网络组按钮
        APSControl.add_Networks_Groups(self)
        #加入默认网络组
        APSControl.check_special_group(self,1)
        #添加网络组中，点击保存
        APSControl.save_Networks_Groups(self)
        #弹出窗口中，点击应用
        APSControl.apply(self)


    #搜索-配对-slave加入所有的网络组
    def search_pair_add_to_all_NG(self,mac):
        pair = APSBusiness(self.driver)
        #点击接入点
        pair.APS_menu()
        #点击搜索
        pair.discover_AP()
        #只发现的一个设备时，点击配对
        pair.pair_AP(mac)
        #关闭搜索设备窗口
        pair.close_search_AP()
        time.sleep(60)
        #选中最后一个设备
        pair.check_last_AP()
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，点击全选
        pair.check_all_Networks_Groups()
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()




    #slave加入所有的网络组
    def add_slave_to_all_NG(self):
        pair = APSControl(self.driver)
        #点击接入点
        pair.APS_menu()
        #选中最后一个设备
        pair.check_last_AP()
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，点击全选
        pair.check_all_Networks_Groups()
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()


    #slave加入特定网络组
    def add_slave_to_NG(self,mac,n):
        pair = APSControl(self.driver)
        #点击接入点
        pair.APS_menu()
        #选中特定的设备
        pair.check_special_AP(mac)
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，加入特定网络组
        pair.check_special_group(n)
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()
        print "the slave ap:%s add to network group:%s successfully!"%(mac,n)

    #特定的slave加入所有的网络组
    def add_special_slave_to_all_NG(self,mac):
        pair = APSControl(self.driver)
        #点击接入点
        pair.APS_menu()
        #选中特定的设备
        pair.check_special_AP(mac)
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，点击全选
        pair.check_all_Networks_Groups()
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()
        time.sleep(10)
        print "the slave ap:%s add to all network groups successfully!"%mac


    #没有配对的slave ap，先设置固件升级方式，然后搜索AP并配对然后升级slave ap的固件(2台slave ap)
    def upgrade_slave_ap(self,host,host2,user,pwd,version,addr,mode,slave_mac,slave_mac2):
        #先设置固件升级方式
        tmp = UpgradeBusiness(self.driver)
        tmp.set_upgrade_mode(addr,mode)

        #搜索AP并配对
        APSBusiness.search_pair_AP(self,slave_mac,slave_mac2)
        #选中所有的设备
        APSControl.check_all_AP(self)
        #点击升级按钮
        APSControl.upgrade(self)
        #升级的提升窗口中点击“逐个升级”
        APSControl.one_by_one_upgrade(self)
        time.sleep(900)
        print "After search and pair slave ap,upgrade slave ap FW successfully!"
        #ping AP的ip，ping通返回0
        result1 = APSControl.get_ping(self,host)
        #登录AP后台取出版本号
        result2 = APSControl.get_router_version(self,host,user,pwd)
        print result1,result2
        #ping AP的ip，ping通返回0
        result3 = APSControl.get_ping(self,host2)
        #登录AP后台取出版本号
        result4 = APSControl.get_router_version(self,host2,user,pwd)
        if (result1 == 0) and (version in result2) and \
            (result3 == 0) and (version in result4):
            return True
        else:
            return False

    #搜索-配对-重启slave ap
    def reboot_slave_ap(self,slave_mac):
        #搜索AP并配对
        APSBusiness.search_pair_special_AP(self,slave_mac)
        # #关闭搜索设备窗口
        # APSControl.close_search_AP(self)
        #选中最后一个设备
        APSControl.check_last_AP(self)
        #点击重启按钮
        APSControl.reboot(self)
        #弹出的提示窗口中，点击确认
        APSControl.notice_ok(self)
        time.sleep(180)

    #重启the last slave ap
    def reboot_slave_ap1(self):
        tmp = APSControl(self.driver)
        #点击接入点
        tmp.APS_menu()
        #选中最后一个设备
        tmp.check_last_AP()
        #点击重启按钮
        tmp.reboot()
        #弹出的提示窗口中，点击确认
        tmp.notice_ok()
        time.sleep(180)
        print "reboot the last slave ap successfully!"

    #重启the last slave ap--backup
    def reboot_slave_ap1_backup(self):
        tmp = APSControl(self.driver)
        #点击接入点
        tmp.APS_menu()
        #选中最后一个设备
        tmp.check_last_AP()
        #点击重启按钮
        tmp.reboot()
        #弹出的提示窗口中，点击确认
        tmp.notice_ok()
        time.sleep(30)
        tmp.notice_ok()


    #已配对完成的slave ap，先设置固件升级方式，然后升级slave ap的固件
    def downgrade_slave_ap(self,host,user,pwd,version,addr,mode):
        #先设置固件升级方式
        tmp = UpgradeBusiness(self.driver)
        tmp.set_upgrade_mode(addr,mode)
        #搜索AP并配对
        #APSBusiness.search_pair_AP(self)
        #关闭搜索设备窗口
        #APSControl.close_search_AP(self)
        #选中最后一个设备
        APSControl.check_last_AP(self)
        #点击升级按钮
        APSControl.upgrade(self)
        #弹出的提示窗口中，点击确认
        APSControl.notice_ok(self)
        tmp.confirm_AP_upgrade_finish(host,user,pwd,version)
        #ping AP的ip，ping通返回0
        result1 = APSControl.get_ping(self,host)
        #登录AP后台取出版本号
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"cat /tmp/gs_version")
        print result1,result2
        if (result1 == 0) and (version in result2):
            return True
        else:
            return False


    #添加slave ap到新建的ssid
    def slave_add_NG(self,host,user,pwd,n,slave_mac,NG_ssid,NG_key):
        #新建的网络组NG2
        tmp = SSIDBusiness(self.driver)
        tmp.new_ssid(NG_ssid,NG_key)
        #点击接入点
        APSControl.APS_menu(self)
        #选中特定的设备
        APSControl.check_special_AP(self,slave_mac)
        #点击添加到网络组按钮
        APSControl.add_Networks_Groups(self)
        #添加网络组中，有多个网络组时，选择特定的一个网络组
        APSControl.check_special_group(self,n)
        #添加网络组中，点击保存
        APSControl.save_Networks_Groups(self)
        #弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(60)
        #mac地址去冒号
        sm = slave_mac.lower()
        m = APSControl.mac_drop(self,sm)
        #调用ssh登录ap后台，输入uci show grandstream.000b82978fd0.zones
        #判断是否还有slave ap的mac
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show grandstream.%s.zones"%m)
        print "zone%s"%(n-2),result
        if "zone%s"%(n-2) in result:
            return True
        else:
            return False

    #########################################################
    ################以下是编辑窗口的操作#########################
    ##########################################################
    #点击编辑，并进入用户页面
    def edit_users_menu(self,mac):
        #点击接入点
        APSControl.APS_menu(self)
        #编辑特定的设备
        APSControl.edit_special_AP(self,mac)
        ##在编辑窗口点击用户菜单
        APSControl.click_users(self)

    #点击编辑，并进入配置页面
    def edit_config_menu(self,mac):
        #点击接入点
        APSControl.APS_menu(self)
        #编辑特定的设备
        APSControl.edit_special_AP(self,mac)
        ##在编辑窗口点击配置菜单
        APSControl.click_config(self)

    #点击编辑，并进入用户页面--备份
    def edit_users_menu_backup(self,n):
        #点击接入点
        APSControl.APS_menu(self)
        #选择特定的ap，点击编辑
        APSControl.click_edit(self,n)
        ##在编辑窗口点击用户菜单
        APSControl.click_users(self)

    #点击编辑，并进入配置页面--备份
    def edit_config_menu_backup(self,n):
        #点击接入点
        APSControl.APS_menu(self)
        #选择特定的ap，点击编辑
        APSControl.click_edit(self,n)
        ##在编辑窗口点击配置菜单
        APSControl.click_config(self)


    #基本状态信息合法性和准确性检查
    def step_002_check_status(self,host,user,pwd,slave_mac,slave_ip):
        result = []
        #点击接入点
        APSControl.APS_menu(self)
        #编辑特定的设备
        APSControl.edit_special_AP(self,slave_mac)
        #获取设备mac地址
        MAC = APSControl.get_device_mac(self)
        mac = MAC.lower()
        # #获取无线网卡的mac地址
        # wmac = APSControl.get_wlan_mac(self,wlan)
        # wlan_mac = wmac.upper()
        #获取产品型号
        Product_Mode = APSControl.get_device_model(self)
        #获取PN值
        PN = APSControl.get_PN(self)
        #获取引导程序
        Boot_Version = APSControl.get_boot_version(self)
        #获取固件版本
        FW_version = APSControl.get_firmware_version(self)
        #获取IP地址
        IP_addr = APSControl.get_ipaddr(self)
        #获取2.4G用户数量
        usercount2g4 = APSControl.get_usercount2g4(self)
        #获取5G用户数量
        usercount5g = APSControl.get_usercount5g(self)
        # #获取当前时间
        # Current_Time = APSControl.get_curtime(self)
        # #获取运行时间
        # Uptime = APSControl.get_curtime(self)
        # #获取平均负荷
        # Loadaverage = APSControl.get_loadaverage(self)

        # #在编辑窗口点击用户菜单
        # APSControl.click_users(self)
        # #获取所有用户设备mac地址
        # users_mac = APSControl.get_users_mac(self)
        # print users_mac
        #在编辑窗口点击关闭按钮
        APSControl.close_edit(self)
        #登录AP后台取出管理员密码,取出设备状态信息
        ssh = SSH(host,pwd)
        result_ssh = ssh.ssh_cmd(user,'ubus call controller.core status')
        print mac,Product_Mode,PN,Boot_Version,FW_version
        if mac and Product_Mode and PN and Boot_Version and FW_version in result_ssh:
            result.append(True)
        else:
            result.append(False)
        if usercount2g4 and usercount5g == "0":
            result.append(False)
        else:
            result.append(True)

        if slave_ip in IP_addr:
            result.append(True)
        else:
            result.append(False)
        # if wlan_mac in users_mac:
        #     result.append(True)
        # else:
        #     result.append(False)
        print result
        return result

    #MAC信息检查
    def check_client_mac(self,mac,wlan):
        #点击编辑，并进入用户页面
        APSBusiness.edit_users_menu(self,mac)
        #获取所有用户设备mac地址
        users_mac = APSControl.get_users_mac(self)

        #获取无线网卡的mac地址
        wmac = APSControl.get_wlan_mac(self,wlan)
        wlan_mac = wmac.upper()

        if wlan_mac in users_mac:
            return True
        else:
            return False


    #获取设备主机名
    def get_client_names(self,mac):
        #点击编辑，并进入用户页面
        APSBusiness.edit_users_menu(self,mac)
        #获取所有用户设备mac地址
        users_name = APSControl.get_users_name(self)
        APSControl.close_edit(self)
        return users_name

    #判断客户端主机名设置是否正确
    #输入：names：主机名列表
    def check_client_name(self,mac,name,slave_mac):
        #只有一个客户端时，修改客户端名称
        tmp1 = ClientsBusiness(self.driver)
        tmp1.change_client_name(mac,name)
        #获取设备主机名
        time.sleep(40)
        users_name = APSBusiness.get_client_names(self,slave_mac)
        #再将客户端主机名设为空
        tmp1.change_client_name(mac,"")
        print name,users_name
        if name in users_name:
            return True
        else:
            return False

    #修改设备名称
    #输入：n:第几个设备,name:设备名称
    def change_device_name(self,n,name):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,n)
        #设置设备名称
        APSControl.set_device_name(self,name)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        #弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change device name of the %s ap to %s successfully!"%(n,name)



    #判断设置设备名称后设备名称是否正确
    #输入：n:第几个设备,name:设备名称列表
    def check_device_names(self,n,names):
        result = []
        for name in names:
            APSBusiness.change_device_name(self,n,name)
            #获取设备名称/MAC
            tmp = APSControl.get_name_mac(self)
            print name,tmp
            if name in tmp:
                result.append(True)
            else:
                result.append(False)
        #测试完毕清空设备名称
        APSBusiness.change_device_name(self,n,"")
        return result

   #Device name各个页面生效情况验证
    def check_all_device_name(self,ssid,password,wlan,name):
        result = []
        #修改设备名称
        APSBusiness.change_device_name(self,1,name)
        #在接入点页面获取设备名称/MAC
        result1 = APSControl.get_name_mac(self)
        print name,result1
        if name in result1:
            result.append(True)
        else:
            result.append(False)
        APSControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        time.sleep(320)
        APSControl.dhcp_release_wlan(self,wlan)
        #在overview页面获取设备名称
        #点击页面上概览
        tmp1 = OVBusiness(self.driver)
        tmp1.OV_menu()
        #获取设备名称
        result2 = tmp1.get_top()
        print name,result2
        if name in result2:
            result.append(True)
        else:
            result.append(False)
        #在客户端页面获取设备名称
        tmp3 =ClientsBusiness(self.driver)
        mac = tmp3.get_wlan_mac(wlan)
        result4 = tmp3.get_AP_names_no_mac(mac)
        print name,result4
        if name in result4:
            result.append(True)
        else:
            result.append(False)
        #测试完毕清空设备名称
        APSBusiness.change_device_name(self,1,"")
        return result

    #查看勾选fixed ip后，各输入框的状态
    def check_choose_fixed_ip(self,n):
        result = []
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,n)
        #点击勾选固定ip
        APSControl.click_fixed_ip(self)
        #获取固定ip的地址
        ip = APSControl.get_fixed_ip(self)
        #固定ip,子网掩码，网关输入框是否可见
        ip_element = self.driver.find_element_by_id("ipv4_static").is_displayed()
        netmask_element = self.driver.find_element_by_id("ipv4_static_mask").is_displayed()
        gateway_element = self.driver.find_element_by_id("ipv4_route").is_displayed()
        result.extend([ip_element,netmask_element,gateway_element])
        print ip,result
        return ip,result

    #查看取消勾选fixed ip后，各输入框的状态
    def check_cancel_fixed_ip(self,n):
        result = []
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,n)
        #点击勾选固定ip
        APSControl.click_fixed_ip(self)
        #点击取消勾选固定ip
        APSControl.click_fixed_ip(self)
        #获取固定ip的地址
        ip = APSControl.get_fixed_ip(self)
        #固定ip,子网掩码，网关输入框是否可见
        ip_element = self.driver.find_element_by_id("ipv4_static").is_displayed()
        netmask_element = self.driver.find_element_by_id("ipv4_static_mask").is_displayed()
        gateway_element = self.driver.find_element_by_id("ipv4_route").is_displayed()
        result.extend([ip_element,netmask_element,gateway_element])
        print ip,result
        return ip,result

    #勾选fixed ip,输入不合法的地址，检查是否有提示
    def check_ip_legal(self,n,ip,netmask,gateway):
        result = []
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,n)
        #点击勾选固定ip
        APSControl.click_fixed_ip(self)
        #设置固定ip的地址
        APSControl.set_fixed_ip(self,ip)
        #设置固定ip的子网掩码
        APSControl.set_fixed_netmask(self,netmask)
        #设置固定ip的网关
        APSControl.set_fixed_gateway(self,gateway)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = APSControl.check_error(self)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2


    #配置ap的固定ip,并判断正确与否
    def set_ap_fixed_ip(self,slave_mac,ip,netmask,gateway):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,slave_mac)
        #点击勾选固定ip
        APSControl.click_fixed_ip(self)
        #设置固定ip的地址
        APSControl.set_fixed_ip(self,ip)
        #设置固定ip的子网掩码
        APSControl.set_fixed_netmask(self,netmask)
        #设置固定ip的网关
        APSControl.set_fixed_gateway(self,gateway)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        # element = self.driver.find_element_by_id("tip-apply")
        # element.click()
        APSControl.apply(self)
        time.sleep(80)
        print "set the %s ap fixed ip : %s successfully!"%(slave_mac,ip)
        #pc ping指定的ip
        result = subprocess.call('ping %s -c 3'%ip,shell=True)
        if result == 0:
            return True
        else:
            return False

    #配置ap的固定ip,已经勾选了固定ip，不在再次点击
    def set_ap_fixed_ip_backup(self,slave_mac,ip,netmask,gateway):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,slave_mac)
        #设置固定ip的地址
        APSControl.set_fixed_ip(self,ip)
        #设置固定ip的子网掩码
        APSControl.set_fixed_netmask(self,netmask)
        #设置固定ip的网关
        APSControl.set_fixed_gateway(self,gateway)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        # element = self.driver.find_element_by_id("tip-apply")
        # element.click()
        APSControl.apply(self)
        time.sleep(80)
        print "set the %s ap fixed ip : %s successfully!"%(slave_mac,ip)


    #取消配置ap的固定ip
    def cancel_ap_fixed_ip(self,slave_mac,ip):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,slave_mac)
        #点击勾选固定ip
        APSControl.click_fixed_ip(self)
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        # element = self.driver.find_element_by_id("tip-apply")
        # element.click()
        APSControl.apply(self)
        time.sleep(80)
        print "cancel the ap fixed ip : %s successfully!"%ip
        #pc ping指定的ip
        result = subprocess.call('ping %s -c 3'%ip,shell=True)
        if result == 0:
            return True
        else:
            return False

    #设置ap频段，然后使用无线网卡连接判断设置是否成功
    def AP_Freq(self,mode,ssid,password,wlan):
        #切换频段
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_AP_Freq(mode)
        #使用无线网卡连接上AP后，取出该AP的频率值
        result = APSControl.connected_AP_Freq(self,ssid,password,wlan)
        return result
    #
    # #设置ap频段，然后使用无线网卡连接判断设置是否成功
    # def change_AP_Freq(self,mode):
    #     #点击编辑，并进入配置页面
    #     APSBusiness.edit_config_menu(self,data_AP["master:mac"])
    #     #切换频段
    #     APSControl.set_Frequency(self,mode)
    #     #在编辑窗口点击保存
    #     APSControl.click_save(self)
    #     ##弹出窗口中，点击应用
    #     APSControl.apply(self)
    #     #time.sleep(30)
    #     print "set frequency of ap:%s to %s successfully!"%(data_AP["master:mac"],mode)
    #
    # #设置ap频段，然后使用无线网卡连接判断设置是否成功
    # def change_AP_Freq_backup(self,mode):
    #     #点击编辑，并进入配置页面
    #     APSBusiness.edit_config_menu_backup(self,1)
    #     #切换频段
    #     APSControl.set_Frequency(self,mode)
    #     #在编辑窗口点击保存
    #     APSControl.click_save(self)
    #     ##弹出窗口中，点击应用
    #     APSControl.apply(self)
    #     #time.sleep(30)
    #     print "set frequency of ap:%s to %s successfully!"%(data_AP["master:mac"],mode)

    #
    #
    # #设置第几个ap频段
    # def change_n_AP_Freq(self,mac,mode):
    #     #点击编辑，并进入配置页面
    #     APSBusiness.edit_config_menu(self,mac)
    #     #切换频段
    #     APSControl.set_Frequency(self,mode)
    #     #在编辑窗口点击保存
    #     APSControl.click_save(self)
    #     ##弹出窗口中，点击应用
    #     APSControl.apply(self)
    #     print "set frequency of ap:%s to %s successfully!"%(mac,mode)
    #


    #切换2.4g的模式
    def change_2g4_mode(self,host,pwd,n,ssh_user):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换2.4G模式
        APSControl.set_2g4_mode(self,n)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change 2.4G mode of ap:%s  successfully!"%data_AP["master:mac"]
        #登录路由后台取出修改后的结果
        tmp1 = SSH(host,pwd)
        result = tmp1.ssh_cmd(ssh_user,"iwconfig ath0 | grep Bit")
        return result

    #检查5g的模式
    def check_5g_mode(self,host,pwd,ssh_user):
        #登录路由后台取出修改后的结果
        tmp1 = SSH(host,pwd)
        result = tmp1.ssh_cmd(ssh_user,"iwconfig ath0 | grep Bit")
        return result





     #设置master ap的2.4G无线信道
    def set_master_ap_2g4_channel(self,channel):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换2.4G信道
        APSControl.set_2g4_channel(self,channel)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change 2.4G channel of ap:%s to %s successfully!"%(data_AP["master:mac"],channel)

    #设置slave ap的2.4G无线信道
    def set_slave_ap_2g4_channel(self,mac,channel):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        #切换2.4G信道
        APSControl.set_2g4_channel(self,channel)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change 2.4g channel of ap:%s to %s successfully!"%(mac,channel)



    #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
    def check_2g4_channel(self,channel,ssid,password,wlan):
        #设置master ap的2.4G无线信道
        APSBusiness.set_master_ap_2g4_channel(self,channel)
        #使用无线网卡连接上AP后，取出该AP的频率值
        result1 = APSControl.connected_AP_Freq(self,ssid,password,wlan)
        print result1
        return result1

    #设置master ap的5G无线信道
    def set_master_ap_5g_channel(self,channel):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换5G信道
        APSControl.set_5g_channel(self,channel)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change 5g channel of ap:%s to %s successfully!"%(data_AP["master:mac"],channel)

     #设置master ap的5G无线信道
    def set_master_ap_5g_channel_backup(self,channel):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,1)
        #切换5G信道
        APSControl.set_5g_channel(self,channel)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change 5g channel of ap:%s to %s successfully!"%(data_AP["master:mac"],channel)


    #设置slave ap的5G无线信道
    def set_slave_ap_5g_channel(self,mac,channel):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        #切换5G信道
        APSControl.set_5g_channel(self,channel)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change 5g channel of ap:%s to %s successfully!"%(mac,channel)



    #设置master ap的5G无线信道,并登录路由后台获取无线的信息是否设置成功
    def check_5g_channel(self,channel,ssid,password,wlan):
        #设置master ap的5G无线信道
        APSBusiness.set_master_ap_5g_channel(self,channel)
        #使用无线网卡连接上AP后，取出该AP的频率值
        result1 = APSControl.connected_AP_Freq(self,ssid,password,wlan)
        print result1
        return result1

    #检查2.4g的信道
    def check_2g4_channel_backup(self,host,pwd,ssh_user):
        #登录路由后台取出修改后的结果
        tmp1 = SSH(host,pwd)
        result = tmp1.ssh_cmd(ssh_user,"uci show wireless.wifi0.channel")
        return result

    #检查5g的信道
    def check_5g_channel_backup(self,host,pwd,ssh_user):
        #登录路由后台取出修改后的结果
        tmp1 = SSH(host,pwd)
        result = tmp1.ssh_cmd(ssh_user,"uci show wireless.wifi1.channel")
        return result



    #检查2.4g的shortGI是否是灰色和是否被选中
    def check_2g4_shortgi(self):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #检查2.4g的shortGI是否是灰色
        result1 = APSControl.check_2g4_shortgi_disable(self)
        #检查2.4g的shortGI是否被选中
        result2 = APSControl.check_2g4_shortgi_checked(self)
        APSControl.close_edit(self)
        print result1,result2
        return result1,result2

    #检查5g的shortGI是否被选中
    def check_5g_shortgi(self):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #检查5g的shortGI是否被选中
        result = APSControl.check_5g_shortgi_checked(self)
        APSControl.close_edit(self)
        print result
        return result

    #取消2.4g的shortgi
    def cancel_2g4_shortgi(self):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #点击2.4g的短保护间隔
        APSControl.set_2g4_shortgi(self)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "click 2.4G shortGI successfully!"

    #取消5g的shortgi
    def cancel_5g_shortgi(self):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #点击5g的短保护间隔
        APSControl.set_5g_shortgi(self)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "click 5g shortGI successfully!"


    #选择2.4g的激活空间流
    def change_2g4_active_streams(self,stream):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换2.4G的激活空间流
        APSControl.s_2g4_active_streams(self,stream)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change ap 2.4G active stream to %s successfully!"%stream

        #选择2.4g的激活空间流
    def change_2g4_active_streams_backup(self,stream):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,1)
        #切换2.4G的激活空间流
        APSControl.s_2g4_active_streams(self,stream)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change ap 2.4G active stream to %s successfully!"%stream


    #依次选择2.4g的激活空间流后，登录路由后台取出比特流--7610
    def check_2g4_active_streams_7610(self,host,user,pwd):
        result = []
        streams = ["1","2","3"]
        for stream in streams:
            #选择2.4g的激活空间流
            APSBusiness.change_2g4_active_streams_backup(self,stream)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user,"iwconfig ath0 | grep Bit")
            result.append(result1)
        print result
        return result

    #依次选择2.4g的激活空间流后，登录路由后台取出比特流--7600,7600lr,7002w
    def check_2g4_active_streams_7600(self,host,user,pwd):
        result = []
        streams = ["1","2"]
        for stream in streams:
            #选择2.4g的激活空间流
            APSBusiness.change_2g4_active_streams_backup(self,stream)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user,"iwconfig ath0 | grep Bit")
            result.append(result1)
        print result
        return result

    #选择2.4G的无线功率
    def set_2g4_power(self,power):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换2.4G的无线功率
        APSControl.s_2g4_power(self,power)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change ap 2.4G power to %s successfully!"%power

    #选择2.4G的无线功率
    def set_2g4_power_backup(self,power):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,1)
        #切换2.4G的无线功率
        APSControl.s_2g4_power(self,power)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(40)
        print "change ap 2.4G power to %s successfully!"%power

    #依次选择2.4G的无线功率后，登录路由后台取出功率值
    def check_2g4_power(self,host,user,pwd):
        result = []
        powers = ["0","1","2"]
        for power in powers:
            #选择2.4G的无线功率
            APSBusiness.set_2g4_power_backup(self,power)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user,"iwconfig ath0 | grep Tx-Power")
            result2 = int(result1.split("=")[-1].split(" dBm")[0])
            result.append(result2)
        print result
        return result

     #选择5g的激活空间流
    def change_5g_active_streams(self,stream):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换5G的激活空间流
        APSControl.s_5g_active_streams(self,stream)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g active streams to %s successfully!"%stream

     #选择5g的激活空间流
    def change_5g_active_streams_backup(self,stream):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,1)
        #切换5G的激活空间流
        APSControl.s_5g_active_streams(self,stream)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g active streams to %s successfully!"%stream

     #选择5g的激活空间流--slave ap
    def change_slave_5g_active_streams(self,mac,stream):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        #切换5G的激活空间流
        APSControl.s_5g_active_streams(self,stream)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g active streams to %s successfully!"%stream

     #选择5g的激活空间流--slave ap--备份
    def change_slave_5g_active_streams_backup(self,mac,stream):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        #切换5G的激活空间流
        APSControl.s_5g_active_streams_backup(self,stream)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g active streams to %s successfully!"%stream

    #依次选择5g的激活空间流后，登录路由后台取出比特流--7610
    def check_5g_active_streams_7610(self,host,user_ssh,pwd):
        result = []
        streams = ["1","2","3"]
        for stream in streams:
            #选择5g的激活空间流
            APSBusiness.change_5g_active_streams_backup(self,stream)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user_ssh,"iwconfig ath1 | grep Bit")
            result.append(result1)
        print result
        return result

    #依次选择5g的激活空间流后，登录路由后台取出比特流--7600,7600lr,7002w
    def check_5g_active_streams_7600(self,host,user_ssh,pwd):
        result = []
        streams = ["1","2"]
        for stream in streams:
            #选择5g的激活空间流
            APSBusiness.change_5g_active_streams_backup(self,stream)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user_ssh,"iwconfig ath1 | grep Bit")
            result.append(result1)
        print result
        return result

    #选择5G的无线功率
    def set_5g_power(self,power):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换5G的无线功率
        APSControl.s_5g_power(self,power)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g power to %s successfully!"%power

    #选择5G的无线功率
    def set_5g_power_backup(self,power):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,1)
        #切换5G的无线功率
        APSControl.s_5g_power(self,power)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g power to %s successfully!"%power

    #依次选择5G的无线功率后，登录路由后台取出功率值
    def check_5g_power(self,host,user_ssh,pwd):
        result = []
        powers = ["0","1","2"]
        for power in powers:
            #选择5G的无线功率
            APSBusiness.set_5g_power_backup(self,power)
            #time.sleep(180)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user_ssh,"iwconfig ath1 | grep Tx-Power")
            result2 = int(result1.split("=")[-1].split(" dBm")[0])
            result.append(result2)
        print result
        return result

    #改变5G的带宽
    def change_5g_width(self,mode):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #切换5G的无线功率
        APSControl.set_5g_width(self,mode)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "change ap 5g width to %s successfully!"%mode



    #获取所有用户设备数
    def check_users_num(self):
        #点击编辑，并进入用户页面
        APSBusiness.edit_users_menu(self,data_AP["master:mac"])
        result = APSControl.get_users_num(self)
        return result

    #获取搜索AP的text
    def check_get_discover_AP(self):
        #点击接入点
        APSControl.APS_menu(self)
        result = APSControl.get_discover_AP(self)
        return result

     #一起修改5G的带宽和信道
    def change_5g_width_channel(self,mode,channel):
        #点击编辑，并进入配置页面
        APSBusiness.edit_config_menu_backup(self,1)
        #切换5G的无线
        APSControl.set_5g_width(self,mode)
        #切换5G信道
        APSControl.set_5g_channel_backup(self,channel)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        ##弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(60)
        print "change ap 5g width and channel to %s successfully!"%mode


    ###################------以下是failover的方法------########################
    #检查failover按钮的名称
    def check_failover_button_name(self):
        #点击接入点
        APSControl.APS_menu(self)
        #获取故障切换的名称
        result = APSControl.get_failover_name(self)
        return result

    #检查failover按钮的有效性
    def check_failover_button(self):
        #点击接入点
        APSControl.APS_menu(self)
        #点击故障切换
        APSControl.click_failover(self)
        #检查设置故障切换AP的页面是否显示
        result = APSControl.check_failover_AP_webpage(self)
        return result

    #检查所有可选择的failover ap的个数
    def check_failover_AP_num(self,num):
        #点击接入点
        APSControl.APS_menu(self)
        #点击故障切换
        APSControl.click_failover(self)
        #获取所有可选择的failover ap的个数
        result = APSControl.get_failover_AP_num(self)
        #关闭设置故障切换AP页面
        APSControl.close_failover_AP_webpage(self)
        if result == num:
            return True
        else:
            return False

    #确认slave ap的mac是否在failover ap的mac list上
    def check_slave_ap_in_failover_AP(self,slave_mac):
        #点击接入点
        APSControl.APS_menu(self)
        #点击故障切换
        APSControl.click_failover(self)
        #确认slave ap的mac是否在failover ap的mac list上
        result = APSControl.check_slave_ap(self,slave_mac)
        #关闭设置故障切换AP页面
        APSControl.close_failover_AP_webpage(self)
        return result


    #设置slave ap为failover ap
    def change_slave_to_failover(self,failover_mac):
        #点击接入点
        APSControl.APS_menu(self)
        self.driver.refresh()
        self.driver.implicitly_wait(20)
        time.sleep(10)
        #点击故障切换
        APSControl.click_failover(self)
        #选择failover AP
        APSControl.set_failover_AP(self,failover_mac)
        #failover上点击保存
        APSControl.save_failover(self)
        # 弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(90)
        print "Switch slave ap to failover successfully!"

    #登录failover ap的web界面
    def login_failover_ap(self, failover_web, failover_user, pwd):
        #打开slave ap的web页面
        self.driver.get(failover_web)
        self.driver.implicitly_wait(30)
        Lg = LoginBusiness(self.driver)
        #登录GWN7610的web界面
        Lg.login(failover_user,pwd)

    #确认点击切换为master，是否弹出确认提示框
    def check_click_switch_to_master(self):
        #点击接入点
        APSControl.APS_menu(self)
        #点击故障切换
        APSControl.click_failover(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #点击切换为master后取消
    def check_cancel_switch_to_master(self,host,user,pwd):
        #点击接入点
        APSControl.APS_menu(self)
        #点击故障切换
        APSControl.click_failover(self)
        #点击取消
        APSControl.notice_cancel(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        print result1
        time.sleep(60)
        #slave ap依然为failover 模式
        ssh = SSH(host, pwd)
        result2 = ssh.ssh_cmd(user, "uci show controller.main.role")
        result3 = ssh.ssh_cmd(user, "uci show controller.main.failover")
        if ("master" in result2) and ("1" in result3):
            result4 = True
        else:
            result4 = False
        return result1,result4

    #点击切换为master后确认
    def check_ok_switch_to_master(self,host,user,pwd):
        #设置failover ap为master ap
        APSBusiness.change_failover_to_master(self)
        #failover ap  变为master 模式
        ssh = SSH(host, pwd)
        result2 = ssh.ssh_cmd(user, "uci show controller.main.role")
        result3 = ssh.ssh_cmd(user, "uci show controller.main.failover")
        if ("master" in result2) and ("Entry not found" in result3):
            result4 = True
        else:
            result4 = False
        return result4


    #设置failover ap为master ap
    def change_failover_to_master(self):
        #点击接入点
        APSControl.APS_menu(self)
        #点击故障切换
        APSControl.click_failover(self)
        #弹出的提示窗口中，点击确认
        APSControl.notice_ok(self)
        time.sleep(60)
        print "Switch failover ap to master successfully!"

    #failover变为master后，slave加入特定网络组
    def add_slave_to_failover_NG(self,n,mac):
        pair = APSControl(self.driver)
        #点击接入点
        pair.APS_menu()
        #选中特定的设备
        pair.check_special_AP(mac)
        #点击添加到网络组按钮
        pair.add_Networks_Groups()
        #添加网络组中，加入默认网络组
        pair.check_special_group(n)
        #添加网络组中，点击保存
        pair.save_Networks_Groups()
        #弹出窗口中，点击应用
        pair.apply()
        #time.sleep(30)

    #检查slave ap是否变为failover ap
    def check_change_to_failover_AP(self,failover_mac,host,user,pwd):
        #mac地址去掉冒号
        fmac = failover_mac.lower()
        mac = APSControl.mac_drop(self,fmac)
        #检查master ap后台的配置
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show grandstream.%s.failover"%mac.lower())
        print "result = %s"%result
        if "1" in result:
            print "Set failover ap pass!"
            print True
            return True
        else:
            print "Set failover ap fail!"
            print False
            return False

    #切换failover ap为不同的slave ap 3次，然后每次切换后检查slave ap是否变为failover ap
    def check_repeatedly_switch_to_failover_AP(self,slave_mac1,slave_mac2,host,user,pwd):
        result = []
        for i in range(3):
            for mac in [slave_mac1,slave_mac2]:
                #设置slave ap为failover ap
                APSBusiness.change_slave_to_failover(self,mac)
                #检查slave ap是否变为failover ap
                tmp = APSBusiness.check_change_to_failover_AP(self,mac,host,user,pwd)
                result.append(tmp)
            print "test %s time finished!"%i
        print result
        return result




    #确认failover ap和master ap有相同的配置
    def check_check_failover_ap_configuation(self,master_host,failover_host,user,pwd):
        #检查master ap后台,取出配置
        ssh = SSH(master_host,pwd)
        tmp1 = ssh.ssh_cmd(user, "md5sum /etc/config/grandstream")
        master_md5 = tmp1.replace("/etc/config/grandstream", "").strip(" ").strip("\r\n")
        print master_md5
        time.sleep(30)
        #检查failover ap后台,取出配置
        ssh = SSH(failover_host,pwd)
        tmp2 = ssh.ssh_cmd(user, "md5sum /etc/config/grandstream")
        failover_md5 = tmp2.replace("/etc/config/grandstream", "").strip(" ").strip("\r\n")
        print failover_md5
        if master_md5 == failover_md5:
            return True
        else:
            return False

    #master ap关闭controller
    def close_master_controller(self,master_host,user,pwd):
        #master ap后台,关闭controller
        ssh = SSH(master_host,pwd)
        #后台杀掉controller
        ssh.ssh_cmd(user,"/etc/init.d/controller stop")
        print "close master ap controller successfully!"

    #判断failover ap的页面是否能够访问
    #输出：True:不能访问;False:能够访问
    def check_access_failover_webUI(self,failover_web):
        #打开slave ap的web页面
        self.driver.get(failover_web)
        self.driver.implicitly_wait(30)
        #判断登录页面是否有“该设备已配对”的元素
        Lg = LoginBusiness(self.driver)
        result = Lg.web_login_dialog_tip()
        return result

    #开启master ap的controller
    def open_master_controller(self, master_host,user,pwd):
        #master ap后台,开启controller
        ssh = SSH(master_host,pwd)
        #后台启动controller
        ssh.ssh_cmd(user,"/etc/init.d/controller start")
        print "open master ap controller successfully!"

    #判断：failover登录后，ap页面上升级，添加的网络组，配置的按钮都不能点击
    def check_failover_AP_cannot_click_button(self):
        result = []
        #点击接入点
        APSControl.APS_menu(self)
        #升级按钮
        upgrade_element = self.driver.find_element_by_id("oper-upgrade-btn")
        result.append(upgrade_element.get_attribute("disabled"))
        #添加到网络组按钮
        addtozone_element = self.driver.find_element_by_id("oper-addtozone-btn")
        result.append(addtozone_element.get_attribute("disabled"))
        #配置按钮
        config_element = self.driver.find_element_by_id("oper-config-btn")
        result.append(config_element.get_attribute("disabled"))
        print result
        return result




    ###################------以下是Exact Radio Power Configuration的方法------########################
    #设置ap的2.4G的自定义功率值
    #输入：mac，所编辑ap的mac地址;power，输入所要配置的功率至
    def set_ap_2g4_custom_power(self, mac, power):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        # 设置2.4G的自定义发射功率
        APSControl.s_2g4_custom_power(self, power)
        # 在编辑窗口点击保存
        APSControl.click_save(self)
        # 弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(30)
        print "set ap:%s 2.4G custom power is %s successfully!"%(mac,power)

    #得到设置的ap的2.4G的自定义功率值
    def get_ap_2g4_custom_power(self, mac):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        #获取2.4G的自定义发射功率
        result = APSControl.g_2g4_custom_power(self)
        #在编辑窗口点击关闭按钮
        APSControl.close_edit(self)
        return result

    #设置ap的2.4G的自定义功率值，并检查页面上是否配置成功
    def check_ap_2g4_custom_power_webpage(self,mac,powers):
        result = []
        for power in powers:
            #设置ap的2.4G的自定义功率值
            APSBusiness.set_ap_2g4_custom_power(self, mac, power)
            #得到设置的ap的2.4G的自定义功率值
            tmp = APSBusiness.get_ap_2g4_custom_power(self, mac)
            if tmp == power:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #验证设置ap的2.4G的自定义功率值非法时，检查页面上是否会报错
    def check_ap_2g4_custom_power_invalid(self,mac,power):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        # 设置2.4G的自定义发射功率
        APSControl.s_2g4_custom_power(self, power)
        # #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        # result1 = APSControl.check_error(self)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result2
        if result2:
            return True
        else:
            return False

    #验证设置ap的2.4G的自定义功率值非法时，检查页面上是否会报错-backup
    def check_ap_2g4_custom_power_invalid_backup(self,mac,power):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        # 设置2.4G的自定义发射功率
        APSControl.s_2g4_custom_power(self, power)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = APSControl.check_error(self)
        print result1
        if result1 :
            return True
        else:
            return False

    #验证设置ap的2.4G的自定义功率值非法时，检查页面上是否会报错--多次输入检查
    def check_ap_2g4_custom_powers_invalid(self,mac,powers):
        result = []
        for power in powers:
            tmp = APSBusiness.check_ap_2g4_custom_power_invalid(self,mac,power)
            result.append(tmp)
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        return result

    #验证ap的2.4G的自定义功率值--返回True和False的列表
    def check_ap_2g4_custom_power(self,mac, powers,host,user_ssh,pwd):
        result = []
        powers_result = []
        print powers
        for power in powers:
            #设置ap的2.4G的自定义功率值
            APSBusiness.set_ap_2g4_custom_power(self, mac, power)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user_ssh,"iwconfig ath0 | grep Tx-Power")
            a = result1.split("dBm")
            b = a[0].strip(" ").split("=")
            c = b[-1]
            powers_result.append(c)
            if power in c:
                result.append(True)
            else:
                result.append(False)
        print powers
        print powers_result
        print result
        return result

    #验证设置2.4G的发射功率，stream分别选择1,2,3流，指定自定义功率是否正确
    def check_ap_2g4_custom_power_correct(self,power,custom_power,host,user,pwd):
        result = []
        #登录web页面获取DUT的hostname
        DUT_hostname = APSBusiness.get_DUT_hostname(self)
        #设置2.4G的发射功率
        APSBusiness.set_2g4_power(self,power)
        # #设置2.4G的自定义发射功率
        # APSBusiness.set_ap_2g4_custom_power(self, data_AP["master:mac"],
        #     custom_power)
        #根据DUT不同的型号选择对应的stream
        streams1 = ["1","2","3"]
        streams2 = ["1","2"]
        if DUT_hostname == "GWN7610":
            streams = streams1
        elif DUT_hostname == "GWN7600":
            streams = streams2
        elif DUT_hostname == "GWN7600LR":
            streams = streams2
        elif DUT_hostname == "GWN7002W":
            streams = streams2
        print streams
        for stream in streams:
            #选择2.4g的激活空间流
            APSBusiness.change_2g4_active_streams(self,stream)
            ssh = SSH(host,pwd)
            tmp = ssh.ssh_cmd(user,"iwconfig ath0 | grep Bit")
            if custom_power in tmp:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #验证设置2.4G的发射功率，radio power分别选择高中低，指定自定义功率是否正确
    def check_ap_2g4_custom_power_correct_highmediumlow(self,custom_power,host,user,pwd):
        result = []
        powers = ["0", "1", "2"]
        for power in powers:
            #设置2.4G的发射功率
            APSBusiness.set_2g4_power(self,power)
            ssh = SSH(host,pwd)
            tmp = ssh.ssh_cmd(user,"iwconfig ath0 | grep Bit")
            if custom_power in tmp:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #验证2.4G的发射功率是否正确
    def check_2g4_custom_power(self,host,user,pwd,power):
        ssh = SSH(host,pwd)
        tmp = ssh.ssh_cmd(user,"iwconfig ath0 | grep Bit")
        if power in tmp:
            return True
        else:
            return False




    #设置ap的5G的自定义功率值
    #输入：mac，所编辑ap的mac地址;power，输入所要配置的功率至
    def set_ap_5g_custom_power(self,mac, power):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        # 设置5G的自定义发射功率
        APSControl.s_5g_custom_power(self, power)
        # 在编辑窗口点击保存
        APSControl.click_save(self)
        # 弹出窗口中，点击应用
        APSControl.apply(self)
        time.sleep(180)
        print "set ap:%s 5G custom power is %s successfully!"%(mac,power)

    #得到设置的ap的5G的自定义功率值
    def get_ap_5g_custom_power(self, mac):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        #获取5G的自定义发射功率
        result = APSControl.g_5g_custom_power(self)
        #在编辑窗口点击关闭按钮
        APSControl.close_edit(self)
        return result

    #设置ap的5G的自定义功率值，并检查页面上是否配置成功
    def check_ap_5g_custom_power_webpage(self,mac,powers):
        result = []
        for power in powers:
            #设置ap的5G的自定义功率值
            APSBusiness.set_ap_5g_custom_power(self, mac, power)
            #得到设置的ap的5G的自定义功率值
            tmp = APSBusiness.get_ap_5g_custom_power(self, mac)
            if tmp == power:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #验证设置ap的5G的自定义功率值非法时，检查页面上是否会报错
    def check_ap_5g_custom_power_invalid(self,mac,power):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        # 设置5G的自定义发射功率
        APSControl.s_5g_custom_power(self, power)
        self.driver.find_element_by_id("custom_5g_power").send_keys(Keys.PAGE_DOWN)
        # #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        # result1 = APSControl.check_error(self)
        #在编辑窗口点击保存
        APSControl.click_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result2
        if  result2:
            return True
        else:
            return False

    #验证设置ap的5G的自定义功率值非法时，检查页面上是否会报错-backup
    def check_ap_5g_custom_power_invalid_backup(self,mac,power):
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,mac)
        # 设置5G的自定义发射功率
        APSControl.s_5g_custom_power(self, power)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = APSControl.check_error(self)
        print result1
        if result1 :
            return True
        else:
            return False

    #验证设置ap的5G的自定义功率值非法时，检查页面上是否会报错--多次输入检查
    def check_ap_5g_custom_powers_invalid(self,mac,powers):
        result = []
        for power in powers:
            tmp = APSBusiness.check_ap_5g_custom_power_invalid(self,mac,power)
            result.append(tmp)
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        return result

    #验证ap的5G的自定义功率值
    def check_ap_5g_custom_power(self,mac, powers,host,user_ssh,pwd):
        result = []
        powers_result = []
        for power in powers:
            #设置ap的5G的自定义功率值
            APSBusiness.set_ap_5g_custom_power(self,mac, power)
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user_ssh,"iwconfig ath1 | grep Tx-Power")
            a = result1.split("dBm")
            b = a[0].strip(" ").split("=")
            c = b[-1]
            powers_result.append(c)
            if power in c:
                result.append(True)
            else:
                result.append(False)
        print powers
        print powers_result
        print result
        return result

    #验证设置5G的发射功率，stream分别选择1,2,3流，指定自定义功率是否正确
    def check_ap_5g_custom_power_correct(self,power,custom_power,host,user,pwd):
        result = []
        #登录web页面获取DUT的hostname
        DUT_hostname = APSBusiness.get_DUT_hostname(self)
        #设置5G的发射功率
        APSBusiness.set_5g_power(self,power)
        # #设置5G的自定义发射功率
        # APSBusiness.set_ap_5g_custom_power(self, data_AP["master:mac"],
        #     custom_power)
        #根据DUT不同的型号选择对应的stream
        streams1 = ["1","2","3"]
        streams2 = ["1","2"]
        if DUT_hostname == "GWN7610":
            streams = streams1
        elif DUT_hostname == "GWN7600":
            streams = streams2
        elif DUT_hostname == "GWN7600LR":
            streams = streams2
        elif DUT_hostname == "GWN7002W":
            streams = streams2
        print streams
        for stream in streams:
            #选择5g的激活空间流
            APSBusiness.change_5g_active_streams(self,stream)
            ssh = SSH(host,pwd)
            tmp = ssh.ssh_cmd(user,"iwconfig ath1 | grep Bit")
            if custom_power in tmp:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #验证设置5G的发射功率，radio power分别选择高中低，指定自定义功率是否正确
    def check_ap_5g_custom_power_correct_highmediumlow(self,custom_power,host,user,pwd):
        result = []
        powers = ["0", "1", "2"]
        for power in powers:
            #设置5G的发射功率
            APSBusiness.set_5g_power(self,power)
            ssh = SSH(host,pwd)
            tmp = ssh.ssh_cmd(user,"iwconfig ath1 | grep Bit")
            if custom_power in tmp:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

     #验证5G的发射功率是否正确
    def check_5g_custom_power(self,host,user,pwd,power):
        ssh = SSH(host,pwd)
        tmp = ssh.ssh_cmd(user,"iwconfig ath1 | grep Bit")
        if power in tmp:
            return True
        else:
            return False

    ##################以下是fallback IP的方法##################
    #over fallback ip,GWN76xx can  pair and configure
    def fallback_ap_pair_configure(self,fallback_IP,slave_mac,NG_ssid,NG_key,wlan):
        #使用192.168.1.2登录web界面，一.判断是否登录成功
        #打开GWN7610的web页面
        self.driver.get("https://%s"%fallback_IP)
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_basic["super_defalut_pwd"])
        #第一次登录页面需要设置管理员和用户密码
        Lg.set_super_user_pwd(data_login["all"],data_login["all"],\
                              data_login["all"],data_login["all"])
        tmp1 = SWBusiness(self.driver)
        tmp1.hidenexttime()
        tmp1.close_wizard()
        #检测是否登录成功
        result1 = Lg.login_test()
        #搜索AP并判断，是否正确--backup
        result2 = APSBusiness.search_AP_backup(self,slave_mac)
        #多个slave ap时，搜索AP并配对并判断是否配对成功
        result3 = APSBusiness.check_search_pair_special_AP(self,fallback_IP,
            data_basic['sshUser'],data_login['all'],slave_mac)
        #修改ssid和密码
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_wifi_ssid_key(NG_ssid,NG_key)
        result4 = tmp2.connect_WPA_AP_backup(NG_ssid,NG_key,wlan)
        if NG_ssid in result4:
            result41 = True
        else:
            result41 = False
        result = [result1,result2,result3,result41]
        print result
        return result

    #disable fixed ip
    def disable_fixed_ip(self,fallback_IP,master_ip):
        #开启7000的dhcp server
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_ip4_dhcp_server()
        #点击编辑默认网络组
        tmp.edit_button()
        #设置dhcp server的租期时间
        tmp.set_7000_ipv4_dhcp_lease_time("12h")
        #添加窗口中，点击保存
        tmp.add_NG_save()
        tmp.apply()

        #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
        result1 = tmp.check_ap_br_lan0_IP(fallback_IP,
            data_basic['sshUser'], data_login["all"])
        #重启ap
        tmp.reboot_router(fallback_IP, data_basic['sshUser'],
            data_login["all"])
        time.sleep(180)
        #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
        result2 = tmp.check_ap_br_lan0_IP(fallback_IP,
            data_basic['sshUser'], data_login["all"])
        #打开GWN7610的web页面
        self.driver.get("https://%s"%fallback_IP)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login["all"])
        # 点击编辑，并进入配置页面
        APSBusiness.edit_config_menu(self,data_AP["master:mac"])
        #确定固定ip是否勾选
        result3 = APSControl.check_fixed_ip(self)
        #点击勾选固定ip
        APSControl.click_fixed_ip(self)
        APSControl.click_save(self)
        #弹出窗口中，点击应用
        element = self.driver.find_element_by_id("tip-apply")
        element.click()
        time.sleep(80)
        #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
        result4 = tmp.check_ap_br_lan0_IP(master_ip,
            data_basic['sshUser'], data_login["all"])
        result = [result1,result2,result3,result4]
        print result
        return result
