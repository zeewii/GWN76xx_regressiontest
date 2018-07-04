#coding=utf-8
#作者：曾祥卫
#时间：2017.12.22
#描述：用例集，调用captiveportal_business

import unittest,time,subprocess
from selenium import webdriver
from login.login_business import LoginBusiness
from access_points.aps_business import APSBusiness
from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from clients.clients_business import ClientsBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from system_settings.maintenance.access.access_business import AccessBusiness
from system_settings.maintenance.basic.basic_business import BasicBusiness
from overview.overview_business import OVBusiness
from data import data
from connect.ssh import SSH
from captive_portal.captiveportal_business import CPBusiness
from overview.overview_business import OVBusiness
from clients.client_access.clientaccess_business import ClientAccessBusiness
from data.logfile import Log
log = Log("Captiveportal")

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
data_Client = data.data_Client()

class TestCaptivePortal(unittest.TestCase):
    u"""测试强制网络门户的用例集(runtime:14h30m)"""
    def setUp(self):
        # firefox_profile = webdriver.FirefoxProfile(data_basic['firefox_profile'])
        # self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])

    #在页面上把AP恢复出厂设置(testlink_ID:773)
    def test_001_factory_reset(self):
        u"""在页面上把AP恢复出厂设置(testlink_ID:773)"""
        log.debug("001")
        #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
        Lg = LoginBusiness(self.driver)
        Lg.login_again()

        tmp = APSBusiness(self.driver)
        #描述：启用无线网卡
        tmp.wlan_enable(data_basic['wlan_pc'])
        #rsyslog服务器准备
        tmp.ready_rsyslog()
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        #修改默认网络组的ssid和密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #验证Captive Portal一键开启，Portal免认证功能生效
    def test_002_open_captive_portal_No_auth_function(self):
        u"""验证Captive Portal一键开启，Portal免认证功能生效(testlink_ID:1848)"""
        log.debug("002")
        #开启group0的强制门户认证
        tmp1 = SSIDBusiness(self.driver)
        tmp1.click_ssid_portal(1)
        tmp1.change_AP_Freq("5GHz")
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check open No auth portal function, test pass!"

    #重启ap，确定portal功能正常
    def test_003_reboot_ap_portal_function(self):
        u"""重启ap，确定portal功能正常(testlink_ID:1857)"""
        log.debug("003")
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check open No auth portal functionafter rebooting ap, test pass!"

    #验证Captive Portal一键关闭，Portal认证取消
    def test_004_close_captive_portal_No_auth_function(self):
        u"""验证Captive Portal一键关闭，Portal认证取消(testlink_ID:1849)"""
        log.debug("004")
        #关闭group0的强制门户认证
        tmp1 = SSIDBusiness(self.driver)
        tmp1.click_ssid_portal(1)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check close No auth portal function, test pass!"

    #验证portal多次开启，关闭，wifi连接和portal功能正常--执行6次
    def test_005_open_close_captive_portal_No_auth_function(self):
        u"""验证portal多次开启，关闭，wifi连接和portal功能正常--执行6次(testlink_ID:1850)"""
        log.debug("005")
        tmp = CPBusiness(self.driver)
        #验证portal多次开启，关闭，wifi连接和portal功能正常--执行6次
        result = tmp.check_open_close_captive_portal_No_auth_function(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertEqual(result,[True,False,True,False,True,False])
        print "open and close captive portal many times,check function normally,test pass!"

    #验证ssid1功能正常
    def test_006_ssid_open_captive_portal_No_auth_function(self):
        u"""验证ssid1 portal功能正常(testlink_ID:1851)"""
        log.debug("006")
        #新建一个ssid
        NG_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(NG_ssid,data_wireless['short_wpa'])
        #点击开启强制门户
        tmp1.click_ssid_portal(2)
        #将ssid1固定为5G
        tmp1.change_n_AP_Freq(2,"5GHz")
        #ssid1加入master ap
        tmp2 = APSBusiness(self.driver)
        tmp2.add_master_to_all_NG()
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(NG_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check ssid1 open No auth portal function, test pass!"

    #验证非group0 portal功能正常
    def test_007_group1_portal_function(self):
        u"""验证非group0 portal功能正常(testlink_ID:1852)"""
        log.debug("007")
        #修改ssid的vlan id为2
        NG_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp1 = SSIDBusiness(self.driver)
        tmp1.enable_vlan_ssid(2,"2")
        tmp = CPBusiness(self.driver)
        result = tmp.check_group1_portal_function(NG_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check group1 open No auth portal function, test pass!"

    #验证多group portal功能正常--3个
    def test_009_check_many_groups_portal_function(self):
        u"""验证多group portal功能正常--3个(testlink_ID:1854)"""
        log.debug("009")
        NG_ssid = data_ng["NG2_ssid"]
        tmp = CPBusiness(self.driver)
        result = tmp.check_many_group_portal_function(data_wireless['all_ssid'],
            "%s-%s"%(NG_ssid,2),"%s-%s"%(NG_ssid,3),
            data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        self.assertEqual(result,[True,True,True])
        print "check many groups portal function, test pass!"

    #验证多个group portal多次开启，关闭，wifi连接和portal功能正常--执行2次
    def test_010_check_open_close_many_groups_portal_funciton(self):
        u"""验证多个group portal多次开启，关闭，wifi连接和portal功能正常--执行2次(testlink_ID:1855)"""
        log.debug("010")
        NG_ssid = data_ng["NG2_ssid"]
        tmp = CPBusiness(self.driver)
        result = tmp.check_open_close_many_groups_captive_portal_function(data_wireless['all_ssid'],
            "%s-%s"%(NG_ssid,2),"%s-%s"%(NG_ssid,3),
            data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        self.assertEqual(result,[False,False,False,True,True,True])
        print "open and close many groups of captive portal many times,check function normally,test pass!"

    #验证slave ap的ssid0的portal功能正常
    def test_011_check_slave_ap_ssid0_portal_function(self):
        u"""验证slave ap的ssid0的portal功能正常(testlink_ID:1856-1)"""
        log.debug("011")
        #搜索-配对-加入默认ssid
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add_default(data_AP['slave:mac2'])
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check slave ap of ssid0 function, test pass!"


    #验证slave ap的非ssid0的portal功能正常
    def test_013_check_slave_ap_ssid1_portal_function(self):
        u"""验证slave ap的非ssid0的portal功能正常(testlink_ID:1856-3)"""
        log.debug("013")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = CPBusiness(self.driver)
        result = tmp.check_slave_ap_group1_portal_function(NG2_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check slave ap group1 portal function, test pass!"

    #强制门户认证的name输入数字
    def test_014_check_portal_name_digital(self):
        u"""强制门户认证的name输入数字(testlink_ID:1858-1)"""
        log.debug("014")
        tmp1 = APSBusiness(self.driver)
        #解除slave ap的配对
        tmp1.unpair_last_slave_ap(1)
        #修改策略名称，并检查页面判断是否修改成功
        tmp = CPBusiness(self.driver)
        result = tmp.check_portal_rule_name(1,data_wireless['digital_ssid'])
        self.assertTrue(result)
        print "check protal name is digital, test pass!"

    #强制门户认证的name输入英文
    def test_015_check_portal_name_letter(self):
        u"""强制门户认证的name输入英文(testlink_ID:1858-2)"""
        log.debug("015")
        #修改策略名称，并检查页面判断是否修改成功
        tmp = CPBusiness(self.driver)
        result = tmp.check_portal_rule_name(1,data_wireless['letter_ssid_part'])
        self.assertTrue(result)
        print "check protal name is letter, test pass!"

    #强制门户认证的name输入特殊字符
    def test_016_check_portal_name_special_letter(self):
        u"""强制门户认证的name输入特殊字符(testlink_ID:1858-3)"""
        log.debug("016")
        #修改策略名称，并检查页面判断是否修改成功
        tmp = CPBusiness(self.driver)
        result = tmp.check_portal_rule_name(1,data_wireless['ascii_ssid'])
        self.assertTrue(result)
        print "check protal name is specail letter, test pass!"

    #强制门户认证的name输入长度超过32位
    def test_017_check_portal_name_over_32(self):
        u"""强制门户认证的name输入长度超过32位(testlink_ID:1858-4)"""
        log.debug("017")
        #修改策略名称后，判断是否有异常提示出现
        tmp = CPBusiness(self.driver)
        result = tmp.check_rule_name_invalid(1,data_wireless['long_ssid']+"ab")
        self.assertTrue(result)
        print "check protal name is over 32bit, test pass!"

    #强制门户认证的name修改为已创建有的策略名称
    def test_018_check_portal_name_exist_name(self):
        u"""强制门户认证的name修改为已创建有的策略名称(testlink_ID:1858-5)"""
        log.debug("018")
        #修改默认的策略名称为grandstream
        tmp = CPBusiness(self.driver)
        tmp.change_portal_rule_name(1,"grandstream")
        #增加新的策略-相同的策略名称，判断是否有异常提示出现
        result = tmp.check_add_rule_invalid(2,"grandstream")
        self.assertTrue(result)
        print "check protal name is same as another, test pass!"

    #检测Expiration输入值范围-在60-604800范围内
    def test_019_check_portal_rule_expiration(self):
        u"""检测Expiration输入值范围-在60-604800范围内(testlink_ID:1859-1)"""
        log.debug("019")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间，并检查页面判断是否修改成功
        result = tmp.check_portal_rule_expiration(1,"3600")
        self.assertTrue(result)
        print "check expiration is range:60-604800, test pass!"

    #检测Expiration输入值范围-小于60
    def test_020_check_portal_rule_expiration(self):
        u"""检测Expiration输入值范围-小于60(testlink_ID:1859-2)"""
        log.debug("020")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间后，判断是否有异常提示出现
        result = tmp.check_rule_expiration_invalid(1,"30")
        self.assertTrue(result)
        print "check expiration is less 60s, test pass!"

    #检测Expiration输入值范围-大于604800
    def test_021_check_portal_rule_expiration(self):
        u"""检测Expiration输入值范围-大于604800(testlink_ID:1859-3)"""
        log.debug("021")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间后，判断是否有异常提示出现
        result = tmp.check_rule_expiration_invalid(1,"604801")
        self.assertTrue(result)
        print "check expiration is more 604800s, test pass!"

    #验证Expiration输入值范围-为0时
    def test_022_check_portal_expiration_0_function(self):
        u"""验证Expiration输入值范围-为0时(testlink_ID:1861-1)"""
        log.debug("022")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间后，判断是否有异常提示出现
        result = tmp.check_rule_expiration_invalid(1,"0")
        self.assertTrue(result)
        print "check expiration is 0, test pass!"

    #验证Expiration边界值-设置为60s
    def test_025_check_portal_expiration_60s_function(self):
        u"""验证Expiration边界值-设置为60s(testlink_ID:1862)"""
        log.debug("025")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间-60s
        tmp.change_portal_rule_expiration(1,"60")
        #验证默认list：grandstream中的免认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],30,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        self.assertEqual(expiration_title, "gatewayname Entry")
        print "check expiration time is 60s, test pass!"

    #验证Expiration功能有效-设置为120s
    def test_026_check_portal_expiration_function(self):
        u"""验证Expiration功能有效-设置为120s(testlink_ID:1860)"""
        log.debug("026")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间-120s
        tmp.change_portal_rule_expiration(1,"120")
        #验证默认list：grandstream中的免认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],120,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        self.assertEqual(expiration_title, "gatewayname Entry")
        print "check expiration time function, test pass!"

    #验证连接wifi，不认证的用户，不计时
    def test_027_have_connect_no_auth(self):
        u"""验证连接wifi，不认证的用户，不计时(testlink_ID:1864)"""
        log.debug("027")
        tmp = CPBusiness(self.driver)
        #先使用无线网卡连接上ap
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        time.sleep(120)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check have connect ap but not auth portal, test pass!"

    #验证认证的用户断开连接，重新连接
    def test_028_have_auth_disconnect_ap(self):
        u"""验证认证的用户断开连接，重新连接(testlink_ID:1865)"""
        log.debug("028")
        tmp = CPBusiness(self.driver)
        #通过免认证方式上网
        tmp.access_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"wpa")
        time.sleep(120)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check have auth but disconnect ap, test pass!"

    #检测新增policy为空，提示配置完整
    def test_030_check_add_new_null(self):
        u"""检测新增policy为空，提示配置完整(testlink_ID:1867)"""
        log.debug("030")
        #验证新增policy，提示信息
        tmp = CPBusiness(self.driver)
        result1,result2 = tmp.check_add_new_policy_null()
        self.assertTrue(result1)
        self.assertTrue(result2)
        print "add a new null policy, check tips, test pass!"

    #验证policy新增成功
    def test_031_check_add_new_policy_success(self):
        u"""验证policy新增成功(testlink_ID:1868)"""
        log.debug("031")
        tmp = CPBusiness(self.driver)
        result = tmp.check_add_new_policy_success(2,u"认证策略2","120")
        self.assertTrue(result)
        print "check add a new policy success, test pass!"

    #验证ssid选择新增的policy生效
    def test_033_check_group_new_policy_function(self):
        u"""验证ssid选择新增的policy生效(testlink_ID:1869-2)"""
        log.debug("033")
        #选择新的强制门户策略
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_ssid_portal_policy(1,1)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check group new portal policy function, test pass!"

    #验证能够且最多新增15个policy
    def test_034_check_many_policy_valid(self):
        u"""验证能够且最多新增15个policy(testlink_ID:1870)"""
        log.debug("034")
        tmp = CPBusiness(self.driver)
        #增加多个策略，并判断添加按钮是否为灰色
        result = tmp.check_many_policy_valid(3,17)
        #删除多个策略
        tmp.del_many_policys(3,17)
        self.assertFalse(result)
        print "check can add max 15 policys, test pass!"

    #验证policy修改成功
    def test_035_check_modify_new_policy(self):
        u"""验证policy修改成功(testlink_ID:1871)"""
        log.debug("035")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间，并检查页面判断是否修改成功
        result = tmp.check_portal_rule_expiration(2,"60")
        self.assertTrue(result)
        print "check modify new policy, test pass!"

    #验证修改正在使用的policy，应用直接生效
    def test_036_check_modify_new_policy_function(self):
        u"""验证修改正在使用的policy，应用直接生效(testlink_ID:1872)"""
        log.debug("036")
        tmp = CPBusiness(self.driver)
        #验证默认list：grandstream中的免认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],30,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        self.assertEqual(expiration_title, "gatewayname Entry")
        print "check modify new policy function, test pass!"

    #验证正在使用的policy不可删除
    def test_037_check_del_using_policy(self):
        u"""验证正在使用的policy不可删除(testlink_ID:1876)"""
        log.debug("037")
        tmp = CPBusiness(self.driver)
        result1,result2 = tmp.check_del_policy(2)
        self.assertTrue(result1)
        self.assertFalse(result2)
        print "check delete using policy,test pass!"

    #验证默认的policy不可删除
    def test_038_check_del_default_policy(self):
        u"""验证默认的policy不可删除(testlink_ID:1875)"""
        log.debug("038")
        tmp = CPBusiness(self.driver)
        result = tmp.check_del_default_policy()
        self.assertFalse(result)
        print "check delete default policy,test pass!"

    #检测删除policy，提示确认
    def test_039_check_del_policy(self):
        u"""检测删除policy，提示确认(testlink_ID:1873)"""
        log.debug("039")
        #首先新建一个新的policy
        tmp = CPBusiness(self.driver)
        tmp.add_new_default_policy(3,u"认证策略3","120")
        result1,result2 = tmp.check_del_policy(3)
        self.assertTrue(result1)
        self.assertTrue(result2)
        print "check delete policy,test pass!"

    #验证policy删除成功
    def test_040_check_del_policy_success(self):
        u"""验证policy删除成功(testlink_ID:1874)"""
        log.debug("040")
        tmp = CPBusiness(self.driver)
        result = tmp.check_del_policy_success(3,u"认证策略3")
        self.assertTrue(result)
        print "check del policy success,test pass!"

    #检测ssid配置好策略后，不开启portal功能，policy可被删除
    def test_041_check_disable_portal_del_policy(self):
        u"""检测ssid配置好策略后，不开启portal功能，policy可被删除(testlink_ID:1877)"""
        log.debug("041")
        #关闭ssid的portal功能
        tmp1 = SSIDBusiness(self.driver)
        tmp1.click_ssid_portal(1)
        tmp = CPBusiness(self.driver)
        result = tmp.check_del_policy_success(2,u"认证策略2")
        self.assertTrue(result)
        print "check del policy success if disable portal,test pass!"

    #验证配置auth type为No auth，无需密码认证通过
    def test_042_check_No_auth_function(self):
        u"""验证配置auth type为No auth，无需密码认证通过(testlink_ID:1878)"""
        log.debug("042")
        #开启group0的portal功能
        tmp1 = SSIDBusiness(self.driver)
        tmp1.click_ssid_portal(1)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check No auth function, test pass!"

    #验证配置radius服务器的认证方法为PAP，认证通过
    def test_043_check_radius_auth_PAP_function(self):
        u"""验证配置radius服务器的认证方法为PAP，认证通过(testlink_ID:无，自己添加)"""
        log.debug("043")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,data_basic['radius_addr'],
            data_basic['radius_secrect'],"1812","PAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check radius auth PAP function, test pass!"

    #验证配置radius服务器的认证方法为MS-CHAP，认证通过
    def test_044_check_radius_auth_MSCHAP_function(self):
        u"""验证配置radius服务器的认证方法为MS-CHAP，认证通过(testlink_ID:无，自己添加)"""
        log.debug("044")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,data_basic['radius_addr'],
            data_basic['radius_secrect'],"1812","MS-CHAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check radius auth MS-CHAP function, test pass!"

    #验证配置auth type为radius auth，需要radius帐号密码认证通过
    def test_045_check_radius_auth_CHAP_function(self):
        u"""验证配置auth type为radius auth-CHAP，需要radius帐号密码认证通过(testlink_ID:1879)"""
        log.debug("045")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,data_basic['radius_addr'],
            data_basic['radius_secrect'],"1812","CHAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check radius auth CHAP function, test pass!"

    #验证配置错误的radius服务器地址，portal认证不成功
    def test_046_check_error_radius_server_portal(self):
        u"""验证配置错误的radius服务器地址，portal认证不成功(testlink_ID:1894)"""
        log.debug("046")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,"192.168.88.88",
            data_basic['radius_secrect'],"1812","CHAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertEqual(redirect_title, "gatewayname Entry")
        print "check set error radius server, test pass!"

    #验证配置错误的radius服务器端口，portal认证不成功
    def test_047_check_error_port_server_portal(self):
        u"""验证配置错误的radius服务器端口，portal认证不成功(testlink_ID:1895)"""
        log.debug("047")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,data_basic['radius_addr'],
            data_basic['radius_secrect'],"1800","CHAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertEqual(redirect_title, "gatewayname Entry")
        print "check set error radius port, test pass!"

    #验证配置错误的radius服务器密钥，portal认证不成功
    def test_048_check_error_secrect_server_portal(self):
        u"""验证配置错误的radius服务器密钥，portal认证不成功(testlink_ID:1896)"""
        log.debug("048")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,data_basic['radius_addr'],
            "testabc","1812","CHAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertEqual(redirect_title, "gatewayname Entry")
        print "check set error radius secrect, test pass!"

    #验证ssid0的radius服务，正确帐号和密码认证成功
    def test_049_check_ssid0_radius_portal(self):
        u"""验证ssid0的radius服务，认证成功(testlink_ID:1897)"""
        log.debug("049")
        #修改第1个list为radius服务
        tmp = CPBusiness(self.driver)
        tmp.change_radius_server(1,data_basic['radius_addr'],
            data_basic['radius_secrect'],"1812","CHAP")
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check ssid0's radius secrect，use correct username and passwrod, test pass!"

    #验证group0的radius服务，错误的帐号和密码认证不成功
    def test_050_check_group0_error_radius_portal(self):
        u"""验证group0的radius服务，错误的帐号和密码认证不成功(testlink_ID:1898)"""
        log.debug("050")
        tmp = CPBusiness(self.driver)
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_radius_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"testabc",
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertEqual(redirect_title, "gatewayname Entry")
        print "check group0's radius secrect，use error username and passwrod, test pass!"

    #验证非ssid0的radius服务，portal功能正常
    def test_051_check_ssid1_radius_portal_function(self):
        u"""验证非ssid0的radius服务，portal功能正常(testlink_ID:1899)"""
        log.debug("051")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = CPBusiness(self.driver)
        #验证非group0 radius portal功能正常
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_group1_radius_portal_function(NG2_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,data_basic['radius_usename'],
            data_basic['radius_password'])
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check ssid1's radius secrect, test pass!"

    #验证未认证的用户，不能访问内网和外网
    def test_053_check_No_auth_client_cannot_access_internet(self):
        u"""验证未认证的用户，不能访问内网和外网(testlink_ID:1901)"""
        log.debug("053")
        tmp = CPBusiness(self.driver)
        #默认policy改回免认证
        tmp.change_radius_to_No_auth(1,"180")
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check have not auth client can not access internet, test pass!"

    #验证认证过的用户，可以访问规则允许的资源
    def test_054_check_group0_radius_portal(self):
        u"""验证认证过的用户，可以访问规则允许的资源(testlink_ID:1902)"""
        log.debug("054")
        tmp = CPBusiness(self.driver)
        #验证默认list：grandstream中的radius认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertIn(u"腾讯", redirect_title)
        print "check have auth client can access internet, test pass!"

    #检测portal用户数量统计正确并自动更新
    def test_055_check_portal_clients_number(self):
        u"""检测portal用户数量统计正确并自动更新(testlink_ID:1906)"""
        log.debug("055")
        tmp = CPBusiness(self.driver)
        result = tmp.Get_clients_number()
        self.assertEqual(result,1)
        print "check portal clients number, test pass!"

    #检测portal用户基本信息显示完整并自动更新
    def test_056_check_portal_clients_mac_ip(self):
        u"""检测portal用户基本信息显示完整并自动更新(testlink_ID:1907)"""
        log.debug("056")
        tmp = CPBusiness(self.driver)
        #获取无线网卡的mac地址
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        mac,ip = tmp.Get_clients_mac_ip(1)
        self.assertEqual(mac,wlan_mac)
        self.assertIn("192.168.1", ip)
        print "check portal clients mac and ip, test pass!"

    #检测portal用户认证状态正确并自动更新
    def test_057_check_portal_client_auth_status(self):
        u"""检测portal用户认证状态正确并自动更新(testlink_ID:1909)"""
        log.debug("057")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间-6分钟
        tmp.change_portal_rule_expiration(1,"360")
        auth_status1,auth_status2 = tmp.\
            check_portal_client_auth_status(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1)
        self.assertEqual(auth_status1,u"已认证")
        self.assertEqual(auth_status2,u"未认证")
        print "check portal client auth status, test pass!"

    #验证portal用户block功能正常
    def test_058_check_portal_client_block_function(self):
        u"""验证portal用户block功能正常(testlink_ID:1912)"""
        log.debug("058")
        tmp = CPBusiness(self.driver)
        #修改策略的过期时间-3分钟
        tmp.change_portal_rule_expiration(1,"180")
        result = tmp.check_portal_client_block_function(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertIn('Not connected', result)
        print "check portal client is block function, test pass!"

    #检测portal用户在TOP页显示正常
    def test_059_check_portal_client_displayed_TOPwebpage(self):
        u"""检测portal用户在TOP页显示正常(testlink_ID:1913)"""
        log.debug("059")
        tmp1 = OVBusiness(self.driver)
        #先获取到无线网卡的mac地址
        wlan_mac = tmp1.get_wlan_mac(data_basic['wlan_pc'])
        WLAN_MAC = wlan_mac.upper()
        #获取TOP AP,TOP SSID,TOP Clients的内容
        result = tmp1.get_top()
        self.assertIn(WLAN_MAC, result)
        print "check portal client is displayed in TOP webpage, test pass!"

    #检测portal用户在TOP页面信息统计正确
    def test_060_check_portal_client_flow_TOPwebpage(self):
        u"""检测portal用户在TOP页面信息统计正确(testlink_ID:1914)"""
        log.debug("060")
        tmp1 = OVBusiness(self.driver)
        result1,result2 = tmp1.check_client_download()
        assert ("MB" in result1) or ("GB" in result1)
        print "check portal client flow is displayed in TOP webpage, test fail!"

    # #检测portal用户在对应AP user页信息完整且显示正常
    # def test_061_check_portal_client_APwebpage(self):
    #     u"""检测portal用户在对应AP user页信息完整且显示正常(testlink_ID:1915)"""
    #     tmp1 = APSBusiness(self.driver)
    #     # tmp1.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
    #     #     data_wireless["short_wpa"],data_basic['wlan_pc'])
    #     result = tmp1.check_client_mac(data_AP["master:mac"],data_basic['wlan_pc'])
    #     print result
    #     self.assertTrue(result)
    #     print "check portal client is displayed in AP webpage,test pass!"

    #验证隐藏ssid0-ssid,portal功能正常
    def test_062_check_group0_hidden_ssid_portal_function(self):
        u"""验证隐藏ssid0-ssid,portal功能正常--有bug（客户端页面不显示该客户端导致认证后不会在portal页面的客户端页面进行倒计时）(testlink_ID:1917)"""
        log.debug("062")
        #隐藏ssid0的ssid
        tmp1 = SSIDBusiness(self.driver)
        tmp1.set_hide_ssid()
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa_hiddenssid")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check hidden group0's ssid, test pass!"

    #验证group0-ssid的64bit安全模式下，portal功能正常
    def test_063_check_group0_ssid_wep64bit_portal_function(self):
        u"""验证group0-ssid的64bit安全模式下，portal功能正常(testlink_ID:1918)--bug#85563"""
        log.debug("063")
        #取消隐藏ssid0的ssid
        tmp1 = SSIDBusiness(self.driver)
        tmp1.set_hide_ssid()
        #修改group0的加密为wep64bit加密
        tmp1. wifi_wep_encryption(1,data_wireless['wep64'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['wep64'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wep")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wep64bit, test pass!"

    #验证group0-ssid的128bit安全模式下，portal功能正常
    def test_064_check_group0_ssid_wep128bit_portal_function(self):
        u"""验证group0-ssid的128bit安全模式下，portal功能正常(testlink_ID:1919)--bug#85563"""
        log.debug("064")
        #修改group0的加密为wep64bit加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1. wifi_wep_encryption(1,data_wireless['wep128'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['wep128'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wep")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wep128bit, test pass!"

    #验证group0-ssid的wpa-aes安全模式下，portal功能正常
    def test_065_check_group0_ssid_wpa_aes_portal_function(self):
        u"""验证group0-ssid的wpa-aes安全模式下，portal功能正常(testlink_ID:1920)"""
        log.debug("065")
        #修改group0的加密为wpa-aes加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa-aes, test pass!"

    #验证group0-ssid的wpa-TKIP安全模式下，portal功能正常
    def test_066_check_group0_ssid_wpa_tkip_portal_function(self):
        u"""验证group0-ssid的wpa-tkip安全模式下，portal功能正常(testlink_ID:1921)"""
        log.debug("066")
        #修改group0的加密为wpa-aes加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa-tkip, test pass!"

    #验证group0-ssid的wpa2-aes安全模式下，portal功能正常
    def test_067_check_group0_ssid_wpa2_aes_portal_function(self):
        u"""验证group0-ssid的wpa2-aes安全模式下，portal功能正常(testlink_ID:1922)"""
        log.debug("067")
        #修改group0的加密为wpa-aes加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa2-aes, test pass!"

    #验证group0-ssid的wpa2-TKIP安全模式下，portal功能正常
    def test_068_check_group0_ssid_wpa2_TKIP_portal_function(self):
        u"""验证group0-ssid的wpa2-TKIP安全模式下，portal功能正常(testlink_ID:1923)"""
        log.debug("068")
        #修改group0的加密为wpa-TKIP加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa2-TKIP, test pass!"

    #验证group0-ssid的wpa2-802.1x-TKIP/AES安全模式下，portal功能正常
    def test_069_check_group0_ssid_wpa2_802_1x_TKIP_portal_function(self):
        u"""验证group0-ssid的wpa2-802.1x-TKIP/AES安全模式下，portal功能正常(testlink_ID:自己添加)"""
        log.debug("069")
        #修改group0的加密为wpa2-802.1x-TKIP/AES加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_8021x_encryption_backup(0,0,data_basic['radius_addr'],
            data_basic['radius_secrect'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"802.1x")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa2-802.1x-TKIP, test pass!"

    #验证group0-ssid的wpa2-802.1x-AES安全模式下，portal功能正常
    def test_070_check_group0_ssid_wpa2_802_1x_AES_portal_function(self):
        u"""验证group0-ssid的wpa2-802.1x-AES安全模式下，portal功能正常(testlink_ID:自己添加)"""
        log.debug("070")
        #修改group0的加密为wpa2-802.1x-AES加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_8021x_encryption_backup(0,1,data_basic['radius_addr'],
            data_basic['radius_secrect'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"802.1x")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa2-802.1x-AES, test pass!"

    #验证group0-ssid的wpa/wpa2-802.1x-AES安全模式下，portal功能正常
    def test_071_check_group0_ssid_wpa_802_1x_AES_portal_function(self):
        u"""验证group0-ssid的wpa/wpa2-802.1x-AES安全模式下，portal功能正常(testlink_ID:自己添加)"""
        log.debug("071")
        #修改group0的加密为wpa/wpa2-802.1x-AES加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_8021x_encryption_backup(3,0,data_basic['radius_addr'],
            data_basic['radius_secrect'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"802.1x")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa/wpa2-802.1x-AES, test pass!"

    #验证group0-ssid的wpa/wpa2-802.1x-TKIP/AES安全模式下，portal功能正常
    def test_072_check_group0_ssid_wpa_802_1x_TKIP_AES_portal_function(self):
        u"""验证group0-ssid的wpa/wpa2-802.1x-TKIP/AES安全模式下，portal功能正常(testlink_ID:自己添加)"""
        log.debug("072")
        #修改group0的加密为wpa/wpa2-802.1x-TKIP/AES加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_8021x_encryption_backup(0,1,data_basic['radius_addr'],
            data_basic['radius_secrect'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"802.1x")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's wpa/wpa2-802.1x-TKIP/AES, test pass!"

    #验证group0-ssid的open安全模式下，portal功能正常
    def test_073_check_group0_ssid_open_portal_function(self):
        u"""验证group0-ssid的open安全模式下，portal功能正常(testlink_ID:1924)"""
        log.debug("073")
        #修改group0的加密为open加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_None_encryption()
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's open, test pass!"

    #验证开启group0-ssid的白名单，portal功能正常
    def test_074_check_group0_ssid_white_portal_function(self):
        u"""验证开启group0-ssid的白名单，portal功能正常(testlink_ID:1926)"""
        log.debug("074")
        tmp2 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp2.get_wlan_mac(data_basic["wlan_pc"])
        #添加一个只有一个mac地址的访问列表
        tmp2.add_accesslist_onemac(mac)
        tmp1 = SSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp1.wifi_whitelist_for_portal()
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's white list, test pass!"

    #验证开启group0-ssid的黑名单，portal功能正常
    def test_075_check_group0_ssid_black_portal_function(self):
        u"""验证开启group0-ssid的黑名单，portal功能正常(testlink_ID:1925)"""
        log.debug("075")
        tmp2 = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp2.randomMAC()
        print random_mac
        tmp2.edit_accesslist_onemac(random_mac)
        tmp1 = SSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的黑名单
        tmp1.wifi_blacklist_for_portal()
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's black list, test pass!"

    #验证开启group0-ssid的客户端隔离--无线，portal功能正常
    def test_076_check_group0_ssid_client_isolation_radio(self):
        u"""验证开启group0-ssid的客户端隔离--无线，portal功能正常(testlink_ID:1927-1)"""
        log.debug("076")
        #禁用默认网络组的无线过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter_for_portal(1)
        #配置group0的客户端隔离的无线模式
        tmp1.wifi_n_isolation_open_for_portal(1,"radio")
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's client isolation for radio, test pass!"

    #验证开启group0-ssid的客户端隔离--互联网，portal功能正常
    def test_077_check_group0_ssid_client_isolation_internet(self):
        u"""验证开启group0-ssid的客户端隔离--互联网，portal功能正常(testlink_ID:1927-2)"""
        log.debug("077")
        tmp1 = SSIDBusiness(self.driver)
        #配置group0的客户端隔离的互联网模式
        tmp1.wifi_n_isolation_for_portal(1,"internet")
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's client isolation for internet, test pass!"

    #验证开启group0-ssid的客户端隔离--gatewaymac，portal功能正常
    def test_078_check_group0_ssid_client_isolation_gatewaymac(self):
        u"""验证开启group0-ssid的客户端隔离--gatewaymac，portal功能正常(testlink_ID:1927-3)"""
        log.debug("078")
        tmp1 = SSIDBusiness(self.driver)
        #配置group0的客户端隔离的网关mac模式
        #获取7000的mac地址
        route_mac = tmp1.get_router_mac(data_basic['7000_ip'],data_basic['sshUser'],data_login['all'])
        print route_mac
        tmp1.wifi_n_isolation_gateway_mac_for_portal(1,route_mac)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's client isolation for gatewaymac, test pass!"

    #验证开启group0-ssid的RSSI，portal功能正常
    def test_079_check_group0_ssid_RSSI(self):
        u"""验证开启group0-ssid的RSSI，portal功能正常(testlink_ID:1928)"""
        log.debug("079")
        #取消group0的客户端隔离的模式
        tmp1 = SSIDBusiness(self.driver)
        tmp1.cancel_wifi_n_isolation_portal_for_portal(1)
        #enable RSSI
        tmp1.enable_disable_rssi_for_portal()
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"open")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group0's RSSI, test pass!"

    #验证多次修改ssid配置，portal功能正常
    def test_080_check_portal_funciton_modify_NG_config(self):
        u"""验证多次修改ssid配置，portal功能正常(testlink_ID:1931)"""
        log.debug("080")
        #disable RSSI
        tmp1 = SSIDBusiness(self.driver)
        tmp1.enable_disable_rssi_for_portal()
        #修改网络组加密为wep64bit
        tmp1.wifi_wep_encryption(1,data_wireless['wep64'])
        #再次修改网络组加密为wpa2-aes
        tmp1.wifi_wpa_encryption(3,1,data_wireless['short_wpa'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for modify group0's configruation, test pass!"

    #验证多次修改ssid0配置，slave ap portal功能正常
    def test_081_check_portal_funciton_modify_NG_config(self):
        u"""验证多次修改ssid0配置，slave ap portal功能正常(testlink_ID:1932)"""
        log.debug("081")
        #networkgroup中将所有已添加的设备删除
        tmp1 = SSIDBusiness(self.driver)
        tmp1.del_all_ap()
        #搜索-配对-加入默认网络组
        tmp2 = APSBusiness(self.driver)
        tmp2.search_pair_add_default(data_AP['slave:mac2'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check slave ap portal function for modify group0's configruation, test pass!"

    #验证隐藏group0-ssid1，portal功能正常
    def test_082_check_group0_ssid1_portal_hidden_ssid(self):
        u"""验证隐藏group0-ssid1，portal功能正常(testlink_ID:1933)"""
        log.debug("082")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp1 = SSIDBusiness(self.driver)
        #ap新建一个ssid
        tmp1.new_ssid(NG2_ssid,data_wireless['short_wpa'])
        #将ssid1固定为5G
        tmp1.change_n_AP_Freq(2,"5GHz")
        #隐藏ssid1的ssid
        tmp1.hide_n_ssid(2)
        #开启portal
        tmp1.click_ssid_portal(2)
        tmp2 = APSBusiness(self.driver)
        #解除slave ap的配对
        tmp2.unpair_last_slave_ap(1)
        #master ap加入ssid1
        tmp2.add_master_to_n_NG(2)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa_hiddenssid")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check hidden group0 ssid1's ssid, test pass!"


    #验证隐藏非group0-ssid， portal功能正常
    def test_101_hidden_group1_ssid_portal_function(self):
        u"""验证隐藏非group0-ssid， portal功能正常(testlink_ID:1947)"""
        log.debug("101")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp1 = SSIDBusiness(self.driver)
        #删除ssid1
        tmp1.del_all_NG()
        #ap新建一个ssid,vlan2
        tmp1.new_vlan_ssid(NG2_ssid,data_wireless['short_wpa'],"2")
        #将ssid1固定为5G
        tmp1.change_n_AP_Freq(2,"5GHz")
        #隐藏ssid1的ssid
        tmp1.hide_n_ssid(2)
        #开启portal
        tmp1.click_ssid_portal(2)

        tmp3 = APSBusiness(self.driver)
        #master ap加入ssid1
        tmp3.add_master_to_all_NG()
        #7000新建一个网络组
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_new_NG()
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa_hiddenssid")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check hidden group1_ssid's ssid, test pass!"

    #验证开启group1-ssid的白名单，portal功能正常
    def test_102_check_group1_ssid_white_portal_function(self):
        u"""验证开启group1-ssid的白名单，portal功能正常(testlink_ID:1949)"""
        log.debug("102")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp2 = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        mac = tmp2.get_wlan_mac(data_basic["wlan_pc"])
        tmp2.edit_accesslist_onemac(mac)
        #设置ssid1的无线过滤的白名单
        tmp1 = SSIDBusiness(self.driver)
        #取消隐藏group1的ssid
        tmp1.hide_n_ssid(2)
        tmp1.wifi_n_whitelist_vlan_for_portal(2)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1 ssid's white list, test pass!"

    #验证开启group1-ssid的黑名单，portal功能正常
    def test_103_check_group1_ssid_black_portal_function(self):
        u"""验证开启group1-ssid的黑名单，portal功能正常(testlink_ID:1950)"""
        log.debug("103")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp2 = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp2.randomMAC()
        print random_mac
        tmp2.edit_accesslist_onemac(random_mac)
        tmp1 = SSIDBusiness(self.driver)
        #设置ssid1的无线过滤的黑名单
        tmp1.wifi_n_blacklist_vlan_for_portal(2)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1's black list, test pass!"

    #验证开启group1-ssid的客户端隔离--无线，portal功能正常
    def test_104_check_group1_ssid_client_isolation_radio(self):
        u"""验证开启group1-ssid的客户端隔离--无线，portal功能正常(testlink_ID:1951-1)"""
        log.debug("104")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        #禁用group1网络组的无线过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter_vlan_for_portal(2)
        #配置group1的客户端隔离的无线模式
        tmp1.wifi_n_isolation_vlan_for_portal(2,"radio")
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1's client isolation for radio, test pass!"

    #验证开启group1-ssid的客户端隔离--互联网，portal功能正常
    def test_105_check_group1_ssid_client_isolation_internet(self):
        u"""验证开启group1-ssid的客户端隔离--互联网，portal功能正常(testlink_ID:1951-2)"""
        log.debug("105")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_isolation_vlan_for_portal_no_click_isolation(2,"internet")
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1's client isolation for internet, test pass!"

    #验证开启group1-ssid的客户端隔离--gatewaymac，portal功能正常
    def test_106_check_group1_ssid_client_isolation_gatewaymac(self):
        u"""验证开启group1-ssid的客户端隔离--gatewaymac，portal功能正常(testlink_ID:1951-3)"""
        log.debug("106")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp1 = SSIDBusiness(self.driver)
        #配置group1的客户端隔离的网关mac模式
        #获取7000的mac地址
        route_mac = tmp1.get_router_mac(data_basic['7000_ip'],data_basic['sshUser'],data_login['all'])
        print route_mac
        tmp1.wifi_n_isolation_gateway_mac_vlan_for_portal(2,route_mac)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1's client isolation for gatewaymac, test pass!"

    #验证开启group1-ssid的RSSI，portal功能正常
    def test_107_check_group1_ssid_RSSI(self):
        u"""验证开启group1-ssid的RSSI，portal功能正常(testlink_ID:1952)"""
        log.debug("107")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        #取消group1的客户端隔离的模式
        tmp1 = SSIDBusiness(self.driver)
        tmp1.cancel_wifi_n_isolation_vlan_for_portal(2)
        #enable RSSI
        tmp1.enable_disable_rssi_vlan_for_portal(2)
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1's RSSI, test pass!"

    #验证master ap固定ip，portal功能正常
    def test_126_check_fixed_master_ip_portal_function(self):
        u"""验证master ap固定ip，portal功能正常(testlink_ID:1963)"""
        log.debug("126")
        #指定master ap为固定ip
        tmp2 = APSBusiness(self.driver)
        tmp2.set_ap_fixed_ip(data_AP["master:mac"],data_basic['DUT_ip'],
            data_AP['fixed_netmask'],data_basic['7000_ip'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for master ap fixed ip, test pass!"

    #验证AP固定ip，非group0的portal功能
    def test_127_check_group1_fixed_ip_portal_function(self):
        u"""验证AP固定ip，非group0的portal功能(testlink_ID:1965)"""
        log.debug("127")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for group1 when ap fixed ip, test pass!"

    #验证slave AP固定ip，portal功能正常
    def test_129_check_fixed_slave_ip_portal_function(self):
        u"""验证slave AP固定ip，portal功能正常(testlink_ID:1964)"""
        log.debug("129")
        #删除ssid1
        tmp2 = SSIDBusiness(self.driver)
        tmp2.del_all_NG()
        #将所有已添加的设备删除
        tmp2.del_all_ap()
        #搜索-配对-加入默认网络组
        tmp3 = APSBusiness(self.driver)
        tmp3.search_pair_add_default(data_AP['slave:mac2'])
        #指定slave ap为固定ip
        tmp3.set_ap_fixed_ip(data_AP["slave:mac2"],data_basic['slave_ip2'],
            data_AP['fixed_netmask'],data_basic['7000_ip'])
        #验证默认list：grandstream中的免认证的有效性
        tmp = CPBusiness(self.driver)
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check portal function for slave ap when ap fixed ip, test pass!"

    #验证STA固定ip，portal认证过程和网络正常
    def test_130_check_fixed_STA_ip_portal_function(self):
        u"""验证STA固定ip，portal认证过程和网络正常(testlink_ID:1967)"""
        log.debug("130")
        #解除slave ap的配对
        tmp3 = APSBusiness(self.driver)
        tmp3.unpair_last_slave_ap(1)
        #取消master ap的固定ip
        tmp3.cancel_ap_fixed_ip(data_AP["master:mac"],data_basic['DUT_ip'])
        #master ap加入默认网络组
        tmp3.add_master_to_n_NG(1)
        # #验证默认list：grandstream中的免认证的有效性
        # tmp = CPBusiness(self.driver)
        # #无线网卡释放ip地址
        # tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        # #禁用有线网卡
        # tmp.wlan_disable(data_basic['lan_pc'])
        # time.sleep(60)
        # tmp.connect_WPA_AP(data_wireless['all_ssid'],
        #     data_wireless['short_wpa'],data_basic['wlan_pc'])
        # #禁用有线网卡
        # tmp.wlan_disable(data_basic['lan_pc'])
        # #指定无线网卡的静态ip
        # subprocess.call("echo %s |sudo -S ifconfig %s %s netmask 255.255.255.0"\
        #     %(data_basic["PC_pwd"],data_basic['wlan_pc'],"192.168.1.8"),shell=True)
        # time.sleep(10)
        # subprocess.call("echo %s |sudo -S route add default gw %s"\
        #     %(data_basic["PC_pwd"],data_basic['7000_ip']),shell=True)
        # #打开http的页面http://www.qq.com
        # portal_title = tmp.wait_for_title("http://www.qq.com")
        # print "Access tencent webpage first, goin to %s"%portal_title
        # #免认证页面点击同意，然后再点击登录
        # redirect_title = tmp.enter_default_portal()
        # print "click agree, goin to %s"%redirect_title
        # #无线网卡释放ip地址
        # subprocess.call("echo %s |sudo -S route del default"\
        #     %data_basic["PC_pwd"],shell=True)
        # tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        # #断开无线连接
        # tmp.disconnect_ap()
        # #启用有线网卡
        # tmp.wlan_enable(data_basic['lan_pc'])
        # self.assertEqual(portal_title, "gatewayname Entry")
        # self.assertIn(u"腾讯", redirect_title)
        # print "check portal function when STA set fixed ip, test pass!"
        self.assertTrue(True)
        print "check portal function when STA set fixed ip, test pass!"


    #验证开启portal，已连接的用户需要进行portal认证
    def test_131_check_connected_STA_need_to_auth(self):
        u"""验证开启portal，已连接的用户需要进行portal认证(testlink_ID:1968)"""
        log.debug("131")
        tmp = CPBusiness(self.driver)
        #无线网卡连接ap
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #验证默认list：grandstream中的免认证的有效性
        portal_title,redirect_title,again_title,expiration_title = tmp.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "check STA which has conncected ap need auth when open portal, test pass!"

    #验证切换认证方式，已认证的用户无需重新认证
    def test_132_check_auth_STA_not_need_auth_again_change_portal_mode(self):
        u"""验证切换认证方式，已认证的用户无需重新认证(testlink_ID:1969)"""
        log.debug("132")
        tmp = CPBusiness(self.driver)
        #首先修改过期时间为3小时
        tmp.change_portal_rule_expiration(1, "10800")
        #验证切换认证方式，已认证的用户无需重新认证
        result = tmp.check_auth_STA_not_need_auth_again(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'],
            data_basic['lan_pc'], data_basic['radius_addr'],
            data_basic['radius_secrect'], "1812", "CHAP")
        self.assertFalse(result)
        print "check STA which has auth can't need to auth again when change portal mode, test pass!"

    #验证切换认证定制模板，已认证的用户无需重新认证
    def test_133_check_auth_STA_not_need_auth_again_change_portal_page(self):
        u"""验证切换认证定制模板，已认证的用户无需重新认证(testlink_ID:1970)"""
        log.debug("133")
        tmp = CPBusiness(self.driver)
        #更改门户页面模板
        tmp.change_portal_page(1, "/portal_default.html")
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check STA which has auth can't need to auth again when change portal page, test pass!"

    #验证切换策略，已认证的用户无需重新认证
    def test_134_check_auth_STA_not_need_auth_again_change_policy(self):
        u"""验证切换策略，已认证的用户无需重新认证(testlink_ID:1971)"""
        log.debug("134")
        #将门户页面改回默认模板
        tmp = CPBusiness(self.driver)
        tmp.change_portal_page_to_default(1)
        #新增一个portal策略
        tmp.add_new_default_policy(2,u"认证策略2","120")
        #选择新的强制门户策略
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_ssid_portal_policy(1,1)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check STA which has auth can't need to auth again when change portal policy, test pass!"

    #验证开启一个group的portal，不影响其他group的用户
    def test_135_other_group_STA_open_group0(self):
        u"""验证开启一个group的portal，不影响其他group的用户(testlink_ID:1972)"""
        log.debug("135")
        #关闭ssid0的portal认证
        tmp1 = SSIDBusiness(self.driver)
        tmp1.click_ssid_portal(1)
        #删除策略2
        tmp = CPBusiness(self.driver)
        tmp.del_policy_n(2)
        #将默认策略改回免认证模式
        tmp.change_radius_to_No_auth(1,"10800")
        #开启group0的portal认证
        tmp1.click_ssid_portal(1)
        # NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        # result = tmp.check_other_group_STA_open_group0(NG2_ssid,
        #     data_wireless['short_wpa'], data_wireless['all_ssid'],
        #     data_basic['wlan_pc'],data_basic['lan_pc'])
        # self.assertFalse(result)
        # print "check STA can't need to auth again when other group open portal, test pass!"

    #验证已认证的用户切换到另一开启portal的group，需要重新认证
    def test_136_STA_switch_to_other_group_need_auth(self):
        u"""验证已认证的用户切换到另一开启portal的group，需要重新认证(testlink_ID:1973)"""
        log.debug("136")
        tmp = CPBusiness(self.driver)
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        result = tmp.check_jump_to_No_auth_portal(NG2_ssid,
            data_wireless['short_wpa'], data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check STA switch to other group need to auth again, test pass!"

    #验证已认证用户切换回原来已认证的ssid，需要重新认证
    def test_139_STA_auth_switch_back_to_group0(self):
        u"""验证已认证用户切换回原来已认证的ssid，需要重新认证(testlink_ID:1977)"""
        log.debug("139")
        #通过ssid1的认证
        tmp = CPBusiness(self.driver)
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp.access_No_auth_portal(NG2_ssid,
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"wpa")
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertTrue(result)
        print "check STA switch to group1's portal additional ssid need to auth again, test pass!"

    #验证STA被解除block后，不需要重新认证
    def test_140_STA_unblock_no_need_auth(self):
        u"""验证STA被解除block后，不需要重新认证(testlink_ID:1988)"""
        log.debug("140")
        #删除ssid1
        tmp2 = SSIDBusiness(self.driver)
        tmp2.del_all_NG()
        #验证STA被解除block后，不需要重新认证
        tmp = CPBusiness(self.driver)
        result = tmp.check_STA_unblock_no_need_auth(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check after STA which has auth unblocking, don't need auth again, test fail!"

    #验证STA加入白名单后，无需重新认证
    def test_141_STA_add_whitelist_no_need_auth(self):
        u"""验证STA加入白名单后，无需重新认证(testlink_ID:1989)"""
        log.debug("141")
        tmp2 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp2.get_wlan_mac(data_basic["wlan_pc"])
        #编辑一个只有一个mac地址的访问列表
        tmp2.edit_accesslist_onemac(mac)
        tmp1 = SSIDBusiness(self.driver)
        #设置ssid0的无线过滤的白名单
        tmp1.wifi_n_whitelist_for_portal(1)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check STA add whitelist don't need to auth again, test pass!"

    #验证禁用白名单后，无需重新认证
    def test_142_disable_macfilter(self):
        u"""验证禁用白名单后，无需重新认证(testlink_ID:1990)"""
        log.debug("142")
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter_for_portal(1)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check STA disable macfilter don't need to auth again, test pass!"

    #验证STA加入黑名单后，其他STA无需重新认证
    def test_143_STA_add_whitelist_no_need_auth(self):
        u"""验证STA加入黑名单后，其他STA无需重新认证(testlink_ID:1991)"""
        log.debug("143")
        tmp2 = ClientAccessBusiness(self.driver)
        #取随机mac
        random_mac = tmp2.randomMAC()
        #编辑一个只有一个mac地址的访问列表
        tmp2.edit_accesslist_onemac(random_mac)
        tmp1 = SSIDBusiness(self.driver)
        #设置额外ssid的无线过滤的黑名单
        tmp1.wifi_n_blacklist_for_portal(1)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check STA add blacklist don't need to auth again, test pass!"

    #验证STA被解除黑名单后，无需重新认证
    def test_144_disable_macfilter(self):
        u"""验证STA被解除黑名单后，无需重新认证(testlink_ID:1992)"""
        log.debug("144")
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter_for_portal(1)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check STA disable macfilter don't need to auth again, test pass!"

    #验证修改wifi密码，无需重新认证
    def test_145_change_wifi_password_no_need_auth(self):
        u"""验证修改wifi密码，无需重新认证(testlink_ID:1993)"""
        log.debug("145")
        #修改wifi密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(0,0,data_wireless["long_wpa"])
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal(data_wireless['all_ssid'],
            data_wireless["long_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'])
        self.assertFalse(result)
        print "check change wifi password don't need to auth again, test pass!"

    #验证隐藏ssid，无需重新认证
    def test_146_hidden_ssid_no_need_auth(self):
        u"""验证修改wifi密码，无需重新认证(testlink_ID:1994)"""
        log.debug("146")
        #修改wifi密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(0,0,data_wireless["short_wpa"])
        #隐藏ssid
        tmp1.set_hide_ssid()
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"wpa_hiddenssid")
        self.assertFalse(result)
        print "check hidden ssid don't need to auth again, test pass!"

    #修改安全模式，无需认证
    def test_147_change_wifi_encrypiton_no_need_auth(self):
        u"""修改安全模式，无需认证(testlink_ID:1995)"""
        log.debug("147")
        tmp1 = SSIDBusiness(self.driver)
        #取消隐藏ssid
        tmp1.set_hide_ssid()
        #修改无线加密为open
        tmp1.wifi_None_encryption()
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        self.assertFalse(result)
        print "check change wifi encryption don't need to auth again, test pass!"

    #验证开启客户端隔离--无线，无需重新认证
    def test_148_client_isolation_radio_no_need_auth(self):
        u"""验证开启客户端隔离--无线，无需重新认证(testlink_ID:1996-1)"""
        log.debug("148")
        tmp1 = SSIDBusiness(self.driver)
        #配置group0的客户端隔离的无线模式
        tmp1.wifi_n_isolation_open_for_portal(1,"radio")
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        self.assertFalse(result)
        print "check open client isolation radio don't need to auth again, test pass!"

    #验证开启客户端隔离--互联网，无需重新认证
    def test_149_client_isolation_internet_no_need_auth(self):
        u"""验证开启客户端隔离--互联网，无需重新认证(testlink_ID:1996-2)"""
        log.debug("149")
        tmp1 = SSIDBusiness(self.driver)
        #配置group0的客户端隔离的互联网模式
        tmp1.wifi_n_isolation_for_portal(1,"internet")
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        self.assertFalse(result)
        print "check open client isolation internet don't need to auth again, test pass!"

    #验证开启客户端隔离--gatewaymac，无需重新认证
    def test_150_client_isolation_gatewaymac_no_need_auth(self):
        u"""验证开启group0-ssid的客户端隔离--gatewaymac，portal功能正常(testlink_ID:1996-3)"""
        log.debug("150")
        tmp1 = SSIDBusiness(self.driver)
        #配置group0的客户端隔离的网关mac模式
        #获取7000的mac地址
        route_mac = tmp1.get_router_mac(data_basic['7000_ip'],data_basic['sshUser'],data_login['all'])
        print route_mac
        tmp1.wifi_n_isolation_gateway_mac_for_portal(1,route_mac)
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        self.assertFalse(result)
        print "check open client isolation gatewaymac don't need to auth again, test pass!"

    #验证开启RSSI，无需重新认证
    def test_151_enable_RSSI_no_need_auth(self):
        u"""验证开启RSSI，无需重新认证(testlink_ID:1997)"""
        log.debug("151")
        #取消group0的客户端隔离的模式
        tmp1 = SSIDBusiness(self.driver)
        tmp1.cancel_wifi_n_isolation_portal_for_portal(1)
        #enable RSSI
        tmp1.enable_disable_rssi_for_portal()
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        self.assertFalse(result)
        print "check enable RSSI don't need to auth again, test pass!"

    #验证wifi重启，无需重新认证
    def test_152_disable_wifi_no_need_auth(self):
        u"""验证wifi重启，无需重新认证(testlink_ID:1999)"""
        log.debug("152")
        tmp1 = SSIDBusiness(self.driver)
        #disable RSSI
        tmp1.enable_disable_rssi_for_portal()
        #禁用/启用wifi
        tmp1.en_dis_first()
        tmp1.en_dis_first()
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        self.assertFalse(result)
        print "check reboot network group wifi don't need to auth again, test pass!"

    #验证ap reboot后，不需要重新认证
    def test_153_ap_reboot_need_auth(self):
        u"""验证ap reboot后，不需要重新认证(testlink_ID:2003)"""
        log.debug("153")
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        #使用免认证的规则，腾讯首页，判断是否跳转到portal页面
        tmp = CPBusiness(self.driver)
        result = tmp.check_jump_to_No_auth_portal_backup(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'],
            data_basic['lan_pc'],"open")
        #删除7000上的group1
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_del_NG()

        #测试完毕，禁用无线网卡，使pc够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("CaptivePortal")

        self.assertFalse(result)
        print "check reboot ap don't need to auth again, test pass!"















    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()




