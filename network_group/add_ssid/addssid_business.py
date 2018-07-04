#coding=utf-8
#作者：曾祥卫
#时间：2017.03.29
#描述：GWN76xx网络组-额外ssid的业务层


from addssid_control import AddSSIDControl
from network_group.networkgroup_control import NGControl
from connect.ssh import SSH
from selenium import webdriver
from data import data
from login.login_business import LoginBusiness
from selenium.webdriver.common.keys import Keys
import time

data_basic = data.data_basic()

class AddSSIDBusiness(AddSSIDControl):

    def __init__(self,driver):
        #继承AddSSIDControl类的属性和方法
        AddSSIDControl.__init__(self,driver)

    #点击网络组菜单，然后在点击额外ssid菜单
    def NG_SSID_menu(self):
        #点击网络组
        tmp = NGControl(self.driver)
        tmp.NG_menu()
        #点击网络组-额外ssid
        AddSSIDControl.SSID_menu(self)


    ########################################################
    ###############新建额外ssid################################
    ########################################################
    #新建一个额外的ssid
    def new_ssid(self,ssid,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击添加
        AddSSIDControl.add_button(self)
        #设置开启额外ssid
        AddSSIDControl.set_enable_disable(self)
        #设置ssid
        AddSSIDControl.set_ssid(self,ssid)
        #设置wpa的密码
        AddSSIDControl.set_wpa_key(self,key)
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)

    #删除新建一个额外的ssid
    def del_new_ssid(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #只有一个额外ssid时，点击删除
        AddSSIDControl.del_add_ssid(self)
        #弹出的提示窗口中，点击确认
        AddSSIDControl.notice_ok(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)


    #删除特定的一个额外的ssid
    def del_n_ssid(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，删除特定的一个
        AddSSIDControl.del_n_button(self,n)
        #弹出的提示窗口中，点击确认
        AddSSIDControl.notice_ok(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)




    #enable/disable first Additional SSID
    def en_dis_first(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #点击关闭额外ssid
        AddSSIDControl.set_enable_disable(self)
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)



    #enable/disable Additional SSID的正常配置
    def check_first_en_dis_status(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        result1 = AddSSIDControl.get_first_status(self)
        #enable/disable first Additional SSID
        AddSSIDBusiness.en_dis_first(self)
        result2 = AddSSIDControl.get_first_status(self)
        return result1,result2


    ########################################################
    ###############修改ssid################################
    ########################################################
    #SSID为空的配置验证
    def check_blank_ssid(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.set_ssid(self,"")
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        #弹出的提示窗口中，点击确认
        AddSSIDControl.notice_ok(self)
        #点击关闭额外ssid
        AddSSIDControl.set_enable_disable(self)
        AddSSIDControl.set_ssid(self,"")
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)
        result2 = AddSSIDControl.get_first_status(self)
        return result1,result2

    #修改第一个额外ssid的ssid
    def modify_ssid(self,ssid):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.set_ssid(self,ssid)
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)


    #英文/数字、英文+数字和ASCII标准符号的 SSID 的正常配置
    def check_ssid_config(self,letter_ssid,digital_ssid,digital_letter_ssid,ascii_ssid):
        #修改第一个额外ssid的ssid
        AddSSIDBusiness.modify_ssid(self,letter_ssid)
        #获取地一个额外ssid的名字
        result1 = AddSSIDControl.get_first_ssid_name(self)
        #修改第一个额外ssid的ssid
        AddSSIDBusiness.modify_ssid(self,digital_ssid)
        #获取地一个额外ssid的名字
        result2 = AddSSIDControl.get_first_ssid_name(self)
        #修改第一个额外ssid的ssid
        AddSSIDBusiness.modify_ssid(self,digital_letter_ssid)
        #获取地一个额外ssid的名字
        result3 = AddSSIDControl.get_first_ssid_name(self)
        #修改第一个额外ssid的ssid
        AddSSIDBusiness.modify_ssid(self,ascii_ssid)
        #获取地一个额外ssid的名字
        result4 = AddSSIDControl.get_first_ssid_name(self)
        return result1,result2,result3,result4



    #设置第一个额外ssid是否隐藏
    def set_hide_ssid(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #点击隐藏/不隐藏SSID
        AddSSIDControl.hide_ssid(self)
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)


    ########################################################
    ###############无线加密################################
    ########################################################



    #设置第一个额外ssid无线为非加密
    def wifi_None_encryption(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为不加密
        AddSSIDControl.wifi_None(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        time.sleep(30)


    #设置第一个额外ssid无线为wep加密
    def wifi_wep_encryption(self,n,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式
        AddSSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi，输入wep密码
        AddSSIDControl.wifi_wep_key(self,key)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        time.sleep(30)



    #设置第一个额外ssid无线为wpa/wpa2加密
    def wifi_wpa_encryption(self,n,m,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        AddSSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        AddSSIDControl.wifi_wpa_mode(self,"PSK")
        #添加窗口中，wifi,选择WPA类型
        AddSSIDControl.wifi_wpa_type(self,m)
        ##添加窗口中，wifi，输入wpa密码
        AddSSIDControl.wifi_wpa_key(self,key)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        time.sleep(30)

    #设置第一个额外ssid无线为802.1x加密
    def wifi_8021x_encryption(self,n,m,addr,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        AddSSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        AddSSIDControl.wifi_wpa_mode(self,"802.1x")
        #添加窗口中，wifi,选择WPA类型
        AddSSIDControl.wifi_wpa_type(self,m)
        #设置radius服务器地址
        AddSSIDControl.set_radius_server(self,addr)
        #设置radius服务器密钥
        AddSSIDControl.set_radius_secret(self,key)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        time.sleep(30)
        print "set group0 additional ssid 802.1x encryption successfully!"

     #设置第一个额外ssid无线为802.1x加密--使用开启强制门户时用到
    def wifi_8021x_encryption_backup(self,n,m,addr,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        AddSSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        AddSSIDControl.wifi_wpa_mode(self,"802.1x")
        #添加窗口中，wifi,选择WPA类型
        AddSSIDControl.wifi_wpa_type(self,m)
        #设置radius服务器地址
        AddSSIDControl.set_radius_server(self,addr)
        #设置radius服务器密钥
        AddSSIDControl.wifi_pagedown2(self)
        AddSSIDControl.set_radius_secret(self,key)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        time.sleep(30)
        print "set group0 additional ssid 802.1x encryption successfully!"


    #输入异常wep密码，是否有提示
    def check_abnormal_wep(self,n,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择wifi的安全模式
        AddSSIDControl.wifi_n_encryption(self,n)
        #添加窗口中，wifi，输入wep密码
        AddSSIDControl.wifi_wep_key(self,key)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = AddSSIDControl.check_error(self)
        #点击保存
        AddSSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2


    ########################################################
    ###############mac地址过滤################################
    ########################################################
    #设置第一个额外ssid的无线过滤的黑名单
    def wifi_blacklist(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        AddSSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口中，选择第一个黑名单列表
        AddSSIDControl.set_onemac_blacklist(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #设置第一个额外ssid的无线过滤的黑名单--不选择list
    def wifi_blacklist_backup(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        AddSSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)



    #有多个额外ssid时，设置第n个额外ssid的无线过滤的黑名单
    def wifi_n_blacklist(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        AddSSIDControl.set_mac_filter(self,'Blacklist')
        #添加窗口中，选择第一个黑名单列表
        AddSSIDControl.set_onemac_blacklist(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #有多个额外ssid时，设置第n个额外ssid的无线过滤的黑名单--不点list
    def wifi_n_blacklist_backup(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        AddSSIDControl.set_mac_filter(self,'Blacklist')
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #有多个额外ssid时,禁用第n个的无线过滤
    def disable_macfilter(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        AddSSIDControl.set_mac_filter(self,'Disable')
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)



    #设置第一个额外ssid的无线过滤的白名单
    def wifi_whitelist(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        AddSSIDControl.set_mac_filter(self,'Whitelist')
        #添加窗口中，wifi,输入白名单
        AddSSIDControl.set_onemac_whitelist(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #设置第一个额外ssid的无线过滤的白名单--不选择list
    def wifi_whitelist_backup(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        AddSSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)



    #有多个额外ssid时，设置第n个额外ssid的无线过滤的白名单
    def wifi_n_whitelist(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        AddSSIDControl.set_mac_filter(self,'Whitelist')
         #添加窗口中，wifi,输入白名单
        AddSSIDControl.set_onemac_whitelist(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)



    #有多个额外ssid时，设置第n个额外ssid的无线过滤的白名单--不点list
    def wifi_n_whitelist_backup(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        AddSSIDControl.set_mac_filter(self,'Whitelist')
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #添加N个mac地址过滤白名单，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_white_mac(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        for i in range(n):
            #添加窗口，wifi，添加mac白名单地址输入框
            AddSSIDControl.set_white_addmac(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #删除所有的mac地址过滤白名单，点击保存应用
    def del_many_white_mac(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口，wifi，删除所有mac地址输入框
        AddSSIDControl.del_white_addmac(self)
        #取本机无线mac地址
        mac = AddSSIDControl.get_wlan_mac(self,data_basic["wlan_pc"])

        #添加窗口中，wifi,输入白名单
        element = self.driver.find_element_by_xpath(".//*[@id='whitelistcontent']//input")
        element.clear()
        element.send_keys(mac)

        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #添加N个mac地址过滤黑名单，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_black_mac(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        for i in range(n):
            #添加窗口，wifi，添加mac黑名单地址输入框
            AddSSIDControl.set_black_addmac(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #删除所有的mac地址过滤黑名单，点击保存应用
    def del_many_black_mac(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口，wifi，删除所有mac地址输入框
        AddSSIDControl.del_black_addmac(self)
        #取本机无线mac地址
        mac = AddSSIDControl.get_wlan_mac(self,data_basic["wlan_pc"])

        #添加窗口中，wifi,输入白名单
        element = self.driver.find_element_by_xpath(".//*[@id='blacklistcontent']//input")
        element.clear()
        element.send_keys(mac)

        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #登录路由后台，判断mac地址过滤，白名单数目
    def check_mac_list(self,host,user,pwd):
        ssh = SSH(host,pwd)
        tmp = ssh.ssh_cmd(user,"cat /etc/config/grandstream | grep mac")
        tmp1 = tmp.split("\r\n\t")
        result = len(tmp1)-2
        print result
        return result



    #非法的 mac 地址格式的输入验证--whitelist
    def check_abnormal_mac_white(self,abnormal_mac):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.set_mac_filter(self,'Whitelist')
        #添加窗口中，wifi,输入白名单
        AddSSIDControl.set_mac_whitelist(self,abnormal_mac)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = AddSSIDControl.check_error(self)
        #点击保存
        AddSSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2




    ########################################################
    ###############客户端隔离#################################
    ########################################################
    #配置第n个额外ssid的客户端隔离的网关mac为错误的测试
    def check_wifi_n_isolation_gateway_mac_err(self,n,err_mac):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        AddSSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        AddSSIDControl.gateway_mac(self,err_mac)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = AddSSIDControl.check_error(self)
        #time.sleep(20)
        #点击保存
        AddSSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #配置第n个额外ssid的客户端隔离的模式--要点击客户端隔离
    def wifi_n_isolation(self,n,value):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式
        AddSSIDControl.isolation_mode(self,value)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #配置第n个额外ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_backup(self,n,value):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.isolation_mode(self,value)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)

    #配置第n个额外ssid的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_backup2(self,n,value):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        AddSSIDControl.wifi_pagedown3(self)
        AddSSIDControl.isolation_mode(self,value)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #配置第n个额外ssid的客户端隔离的网关mac--要点击客户端隔离
    def wifi_n_isolation_gateway_mac(self,n,mac):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        AddSSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        AddSSIDControl.gateway_mac(self,mac)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #配置第n个额外ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_backup(self,n,mac):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        AddSSIDControl.gateway_mac(self,mac)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)

    #配置第n个额外ssid的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_backup2(self,n,mac):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        #添加窗口中，wifi,点击客户端隔离
        #AddSSIDControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        AddSSIDControl.wifi_pagedown3(self)
        AddSSIDControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        AddSSIDControl.gateway_mac(self,mac)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #取消第n个额外ssid的客户端隔离的模式
    def cancel_wifi_n_isolation(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        self.driver.refresh()
        time.sleep(5)
        #有多个额外ssid时，选择特定的一个，点击编辑
        AddSSIDControl.edit_n_button(self,n)
        AddSSIDControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        AddSSIDControl.click_isolation(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #检查客户端隔离的结果
    def check_isolation(self,ssid):
        #无线网卡连接ap
        AddSSIDControl.connect_NONE_AP(self,ssid,data_basic['wlan_pc'])
        AddSSIDControl.dhcp_wlan(self,data_basic['wlan_pc'])
        #禁用有线网卡
        AddSSIDControl.wlan_disable(self,data_basic['lan_pc'])
        #无线ping网关
        result1 = AddSSIDControl.get_ping(self,data_basic['7000_ip'])
        #无线pingqq
        result2 = AddSSIDControl.get_ping(self,"180.76.76.76")
        #释放无线网卡ip
        AddSSIDControl.dhcp_release_wlan(self,data_basic['wlan_pc'])
        #启用有线网卡
        AddSSIDControl.wlan_enable(self,data_basic['lan_pc'])
        return result1,result2


    ########################################################
    ###############RSSI#####################################
    ########################################################
    #输入最小RSSI值
    def set_rssi(self,value):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #设置最小RSSI值
        AddSSIDControl.wifi_pagedown1(self)
        AddSSIDControl.set_min_rssi(self,value)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    #设置最小RSSI值，并检查是否正确
    def check_min_rssi(self,value):
        AddSSIDBusiness.set_rssi(self,value)
         #获取第一个额外rssi的值
        result = AddSSIDControl.get_first_rssi_value(self)
        print "result = %s"%result
        return result

    #enable/disable RSSI
    def enable_disable_rssi(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.wifi_pagedown3(self)
        #点击开启RSSI
        AddSSIDControl.click_rssi(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)

    #enableRSSI 配置验证并检查
    def check_enable_rssi(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #点击开启RSSI
        AddSSIDControl.click_rssi(self)
        #获取默认最小RSSI值
        result1 = AddSSIDControl.get_min_rssi(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        #获取第一个额外rssi的值
        result2 = AddSSIDControl.get_first_rssi_value(self)
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #disableRSSI 配置验证并检查
    def check_disable_rssi(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #点击关闭RSSI
        AddSSIDControl.click_rssi(self)
        #获取默认最小RSSI值
        result1 = AddSSIDControl.get_min_rssi(self)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        #获取第一个额外rssi的状态
        result2 = AddSSIDControl.get_first_rssi(self)
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #enable rssi,错误Minimum RSSI (dBm)的配置验证
    def check_enable_min_rssi_error(self,err_value):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #点击开启RSSI
        AddSSIDControl.click_rssi(self)
        #设置最小RSSI值
        AddSSIDControl.set_min_rssi(self,err_value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = AddSSIDControl.check_error(self)
        #点击保存
        AddSSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #disable rssi,错误Minimum RSSI (dBm)的配置验证
    def check_disable_min_rssi_error(self,err_value):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        AddSSIDControl.wifi_pagedown1(self)
        #设置最小RSSI值
        AddSSIDControl.set_min_rssi(self,err_value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = AddSSIDControl.check_error(self)
        #点击保存
        AddSSIDControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        return result1,result2

    #在2分钟内每隔0.5秒检查无线网卡是否一直保持和ap连接
    def check_wifi_client_connected_allthetime(self,wlan):
        result = []
        i = 0
        while (i<120):
            status = AddSSIDControl.get_client_cmd_result(self,"iw %s link"%wlan)
            result.append(status)
            time.sleep(0.5)
            i = i+0.5
        print "result = %s"%result
        return result

    ########################################################
    ###############Network Group Membership#################
    ########################################################
    #检查是否有第2个，第3个网络组
    def check_2_3_network_group_membership(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击添加
        AddSSIDControl.add_button(self)
        #获取是否有第2个，第3个网络组的组名
        result1,result2 = AddSSIDControl.get_2_3_network_group_membership(self)
        #点击关闭按钮
        AddSSIDControl.close(self)
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #获取默认网络组的组名
    def check_1_network_group_membership(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击添加
        AddSSIDControl.add_button(self)
        #获取是否有第2个，第3个网络组的组名
        result = AddSSIDControl.get_1_network_group_membership(self)
        #点击关闭按钮
        AddSSIDControl.close(self)
        print "result = %s"%result
        return result

    #设置第一个额外ssid的网路组
    def set_zone(self,n):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #有多个网络组时，选择第几个网络组
        AddSSIDControl.choose_zone(self,n)
        #点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)



    #增加到最大的额外ssid
    def add_NG_max(self,host,user,pwd,add_ssid,key):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        for i in range(14):
            #点击添加
            AddSSIDControl.add_button(self)
            #设置开启额外ssid
            AddSSIDControl.set_enable_disable(self)
            #设置ssid
            AddSSIDControl.set_ssid(self,"%s%s"%(add_ssid,(i+2)))
            #设置wpa的密码
            AddSSIDControl.set_wpa_key(self,key)
            #添加窗口中，点击保存
            AddSSIDControl.save(self)
        #弹出窗口中，点击应用
        AddSSIDControl.apply(self)
        element = self.driver.find_element_by_id("newssid")
        result1 = element.get_attribute("disabled")
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show grandstream.ssid14.id")
        result3 = ssh.ssh_cmd(user,"iwconfig ath31")
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        print "result3 = %s"%result3
        return result1,result2,result3

    #获取所有group0的网络组，并判断个数
    def check_group_number(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        i = 0
        elements = self.driver.find_elements_by_css_selector(".titlediv")
        for element in elements:
            if element.text == "group0":
                i = i+1
        print i
        return i


    #删除所有网络组
    def del_all_NG(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        AddSSIDControl.del_all_button(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)


    ################以下是强制门户认证的方法##################
    #点击开启强制门户
    def click_addssid_portal(self):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #点击开启强制门户
        AddSSIDControl.click_portal(self)
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        print "click captive portal in additional SSID successfully!"

    #选择对应的强制门户策略
    def change_addssid_portal_policy(self,m):
        #点击网络组菜单，然后在点击额外ssid菜单
        AddSSIDBusiness.NG_SSID_menu(self)
        #点击编辑第一个ssid
        AddSSIDControl.click_first_edit(self)
        #选择对应的强制门户策略
        AddSSIDControl.set_portal_policy(self,m)
        #添加窗口中，点击保存
        AddSSIDControl.save(self)
        #点击弹出窗口中的应用
        AddSSIDControl.apply(self)
        print "choose captive portal policy in additional SSID successfully!"

