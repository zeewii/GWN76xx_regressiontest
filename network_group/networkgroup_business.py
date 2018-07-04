#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：GWN76xx网络组的业务层


from networkgroup_control import NGControl
from clients.client_access.clientaccess_business import ClientAccessBusiness
from connect.ssh import SSH
from data import data
from login.login_business import LoginBusiness
import time
from selenium.webdriver.common.keys import Keys
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness


data_basic = data.data_basic()
data_ng = data.data_networkgroup()


class NGBusiness(NGControl):

    def __init__(self,driver):
        #继承NGControl类的属性和方法
        NGControl.__init__(self,driver)

    #####################################################################
    #######以下是GWN7000的页面控制
    #####################################################################
    #打开web登录7000,并进入网络组，修改网络组的dhcp选项
    def mixed_7000_dhcp_option(self,value):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #设置dhcp选项的值
        NGControl.basic_pagedown3(self)
        NGControl.set_7000_dhcp_option(self,value)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)

    #测试完毕后改回空值，以免影响后面的升级测试
    def mixed_7000_dhcp_option_blank(self):
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #设置dhcp选项的值
        NGControl.basic_pagedown3(self)
        NGControl.set_7000_dhcp_option(self,"")
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)

    #7000新建一个网络组，vid设为2,开启dhcp server
    def mixed_7000_new_NG(self):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #输入网络组名
        NGControl.add_NG_basic_name(self,"group1")
        #添加窗口中，基本，勾选开启
        NGControl.add_NG_basic_enable(self)
        #添加窗口中，基本，流量转发选择wan0
        NGControl.add_NG_basic_wan0(self)
        #添加窗口中，基本，输入VLAN ID
        NGControl.set_NG_basic_VLANID(self,"2")
        #点击开启ipv4
        NGControl.set_7000_ipv4(self)
        #点击开启ipv4 DHCP
        time.sleep(5)
        self.driver.find_element_by_xpath(".//*[@id='additionalipcontent']/div[2]/span/button").send_keys(Keys.TAB)
        time.sleep(5)
        self.driver.implicitly_wait(10)
        NGControl.set_7000_ipv4_dhcp(self)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)

    #7000新建一个网络组，vid设为2,不开启dhcp server
    def mixed_7000_new_NG_no_DHCP(self):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #输入网络组名
        NGControl.add_NG_basic_name(self,"group1")
        #添加窗口中，基本，勾选开启
        NGControl.add_NG_basic_enable(self)
        #添加窗口中，基本，流量转发选择wan0
        NGControl.add_NG_basic_wan0(self)
        #添加窗口中，基本，输入VLAN ID
        NGControl.set_NG_basic_VLANID(self,"2")
        #点击开启ipv4
        NGControl.set_7000_ipv4(self)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)

    #7000新建多个网络组，group名和vid设为可选,开启dhcp server
    def mixed_7000_new_many_NG(self,n):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        for i in range(n):
            #点击添加
            NGControl.add_button(self)
            #输入网络组名
            NGControl.add_NG_basic_name(self,"group%s"%(i+2))
            #添加窗口中，基本，勾选开启
            NGControl.add_NG_basic_enable(self)
            #添加窗口中，基本，流量转发选择wan0
            NGControl.add_NG_basic_wan0(self)
            #添加窗口中，基本，输入VLAN ID
            NGControl.set_NG_basic_VLANID(self,"%s"%(i+2))
            #点击开启ipv4
            NGControl.set_7000_ipv4(self)
            #点击开启ipv4 DHCP
            self.driver.find_element_by_xpath(".//*[@id='additionalipcontent']/div[1]/span/button").send_keys(Keys.PAGE_DOWN)
            self.driver.implicitly_wait(10)
            NGControl.set_7000_ipv4_dhcp(self)
            #添加窗口中，点击保存
            NGControl.add_NG_save(self)
        NGControl.apply(self)

    #删除7000新建的网络组
    def mixed_7000_del_NG(self):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(60)
        self.driver.refresh()
        self.driver.implicitly_wait(60)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        #删除网络组
        NGControl.del_all_button(self)
        NGControl.apply(self)

    #进入7000网络组，点击ip4 dhcp server
    def mixed_7000_ip4_dhcp_server(self):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(10)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)
        print "go in GWN7000's network group,and click ipv4 dhcp server successfully!"

    #打开web登录7000,并进入网络组，修改网络组的dhcp ipv4的租期时间
    def mixed_7000_dhcp_lease_time(self,value):
        #打开GWN7000的web页面
        self.driver.get(data_basic['7000_web'])
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['7000_superUser'],data_basic['7000_pwd'])
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #设置dhcp server的租期时间
        NGControl.basic_pagedown3(self)
        NGControl.set_7000_ipv4_dhcp_lease_time(self,value)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)



    #####################################################################
    #######以下是GWN76xx的页面控制
    #####################################################################
    #点击添加，检查页面上是否有添加对话框
    def check_create_dialog(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #检查界面上是否有配置的对话框窗口
        result = NGControl.check_dialog(self)
        return result

    #点击编辑，检查页面上是否有添加对话框
    def check_edit_dialog(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.edit_button(self)
        #检查界面上是否有配置的对话框窗口
        result = NGControl.check_dialog(self)
        return result

    #点击网络组，添加一个新的网络组
    def new_network_group(self,NG_name,NG_ssid,NG_key):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #输入网络组名，并且开启
        NGControl.add_NG_basic_name(self,NG_name)
        NGControl.add_NG_basic_enable(self)
        #点击WIFI
        NGControl.add_NG_wifi(self)
        #开启wifi
        NGControl.add_NG_wifi_enable(self)
        #输入ssid
        NGControl.add_NG_wifi_ssid(self,NG_ssid)
        #输入WPA加密的密码
        NGControl.add_NG_wifi_wpa_key(self,NG_key)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "Add a new network group:%s successfully!"%NG_name

    #enable/disable wifi
    def enable_disable_NG_wifi(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #点击wifi
        NGControl.add_NG_wifi_enable(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #点击网络组，添加一个新的网络组时判断是否提示不能添加
    def check_tip_new_network_group(self,NG_name,NG_ssid,NG_key):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #输入网络组名，并且开启
        NGControl.add_NG_basic_name(self,NG_name)
        NGControl.add_NG_basic_enable(self)
        #点击WIFI
        NGControl.add_NG_wifi(self)
        #开启wifi
        NGControl.add_NG_wifi_enable(self)
        #输入ssid
        NGControl.add_NG_wifi_ssid(self,NG_ssid)
        #输入WPA加密的密码
        NGControl.add_NG_wifi_wpa_key(self,NG_key)
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        return result




    #添加一个新网络组，不输入任何参数
    def new_default(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #只添加一个新网络组后，判断是否添加成功
    def check_new_NG(self,host,user,pwd,NG_name):
        #调用ssh登录ap后台，输入uci show grandstream.general.zone1.name获取是否有新建的网络组名
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show grandstream.zone1.name")
        #print result
        if NG_name in result:
            return True
        else:
            return False

    #添加网络组时，检查VLAN是否启用
    def check_VLAN_enable(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #取VLAN的勾选情况,True:被选中,None:没选中
        result1 = NGControl.get_NG_basic_VLAN(self)
        #获取VLAN ID
        VLAN_ID = NGControl.get_NG_basic_VLANID(self)
        result2 = int(VLAN_ID)
        #点击VLAN的勾选
        NGControl.set_NG_basic_VLAN(self)
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result3 = element.is_displayed()
        print result1,result2,result3
        return result1,result2,result3

    #添加网络组时,检查VID的合理范围
    def check_VID_range(self,VID,host,user,pwd):
        result1 = []
        result2 = []
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #首先输入错误的VID
        for error_VID in VID[2:4]:
            #输入小于最小VLAN ID和最大VLAN ID
            NGControl.set_NG_basic_VLANID(self,error_VID)
            #判断输入框下方是否有错误提示,有则返回True，没有则返回False
            result1.append(NGControl.check_error(self))
        #添加窗口中，点击关闭
        NGControl.add_NG_close(self)
        #然后输入正确的VID
        for correct_VID in VID[0:2]:
            #点击添加
            NGControl.add_button(self)
            NGControl.set_NG_basic_VLANID(self,correct_VID)
            #点击保存
            NGControl.add_NG_save(self)
            #点击弹出窗口中的应用
            NGControl.apply(self)
            #登录路由后台确定vid是否正确
            i = VID.index(correct_VID)
            ssh = SSH(host,pwd)
            result = ssh.ssh_cmd(user,"uci show grandstream.zone%s.vlan"%(i+1))
            if correct_VID in result:
                result2.append(True)
            else:
                result2.append(False)
            #删除掉新建的网络组
            NGControl.del_all_button(self)
            #点击弹出窗口中的应用
            NGControl.apply(self)
        print result1,result2
        return result1,result2

    #设置相同的VID的情况
    def check_same_VID(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        #再次点击添加
        NGControl.add_button(self)
        #添加窗口中，基本，输入VLAN ID为2,即上一个同样的VID
        NGControl.set_NG_basic_VLANID(self,"2")
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        return result


    #只添加了一个网络组时，点击删除这个网络组
    def del_first_NG(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        NGControl.del_first_button(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        #弹出的提示窗口中，点击确认
        NGControl.notice_ok(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print result
        return result

    #删除默认的网络组
    def del_group0(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #获取默认网络组的删除的显示状态
        result1 = NGControl.get_group0_del_button_status(self)
        #点击默认网络组的删除按钮
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #增加到最大的网络组
    def add_NG_max(self,host,user,pwd,NG_key):
        NG_name = data_ng["NG2_name"]
        NG_ssid = data_ng["NG2_ssid"]
        #进入网络组页面
        NGControl.NG_menu(self)
        for i in range(15):
            #点击添加
            NGControl.add_button(self)
            #输入网络组名，并且开启
            NGControl.add_NG_basic_name(self,"%s-%s"%(NG_name,(i+2)))
            NGControl.add_NG_basic_enable(self)
            #点击WIFI
            NGControl.add_NG_wifi(self)
            #开启wifi
            NGControl.add_NG_wifi_enable(self)
            #输入ssid
            NGControl.add_NG_wifi_ssid(self,"%s-%s"%(NG_ssid,(i+2)))
            #输入WPA加密的密码
            NGControl.add_NG_wifi_wpa_key(self,NG_key)
            #点击保存
            NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        element = self.driver.find_element_by_id("newzone")
        print element.get_attribute("disabled")
        #调用ssh登录ap后台，输入uci show grandstream.general.zone15.name获取是否有新建的网络组名
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show grandstream.zone15.name")
        print result
        if element.get_attribute("disabled") and ("%s-16"%NG_name in result):
            return True
        else:
            return False

    #增加多个网络组
    def add_many_NG(self,n,NG_key):
        NG_name = data_ng["NG2_name"]
        NG_ssid = data_ng["NG2_ssid"]
        #进入网络组页面
        NGControl.NG_menu(self)
        for i in range(n):
            #点击添加
            NGControl.add_button(self)
            #输入网络组名，并且开启
            NGControl.add_NG_basic_name(self,"%s-%s"%(NG_name,(i+2)))
            NGControl.add_NG_basic_enable(self)
            #点击WIFI
            NGControl.add_NG_wifi(self)
            #开启wifi
            NGControl.add_NG_wifi_enable(self)
            #输入ssid
            NGControl.add_NG_wifi_ssid(self,"%s-%s"%(NG_ssid,(i+2)))
            #输入WPA加密的密码
            NGControl.add_NG_wifi_wpa_key(self,NG_key)
            #点击保存
            NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #选择特定的一个网络组，disable网络组和wifi
    def disable_NG_wifi(self,n):
        #进入网络组页面
        NGControl.NG_menu(self)
        #有多个网络组时，选择特定的网络组，点击编辑
        NGControl.edit_groupn_button(self,n)
        #disable网络组
        NGControl.add_NG_basic_enable(self)
        #点击WIFI
        NGControl.add_NG_wifi(self)
        #disable wifi
        NGControl.add_NG_wifi_enable(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #获取特定的网络组的网络组名
    def get_NG_name(self,n):
        #进入网络组页面
        NGControl.NG_menu(self)
        #有多个网络组时，选择特定的网络组，点击编辑
        NGControl.edit_groupn_button(self,n)
        result = NGControl.get_add_NG_basic_name(self)
        #添加窗口中，点击关闭
        NGControl.add_NG_close(self)
        print result
        return result



    #验证16个网络组在页面的显示情况
    def check_max_disaplay(self):
        result1 = []
        NG_name = data_ng["NG2_name"]
        NG_ssid = data_ng["NG2_ssid"]
        #获取所有的网络组名和SSID名
        display_info = NGControl.get_titlediv(self)
        print display_info
        for i in range(15):
            if ("%s-%s"%(NG_name,(i+2)) and "%s-%s"%(NG_ssid,(i+2))) in display_info:
                print "%s-%s"%(NG_name,(i+2)),"%s-%s"%(NG_ssid,(i+2))
                result1.append(True)
            else:
                print "%s-%s"%(NG_name,(i+2)),"%s-%s"%(NG_ssid,(i+2))
                result1.append(False)
        #获取所有enableicon的个数
        result2 = NGControl.get_enableicon(self)
        #获取所有disableicon的个数
        result3 = NGControl.get_disableicon(self)
        print result1,result2,result3
        return result1,result2,result3

    #验证AP加入16个网络组后，配置是否生效
    def check_maxNG_config(self,host,user,pwd):
        #首先验证后台接口是否有添加
        ssh = SSH(host,pwd)
        result1 = ssh.ssh_cmd(user,"ifconfig eth0.16")
        result2 = ssh.ssh_cmd(user,"ifconfig ath31")
        return result1,result2

    #删除所有网络组
    def del_all_NG(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        NGControl.del_all_button(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)







    #进入网络组-编辑-点击wifi
    def NG_edit_wifi_menu(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击编辑
        NGControl.edit_button(self)
        #点击wifi
        NGControl.add_NG_wifi(self)

    #有多个网络组时，选择特定的网络组,进入网络组-编辑-点击wifi
    def NG_edit_groupn_wifi_menu(self,n):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击编辑
        NGControl.edit_groupn_button(self,n)
        #点击wifi
        NGControl.add_NG_wifi(self)

    #修改默认网络组的ssid和密码
    def change_wifi_ssid_key(self,NG_ssid,NG_key):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi，输入ssid
        NGControl.add_NG_wifi_ssid(self,NG_ssid)
        #添加窗口中，wifi，输入wpa密码
        NGControl.add_NG_wifi_wpa_key(self,NG_key)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "change group0's ssid and password successfully!"


    #修改特定网络组的ssid和密码
    def change_specail_wifi_ssid_key(self,n,NG_ssid,NG_key):
        #有多个网络组时，选择特定的网络组,进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi，输入ssid
        NGControl.add_NG_wifi_ssid(self,NG_ssid)
        #添加窗口中，wifi，输入wpa密码
        NGControl.add_NG_wifi_wpa_key(self,NG_key)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "change specail group's ssid and password successfully!"

    #检查ssid是否修改成功
    def check_NG_ssid(self,host,user,pwd):
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show wireless.ath0.ssid")
        return result

    #禁用启用默认网络组的wifi
    def disable_enable_wifi(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #disable wifi
        NGControl.add_NG_wifi_enable(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "click wifi status successfully!"


    #隐藏ssid
    def hidden_ssid(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #点击隐藏ssid
        NGControl.set_hidden_ssid(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "click hidden group0's ssid successfully!"

    #隐藏第N个group的ssid
    def hidden_n_ssid(self,n):
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #点击隐藏ssid
        NGControl.set_hidden_ssid(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "click hidden group%s's ssid successfully!"%n



    #使用无线网卡连接隐藏的ssid，判断是否能够连接上
    def check_WPA_hiddenssid_AP(self,ssid,password,wlan):
        #通过wpa_cli命令来连接WPA的隐藏无线网络
        result = NGControl.connect_WPA_hiddenssid_AP(self,ssid,password,wlan)
        print ssid
        if ssid in result:
            return True
        else:
            return False

    #重启7610并取出版本号来判断
    def reboot_get_version(self,host,user,pwd,version):
        #重启7610
        NGControl.reboot_router(self,host,user,pwd)
        tmp = UpgradeBusiness(self.driver)
        #AP重启升降级固件--AP重启后，检查ap是否升级完成
        tmp.confirm_AP_upgrade_finish_after_reboot(host,user,pwd,version)
        #通过ssh登录路由后台，取出路由当前的版本号
        result = NGControl.get_router_version(self,host,user,pwd)
        if version in result:
            return True
        else:
            return False









    #设置默认网络组无线为非加密
    def wifi_None_encryption(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择wifi的安全模式为不加密
        NGControl.add_NG_wifi_None(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        time.sleep(30)
        print "set group0 NONE encryption successfully!"

    #设置默认网络组无线为wep加密
    def wifi_wep_encryption(self,n,NG_key):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择wifi的安全模式为wep64
        NGControl.add_NG_wifi_n_encryption(self,n)
        #添加窗口中，wifi，输入wep密码
        NGControl.add_NG_wifi_wep_key(self,NG_key)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        time.sleep(30)
        print "set group0 wep encryption successfully!"

    #设置默认网络组无线为wpa/wpa2加密
    def wifi_wpa_encryption(self,n,m,NG_key):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        NGControl.add_NG_wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        NGControl.add_NG_wifi_wpa_mode(self,"PSK")
        #添加窗口中，wifi,选择WPA类型
        NGControl.add_NG_wifi_wpa_type(self,m)
        ##添加窗口中，wifi，输入wpa密码
        NGControl.add_NG_wifi_wpa_key(self,NG_key)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        time.sleep(30)
        print "set group0 wpa encryption successfully!"

    #设置默认网络组无线为802.1x加密
    def wifi_8021x_encryption(self,n,m,addr,key):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择wifi的安全模式为wpa/wpa2加密
        NGControl.add_NG_wifi_n_encryption(self,n)
        #添加窗口中，wifi,选择WPA密钥模式
        NGControl.add_NG_wifi_wpa_mode(self,"802.1x")
        #添加窗口中，wifi,选择WPA类型
        NGControl.add_NG_wifi_wpa_type(self,m)
        #设置radius服务器地址
        NGControl.set_radius_server(self,addr)
        #设置radius服务器密钥
        NGControl.set_radius_secret(self,key)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        #time.sleep(30)
        print "set group0 802.1x encryption successfully!"





    #输入异常wep密码，是否有提示
    def check_abnormal_wep(self,n,NG_key):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择wifi的安全模式
        NGControl.add_NG_wifi_n_encryption(self,n)
        #添加窗口中，wifi，输入wep密码
        NGControl.add_NG_wifi_wep_key(self,NG_key)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = NGControl.check_error(self)
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2


    #设置默认网络组的无线过滤的白名单
    def wifi_whitelist(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        NGControl.set_mac_filter(self,'Whitelist')
        #mac = NGControl.get_wlan_mac(self,wlan)
        #添加窗口中，选择第一个白名单列表
        NGControl.wifi_pagedown1(self)
        NGControl.set_onemac_whitelist(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #设置默认网络组的无线过滤的白名单--不选择list
    def wifi_whitelist_backup(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        NGControl.set_mac_filter(self,'Whitelist')
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #获取默认网络组的无线过滤的白名单
    def get_wifi_whitelist(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,获取白名单的值
        result = NGControl.get_mac_whitelist(self)
        return result

    #添加N个mac地址过滤白名单，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_white_mac(self,n):
       #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        for i in range(n):
            #添加窗口，wifi，添加mac白名单地址输入框
            NGControl.set_white_addmac(self)
        #点击保存
        NGControl.add_NG_save(self)
        #time.sleep(60)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #删除所有的mac地址过滤白名单，点击保存应用
    def del_many_white_mac(self):
       #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口，wifi，删除所有mac地址输入框
        NGControl.del_white_addmac(self)
        #取本机无线mac地址
        mac = NGControl.get_wlan_mac(self,data_basic["wlan_pc"])

        #添加窗口中，wifi,输入白名单
        element = self.driver.find_element_by_xpath(".//*[@id='whitelistcontent']//input")
        element.clear()
        element.send_keys(mac)

        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #添加N个mac地址过滤黑名单，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_black_mac(self,n):
       #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        for i in range(n):
            #添加窗口，wifi，添加mac黑名单地址输入框
            NGControl.set_black_addmac(self)
        #点击保存
        NGControl.add_NG_save(self)
        #time.sleep(60)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #删除所有的mac地址过滤黑名单，点击保存应用
    def del_many_black_mac(self):
       #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口，wifi，删除所有mac地址输入框
        NGControl.del_black_addmac(self)
        #取本机无线mac地址
        mac = NGControl.get_wlan_mac(self,data_basic["wlan_pc"])

        #添加窗口中，wifi,输入白名单
        element = self.driver.find_element_by_xpath(".//*[@id='blacklistcontent']//input")
        element.clear()
        element.send_keys(mac)

        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)




    #登录路由后台，判断mac地址过滤，白名单数目
    def check_mac_list(self,host,user,pwd):
        ssh = SSH(host,pwd)
        tmp = ssh.ssh_cmd(user,"cat /etc/config/grandstream | grep mac")
        tmp1 = tmp.split("\r\n\t")
        result = len(tmp1)-2
        print result
        return result


    #设置默认网络组的无线过滤的黑名单
    def wifi_blacklist(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        #mac = NGControl.get_wlan_mac(self,wlan)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择第一个黑名单列表
        NGControl.set_onemac_blacklist(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #设置默认网络组的无线过滤的黑名单---不选择list
    def wifi_blacklist_backup(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #有多个网络组时,设置第n个网络组的无线过滤的黑名单
    def groupn_wifi_blacklist(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择第一个黑名单列表
        NGControl.set_onemac_blacklist(self)
        #mac = NGControl.get_wlan_mac(self,wlan)
        #添加窗口中，wifi,输入黑名单
        #NGControl.set_mac_blacklist(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


     #有多个网络组时,设置第n个网络组的无线过滤的黑名单
    def groupn_wifi_blacklist2(self,n):
        #进入网络组页面
        NGControl.NG_menu(self)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(10)
        #点击编辑
        NGControl.edit_groupn_button(self,n)
        #点击wifi
        NGControl.add_NG_wifi(self)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择第一个黑名单列表
        NGControl.set_onemac_blacklist(self)
        #mac = NGControl.get_wlan_mac(self,wlan)
        #添加窗口中，wifi,输入黑名单
        #NGControl.set_mac_blacklist(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #有多个网络组时,设置第n个网络组的无线过滤的黑名单--不点击list
    def groupn_wifi_blacklist_backup(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        NGControl.wifi_pagedown1(self)
        #mac = NGControl.get_wlan_mac(self,wlan)
        #添加窗口中，wifi,输入黑名单
        #NGControl.set_mac_blacklist(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #有多个网络组时,点击第n个网络组的无线过滤的黑名单下的第2个列表
    def groupn_wifi_blacklist_twolist(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择第二个黑名单列表
        NGControl.set_twomac_blacklist(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #有多个网络组时,设置第n个网络组的无线过滤的白名单
    def groupn_wifi_whitelist(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        NGControl.set_mac_filter(self,'Whitelist')
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择第一个白名单列表
        NGControl.set_onemac_whitelist(self)
        #mac = NGControl.get_wlan_mac(self,wlan)
        #添加窗口中，wifi,输入黑名单
        #NGControl.set_mac_whitelist(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #有多个网络组时,设置第n个网络组的无线过滤的白名单--不点击list
    def groupn_wifi_whitelist_backup(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        NGControl.set_mac_filter(self,'Whitelist')
        NGControl.wifi_pagedown1(self)
        #mac = NGControl.get_wlan_mac(self,wlan)
        #添加窗口中，wifi,输入黑名单
        #NGControl.set_mac_whitelist(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #有多个网络组时,点击第n个网络组的无线过滤的白名单下的第2个列表
    def groupn_wifi_whitelist_twolist(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择第二个白名单列表
        NGControl.set_twomac_whitelist(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #有多个网络组时,禁用第n个网络组的无线过滤
    def disable_macfilter(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-禁用
        NGControl.set_mac_filter(self,'Disable')
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #有多个网络组时,设置第n个网络组的无线过滤的白名单,获取mac白名单提示信息
    def get_groupn_wifi_whitelist(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        NGControl.set_mac_filter(self,'Whitelist')
        NGControl.wifi_pagedown1(self)
        #添加窗口，wifi，mac白名单提示信息
        result = NGControl.get_white_mac_info(self)
        NGControl.add_NG_close(self)
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的黑名单,获取mac黑名单提示信息
    def get_groupn_wifi_blacklist(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        NGControl.wifi_pagedown1(self)
        #添加窗口，wifi，mac黑名单提示信息
        result = NGControl.get_black_mac_info(self)
        NGControl.add_NG_close(self)
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的白名单,列表能显示
    def get_groupn_wifi_whitelist_display(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-白名单
        NGControl.set_mac_filter(self,'Whitelist')
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择白名单,列表能显示
        result = NGControl.get_whitelist(self)
        NGControl.add_NG_close(self)
        return result

    #有多个网络组时,设置第n个网络组的无线过滤的黑名单,列表能显示
    def get_groupn_wifi_blacklist_display(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #添加窗口中，wifi,选择使用mac地址过滤-黑名单
        NGControl.set_mac_filter(self,'Blacklist')
        NGControl.wifi_pagedown1(self)
        #添加窗口中，选择黑名单,列表能显示
        result = NGControl.get_blacklist(self)
        NGControl.add_NG_close(self)
        return result

    #进入编辑-设备管理，获取已添加设备的名称
    def get_added_device_name(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击group0编辑
        NGControl.edit_group0_button(self)
        #添加窗口中，点击设备管理
        NGControl.add_NG_device(self)
        #获取已添加的设备的名称
        result = NGControl.get_Member_Devices_name(self)
        #添加窗口中，点击关闭
        NGControl.add_NG_close(self)
        return result

    ########################################################
    ###############客户端隔离#################################
    ########################################################
    #配置group0的客户端隔离的网关mac为错误的测试
    def check_wifi_isolation_gateway_mac_err(self,err_mac):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        NGControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        NGControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        NGControl.gateway_mac(self,err_mac)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = NGControl.check_error(self)
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #配置group0的客户端隔离的模式--要点击客户端隔离
    def wifi_isolation(self,value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        NGControl.click_isolation(self)
        #选择客户端隔离模式
        NGControl.isolation_mode(self,value)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #配置第n个group的客户端隔离的模式--要点击客户端隔离
    def wifi_n_isolation(self,n,value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        NGControl.click_isolation(self)
        #选择客户端隔离模式
        NGControl.isolation_mode(self,value)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #配置group0的客户端隔离的模式--不点击客户端隔离
    def wifi_isolation_backup(self,value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #选择客户端隔离模式
        NGControl.isolation_mode(self,value)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #配置第n个group的客户端隔离的模式--不点击客户端隔离
    def wifi_n_isolation_backup(self,n,value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #选择客户端隔离模式
        NGControl.isolation_mode(self,value)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #配置group0的客户端隔离的网关mac--要点击客户端隔离
    def wifi_isolation_gateway_mac(self,mac):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        NGControl.click_isolation(self)
        #选择客户端隔离模式--网关mac地址
        NGControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        NGControl.gateway_mac(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #配置group0的客户端隔离的网关mac--不点击客户端隔离
    def wifi_isolation_gateway_mac_backup(self,mac):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #选择客户端隔离模式--网关mac地址
        NGControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        NGControl.gateway_mac(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #配置第n个group的客户端隔离的网关mac--不点击客户端隔离
    def wifi_n_isolation_gateway_mac_backup(self,n,mac):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #选择客户端隔离模式--网关mac地址
        NGControl.isolation_mode(self,"gateway_mac")
        #输入网关mac地址
        NGControl.gateway_mac(self,mac)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #取消group0的客户端隔离的模式
    def cancel_wifi_isolation(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        NGControl.click_isolation(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #取消第n个group的客户端隔离的模式
    def cancel_wifi_n_isolation(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #添加窗口中，wifi,点击客户端隔离
        NGControl.click_isolation(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #检查客户端隔离的结果
    def check_isolation(self,ssid,password):
        #无线网卡连接ap
        NGControl.connect_DHCP_WPA_AP(self,ssid,password,data_basic['wlan_pc'])
        #禁用有线网卡
        NGControl.wlan_disable(self,data_basic['lan_pc'])
        #无线ping网关
        result1 = NGControl.get_ping(self,data_basic['7000_ip'])
        #无线pingqq
        result2 = NGControl.get_ping(self,"180.76.76.76")
        #释放无线网卡ip
        NGControl.dhcp_release_wlan(self,data_basic['wlan_pc'])
        #启用有线网卡
        NGControl.wlan_enable(self,data_basic['lan_pc'])
        return result1,result2

    ########################################################
    ###############RSSI#####################################
    ########################################################
    #输入最小RSSI值
    def set_rssi(self,value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #设置最小RSSI值
        NGControl.set_min_rssi(self,value)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #enable/disable RSSI
    def enable_disable_rssi(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #点击开启RSSI
        NGControl.click_rssi(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

     #enable/disable 第n个group的RSSI
    def enable_disable_n_rssi(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        NGControl.wifi_pagedown1(self)
        #点击开启RSSI
        NGControl.click_rssi(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #设置最小RSSI值，并检查是否正确
    def check_min_rssi(self,value):
        NGBusiness.set_rssi(self,value)
        #获取第一个额外rssi的值
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        result = NGControl.get_min_rssi(self)
        print "result = %s"%result
        return result

    #enableRSSI 配置验证并检查
    def check_enable_rssi(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #点击开启RSSI
        NGControl.click_rssi(self)
        #获取默认最小RSSI值
        result = NGControl.get_min_rssi(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "result = %s"%result
        return result

    #disableRSSI 配置验证并检查
    def check_disable_rssi(self):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #点击关闭RSSI
        NGControl.click_rssi(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        #再次进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #获取RSSI是否被选中
        result1 = NGControl.get_rssi_status(self)
        #获取默认最小RSSI值
        result2 = NGControl.get_min_rssi(self)
        print "The result of RSSI whether been checked is %s"%result1
        print "After disabling RSSI,The min RSSI value is %s"%result2
        return result1,result2

    #enable rssi,错误Minimum RSSI (dBm)的配置验证
    def check_enable_min_rssi_error(self,err_value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #点击开启RSSI
        NGControl.click_rssi(self)
        #设置最小RSSI值
        NGControl.set_min_rssi(self,err_value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = NGControl.check_error(self)
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #disable rssi,错误Minimum RSSI (dBm)的配置验证
    def check_disable_min_rssi_error(self,err_value):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_wifi_menu(self)
        NGControl.wifi_pagedown1(self)
        #设置最小RSSI值
        NGControl.set_min_rssi(self,err_value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = NGControl.check_error(self)
        #点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        return result1,result2

    #在2分钟内每隔0.5秒检查无线网卡是否一直保持和ap连接
    def check_wifi_client_connected_allthetime(self,wlan):
        result = []
        i = 0
        while (i<120):
            status = NGControl.get_client_cmd_result(self,"iw %s link"%wlan)
            result.append(status)
            time.sleep(0.5)
            i = i+0.5
        return result

    #################################################################
    #############设备管理#############################################
    #################################################################
    #将所有已添加的设备删除
    def del_all_ap(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击编辑
        NGControl.edit_button(self)
        #添加窗口中，点击设备管理
        NGControl.add_NG_device(self)
        #添加窗口中，设备管理，已添加设备，删除所有设备
        NGControl.del_Member_device_all(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #将所有可添加的设备添加
    def add_all_ap(self):
        #进入网络组页面
        NGControl.NG_menu(self)
        #点击编辑
        NGControl.edit_button(self)
        #添加窗口中，点击设备管理
        NGControl.add_NG_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        NGControl.add_Available_device_all(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        time.sleep(30)


    ##################以下是fallback IP的方法##################
    #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
    def check_ap_br_lan0_IP(self,ip,user,pwd):
        result1 = NGControl.get_ping(self,ip)
        ssh = SSH(ip,pwd)
        result2 = ssh.ssh_cmd(user,"ifconfig br-lan0_zone0 | grep inet")
        if (result1 == 0) and (ip in result2):
            return True
        else:
            return False

    #disable/enable dhcp server when GWN76xx is in unpaired status,fallback IP works fine
    def check_fallback_IP_function(self,fallback_ip,master_ip,user,default_pwd):
        #关闭7000的dhcp server
        NGBusiness.mixed_7000_ip4_dhcp_server(self)
        #等待dhcp server的过期时间-2分钟
        time.sleep(150)
        #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
        result1 = NGBusiness.check_ap_br_lan0_IP(self,
            fallback_ip,user,default_pwd)
        #开启7000的dhcp server
        NGBusiness.click_ip4_dhcp(self)
        time.sleep(60)
        #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
        result2 = NGBusiness.check_ap_br_lan0_IP(self,master_ip,
            user, default_pwd)
        print result1,result2
        return result1,result2

    #ap goin fallback ip
    def check_ap_goin_fallback_IP(self,fallback_ip,user,default_pwd):
        #关闭7000的dhcp server
        NGBusiness.mixed_7000_ip4_dhcp_server(self)
        #等待dhcp server的过期时间-2分钟
        time.sleep(150)
        #重启ap
        NGBusiness.reboot_router(self, fallback_ip, user, default_pwd)
        time.sleep(200)
        #验证ap的ip是否能够访问，并确定ap的br-lan0_zone0接口ip地址
        result = NGBusiness.check_ap_br_lan0_IP(self,fallback_ip,
            user, default_pwd)
        print result
        return result

    #fallback mode can login as master mode
    def check_fallback_login_as_master(self,master_ip, user, default_pwd):
        #关闭7000的dhcp server
        NGBusiness.mixed_7000_ip4_dhcp_server(self)
        #重启ap
        NGBusiness.reboot_router(self, master_ip, user, default_pwd)
        time.sleep(180)





    ##################以下是AP DHCP server的方法##################
    #进入网络组，点击ip4 dhcp server
    def click_ip4_dhcp(self):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)
        print "go in ap's network group,and click ipv4 dhcp server successfully!"

    #进入网络组，点击ip4 dhcp server-输入网关
    def click_ip4_dhcp_server(self,gateway):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #设置dhcp网关
        NGControl.s_dhcp_gateway(self,gateway)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)
        print "go in ap's network group,and click ipv4 dhcp server successfully!"

    ##验证dhcp开启功能生效
    def check_ap_dhcp_server(self):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #检查ipv4 DHCP server是否勾选
        result = NGControl.check_ipv4_dhcp(self)
        return result

    #dhcp起始地址是否合法
    def check_dhcp_start_valid(self,ip):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        ##DHCP开始地址
        NGControl.s_ipv4_dhcp_start(self,ip)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result = NGControl.check_error(self)
        NGControl.add_NG_close(self)
        print result
        return result

    #dhcp结束地址是否合法
    def check_dhcp_end_valid(self,ip):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        ##DHCP结束地址
        NGControl.s_ipv4_dhcp_end(self,ip)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result = NGControl.check_error(self)
        NGControl.add_NG_close(self)
        print result
        return result

    #开始地址大于结束地址是否合法
    def check_dhcp_start_more_end(self,start_ip,end_ip):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        ##DHCP开始地址
        NGControl.s_ipv4_dhcp_start(self,start_ip)
        ##DHCP结束地址
        NGControl.s_ipv4_dhcp_end(self,end_ip)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #验证格式的dhcp的租约
    def check_dhcp_lease_time(self,time):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #设置dhcp server的租期时间
        NGControl.set_7000_ipv4_dhcp_lease_time(self,time)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result = NGControl.check_error(self)
        NGControl.add_NG_close(self)
        print result
        return result

    #仅仅设置租期
    def set_dhcp_lease_time(self,time):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #设置dhcp server的租期时间
        NGControl.set_7000_ipv4_dhcp_lease_time(self,time)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)
        print "go in ap's network group,and set lease time successfully!"

    #登录后台，检查租期时间
    def check_ap_dhcp_lease_time(self,host,user,pwd,time):
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show dhcp.lan0_zone0.leasetime")
        if time in result:
            return True
        else:
            return False




    #验证格式的网关地址
    def check_dhcp_gateway(self,value):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #设置dhcp网关
        NGControl.s_dhcp_gateway(self,value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result = NGControl.check_error(self)
        NGControl.add_NG_close(self)
        print result
        return result

    #验证网关与接口地址不在同一网段，设置失败
    def check_dhcp_gateway_different_ip(self,value):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #设置dhcp网关
        NGControl.s_dhcp_gateway(self,value)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #验证dns格式
    def check_dhcp_dns(self,value):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        # #设置首选dns
        NGControl.basic_pagedown1(self)
        NGControl.s_dhcp_dns1(self,value)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result = NGControl.check_error(self)
        NGControl.add_NG_close(self)
        print result
        return result

    #设置首选dns和次选dns-点击dhcp server
    def set_ap_dhcp_dns1_dns2(self,dns1,dns2):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        #设置首选dns
        NGControl.basic_pagedown1(self)
        NGControl.s_dhcp_dns1(self,dns1)
        NGControl.s_dhcp_dns2(self,dns2)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)
        print "go in ap's network group,and set dns1 and dns2 successfully!"

    #设置首选dns和次选dns-不点击dhcp server
    def set_ap_dns1_dns2(self,dns1,dns2):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #设置首选dns
        NGControl.basic_pagedown1(self)
        NGControl.s_dhcp_dns1(self,dns1)
        NGControl.s_dhcp_dns2(self,dns2)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)
        print "go in ap's network group,and set dns1 and dns2 successfully!"

    #验证首选dns和次选dns是否设置成功
    def check_ap_dhcp_dns1_dns2(self):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        NGControl.basic_pagedown1(self)
        #获取首选dns
        dns1 = NGControl.g_dhcp_dns1(self)
        #获取次选dns
        dns2 = NGControl.g_dhcp_dns2(self)
        NGControl.add_NG_close(self)
        return dns1,dns2

    #完整设置
    def set_all_config(self,start_ip,end_ip,gateway,dns1,dns2):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        ##DHCP开始地址
        NGControl.s_ipv4_dhcp_start(self,start_ip)
        ##DHCP结束地址
        NGControl.s_ipv4_dhcp_end(self,end_ip)
        #设置dhcp网关
        NGControl.s_dhcp_gateway(self,gateway)
        #设置首选dns
        NGControl.basic_pagedown1(self)
        NGControl.s_dhcp_dns1(self,dns1)
        NGControl.s_dhcp_dns2(self,dns2)
        #添加窗口中，点击保存
        NGControl.add_NG_save(self)
        NGControl.apply(self)

    #检查完整配置
    def check_all_config(self):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑默认网络组
        NGControl.edit_button(self)
        #检查ipv4 DHCP server是否勾选
        dhcp_checked = NGControl.check_ipv4_dhcp(self)
        #获取dhcp网关
        gateway = NGControl.g_dhcp_gateway(self)
        NGControl.basic_pagedown1(self)
        #获取首选dns
        dns1 = NGControl.g_dhcp_dns1(self)
        #获取次选dns
        dns2 = NGControl.g_dhcp_dns2(self)
        NGControl.add_NG_close(self)
        return dhcp_checked,gateway,dns1,dns2


    #新建网络组，开启dhcp server和wifi
    def new_group_open_dhcp_server(self,NG_name,ip,
            start_ip, end_ip, gateway,dns1,NG_ssid,NG_key):
        #进入网络组
        NGControl.NG_menu(self)
        #点击添加
        NGControl.add_button(self)
        #输入网络组名，并且开启
        NGControl.add_NG_basic_name(self,NG_name)
        NGControl.add_NG_basic_enable(self)
        #点击开启ipv4
        NGControl.s_ipv4(self)
        #设置IPv4静态地址
        NGControl.s_ipv4_static(self,ip)
        #点击开启IPv4 DHCP
        NGControl.set_7000_ipv4_dhcp(self)
        ##DHCP开始地址
        NGControl.s_ipv4_dhcp_start(self,start_ip)
        ##DHCP结束地址
        NGControl.s_ipv4_dhcp_end(self,end_ip)

        #设置dhcp网关
        NGControl.basic_pagedown2(self)
        NGControl.s_dhcp_gateway(self,gateway)
        #设置dns
        NGControl.s_dhcp_dns1(self,dns1)
        # NGControl.s_dhcp_dns2(self,dns2)

        #点击WIFI
        NGControl.add_NG_wifi(self)
        #开启wifi
        NGControl.add_NG_wifi_enable(self)
        #输入ssid
        NGControl.add_NG_wifi_ssid(self,NG_ssid)
        #输入WPA加密的密码
        NGControl.add_NG_wifi_wpa_key(self,NG_key)
        #添加窗口中，点击设备管理
        NGControl.add_NG_device(self)
        #添加窗口中，设备管理，可添加设备，添加所有设备
        NGControl.add_Available_device_all(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #更改新建网络组的起始ip和终止ip
    def change_groupn_start_end_ip(self,n,start_ip,end_ip):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑新建的网络组
        NGControl.edit_groupn_button(self,n)
        ##DHCP开始地址
        NGControl.s_ipv4_dhcp_start(self,start_ip)
        ##DHCP结束地址
        NGControl.s_ipv4_dhcp_end(self,end_ip)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)

    #点击新建网络组的dhcp server
    def click_groupn_dhcp_server(self,n):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑新建的网络组
        NGControl.edit_groupn_button(self,n)
        NGControl.set_7000_ipv4_dhcp(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    #点击新建网络组的ipv4
    def click_groupn_ipv4(self,n):
        #进入网络组
        NGControl.NG_menu(self)
        #点击编辑新建的网络组
        NGControl.edit_groupn_button(self,n)
        NGControl.s_ipv4(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    ################以下是客户端时间策略的方法##################

    #选择客户端时间策略
    def change_client_time_policy(self, n, text):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #设置客户端时间策略
        NGBusiness.set_client_time_policy(self,text)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)


    ################以下是强制门户认证的方法##################
    #点击开启强制门户
    def click_groupn_portal(self,n):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #点击开启强制门户
        NGControl.click_portal(self)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "click captive portal of networkgroup:%s successfully!"%n

    #点击多个网络组的强制门户
    #输入：n，一共有多少个网络组
    def click_many_group_portal(self,n):
        #进入网络组页面
        NGControl.NG_menu(self)
        for i in range(n):
            #点击编辑
            NGControl.edit_groupn_button(self,(i+1))
            #点击wifi
            NGControl.add_NG_wifi(self)
            #点击开启强制门户
            NGControl.click_portal(self)
            #点击保存
            NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "click captive portal for many networkgroups successfully!"

    #选择对应的强制门户策略
    def change_groupn_portal_policy(self,n,m):
        #进入网络组-编辑-点击wifi
        NGBusiness.NG_edit_groupn_wifi_menu(self,n)
        #选择对应的强制门户策略
        NGControl.set_portal_policy(self,m)
        #点击保存
        NGControl.add_NG_save(self)
        #点击弹出窗口中的应用
        NGControl.apply(self)
        print "choose captive portal policy of networkgroup:%s successfully!"%n



