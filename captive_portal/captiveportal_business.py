#coding=utf-8
#作者：曾祥卫
#时间：2017.07.27
#描述：GWN76xx强制门户认证的业务层

from captiveportal_control import CPControl
import time
from selenium.webdriver.support.ui import WebDriverWait
from connect.ssh import SSH
from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from login.login_business import LoginBusiness
from data import data
from access_points.aps_business import APSBusiness
from clients.clients_business import ClientsBusiness
from clients.client_access.clientaccess_business import ClientAccessBusiness



data_basic = data.data_basic()
data_login = data.data_login()

class CPBusiness(CPControl):

    def __init__(self,driver):
        #继承CPControl类的属性和方法
        CPControl.__init__(self,driver)

    #访问web页面，只要获取到页面的title就停止等待--防止由于有些页面内容过多，打开时等待过久
    def wait_for_title(self,web):
        self.driver.get(web)
        self.driver.implicitly_wait(5)
        try:
            time.sleep(10)
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:1.start opening web time:%s-----------"%current_time
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.title)
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:2.obtain title time:%s-----------"%current_time
            #停止页面加载
            self.driver.execute_script('window.stop()')
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:3.stop loading web time:%s-----------"%current_time
        except:
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:4.goin except and reloading web time:%s-----------"%current_time
            self.driver.get(web)
            #停止页面加载
            time.sleep(60)
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:5.goin except and finish loading web time:%s-----------"%current_time
            self.driver.execute_script('window.stop()')
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:6.goin except and stop loading web time:%s-----------"%current_time
        finally:
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng title debug:7.return title time:%s-----------"%current_time
            return self.driver.title

    #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
    def check_jump_to_No_auth_portal(self,ssid,password,wlan,eth):
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #禁用有线网卡
        CPControl.wlan_disable(self,eth)
        time.sleep(30)
        #使用无线网卡连接group0的ssid
        CPControl.connect_WPA_AP(self,ssid,password,wlan)
        #再次禁用有线网卡--防止无线网卡的多次连接时会重启全部网络导致有限网卡再次开启
        CPControl.wlan_disable(self,eth)
        #循环三次检查无线网卡是否能够上网
        for i in range(3):
            #无线网卡释放ip地址
            CPControl.dhcp_release_wlan(self,wlan)
            #无线网卡再次获取ip地址
            CPControl.dhcp_wlan(self,wlan)
            CPControl.move_resolv(self)
            #如果不能访问网络
            tmp = CPControl.get_ping(self,"www.qq.com")
            if tmp == 0 :
                break
            else:
                print "check wlan card can access internet or not,again."
        #打开http的页面http://www.qq.com
        redirect_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "Access tencent webpage, jump to %s webpage"%redirect_title
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        print redirect_title
        if redirect_title == "gatewayname Entry":
            return True
        else:
            return False

    #验证portal多次开启，关闭，wifi连接和portal功能正常--执行6次
    def check_open_close_captive_portal_No_auth_function(self,ssid,password,wlan,eth):
        result = []
        for i in range(6):
            #点击group0的强制门户认证
            tmp1 = SSIDBusiness(self.driver)
            tmp1.click_ssid_portal(1)
            #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
            result1 = CPBusiness.check_jump_to_No_auth_portal(self,ssid,password,wlan,eth)
            result.append(result1)
            #测试完成一遍后，再次登录ap页面，为后续循环测试做好准备
            #刷新页面重新登录ap页面
            Lg = LoginBusiness(self.driver)
            Lg.refresh_login_ap()
        print result
        return result




    #验证非group0 portal功能正常
    def check_group1_portal_function(self,NG2_ssid,password,wlan,eth):
        #7000新建一个网络组-vlan id = 2
        tmp1 = NGBusiness(self.driver)
        tmp1.mixed_7000_new_NG()
        #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
        result = CPBusiness.check_jump_to_No_auth_portal(self,NG2_ssid,password,wlan,eth)
        #删除7000新建的网络组
        tmp1.mixed_7000_del_NG()
        print result
        return result

    #验证非ssid0由AP自身提供dhcp功能，portal功能正常
    def check_group1_open_DHCP_portal_function(self,NG2_name,ip,
            start_ip,end_ip,gateway,dns1,NG2_ssid,
            password,wlan,eth):
        #7000新建一个网络组，vid设为2,不开启dhcp server
        tmp1 = NGBusiness(self.driver)
        tmp1.mixed_7000_new_NG_no_DHCP()
        #76xx上新建一个网络组，vid为2,开启dhcp server和wifi
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        self.driver.refresh()
        time.sleep(10)
        tmp1.new_group_open_dhcp_server(NG2_name,ip,
            start_ip, end_ip, gateway,dns1,NG2_ssid,password)
        #开启group1的强制门户认证
        tmp1.click_groupn_portal(1)
        #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
        result = CPBusiness.check_jump_to_No_auth_portal(self,NG2_ssid,password,wlan,eth)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #删除master ap的group1
        tmp1.del_all_NG()
        #删除7000新建的网络组
        tmp1.mixed_7000_del_NG()
        print result
        return result

    #验证多group portal功能正常--3个
    def check_many_group_portal_function(self,group0_ssid,
            group1_ssid,group2_ssid,password,wlan,eth):
        result = []
        #7000新建两个网络组,开启dhcp server
        tmp1 = NGBusiness(self.driver)
        tmp1.mixed_7000_new_many_NG(2)
        #76xx上新建1个对应的网络组
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        self.driver.refresh()
        time.sleep(10)
        tmp3 = SSIDBusiness(self.driver)
        tmp3.new_vlan_ssid(group2_ssid,password,"3")
        #开启三个网络组的强制门户认证
        tmp3.click_ssid_portal(1)
        tmp3.click_ssid_portal(3)
        #master ap加入所有的网络组
        tmp2 = APSBusiness(self.driver)
        tmp2.add_master_to_all_NG()
        #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
        for j in [group0_ssid,group1_ssid,group2_ssid]:
            result1 = CPBusiness.check_jump_to_No_auth_portal(self,j,password,wlan,eth)
            result.append(result1)
        print result
        return result

    #验证多个group portal多次开启，关闭，wifi连接和portal功能正常--执行2次
    def check_open_close_many_groups_captive_portal_function(self,
            group0_ssid,group1_ssid,group2_ssid,
            password,wlan,eth):
        result = []
        tmp1 = SSIDBusiness(self.driver)
        for i in range(2):
            #点击group0的强制门户认证
            #点击三个网络组的强制门户认证
            tmp1.click_many_group_portal(3)
            #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
            for j in [group0_ssid,group1_ssid,group2_ssid]:
                result1 = CPBusiness.check_jump_to_No_auth_portal(self,j,password,wlan,eth)
                result.append(result1)
            #测试完成一遍后，再次登录ap页面，为后续循环测试做好准备
            #刷新页面重新登录ap页面
            Lg = LoginBusiness(self.driver)
            Lg.refresh_login_ap()
            time.sleep(30)
        #删除master ap的两个ssid
        tmp1 = SSIDBusiness(self.driver)
        tmp1.del_all_NG()
        #删除7000新建的两个网络组
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_del_NG()
        print result
        return result

    #验证slave ap 的非group0 portal功能正常
    def check_slave_ap_group1_portal_function(self,NG2_ssid,password,wlan,eth):
        #7000新建一个网络组，vid设为2,开启dhcp server
        tmp1 = NGBusiness(self.driver)
        tmp1.mixed_7000_new_NG()
        #76xx上新建一个网络组，vid为2
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        self.driver.refresh()
        time.sleep(10)
        tmp2 = SSIDBusiness(self.driver)
        tmp2.new_vlan_ssid(NG2_ssid,password,"2")
        #开启group1的强制门户认证
        tmp2.click_ssid_portal(2)
        #slave ap加入所有的网络组
        tmp3 = APSBusiness(self.driver)
        tmp3.add_slave_to_all_NG()
        #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
        result = CPBusiness.check_jump_to_No_auth_portal(self,NG2_ssid,password,wlan,eth)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #删除ssid1
        tmp2.del_all_NG()
        #删除7000新建的网络组
        tmp1.mixed_7000_del_NG()
        print result
        return result




    #修改策略的名称
    def change_portal_rule_name(self,n,name):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #输入list名称
        CPControl.set_policy_name(self,name)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)

    #修改策略名称，并检查页面判断是否修改成功
    def check_portal_rule_name(self,n,name):
        #修改策略的名称
        CPBusiness.change_portal_rule_name(self,n,name)
        #获取页面所有标题
        result = CPControl.get_titlediv(self)
        if name in result:
            return True
        else:
            return False

    #修改策略名称后，判断是否有异常提示出现
    def check_rule_name_invalid(self,n,name):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #输入list名称
        CPControl.set_policy_name(self,name)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = CPControl.check_error(self)
        #点击保存
        CPControl.click_add_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #增加新的策略，判断是否有异常提示出现
    def check_add_rule_invalid(self,n,name):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击添加按钮
        CPControl.click_add(self)
        #输入list名称
        CPControl.set_policy_name(self,name)
        #输入有效期
        CPControl.set_expiration(self,n,"86400")
        #点击保存
        CPControl.click_add_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #修改策略的过期时间
    def change_portal_rule_expiration(self,n,t):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #输入有效期
        CPControl.set_expiration(self,n,t)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)

    #修改策略的过期时间，并检查页面判断是否修改成功
    def check_portal_rule_expiration(self,n,t):
        #修改策略的过期时间
        CPBusiness.change_portal_rule_expiration(self,n,t)
        #获取页面所有标题
        result = CPControl.get_titlediv(self)
        if (t+"s") in result:
            return True
        else:
            return False

    #修改策略的过期时间后，判断是否有异常提示出现
    def check_rule_expiration_invalid(self,n,t):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #输入有效期
        CPControl.set_expiration(self,n,t)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = CPControl.check_error(self)
        #点击保存
        CPControl.click_add_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #免认证页面点击同意，然后再点击登录
    def enter_default_portal(self):
        try:
            #点击进入，确定能够跳转
            CPControl.click_agree(self)
            CPControl.click_connect_WiFi(self)
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng portal debug:access auth time:%s-----------"%current_time
            time.sleep(30)
            self.driver.execute_script('window.stop()')
            current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
            print "-----------rick.zeng portal debug:return title time:%s-----------"%current_time
            return self.driver.title
        except:
            #如果页面没有跳转到认证页面，捕捉页面
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_redirect_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            print "-----------rick.zeng portal debug:Can't goin portal webpage, refresh webpage and return webpage title!"
            time.sleep(30)
            self.driver.refresh()
            self.driver.implicitly_wait(30)
            #如果页面没有跳转到认证页面,返回当前页面
            return self.driver.title

    #通过免认证方式上网
    def access_No_auth_portal(self,ssid,password,wlan,eth,wifi_encryption):
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #禁用有线网卡
        CPControl.wlan_disable(self,eth)
        time.sleep(30)
        #使用无线网卡连接group0的ssid
        if wifi_encryption == "open":
            CPControl.connect_NONE_AP(self,ssid,wlan)
        elif wifi_encryption == "wep":
            CPControl.connect_WEP_AP(self,ssid,password,wlan)
        elif wifi_encryption == "wpa":
            CPControl.connect_WPA_AP(self,ssid,password,wlan)
        elif wifi_encryption == "wpa_hiddenssid":
            CPControl.connect_WPA_hiddenssid_AP(self,ssid,password,wlan)
        elif wifi_encryption == "802.1x":
            CPControl.connect_8021x_AP(self,
                ssid,data_basic['radius_usename'],
                data_basic['radius_password'],wlan)

        #再次禁用有线网卡--防止无线网卡的多次连接时会重启全部网络导致有限网卡再次开启
        CPControl.wlan_disable(self,eth)
        #循环三次检查无线网卡是否能够上网
        for i in range(3):
            #无线网卡释放ip地址
            CPControl.dhcp_release_wlan(self,wlan)
            #无线网卡再次获取ip地址
            CPControl.dhcp_wlan(self,wlan)
            CPControl.move_resolv(self)
            #如果不能访问网络
            tmp = CPControl.get_ping(self,"www.qq.com")
            if tmp == 0 :
                break
            else:
                print "check wlan card can access internet or not,again."
        #打开http的页面http://www.qq.com
        portal_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "Access tencent webpage first, goin to %s"%portal_title
        #免认证页面点击同意，然后再点击登录
        redirect_title = CPBusiness.enter_default_portal(self)
        print "click agree, goin to %s"%redirect_title
        return portal_title,redirect_title

    #验证默认list：grandstream中的免认证的有效性
    #输入：t：过期时间
    def check_No_auth_portal(self,ssid,password,wlan,eth,t,wifi_encryption):
        #通过免认证方式上网
        portal_title,redirect_title = CPBusiness.\
            access_No_auth_portal(self,ssid,password,wlan,eth,wifi_encryption)
        #再次确定能否访问腾讯首页
        again_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "Access tencent webpage again, goin to %s"%again_title
        current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "-----------rick.zeng portal debug:finished access tencent again time:%s-----------"%current_time
        #验证过期时间
        #再次等待一段时间
        time.sleep(t)
        #打开http的页面http://www.qq.com
        expiration_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "wait %s seconds,access tencent webpage again, goin to %s"%(t,expiration_title)
        current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "-----------rick.zeng portal debug:wait expiration time,finished access tencent time:%s-----------"%current_time
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        print "portal_title is %s"%portal_title
        print "redirect_title is %s"%redirect_title
        print "again_title is %s"%again_title
        print "expiration_title is %s"%expiration_title
        return portal_title,redirect_title,again_title,expiration_title

    #验证STA漫游，Expiration累计-12min
    def check_client_roaming_expiration(self,ssid,password,wlan,eth,n,
            slave_mac):
        #修改过期时间为12min
        CPBusiness.change_portal_rule_expiration(self,n,"720")
        current_time1 = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "------1:%s"%current_time1
        #client连接master ap，并通过认证-不等待（1s）
        CPBusiness.check_No_auth_portal(self,ssid,password,wlan,eth,1,"wpa")
        current_time2 = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "------2:%s"%current_time2
        #在网络组里面将master ap从group0中移除
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        tmp1 = NGBusiness(self.driver)
        tmp1.del_all_ap()
        current_time3 = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "------3:%s"%current_time3
        #slave ap pair并添加到group0
        tmp2 = APSBusiness(self.driver)
        tmp2.search_pair_add_default(slave_mac)
        current_time4 = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "------4:%s"%current_time4
        #client连接上slave ap，不需要认证
        result1 = CPBusiness.check_jump_to_No_auth_portal(self,ssid,password,wlan,eth)
        current_time5 = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "------5:%s"%current_time5
        #等待过期时间到期后，client需要重新认证
        time.sleep(180)
        current_time6 = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "------6:%s"%current_time6
        result2 = CPBusiness.check_jump_to_No_auth_portal(self,ssid,password,wlan,eth)
        print result1,result2
        return result1,result2

    #新增一个policy
    def add_new_default_policy(self,n,name,t):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击添加按钮
        CPControl.click_add(self)
        #输入list名称
        CPControl.set_policy_name(self,name)
        #输入有效期
        CPControl.set_expiration(self,n,t)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)
        print "new add a policy successfully!"

    #验证新增空的policy，提示信息
    def check_add_new_policy_null(self):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击添加按钮
        CPControl.click_add(self)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = CPControl.check_error(self)
        #点击保存
        CPControl.click_add_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #验证新增policy成功
    def check_add_new_policy_success(self,n,name,t):
        #新增一个policy
        CPBusiness.add_new_default_policy(self,n,name,t)
        #获取页面所有标题
        result1 = CPControl.get_titlediv(self)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #再次获取页面所有标题
        result2 = CPControl.get_titlediv(self)
        if (name in result1) and (name in result2):
            return True
        else:
            return False


    #增加多个策略，并判断添加按钮是否为灰色
    def check_many_policy_valid(self,start_n,end_n):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        for i in range(start_n,end_n):
            #点击添加按钮
            CPControl.click_add(self)
            #输入list名称
            CPControl.set_policy_name(self,u"认证策略%s"%i)
            #输入有效期
            CPControl.set_expiration(self,i,"120")
            #编辑或添加的页面点击保存
            CPControl.click_add_save(self)
        CPControl.apply(self)
        #添加按钮是否不可点击
        element = self.driver.find_element_by_id("newcaptiveportal")
        result = element.is_enabled()
        print result
        return result

    #删除策略
    def del_policy_n(self,n):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击删除按钮
        CPControl.del_button(self,n)
        #弹出的提示窗口中，点击确认
        CPControl.notice_ok(self)
        CPControl.apply(self)

    #删除多个策略
    def del_many_policys(self,start_n,end_n):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        for i in range(start_n,end_n):
            #点击删除按钮
            CPControl.del_button(self,i)
            #弹出的提示窗口中，点击确认
            CPControl.notice_ok(self)
        CPControl.apply(self)

    #验证正在使用的policy不可删除
    def check_del_policy(self,n):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击删除按钮
        CPControl.del_button(self,n)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element1 = self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element1.is_displayed()
        try:
            element2 =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-cancel']")
            result2 = True
        except:
            result2 = False
        print result1,result2
        return result1,result2

    #验证默认的policy不可删除
    def check_del_default_policy(self):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        element = self.driver.find_element_by_id("del_portal_policy_0")
        result = element.is_enabled()
        print result
        return result

    #验证policy删除成功
    def check_del_policy_success(self,n,name):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击删除按钮
        CPControl.del_button(self,n)
        CPControl.notice_ok(self)
        CPControl.apply(self)
        result = CPControl.get_titlediv(self)
        if name not in result:
            return True
        else:
            return False

    #修改第n个list为No auth服务
    def change_No_auth(self,n,t):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #选择认证方式
        CPControl.set_auth_type(self,"0")
        #输入有效期
        CPControl.set_expiration(self,n,t)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)

    #修改第n个list由radisu改回免认证
    def change_radius_to_No_auth(self,n,t):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #选择认证方式--radius改回免认证
        CPControl.set_radius_to_No_auth(self)
        #输入有效期
        CPControl.set_expiration(self,n,t)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)


    #修改第n个list为radius服务
    def change_radius_server(self,n,radius_addr,radius_key,port,mode):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self,n)
        #选择认证方式-radius
        CPControl.set_auth_type(self,"1")
        #输入radius服务器地址
        CPControl.set_radius_server_address(self,n,radius_addr)
        #输入radius服务器的端口
        CPControl.set_radius_server_port(self,port)
        #输入radius服务器密钥
        CPControl.set_radius_server_secret(self,n,radius_key)
        #选择radius认证方式
        CPControl.set_radius_auth_method(self,mode)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)
        print "change the %s list to radius auth successfully!"%n

    #radius portal页面输入用户名密码然后点击登录
    def enter_radius_portal(self,radius_name,radius_password):
        #输入用户名
        CPControl.set_radius_name(self,radius_name)
        #输入用户名
        CPControl.set_radius_password(self,radius_password)
        #点击进入，确定能够跳转
        result = CPBusiness.enter_default_portal(self)
        return result


    #验证默认list：grandstream中的radius认证的有效性
    def check_radius_portal(self,ssid,password,wlan,eth,t,radius_name,\
                            radius_password):
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #禁用有线网卡
        CPControl.wlan_disable(self,eth)
        time.sleep(60)
        #使用无线网卡连接group0的ssid
        CPControl.connect_WPA_AP(self,ssid,password,wlan)
        #再次禁用有线网卡--防止无线网卡的多次连接时会重启全部网络导致有限网卡再次开启
        CPControl.wlan_disable(self,eth)
        #循环三次检查无线网卡是否能够上网
        for i in range(3):
            #无线网卡释放ip地址
            CPControl.dhcp_release_wlan(self,wlan)
            #无线网卡再次获取ip地址
            CPControl.dhcp_wlan(self,wlan)
            CPControl.move_resolv(self)
            #如果不能访问网络
            tmp = CPControl.get_ping(self,"www.qq.com")
            if tmp == 0 :
                break
            else:
                "check wlan card can access internet or not,again."
        #打开http的页面http://www.qq.com
        portal_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "Access tencent webpage first, goin to %s"%portal_title
        #radius portal页面输入用户名密码然后点击登录
        redirect_title = CPBusiness.enter_radius_portal(self,radius_name,radius_password)
        print "click agree, goin to %s"%redirect_title
        #再次确定能否访问腾讯首页
        again_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "Access tencent webpage again, goin to %s"%again_title
        current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "-----------rick.zeng portal debug:finished access tencent again time:%s-----------"%current_time
        #验证过期时间
        #再次等待一段时间
        time.sleep(t)
        #打开http的页面http://www.qq.com
        expiration_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "wait %s seconds,access tencent webpage again, goin to %s"%(t,expiration_title)
        current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "-----------rick.zeng portal debug:wait expiration time,finished access tencent time:%s-----------"%current_time
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        print "portal_title is %s"%portal_title
        print "redirect_title is %s"%redirect_title
        print "again_title is %s"%again_title
        print "expiration_title is %s"%expiration_title
        return portal_title,redirect_title,again_title,expiration_title

    #验证非group0 radius portal功能正常
    def check_group1_radius_portal_function(self,NG2_ssid,
            password,wlan,eth,t,radius_name,radius_password):
        #7000新建一个网络组，vid设为2,开启dhcp server
        tmp1 = NGBusiness(self.driver)
        tmp1.mixed_7000_new_NG()
        #76xx上新建一个网络组，vid为2
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        self.driver.refresh()
        time.sleep(10)
        tmp3 = SSIDBusiness(self.driver)
        tmp3.new_vlan_ssid(NG2_ssid,password,"2")
        #开启ssid1的强制门户认证
        tmp3.click_ssid_portal(2)
        #master ap加入所有的网络组
        tmp2 = APSBusiness(self.driver)
        tmp2.add_master_to_all_NG()
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = \
            CPBusiness.check_radius_portal(self,NG2_ssid,password,
            wlan,eth,t,radius_name,radius_password)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #删除master ap的ssid1
        tmp3.del_all_NG()
        #删除7000新建的网络组
        tmp1.mixed_7000_del_NG()
        return portal_title,redirect_title,again_title,expiration_title

    #获取portal用户的数量
    def Get_clients_number(self):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击强制网络门户页面上的客户端菜单
        CPControl.client_menu(self)
        #获取客户端的数量
        result = CPControl.get_clients_number(self)
        return result

    #获取portal用户的mac和ip地址
    def Get_clients_mac_ip(self,n):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击强制网络门户页面上的客户端菜单
        CPControl.client_menu(self)
        mac = CPControl.get_client_mac(self,n)
        ip = CPControl.get_client_ip(self,n)
        return mac,ip

    #检测portal用户认证状态正确并自动更新
    def check_portal_client_auth_status(self,ssid,password,wlan,eth,n):
        #通过免认证方式上网
        CPBusiness.\
            access_No_auth_portal(self,ssid,password,wlan,eth,"wpa")
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击强制网络门户页面上的客户端菜单
        CPControl.client_menu(self)
        auth_status1 = CPControl.get_client_auth_status(self,n)
        #禁用有线网卡
        CPControl.wlan_disable(self,eth)
        time.sleep(60)
        #使用无线网卡再次连接上
        CPControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #等待过期时间
        time.sleep(300)
        #使用无线网卡再次连接上
        CPControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击强制网络门户页面上的客户端菜单
        CPControl.client_menu(self)
        auth_status2 = CPControl.get_client_auth_status(self,n)
        return auth_status1,auth_status2

    #验证portal用户block功能正常
    def check_portal_client_block_function(self,ssid,password,wlan,eth):
        #通过免认证方式上网
        CPBusiness.\
            access_No_auth_portal(self,ssid,password,wlan,eth,"wpa")
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        tmp = ClientsBusiness(self.driver)
        #使用无线网卡能够连接上ssid,并正常使用
        tmp.connect_DHCP_WPA_AP(ssid,password,wlan)
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #只有一个客户端，阻塞该客户端
        wlan_mac = tmp.get_wlan_mac(wlan)
        tmp.block_client(wlan_mac)
        time.sleep(60)
        #测试机上判断无线客户端是否依然是连接上的
        result = tmp.get_client_cmd_result("iw dev %s link"%wlan)
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        tmp1 = ClientAccessBusiness(self.driver)
        #删除Global Blacklist里面的所有的mac
        tmp1.del_Global_Blacklist_mac()
        return result

    #验证切换认证方式，已认证的用户无需重新认证
    def check_auth_STA_not_need_auth_again(self,ssid,password,wlan,eth,
            radius_addr,radius_key,port,mode):
        #通过免认证方式上网
        CPBusiness.\
            access_No_auth_portal(self,ssid,password,wlan,eth,"wpa")
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #将免认证改为radius认证
        CPBusiness.\
            change_radius_server(self,1,radius_addr,radius_key,port,mode)
        #验证是否需要弹出认证
        result = CPBusiness.\
            check_jump_to_No_auth_portal(self,ssid,password,wlan,eth)
        print result
        return result

    #更改门户页面模板
    def change_portal_page(self, n, page):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self, n)
        #点击使用默认门户页面
        CPControl.click_default_page(self)
        #选择门户页面定制
        CPControl.set_portal_page(self,page)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)
        print "change portal page of the %s list to %s successfully!"%(n, page)

    #将门户页面改回默认模板
    def change_portal_page_to_default(self, n):
        #点击页面上强制网络门户
        CPControl.CP_menu(self)
        #点击编辑按钮
        CPControl.click_edit_button(self, n)
        #点击使用默认门户页面
        CPControl.click_default_page(self)
        #编辑或添加的页面点击保存
        CPControl.click_add_save(self)
        CPControl.apply(self)
        print "change portal page of the %s list to default page successfully!"%n

    #验证开启一个group的portal，不影响其他group的用户
    def check_other_group_STA_open_group0(self, NG2_ssid, password,
            ssid,wlan,eth):
        #新建一个ssid1,vid2
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_vlan_ssid(NG2_ssid, password,"2")
        #开启ssid1的强制门户认证
        tmp1.click_ssid_portal(2)
        #master ap加入所有的网络组
        tmp2 = APSBusiness(self.driver)
        tmp2.add_master_to_all_NG()
        #确认STA连接group0,并且不需要认证
        #验证是否需要弹出认证
        result = CPBusiness.\
            check_jump_to_No_auth_portal(self,ssid,password,wlan,eth)
        print result
        return result

    #验证STA被解除block后，不需要重新认证
    def check_STA_unblock_no_need_auth(self,ssid,password,wlan,eth):
        #无线STA通过group0的认证
        tmp = CPBusiness(self.driver)
        tmp.access_No_auth_portal(ssid,password,wlan,eth,"wpa")
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #block STA
        tmp.connect_WPA_AP(ssid,password,wlan)
        tmp3 = ClientsBusiness(self.driver)
        wlan_mac = tmp3.get_wlan_mac(wlan)
        tmp3.block_client(wlan_mac)
        #unblock STA
        tmp4 = ClientAccessBusiness(self.driver)
        #删除Global Blacklist里面的所有的mac
        tmp4.del_Global_Blacklist_mac()
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        result = tmp.check_jump_to_No_auth_portal(ssid,password,wlan,eth)
        return result

    #使用免认证的规则，访问腾讯首页，判断是否跳转到portal页面
    def check_jump_to_No_auth_portal_backup(self,ssid,password,wlan,eth,wifi_encryption):
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #禁用有线网卡
        CPControl.wlan_disable(self,eth)
        time.sleep(60)
        #使用无线网卡连接group0的ssid
        if wifi_encryption == "open":
            CPControl.connect_NONE_AP(self,ssid,wlan)
        elif wifi_encryption == "wep":
            CPControl.connect_WEP_AP(self,ssid,password,wlan)
        elif wifi_encryption == "wpa":
            CPControl.connect_WPA_AP(self,ssid,password,wlan)
        elif wifi_encryption == "wpa_hiddenssid":
            CPControl.connect_WPA_hiddenssid_AP(self,ssid,password,wlan)
        elif wifi_encryption == "802.1x":
            CPControl.connect_8021x_AP(self,
                ssid,data_basic['radius_usename'],
                data_basic['radius_password'],wlan)

        #再次禁用有线网卡--防止无线网卡的多次连接时会重启全部网络导致有限网卡再次开启
        CPControl.wlan_disable(self,eth)
        #循环三次检查无线网卡是否能够上网
        for i in range(3):
            #无线网卡释放ip地址
            CPControl.dhcp_release_wlan(self,wlan)
            #无线网卡再次获取ip地址
            CPControl.dhcp_wlan(self,wlan)
            CPControl.move_resolv(self)
            #如果不能访问网络
            tmp = CPControl.get_ping(self,"www.qq.com")
            if tmp == 0 :
                break
            else:
                "check wlan card can access internet or not,again."
        #打开http的页面http://www.qq.com
        redirect_title = CPBusiness.wait_for_title(self,"http://www.qq.com")
        print "Access tencent webpage, jump to %s webpage"%redirect_title
        #无线网卡释放ip地址
        CPControl.dhcp_release_wlan(self,wlan)
        #断开无线连接
        CPControl.disconnect_ap(self)
        #启用有线网卡
        CPControl.wlan_enable(self,eth)
        print redirect_title
        if redirect_title == "gatewayname Entry":
            return True
        else:
            return False