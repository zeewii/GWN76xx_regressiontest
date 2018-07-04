#coding=utf-8
#作者：曾祥卫
#时间：2018.01.22
#描述：GWN76xxssid的业务层

from ssid_control import SSIDControl
from network_group.networkgroup_business import NGBusiness
from connect.ssh import SSH
from selenium import webdriver
from data import data
from login.login_business import LoginBusiness
from selenium.webdriver.common.keys import Keys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from clients.clients_business import ClientsBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
import time

data_basic = data.data_basic()

class SSIDBusiness(SSIDControl):

    def __init__(self,driver):
        #继承SSIDControl类的属性和方法
        SSIDControl.__init__(self,driver)


    ########################################################
    ###############新建ssid################################
    ########################################################
    #新建一个ssid
    def new_ssid(self,ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击添加
        SSIDControl.add_button(self)
        #设置开启ssid
        SSIDControl.set_enable_disable(self)
        #设置ssid
        SSIDControl.set_ssid(self,ssid)
        SSIDControl.wifi_pagedown1(self)
        #设置wpa的密码
        SSIDControl.wifi_wpa_key(self,key)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #新建一个ssid
    def new_ssid_device(self,ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击添加
        SSIDControl.add_button(self)
        #设置开启ssid
        SSIDControl.set_enable_disable(self)
        #设置ssid
        SSIDControl.set_ssid(self,ssid)
        #设置wpa的密码
        SSIDControl.wifi_wpa_key(self,key)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        SSIDControl.add_Available_device_all(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #新建从i到n个ssid
    #作者:蒋甜
    def new_n_ssid(self,i,n,ssid,key):
        while(i<=n):
            ssid_name = ssid + str(i)
            #点击ssid菜单
            SSIDBusiness.SSID_menu(self)
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,ssid_name)
            SSIDControl.wifi_pagedown1(self)
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击保存
            SSIDControl.save(self)
            #弹出窗口中，点击应用
            SSIDControl.apply(self)
            i+=1

     #新建一个ssid，判断界面是否有错误提示
     #作者:蒋甜
    def check_new_ssid_error(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        result = SSIDControl.new_ssid_tips_mesh(self)
        print(result)
        return result

     #新建一个2.4Gssid，判断界面是否有错误提示
     #作者:蒋甜
    def check_new_ssid_2G_error(self,ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击添加
        SSIDControl.add_button(self)
        #设置开启ssid
        SSIDControl.set_enable_disable(self)
        #设置ssid
        SSIDControl.set_ssid(self,ssid)
        #设置频段
        SSIDControl.set_Frequency(self,"2.4GHz")
        #设置wpa的密码
        SSIDControl.wifi_wpa_key(self,key)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        SSIDControl.add_Available_device_all(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        result = SSIDControl.new_ssid_tips(self)
        if result:
            SSIDControl.ssid_cancel(self)
            return True
        else:
            #弹出窗口中，点击应用
            SSIDControl.apply(self)
            return False

    #新建一个带有vlan的ssid
    def new_vlan_ssid(self,ssid,key,VID):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击添加
        SSIDControl.add_button(self)
        #设置开启ssid
        SSIDControl.set_enable_disable(self)
        #设置ssid
        SSIDControl.set_ssid(self,ssid)
        #点击VLAN的勾选
        SSIDControl.set_VLAN(self)
        #输入VLAN ID
        SSIDControl.set_VLANID(self,VID)
        SSIDControl.wifi_pagedown7(self)
        #设置wpa的密码
        SSIDControl.wifi_wpa_key(self,key)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

      #新建一个带有vlan的ssid
    def new_vlan_ssid_device(self,ssid,key,VID):
           #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击添加
        SSIDControl.add_button(self)
        #设置开启ssid
        SSIDControl.set_enable_disable(self)
        #设置ssid
        SSIDControl.set_ssid(self,ssid)
        #点击VLAN的勾选
        SSIDControl.set_VLAN(self)
        #输入VLAN ID
        SSIDControl.set_VLANID(self,VID)
        SSIDControl.wifi_pagedown7(self)
        #设置wpa的密码
        SSIDControl.wifi_wpa_key(self,key)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        SSIDControl.add_Available_device_all(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #删除新建一个ssid
    def del_new_ssid(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #只有一个ssid时，点击删除
        SSIDControl.del_add_ssid(self)
        #弹出的提示窗口中，点击确认
        SSIDControl.notice_ok(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #删除特定的一个ssid
    def del_n_ssid(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，删除特定的一个
        SSIDControl.del_n_button(self,n)
        #弹出的提示窗口中，点击确认
        SSIDControl.notice_ok(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #enable/disable first SSID
    def en_dis_first(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击关闭ssid
        SSIDControl.set_enable_disable(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

       #enable/disable n SSID
    def en_dis_nssid(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.edit_n_Bt(self,n)
        #点击关闭ssid
        SSIDControl.set_enable_disable(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #enable/disable SSID的正常配置
    def check_first_en_dis_status(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        result1 = SSIDControl.get_first_status(self)
        #enable/disable first SSID
        SSIDBusiness.en_dis_first(self)
        result2 = SSIDControl.get_first_status(self)
        return result1,result2


    ########################################################
    ###############修改ssid################################
    ########################################################
    #SSID为空的配置验证
    def check_blank_ssid(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.set_ssid(self,"")
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        #弹出的提示窗口中，点击确认
        SSIDControl.notice_ok(self)
        #点击关闭ssid
        SSIDControl.set_enable_disable(self)
        SSIDControl.set_ssid(self,"")
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        result2 = SSIDControl.get_first_status(self)
        return result1,result2

    #修改第一个ssid的ssid
    def modify_ssid(self,ssid):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.set_ssid(self,ssid)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #修改第一个ssid的ssid和密码
    def change_wifi_ssid_key(self,ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.set_ssid(self,ssid)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi，输入wpa密码
        SSIDControl.wifi_wpa_key(self,key)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "change first ssid and password successfully!"

     #修改第n个ssid的ssid和密码
    def change_n_wifi_ssid_key(self,n,ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.set_ssid(self,ssid)
        #添加窗口中，wifi，输入wpa密码
        SSIDControl.wifi_wpa_key(self,key)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "change first ssid and password successfully!"

    #英文/数字、英文+数字和ASCII标准符号的 SSID 的正常配置
    def check_ssid_config(self,letter_ssid,digital_ssid,digital_letter_ssid,ascii_ssid):
        #修改第一个ssid的ssid
        SSIDBusiness.modify_ssid(self,letter_ssid)
        #获取地一个ssid的名字
        result1 = SSIDControl.get_first_ssid_name(self)
        #修改第一个ssid的ssid
        SSIDBusiness.modify_ssid(self,digital_ssid)
        #获取地一个ssid的名字
        result2 = SSIDControl.get_first_ssid_name(self)
        #修改第一个ssid的ssid
        SSIDBusiness.modify_ssid(self,digital_letter_ssid)
        #获取地一个ssid的名字
        result3 = SSIDControl.get_first_ssid_name(self)
        #修改第一个ssid的ssid
        SSIDBusiness.modify_ssid(self,ascii_ssid)
        #获取地一个ssid的名字
        result4 = SSIDControl.get_first_ssid_name(self)
        return result1,result2,result3,result4

    #检查ssid是否修改成功
    def check_NG_ssid(self,host,user,pwd):
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show wireless.ath0.ssid")
        return result

    #设置第一个ssid是否隐藏
    def set_hide_ssid(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击隐藏/不隐藏SSID
        SSIDControl.hide_ssid(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #隐藏第N个ssid的ssid
    def hide_n_ssid(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #点击隐藏/不隐藏SSID
        SSIDControl.hide_ssid(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        print "click hidden ssid%s's ssid successfully!"%n

    #设置ap频段，然后使用无线网卡连接判断设置是否成功
    def change_AP_Freq(self,mode):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #切换频段
        SSIDControl.set_Frequency(self,mode)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        time.sleep(30)
        print "set frequency of ssid to %s successfully!"%mode

    #设置第n个ssid频段，然后使用无线网卡连接判断设置是否成功
    def change_n_AP_Freq(self,n,mode):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.edit_n_button(self,n)
        #切换频段
        SSIDControl.set_Frequency(self,mode)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        time.sleep(30)
        print "set frequency of ssid to %s successfully!"%mode

    #循环改变n个ssid的频段
    #蒋甜
    def change_n_ssid_Freq(self,i,n,mode):
        while(i<=n):
            #点击ssid菜单
            SSIDBusiness.SSID_menu(self)
            #点击编辑第一个ssid
            SSIDControl.edit_n_Bt(self,i)
            #切换频段
            SSIDControl.set_Frequency(self,mode)
            #添加窗口中，点击保存
            SSIDControl.save(self)
            print "set frequency of ssid to %s successfully!"%mode
            i+=1
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #开启并设置ssid的vlan id
    def enable_vlan_ssid(self,n,VID):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #点击VLAN的勾选
        SSIDControl.set_VLAN(self)
        #输入VLAN ID
        SSIDControl.set_VLANID(self,VID)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

      #关闭ssid的vlan
    def disable_vlan_ssid(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #点击VLAN的勾选
        SSIDControl.set_VLAN(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)


    ########################################################
    ###############无线加密################################
    ########################################################



    #设置第一个ssid无线为非加密
    def wifi_None_encryption(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为不加密
        SSIDControl.wifi_None(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)


    #设置第一个ssid无线为wep加密
    def wifi_wep_encryption(self,n,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式
        SSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi，输入wep密码
        SSIDControl.wifi_wep_key(self,key)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)



    #设置第一个ssid无线为wpa/wpa2加密
    def wifi_wpa_encryption(self,n,m,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        SSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        SSIDControl.wifi_wpa_mode(self,"PSK")
        #添加窗口中，wifi,选择WPA类型
        SSIDControl.wifi_wpa_type(self,m)
        ##添加窗口中，wifi，输入wpa密码
        SSIDControl.wifi_wpa_key(self,key)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)

    #设置第一个ssid无线为802.1x加密
    def wifi_8021x_encryption(self,n,m,addr,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        SSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        SSIDControl.wifi_wpa_mode(self,"802.1x")
        #添加窗口中，wifi,选择WPA类型
        SSIDControl.wifi_wpa_type(self,m)
        #设置radius服务器地址
        SSIDControl.set_radius_server(self,addr)
        #设置radius服务器密钥
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_radius_secret(self,key)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)
        print "set group0 SSID 802.1x encryption successfully!"

     #设置第一个ssid无线为802.1x加密--使用开启强制门户时用到
    def wifi_8021x_encryption_backup(self,n,m,addr,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        SSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        SSIDControl.wifi_wpa_mode(self,"802.1x")
        #添加窗口中，wifi,选择WPA类型
        SSIDControl.wifi_wpa_type(self,m)
        #设置radius服务器地址
        SSIDControl.set_radius_server(self,addr)
        #设置radius服务器密钥
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_radius_secret(self,key)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)
        print "set group0 SSID 802.1x encryption successfully!"


    #输入异常wep密码，是否有提示
    def check_abnormal_wep(self,n,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式
        SSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi，输入wep密码
        SSIDControl.wifi_wep_key(self,key)
        time.sleep(5)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = SSIDControl.check_error(self)
        #点击保存
        SSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2


    ########################################################
    ###############mac地址过滤################################
    ########################################################
    #设置第一个ssid的无线过滤的黑名单
    def wifi_blacklist(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口中，选择第一个黑名单列表
        SSIDControl.set_onemac_blacklist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #设置第一个ssid的无线过滤的黑名单--不选择list
    def wifi_blacklist_backup(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

        #设置第一个ssid的无线过滤的黑名单--不选择list
    def wifi_blacklist_backup1(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown3(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    def wifi_blacklist_backup2(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown6(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)



    #有多个ssid时，设置第n个ssid的无线过滤的黑名单
    def wifi_n_blacklist(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口中，选择第一个黑名单列表
        SSIDControl.set_onemac_blacklist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的黑名单--不点list
    def wifi_n_blacklist_backup(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

        #有多个ssid时，设置第n个ssid的无线过滤的黑名单--不点list
    def wifi_n_blacklist_backup1(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown6(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

        #有多个ssid时，设置第n个ssid的无线过滤的黑名单
    def wifi_n_blacklist_backup2(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
         #添加窗口中，wifi,输入黑名单
        SSIDControl.set_onemac_blacklist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的黑名单--不点list
    def wifi_n_blacklist_backup3(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时,禁用第n个的无线过滤
    def disable_macfilter(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        SSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


       #有多个ssid时,禁用第n个的无线过滤
    def disable_macfilter1(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown6(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        SSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #有多个ssid时,禁用第n个的无线过滤
    def disable_macfilter_backup(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        SSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #有多个ssid时,禁用第n个的无线过滤
    def disable_macfilter_backup2(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        SSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #设置第一个ssid的无线过滤的白名单
    def wifi_whitelist(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #添加窗口中，wifi,输入白名单
        SSIDControl.set_onemac_whitelist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #设置第一个ssid的无线过滤的白名单--不选择list
    def wifi_whitelist_backup(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

        #设置第一个ssid的无线过滤的白名单--不选择list
    def wifi_whitelist_backup1(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown3(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

            #设置第一个ssid的无线过滤的白名单--不选择list
    def wifi_whitelist_backup2(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown6(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)




    #有多个ssid时，设置第n个ssid的无线过滤的白名单
    def wifi_n_whitelist(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
         #添加窗口中，wifi,输入白名单
        SSIDControl.set_onemac_whitelist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)



    #有多个ssid时，设置第n个ssid的无线过滤的白名单--不点list
    def wifi_n_whitelist_backup(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的白名单--不点list
    def wifi_n_whitelist_backup1(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown3(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的白名单
    def wifi_n_whitelist_backup2(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
         #添加窗口中，wifi,输入白名单
        SSIDControl.set_onemac_whitelist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #有多个ssid时，设置第n个ssid的无线过滤的白名单--不点list
    def wifi_n_whitelist_backup3(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #添加N个mac地址过滤白名单，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_white_mac(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        for i in range(n):
            #添加窗口，wifi，添加mac白名单地址输入框
            SSIDControl.set_white_addmac(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #删除所有的mac地址过滤白名单，点击保存应用
    def del_many_white_mac(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口，wifi，删除所有mac地址输入框
        SSIDControl.del_white_addmac(self)
        #取本机无线mac地址
        mac = SSIDControl.get_wlan_mac(self,data_basic["wlan_pc"])

        #添加窗口中，wifi,输入白名单
        element = self.driver.find_element_by_xpath(".//*[@id='whitelistcontent']//input")
        element.clear()
        element.send_keys(mac)

        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #添加N个mac地址过滤黑名单，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_black_mac(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        for i in range(n):
            #添加窗口，wifi，添加mac黑名单地址输入框
            SSIDControl.set_black_addmac(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #删除所有的mac地址过滤黑名单，点击保存应用
    def del_many_black_mac(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #添加窗口，wifi，删除所有mac地址输入框
        SSIDControl.del_black_addmac(self)
        #取本机无线mac地址
        mac = SSIDControl.get_wlan_mac(self,data_basic["wlan_pc"])

        #添加窗口中，wifi,输入白名单
        element = self.driver.find_element_by_xpath(".//*[@id='blacklistcontent']//input")
        element.clear()
        element.send_keys(mac)

        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #登录路由后台，判断mac地址过滤，白名单数目
    def check_mac_list(self,host,user,pwd):
        ssh = SSH(host,pwd)
        tmp = ssh.ssh_cmd(user,"cat /etc/config/grandstream | grep mac")
        tmp1 = tmp.split("\r\n\t")
        result = len(tmp1)-2
        print result
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的白名单,获取mac白名单提示信息
    def get_groupn_wifi_whitelist(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_mac_filter(self,'Whitelist')
        #添加窗口，wifi，mac白名单提示信息
        result = SSIDControl.get_white_mac_info(self)
        SSIDControl.close(self)
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的黑名单,获取mac黑名单提示信息
    def get_groupn_wifi_blacklist(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口，wifi，mac黑名单提示信息
        result = SSIDControl.get_black_mac_info(self)
        SSIDControl.close(self)
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的白名单,列表能显示
    def get_groupn_wifi_whitelist_display(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_mac_filter(self,'Whitelist')
        #添加窗口中，选择白名单,列表能显示
        result = SSIDControl.get_whitelist(self)
        SSIDControl.close(self)
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的黑名单,列表能显示
    def get_groupn_wifi_blacklist_display(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口中，选择黑名单,列表能显示
        result = SSIDControl.get_blacklist(self)
        SSIDControl.close(self)
        return result





     #有多个网络组时,点击第n个网络组的无线过滤的白名单下的第2个列表
    def groupn_wifi_whitelist_twolist(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，选择第二个白名单列表
        SSIDControl.set_twomac_whitelist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个网络组时,点击第n个网络组的无线过滤的黑名单下的第2个列表
    def groupn_wifi_blacklist_twolist(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，选择第二个黑名单列表
        SSIDControl.set_twomac_blacklist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #进入编辑-设备管理，获取已添加设备的名称
    def get_added_device_name(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击ssid0编辑
        SSIDControl.click_first_edit(self)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #获取已添加的设备的名称
        result = SSIDControl.get_Member_Devices_name(self)
        #添加窗口中，点击关闭
        SSIDControl.close(self)
        return result







    ########################################################
    ###############客户端隔离#################################
    ########################################################
    #配置第n个ssid的客户端隔离的网关mac为错误的测试
    def check_wifi_n_isolation_gateway_mac_err(self,n,err_mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown6(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,err_mac)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = SSIDControl.check_error(self)
        time.sleep(5)
        #点击保存
        SSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

     #配置第n个ssid的客户端隔离的网关mac为错误的测试
    def check_wifi_n_isolation_gateway_mac_err_backup(self,n,err_mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        # SSIDControl.wifi_pagedown1(self)
         #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown6(self)
        SSIDControl.click_isolation(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,err_mac)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = SSIDControl.check_error(self)
        time.sleep(5)
        #点击保存
        SSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #配置第n个ssid的客户端隔离的模式--要点击客户端隔离(open加密方式下，无portal)
    def wifi_n_isolation(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown6(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #open加密方式下，配置第n个ssid的客户端隔离的模式--要点击客户端隔离
    def wifi_n_isolation_open(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown3(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #配置第n个ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_backup(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown6(self)
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的模式--点击客户端隔离
    def wifi_n_isolation_backup22(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown3(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_backup2(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown3(self)
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的模式--要点击客户端隔离
    def wifi_n_isolation_backup3(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_backup4(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown1(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的网关mac--要点击客户端隔离
    def wifi_n_isolation_gateway_mac(self,n,mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,mac)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #配置第n个ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_backup(self,n,mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown6(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,mac)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_backup2(self,n,mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown3(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,mac)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_backup3(self,n,mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,mac)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #取消第n个ssid的客户端隔离的模式，不开启portal
    def cancel_wifi_n_isolation(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.click_isolation(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #取消第n个ssid的客户端隔离的模式，开启portal
    def cancel_wifi_n_isolation_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown3(self)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.click_isolation(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #取消第n个ssid的客户端隔离的模式
    def cancel_wifi_n_isolation_backup(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.click_isolation(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #检查客户端隔离的结果
    def check_isolation(self,ssid):
        #无线网卡连接ap
        SSIDControl.connect_NONE_AP(self,ssid,data_basic['wlan_pc'])
        SSIDControl.dhcp_wlan(self,data_basic['wlan_pc'])
        #禁用有线网卡
        SSIDControl.wlan_disable(self,data_basic['lan_pc'])
        #无线ping网关
        result1 = SSIDControl.get_ping(self,data_basic['7000_ip'])
        #无线pingqq
        result2 = SSIDControl.get_ping(self,"180.76.76.76")
        #释放无线网卡ip
        SSIDControl.dhcp_release_wlan(self,data_basic['wlan_pc'])
        #启用有线网卡
        SSIDControl.wlan_enable(self,data_basic['lan_pc'])
        return result1,result2


    ########################################################
    ###############RSSI#####################################
    ########################################################
    #输入最小RSSI值
    def set_rssi(self,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #设置最小RSSI值
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.set_min_rssi(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #设置最小RSSI值，并检查是否正确
    def check_min_rssi(self,value):
        SSIDBusiness.set_rssi(self,value)
         #获取第一个额外rssi的值
        result = SSIDControl.get_first_rssi_value(self)
        print "result = %s"%result
        return result

    #enable/disable RSSI
    def enable_disable_rssi(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown3(self)
        #点击开启RSSI
        SSIDControl.click_rssi(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #enable/disable RSSI
    def enable_disable_rssi_backup(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #点击开启RSSI
        SSIDControl.click_rssi(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #enableRSSI 配置验证并检查
    def check_enable_rssi(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击开启RSSI
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.click_rssi(self)
        #获取默认最小RSSI值
        result1 = SSIDControl.get_min_rssi(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        #获取第一个额外rssi的值
        result2 = SSIDControl.get_first_rssi_value(self)
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #disableRSSI 配置验证并检查
    def check_disable_rssi(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击关闭RSSI
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.click_rssi(self)
        #获取默认最小RSSI值
        result1 = SSIDControl.get_min_rssi(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        #获取第一个额外rssi的状态
        result2 = SSIDControl.get_first_rssi(self)
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #enable rssi,错误Minimum RSSI (dBm)的配置验证
    def check_enable_min_rssi_error(self,err_value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击开启RSSI
        SSIDControl.wifi_pagedown1(self)
        SSIDControl.click_rssi(self)
        #设置最小RSSI值
        SSIDControl.set_min_rssi(self,err_value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = SSIDControl.check_error(self)
        #点击保存
        SSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #disable rssi,错误Minimum RSSI (dBm)的配置验证
    def check_disable_min_rssi_error(self,err_value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown1(self)
        #设置最小RSSI值
        SSIDControl.set_min_rssi(self,err_value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = SSIDControl.check_error(self)
        #点击保存
        SSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        return result1,result2

    #在2分钟内每隔0.5秒检查无线网卡是否一直保持和ap连接
    def check_wifi_client_connected_allthetime(self,wlan):
        result = []
        i = 0
        while (i<120):
            status = SSIDControl.get_client_cmd_result(self,"iw %s link"%wlan)
            result.append(status)
            time.sleep(0.5)
            i = i+0.5
        print "result = %s"%result
        return result


    #删除所有ssid
    def del_all_NG(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        SSIDControl.del_all_button(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #删除所有ssid
    def del_all_NG_backup(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        SSIDControl.del_all_button_backup(self,n)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    #增加到最大的ssid--32个
    def add_SSID_max(self,host,user,pwd,add_ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(31):
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,"%s-%s"%(add_ssid,(i+2)))
            #点击VLAN的勾选
            SSIDControl.set_VLAN(self)
            #输入VLAN ID
            SSIDControl.set_VLANID(self,"%s"%(i+2))
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击保存
            SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        element = self.driver.find_element_by_id("newssid")
        result1 = element.is_enabled()
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show grandstream.ssid31.id")
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

        #增加到最大的ssid--16个
    def add_SSID_max_16(self,host,user,pwd,add_ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(15):
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,"%s-%s"%(add_ssid,(i+2)))
            #点击VLAN的勾选
            SSIDControl.set_VLAN(self)
            #输入VLAN ID
            SSIDControl.set_VLANID(self,"%s"%(i+2))
            SSIDControl.wifi_pagedown7(self)
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击保存
            SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        element = self.driver.find_element_by_id("newssid")
        result1 = element.is_enabled()
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show grandstream.ssid15.id")
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2


         #增加到最大的ssid--16个
    def add_SSID_max_16_device(self,host,user,pwd,add_ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(15):
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,"%s-%s"%(add_ssid,(i+2)))
            #点击VLAN的勾选
            SSIDControl.set_VLAN(self)
            #输入VLAN ID
            SSIDControl.set_VLANID(self,"%s"%(i+2))
            SSIDControl.wifi_pagedown7(self)
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击设备管理
            SSIDControl.add_ssid_device(self)
            #添加窗口中，设备管理，可添加设备，添加所有设备
            SSIDControl.add_Available_device_all(self)
            #添加窗口中，点击保存
            SSIDControl.save(self)
            time.sleep(5)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        element = self.driver.find_element_by_id("newssid")
        result1 = element.is_enabled()
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show grandstream.ssid15.id")
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2


    #增加到最大的ssid--8个
    def add_SSID_8_device(self,add_ssid,key):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(7):
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,"%s-%s"%(add_ssid,(i+2)))
            #点击VLAN的勾选
            SSIDControl.set_VLAN(self)
            #输入VLAN ID
            SSIDControl.set_VLANID(self,"%s"%(i+2))
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击设备管理
            SSIDControl.add_ssid_device(self)
            #添加窗口中，设备管理，可添加设备，添加所有设备
            SSIDControl.add_Available_device_all(self)
            #添加窗口中，点击保存
            SSIDControl.save(self)
            time.sleep(5)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)

    #循环增加ssid
    #作者:蒋甜
    #增加到最大的ssid--16个2.4G
    def add_SSID_16_2G4(self,host,user,pwd,add_ssid,key,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(n):
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,"%s-%s"%(add_ssid,(i+2)))
            #设置ssid的频段
            SSIDControl.set_Frequency(self,"2.4GHz")
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击设备管理
            SSIDControl.add_ssid_device(self)
            #添加窗口中，设备管理，可添加设备，添加所有设备
            SSIDControl.add_Available_device_all(self)
            #添加窗口中，点击保存
            SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        ssh = SSH(host,pwd)
        result1 = ssh.ssh_cmd(user,"uci show grandstream.ssid16.id")
        print "result1 = %s"%result1
        return result1

    #增加到最大的ssid--16个5G
    def add_SSID_16_5G(self,host,user,pwd,add_ssid,key,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(n):
            #点击添加
            SSIDControl.add_button(self)
            #设置开启ssid
            SSIDControl.set_enable_disable(self)
            #设置ssid
            SSIDControl.set_ssid(self,"%s-%s"%(add_ssid,(i+18)))
            #设置ssid的频段
            SSIDControl.set_Frequency(self,"5GHz")
            #设置wpa的密码
            SSIDControl.wifi_wpa_key(self,key)
            #添加窗口中，点击设备管理
            SSIDControl.add_ssid_device(self)
            #添加窗口中，设备管理，可添加设备，添加所有设备
            SSIDControl.add_Available_device_all(self)
            #添加窗口中，点击保存
            SSIDControl.save(self)
        #弹出窗口中，点击应用
        SSIDControl.apply(self)
        element = self.driver.find_element_by_id("newssid")
        result1 = element.is_enabled()
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show grandstream.ssid31.id")
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    ################以下是强制门户认证的方法##################
    #点击开启强制门户
    def click_SSID_portal(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击开启强制门户
        SSIDControl.click_portal(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "click captive portal in SSID successfully!"

    #选择对应的强制门户策略
    def change_SSID_portal_policy(self,m):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #选择对应的强制门户策略
        SSIDControl.set_portal_policy(self,m)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "choose captive portal policy in SSID successfully!"



    #################################################################
    #############设备管理#############################################
    #################################################################
    #将所有已添加的设备删除
    def del_all_ap(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑
        SSIDControl.click_first_edit(self)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #添加窗口中，设备管理，已添加设备，删除所有设备
        SSIDControl.del_Member_device_all(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #将所有可添加的设备添加
    def add_all_ap(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑
        SSIDControl.click_first_edit(self)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        SSIDControl.add_Available_device_all(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)

    ################以下是强制门户认证的方法##################
    #点击开启强制门户
    def click_ssid_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #点击开启强制门户
        SSIDControl.click_portal(self)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "click captive portal in SSID successfully!"

    #点击多个ssid的强制门户
    #输入：n，一共有多少个ssids
    def click_many_group_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        for i in range(n):
            #点击编辑
            SSIDControl.edit_n_button(self,(i+1))
            #点击开启强制门户
            SSIDControl.click_portal(self)
            #点击保存
            SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "click captive portal for many ssids successfully!"


    #选择对应的强制门户策略
    def change_ssid_portal_policy(self,n,m):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #选择对应的强制门户策略
        SSIDControl.set_portal_policy(self,m)
        #添加窗口中，点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        print "choose captive portal policy in SSID successfully!"



    ################以下是客户端时间策略的方法##################

    #选择客户端时间策略
    def change_client_time_policy(self, n, text):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #设置客户端时间策略
        SSIDControl.set_client_time_policy(self,text)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #选择客户端时间策略
    def change_client_time_policy_pagedown(self, n, text):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown1(self)
        #设置客户端时间策略
        SSIDControl.set_client_time_policy(self,text)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    ################以下是客户端数量限制的方法##################
    #作者:蒋甜
    #时间:2018年3月8日

    #设置第n个ssid中的客户端数量number
    def set_wireless_client_limit(self,n,number):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        # 有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #设置客户端数量限制
        SSIDControl.set_wifi_client_limit(self,number)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(5)

    # 客户端数量限制(异常情况判断)
    def set_client_limit_error(self,n,number):
        # 点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        # 点击编辑第一个ssid
        SSIDControl.edit_n_Bt(self,n)
        #给ssid设置客户端数量限制
        SSIDControl.set_wifi_client_limit(self,number)
        # 添加窗口中，点击保存
        SSIDControl.save(self)
        # 判断是否会弹出提示框,有则返回True，没有则返回False
        time.sleep(3)
        element = self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        # 弹出的提示窗口中，点击确认
        # if result1 == True:
        #     print("client limit can not input %s")%number
        #     SSIDControl.notice_ok(self)
        #     SSIDControl.wifi_client_limit_tips(self)
        #     # 点击关闭ssid编辑框
        #
        # else:
        #     #点击应用
        #     SSIDControl.apply(self)
        #     print("client limit input %s successfully!")%number
        return result1

    # 客户端数量限制+勾选portal
    def check_portal_clientlimit(self,n,number):
        # 点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        # 点击编辑第一个ssid
        SSIDControl.edit_n_button(self,n)
        # 点击开启强制门户
        SSIDControl.click_portal(self)
        #给ssid设置客户端数量限制
        SSIDControl.set_wifi_client_limit(self,number)
        # 添加窗口中，点击保存
        SSIDControl.save(self)
        # 判断是否会弹出提示框,有则返回True，没有则返回False
        element = self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        # 弹出的提示窗口中，点击确认
        if result1 == True:
            print("client limit can not input %s")%number
            SSIDControl.notice_ok(self)
            SSIDControl.wifi_client_limit_tips(self)
            # 点击关闭ssid编辑框
            SSIDControl.close(self)
        else:
            #点击应用
            SSIDControl.apply(self)
            time.sleep(5)
            print("client limit input %s successfully!")%number
        return result1

    #登录ssh检查第n个ssid客户端数量是否限制成功
    def check_client_limit(self,host,pwd,user,n,number):
        ssh = SSH(host, pwd)
        n =str(n-1)
        command = "uci show grandstream.ssid%s.wifi_client_limit"%n
        result = ssh.ssh_cmd(user,command)
        result1 = "grandstream.ssid%s.wifi_client_limit='%s'"%(n,number)
        if result1 in result:
            return True
        else:
            return False

      #登录ssh检查第n个接口的客户端数量是否限制成功
    def check_ath_client_limit(self,host,pwd,user,n,number):
        ssh = SSH(host, pwd)
        command = "uci show wireless"
        result = ssh.ssh_cmd(user,command)
        result1 = "wireless.ath%s.maxsta='%s'"%(n,number)
        if result1 in result:
            return True
        else:
            return False

        # 设置第一个ssid无线为802.1x加密,并点击勾选portal按钮
    def wifi_8021x_portal(self, n, m, addr, key):
        # 点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        # 点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        #点击勾选/去勾选portal
        SSIDControl.click_portal(self)
        # 添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        SSIDControl.wifi_n_encryption(self, n)
        # 添加窗口中，wifi,选择WPA密钥模式
        SSIDControl.wifi_wpa_mode(self, "802.1x")
        # 添加窗口中，wifi,选择WPA类型
        SSIDControl.wifi_wpa_type(self, m)
        # 设置radius服务器地址
        SSIDControl.set_radius_server(self, addr)
        #翻页
        SSIDControl.wifi_pagedown1(self)
        # 设置radius服务器密钥
        SSIDControl.set_radius_secret(self, key)
        # 点击保存
        SSIDControl.save(self)
        # 点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)
        print "set group0 SSID 802.1x encryption successfully!"

#取消隐藏ssid,并且添加一个access list，填入一个mac地址,并在ssid中选择这个access list
    def add_accesslist_hide_ssid(self,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        tmp1 = ClientAccessBusiness(self.driver)
        tmp1.clientaccess_menu()
        #点击添加按钮
        tmp1.add_button()
        #在添加窗口输入一个mac地址
        tmp1.set_mac(mac)
        #点击保存
        tmp1.save()
         # 点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        # 点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        # 点击隐藏/不隐藏SSID
        SSIDControl.hide_ssid(self)
        #选择黑白名单
        SSIDControl.wifi_pagedown1(self)
        # 添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self, 'Whitelist')
        # 添加窗口中，wifi,输入白名单
        SSIDControl.set_onemac_whitelist(self)
        # 添加窗口中，点击保存
        SSIDControl.save(self)
        #弹出窗口中，点击应用
        tmp1.apply()

    #多个ssid时，加入特定的ap
    def add_special_ap(self,n,mac):
        # 点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        # 点击编辑第n个ssid
        SSIDControl.edit_n_button(self,n)
        #点击设备管理
        SSIDControl.add_ssid_device(self)
        #点击添加特定的设备
        SSIDControl.add_special_device(self,mac)
        #保存
        SSIDControl.save(self)
        # 点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(10)
        print "add special ap success!"

       #向第n个ssid中加入所有设备
    def n_add_all_ap(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑
        SSIDControl.edit_n_Bt(self,n)
        #添加窗口中，点击设备管理
        SSIDControl.add_ssid_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        SSIDControl.add_Available_device_all(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)
        time.sleep(30)
        time.sleep(10)
        print "add special ap success!"

    #登录设备查看iwconfig内容
    def ssh_iwconfig(self,host,pwd,user):
        ssh = SSH(host, pwd)
        command = "iwconfig"
        result = ssh.ssh_cmd(user,command)
        print result
        return result

    ################以下是频段设置的方法##################
    #作者:蒋甜
    #时间:2018年3月22日

    #登录ssh检查第n个ssid频段是否限制成功
    def check_ssid_band(self,host,pwd,user,n,number):
        ssh = SSH(host, pwd)
        n =str(n-1)
        command = "uci show grandstream.ssid%s.ssid_band"%n
        result = ssh.ssh_cmd(user,command)
        result1 = "grandstream.ssid%s.ssid_band='%s'"%(n,number)
        if result1 in result:
            return True
        else:
            return False

    #登录设备查看iwconfig athn的内容,并判断双频的ssid在其中
    def ssh_iwconfig_ath(self,host,pwd,user,n):
        ssh = SSH(host, pwd)
        command = "iwconfig"+" ath"+str(n)
        result = ssh.ssh_cmd(user,command)
        return result

    #登录设备查看iwconfig athn的内容,并判断ath所处的频段
    def ssh_iwconfig_ath_Fre(self,host,pwd,user,n):
        ssh = SSH(host, pwd)
        command = "iwconfig"+" ath"+str(n)
        result = ssh.ssh_cmd(user,command)
        if "Frequency:2.4" in result:
            return 2
        if "Frequency:5" in result:
            return 5

    #登录设备查看iwconfig athn的内容,并判断ath所处的频段
    def ssh_iwconfig_ath_Fre_ssid(self,host,pwd,user,n,ssid):
        ssh = SSH(host, pwd)
        command = "iwconfig"+" ath"+str(n)
        result = ssh.ssh_cmd(user,command)
        if ("Frequency:2.4" in result) and (ssid in result):
            return 2
        if ("Frequency:5" in result) and (ssid in result):
            return 5
        else:
            return False



##############曾祥卫在2018.6.26,为FP6版本，captive portal用例中################


    #设置第一个ssid的无线过滤的白名单
    def wifi_whitelist_for_portal(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown7(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #添加窗口中，wifi,输入白名单
        SSIDControl.set_onemac_whitelist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的白名单--不点list
    def wifi_n_whitelist_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown7(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)


    def wifi_blacklist_for_portal(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown7(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口中，选择第一个黑名单列表
        SSIDControl.set_onemac_blacklist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的黑名单--不点list
    def wifi_n_blacklist_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown7(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时,禁用第n个的无线过滤
    def disable_macfilter_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown7(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        SSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #open加密方式下，配置第n个ssid的客户端隔离的模式--要点击客户端隔离
    def wifi_n_isolation_open_for_portal(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown7(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_for_portal(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown7(self)
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #配置第n个ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_for_portal(self,n,mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown7(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,mac)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #取消第n个ssid的客户端隔离的模式，开启portal
    def cancel_wifi_n_isolation_portal_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown7(self)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.click_isolation(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #enable/disable RSSI
    def enable_disable_rssi_for_portal(self):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #点击编辑第一个ssid
        SSIDControl.click_first_edit(self)
        SSIDControl.wifi_pagedown7(self)
        #点击开启RSSI
        SSIDControl.click_rssi(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的白名单
    def wifi_n_whitelist_vlan_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown8(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        SSIDControl.set_mac_filter(self,'Whitelist')
         #添加窗口中，wifi,输入白名单
        SSIDControl.set_onemac_whitelist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #有多个ssid时，设置第n个ssid的无线过滤的黑名单
    def wifi_n_blacklist_vlan_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown8(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        SSIDControl.set_mac_filter(self,'Blacklist')
         #添加窗口中，wifi,输入黑名单
        SSIDControl.set_onemac_blacklist(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #有多个ssid时,禁用第n个的无线过滤
    def disable_macfilter_vlan_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown8(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        SSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

     #配置第n个ssid的客户端隔离的模式--要点击客户端隔离
    def wifi_n_isolation_vlan_for_portal(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown8(self)
        SSIDControl.click_isolation(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_vlan_for_portal_no_click_isolation(self,n,value):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.wifi_pagedown8(self)
        #选择客户端隔离模式
        SSIDControl.isolation_mode(self,value)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #配置第n个ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_vlan_for_portal(self,n,mac):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #SSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        SSIDControl.wifi_pagedown8(self)
        SSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        SSIDControl.gateway_mac(self,mac)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #取消第n个ssid的客户端隔离的模式
    def cancel_wifi_n_isolation_vlan_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown8(self)
        #添加窗口中，wifi,点击客户端隔离
        SSIDControl.click_isolation(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)

    #enable/disable RSSI
    def enable_disable_rssi_vlan_for_portal(self,n):
        #点击ssid菜单
        SSIDBusiness.SSID_menu(self)
        #有多个ssid时，选择特定的一个，点击编辑
        SSIDControl.edit_n_button(self,n)
        SSIDControl.wifi_pagedown8(self)
        #点击开启RSSI
        SSIDControl.click_rssi(self)
        #点击保存
        SSIDControl.save(self)
        #点击弹出窗口中的应用
        SSIDControl.apply(self)