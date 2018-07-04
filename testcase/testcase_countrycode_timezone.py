#coding=utf-8
#作者：曾祥卫
#时间：2017.11.15
#描述：country code and time zone的用例集

import unittest,time
from selenium import webdriver
from system_settings.maintenance.access.access_business import AccessBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from system_settings.maintenance.basic.basic_business import BasicBusiness
from login.login_business import LoginBusiness
from data import data
from access_points.aps_business import APSBusiness
from navbar.navbar_business import NavbarBusiness
from connect.ssh import SSH


data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()

class TestCountryCodeTimeZone(unittest.TestCase):
    u"""测试国家代码和时区用例集(runtime:9h)"""
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
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"


    #设置不同的国家，检查当前可用信道，Tx-Power参数是否生效
    def test_002_country_code(self):
        u"""修改国家代码，验证信道与Tx-Power是否与预期一致"""
        #修改2.4g和5g的空间流
        tmp2 = APSBusiness(self.driver)
        #登录web页面获取DUT的hostname
        DUT_hostname = tmp2.get_DUT_hostname()
        if DUT_hostname == "GWN7610":
            tmp2.change_2g4_active_streams("3")
            tmp2.change_5g_active_streams("3")
        elif DUT_hostname == "GWN7600":
            tmp2.change_2g4_active_streams("2")
            tmp2.change_5g_active_streams("2")
        elif DUT_hostname == "GWN7600LR":
            tmp2.change_2g4_active_streams("2")
            tmp2.change_5g_active_streams("2")
        elif DUT_hostname == "GWN7602W":
            tmp2.change_2g4_active_streams("2")
            tmp2.change_5g_active_streams("2")
        tmp = BasicBusiness(self.driver)
        chan_2g4,chan_5g,rate_2g4,rate_5g_1,rate_5g_2 = \
            tmp.check_country_channel_power(data_basic['DUT_ip'],\
               data_basic['sshUser'],data_login['all'])
        assert (False not in chan_2g4) and (False not in chan_5g) \
               and (False not in rate_2g4) and (False not in rate_5g_1) \
               and (False not in rate_5g_2),\
            "check different country code,test fail!"
        print "check different country code,test pass!"

    #选择不同时区，然后登录ap后台来判断是否正确(testlink_ID:776)---bug89429
    def test_003_check_timezone(self):
        u"""选择不同时区，然后登录ap后台来判断是否正确(testlink_ID:776)---bug89429"""
        tmp = BasicBusiness(self.driver)
        #选择不同时区，然后登录ap后台来判断是否正确
        result = tmp.check_time_zone()
        print result

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("countrycodetimezone")

        assert False not in result,"check different time zone,test fail!"
        print "check different time zone,test pass!"



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
