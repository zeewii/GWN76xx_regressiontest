#coding=utf-8
#作者：曾祥卫
#时间：2017.03.10
#描述：用例层代码，调用login_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from setupwizard.setupwizard_business import SWBusiness
from connect.ssh import SSH
from data import data
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_AP = data.data_AP()
log = Log("Login")
class TestLogin(unittest.TestCase):
    u"""测试登录的用例集(runtime:8m)"""
    def setUp(self):
        # firefox_profile = webdriver.FirefoxProfile(data_basic['firefox_profile'])
        # self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)

    #登录路由后台把AP恢复出厂设置
    def test_001_factory_reset(self):
        u"""登录路由后台把AP恢复出厂设置"""
        log.debug("001")
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录GWN7610的web界面
        Lg.login(data_basic['superUser'],data_login['all'])
        Lg.login_again()
        tmp = UpgradeBusiness(self.driver)
        tmp.web_factory_reset_backup(data_basic['DUT_ip'])
        time.sleep(30)
        #登录AP后台取出管理员密码
        tmp1 = SSH(data_basic['DUT_ip'],data_basic['super_defalut_pwd'])
        result = tmp1.ssh_cmd(data_basic['sshUser'],"uci show grandstream.general.admin_password")
        print result
        #描述：启用无线网卡
        tmp.wlan_enable(data_basic['wlan_pc'])
        assert "='admin'" in result,"reset the AP defalut config in ssh,fail!"
        print "reset the AP defalut config in ssh,pass!"

    #第一次登录页面需要设置管理员和用户密码
    def test_002_first_login(self):
        u"""第一次登录页面需要设置管理员和用户密码"""
        log.debug("002")
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录GWN76xx的web界面
        Lg.login(data_basic['superUser'],data_basic["super_defalut_pwd"])
        #第一次登录页面需要设置管理员和用户密码
        Lg.set_super_user_pwd(data_login["all"],data_login["all"],\
                              data_login["all"],data_login["all"])
        ##点击下次不再显示
        tmp1 = SWBusiness(self.driver)
        tmp1.hidenexttime()
        tmp1.close_wizard()
        #检测是否登录成功
        result = Lg.login_test()
        assert result ,"login AP webpage first and set admin and user password ,test fail!"
        print "login AP webpage first and set admin and user password ,test pass!"

    #router mac地址登录web UI（llmnr）
    def test_003_router_mac_login(self):
        u"""router mac地址登录web UI（llmnr）"""
        log.debug("003")
        #登录AP
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        mac = Lg.mac_drop(data_AP['master:mac'])
        self.driver.get("https://gwn_%s.local"%mac)
        self.driver.implicitly_wait(10)
        #调用实例的登录GWN7002w的web界面
        Lg.login(data_basic['superUser'],data_login["all"])
        #检测是否登录成功
        result = Lg.login_test()
        assert result ,"Check using router mac to login ,test fail!\n\n\n\
        TEST STEPS of THE CASE:\n\
        1.Open AP's url webpage by AP mac:https://gwn_mac.local.\n\
        2.Input user and password to login ap.\n\
        3.Confirm can login AP's webpage.\n"
        print "Check using router mac to login,test pass!"

    #输入管理员的用户名和密码，登录GWN7610的web界面
    def test_004_admin_login(self):
        u"""输入管理员的用户名和密码，登录GWN7610的web界面"""
        log.debug("004")
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录GWN7610的web界面
        Lg.login(data_basic['superUser'],data_login['all'])
        #检测是否登录成功
        result = Lg.login_test()
        assert result ,"login AP webpage,test fail!"
        print "login AP webpage,test pass!"

    #输入user的用户名和密码，登录GWN7610的web界面
    def test_005_user_login(self):
        u"""输入user的用户名和密码，登录GWN7610的web界面"""
        log.debug("005")
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录GWN7610的web界面
        Lg.login(data_basic['user'],data_login['all'])
        #检测是否登录成功
        result = Lg.login_test()
        #测试完毕，禁用无线网卡，使pc能够上网
        Lg.dhcp_release_wlan(data_basic['wlan_pc'])
        Lg.disconnect_ap()
        Lg.wlan_disable(data_basic['wlan_pc'])
        assert result ,"login AP webpage,test fail!"
        print "login AP webpage,test pass!"


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
