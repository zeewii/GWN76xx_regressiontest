#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：用例集，调用setupwizard_business

import unittest
from selenium import webdriver

from login.login_business import LoginBusiness
from setupwizard.setupwizard_business import SWBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from connect.ssh import SSH
from data import data
from data.logfile import Log
data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_AP = data.data_AP()
log = Log("Setupwozard")
class TestSetupWizard(unittest.TestCase):
    u"""测试设置向导的用例集(runtime:0.5h)"""
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

        tmp = UpgradeBusiness(self.driver)
        #描述：启用无线网卡
        tmp.wlan_enable(data_basic['wlan_pc'])
        #rsyslog服务器准备
        tmp.ready_rsyslog()
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        tmp1 = SWBusiness(self.driver)
        #关闭设置向导窗口
        tmp1.close_wizard()
        #设置系统系统日志的地址
        tmp.syslog_uri()
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #初次登陆显示设置向导(testlink_ID:1289)
    def test_002_setupwizard_first_login(self):
        u"""初次登陆显示设置向导(testlink_ID:1289)"""
        log.debug("002")
        value = SWBusiness(self.driver)
        result = value.check_wizard()
        print result
        assert result,"test login webpage first display setupwizard,test fail!"
        print "test login webpage first display setupwizard,test pass!"

    #"下次不显示"的默认状态没有勾选(testlink_ID:1290)
    def test_003_setupwizard_default_config(self):
        u"""下次不显示的默认状态没有勾选(testlink_ID:1290)"""
        log.debug("003")
        tmp = SWBusiness(self.driver)
        #下次不再显示是否被选中
        result = tmp.get_hidenexttime()
        print result
        assert result == None,"Don't show me this again has not been checked,test fail!"
        print "Don't show me this again has not been checked,test pass!"

    #提示信息检查(testlink_ID:1291)
    def test_004_setupwizard_startcontent(self):
        u"""提示信息检查(testlink_ID:1291)"""
        log.debug("004")
        tmp = SWBusiness(self.driver)
        #获取提示信息
        result = tmp.get_startcontent()
        print result
        assert (u'此设置向导将会指导您完成GWN设备的基本设置. 若不想下次再自动显示此向导, 可勾选下方的"下次不再显示", 当然, 您也可以通过点击上方操作栏的帮助图标进入此向导.' \
               or "The setup wizard will guide you through the basic setup of your GWN product. If you don't wish to see this wizard again, please check the box below. You can always maintenance the setup wizard by selecting the gear icon at the top right of the screen.") \
               in result,"Start content check,test fail!"
        print "Start content check,test pass!"

    #Dis下次不再显示(testlink_ID:1292_1)
    def test_005_setupwizard_disable(self):
        u"""Dis下次不再显示,关闭设备向导，点击其他页面判断是否有无设置向导窗口(testlink_ID:1292_1)"""
        log.debug("005")
        #关闭设备向导，点击其他页面判断是否有无设置向导窗口
        tmp = SWBusiness(self.driver)
        result = tmp.close_wizard_click_othermenu()
        print result
        assert result == False,"test disable don't display nexttime,test fail!"
        print "test disable don't display nexttime,test pass!"

    #Dis下次不再显示(testlink_ID:1292_2)
    def test_006_setupwizard_disable(self):
        u"""Dis下次不再显示,再次登录依然显示设置向导窗口(testlink_ID:1292_2)"""
        log.debug("006")
        #再次登录依然显示设置向导窗口
        tmp = SWBusiness(self.driver)
        result = tmp.check_wizard()
        print result
        assert result == True,"test disable don't display nexttime,test fail!"
        print "test disable don't display nexttime,test pass!"


    #En下次不再显示(testlink_ID:1293_1)
    def test_007_setupwizard_enable(self):
        u"""En下次不再显示，点击下次不再显示，点击其他页面判断是否有无设置向导窗口(testlink_ID:1293_1)"""
        log.debug("007")
        tmp = SWBusiness(self.driver)
        ##点击下次不再显示
        tmp.hidenexttime()
        result = tmp.close_wizard_click_othermenu()
        print result
        assert result == False,"test enable don't display nexttime,test fail!"
        print "test enable don't display nexttime,test pass!"

    #En下次不再显示(testlink_ID:1293_2)
    def test_008_setupwizard_enable(self):
        u"""En下次不再显示，再次登录不再显示设置向导窗口(testlink_ID:1293_2)"""
        log.debug("008")
        #再次登录不再显示设置向导窗口
        tmp = SWBusiness(self.driver)
        result = tmp.check_wizard()
        print result
        assert result == False,"test enable don't display nexttime,test fail!"
        print "test enable don't display nexttime,test pass!"


    #其他页面点击问号打开向导(testlink_ID:1294)
    def test_009_setupwizard_other(self):
        u"""其他页面点击向导(testlink_ID:1294)"""
        log.debug("009")
        #进入接入点确定没有设置向导窗口
        tmp = SWBusiness(self.driver)
        result = tmp.othermenu_click()
        print result
        assert result == [True,True,True,True],"test click wizard in other webpage,test fail!"
        print "test click wizard in other webpage,test pass!"

    #AP发现-master AP状态(testlink_ID:1295)
    def test_010_setupwizard_masterAP_status(self):
        u"""AP发现-master AP状态(testlink_ID:1295)"""
        log.debug("010")
        tmp = SWBusiness(self.driver)
        result = tmp.AP_status(data_AP['master:mac'],data_AP['slave:mac1'],
                               data_AP['slave:mac2'])
        print result
        assert result == [True,True],"test master AP status,test fail!"
        print "test master AP status,test pass!"

    #AP发现-slave AP(testlink_ID:1296)
    def test_011_setupwizard_slaveAP_status(self):
        u"""AP发现-slave AP(testlink_ID:1296)"""
        log.debug("011")
        tmp = SWBusiness(self.driver)
        result = tmp.AP_status(data_AP['master:mac'],data_AP['slave:mac1'],
                               data_AP['slave:mac2'])
        print result
        assert result[0] == True,"test slave AP status,test fail!"
        print "test slave AP status,test pass!"

    #AP发现-slave AP配对(testlink_ID:1297)
    def test_012_setupwizard_pair_slaveAP(self):
        u"""AP发现-slave AP配对(testlink_ID:1297)"""
        log.debug("012")
        tmp = SWBusiness(self.driver)
        result = tmp.pair_slaveAP(data_AP['slave:mac2'])
        print result
        assert result == True,"test pair slave AP,test fail!"
        print "test pair slave AP,test pass!"

    #网络组-默认wifi状态(testlink_ID:1298)
    def test_013_setupwizard_wifi_status(self):
        u"""网络组-默认wifi状态(testlink_ID:1298)"""
        log.debug("013")
        tmp = SWBusiness(self.driver)
        result = tmp.wifi_status()
        print result
        assert result == 'true',"test defalut wifi status,test fail!"
        print "test defalut wifi status,test pass!"

    #网络组-默认SSID(testlink_ID:1299)
    def test_014_setupwizard_defalut_ssid(self):
        u"""网络组-默认SSID(testlink_ID:1299)"""
        log.debug("014")
        tmp = SWBusiness(self.driver)
        result = tmp.check_default_ssid(data_AP['master:mac'])
        print result
        assert result ,"test defalut ssid,test fail!"
        print "test defalut ssid,test pass!"

    ##网络组-无线默认密码-使用无线网卡连接默认的ssid
    def test_015_setupwizard_defalut_password(self):
        u"""网络组-默认密码"""
        log.debug("015")
        #登录路由后台取出初始配置的密码
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        pwd_str = ssh.ssh_cmd(data_basic['sshUser'],'cat /proc/gxp/dev_info/security/ssid_password')
        pwd = pwd_str.strip("\r\n")
        #使用无线网卡连接并获取到ip
        tmp = SWBusiness(self.driver)
        #取得应该的ssid
        ssid = tmp.default_ssid(data_AP['master:mac'])
        result1 = tmp.connect_WPA_AP(ssid,pwd,data_basic['wlan_pc'])
        print ssid,pwd
        assert ssid in result1,"test wifi defalut password,test fail!"
        print "test wifi defalut password,test pass!"

    #网络组-默认设备(testlink_ID:1300)
    def test_016_setupwizard_defalut_devices(self):
        u"""网络组-默认设备(testlink_ID:1300)"""
        log.debug("016")
        tmp = SWBusiness(self.driver)
        result = tmp.default_devices(data_AP['slave:mac2'],data_AP['master:mac'])
        print result
        assert result ,"test defalut devices,test fail!"
        print "test defalut devices,test pass!"

    #网络组-添加AP(testlink_ID:1302)
    def test_017_setupwizard_add_slave_ap(self):
        u"""网络组-添加AP(testlink_ID:1302)"""
        log.debug("017")
        tmp = SWBusiness(self.driver)
        result = tmp.add_slave_ap(data_AP['slave:mac2'])
        print result
        assert result ,"test adding slave ap,test fail!"
        print "test adding slave ap,test pass!"


    #网络组-disable wifi(testlink_ID:1303_1)
    def test_018_setupwizard_dis_wifi(self):
        u"""网络组-disable wifi(testlink_ID:1303_1)"""
        log.debug("018")
        tmp = SWBusiness(self.driver)
        #取得应该的ssid
        ssid = tmp.default_ssid(data_AP['master:mac'])
        result1 = tmp.disable_wifi(ssid,data_basic['wlan_pc'])
        assert result1 == False ,"test disable wifi,test fail!"
        print "test disable wifi,test pass!"

    #网络组-Enable wifi(testlink_ID:1303_2)
    def test_019_setupwizard_en_wifi(self):
        u"""网络组-Enable wifi(testlink_ID:1303_2)"""
        log.debug("019")
        tmp = SWBusiness(self.driver)
        result2 = tmp.enable_wifi(data_wireless['letter_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result2 ,"test enable wifi,test fail!"
        print "test enable wifi,test pass!"

    #网络组-移除AP(testlink_ID:1304)
    def test_020_setupwizard_del_ap(self):
        u"""网络组-移除AP(testlink_ID:1304)"""
        log.debug("020")
        tmp = SWBusiness(self.driver)
        result = tmp.del_ap(data_AP['slave:mac2'],data_basic['slave_ip2'],data_basic['sshUser'],data_login['all'])
        assert result ,"test delete ap,test fail!"
        print "test delete ap,test pass!"

    #解除配对(testlink_ID:1305)
    def test_021_setupwizard_unpair_slave_ap(self):
        u"""解除配对(testlink_ID:1305)"""
        log.debug("021")
        tmp = SWBusiness(self.driver)
        result = tmp.unpair_slave_ap(data_basic['slave_ip2'],data_basic['sshUser'],data_basic['super_defalut_pwd'])
        print result
        assert result ,"unpair slave ap,test fail!"
        print "unpair slave ap,test pass!"

    #complete检查(testlink_ID:1306)
    def test_022_setupwizard_complete(self):
        u"""complete检查(testlink_ID:1306)"""
        log.debug("022")
        tmp = SWBusiness(self.driver)
        result = tmp.complete(data_wireless['all_ssid'],
                              data_wireless['short_wpa'],
                              data_basic['wlan_pc'],
                              data_AP['slave:mac1'],
                              data_AP['slave:mac2'])
        print result
        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("SetupWizard")
        assert result,"complete check setupwizard,test fail!"
        print "complete check setupwizard,test pass!"


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
