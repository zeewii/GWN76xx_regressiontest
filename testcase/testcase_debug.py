#coding=utf-8
#作者：曾祥卫
#时间：2017.06.13
#描述：用例层代码

import unittest
import time
from selenium import webdriver
import sys
from connect.ssh import SSH
from login.login_business import LoginBusiness
from access_points.aps_business import APSBusiness
from system_settings.debug.ping_traceroute.ping_business import PingBusiness
from data import data
from data.logfile import Log
reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_AP = data.data_AP()
data_ng = data.data_networkgroup()
data_client = data.data_Client()

log = Log("Debug")
class TestDebug(unittest.TestCase):
    u"""测试调试的用例集(runtime:20m)"""
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
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #Target输入框内容为空--选择IPv4 Ping(testlink_ID:622_1)
    def test_002_ipv4ping_empty(self):
        u"""Target输入框内容为空--选择IPv4 Ping(testlink_ID:622_1)"""
        log.debug("002")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Ping","")
        #获取输出的结果
        result = tmp.get_ping_output()
        assert result == "ping: bad address ''","ipv4 ping empty,test fail!"
        print "ipv4 ping empty,test pass!"


    #Target输入框内容为空--选择IPv4 Traceroute(testlink_ID:622_2)
    def test_003_ipv4traceroute_empty(self):
        u"""Target输入框内容为空--选择IPv4 Traceroute(testlink_ID:622_2)"""
        log.debug("003")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Traceroute","")
        #获取输出的结果
        result = tmp.get_ping_output()
        assert result == "traceroute: bad address ''","ipv4 traceroute empty,test fail!"
        print "ipv4 traceroute empty,test pass!"


    #Target输入框内容为非法IP地址--选择IPv4 Ping(testlink_ID:623_1)
    def test_004_ipv4ping_illegal(self):
        u"""Target输入框内容为非法IP地址--选择IPv4 Ping(testlink_ID:623_1)"""
        log.debug("004")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Ping",data_AP['validity_fixed_netmask'])
        #获取输出的结果
        result = tmp.get_ping_output()
        assert "ping: bad address" in result,"ipv4 ping illegal,test fail!"
        print "ipv4 ping illegal,test pass!"


    #Target输入框内容为非法IP地址--选择IPv4 Traceroute(testlink_ID:623_2)
    def test_005_ipv4traceroute_illegal(self):
        u"""Target输入框内容为非法IP地址--选择IPv4 Traceroute(testlink_ID:623_2)"""
        log.debug("005")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Traceroute",data_AP['validity_fixed_netmask'])
        #获取输出的结果
        result = tmp.get_ping_output()
        assert "traceroute: bad address" in result,"ipv4 traceroute illegal,test fail!"
        print "ipv4 traceroute illegal,test pass!"


    #Target输入框内容为特殊地址--选择IPv4 Ping(testlink_ID:624_1)
    def test_006_ipv4ping_special(self):
        u"""Target输入框内容为特殊地址--选择IPv4 Ping(testlink_ID:624_1)"""
        log.debug("006")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Ping","255.255.255.255")
        #获取输出的结果
        result = tmp.get_ping_output()
        assert "100% packet loss" in result,"ipv4 ping special,test fail!"
        print "ipv4 ping special,test pass!"

     #Target输入框内容为特殊地址--选择IPv4 Traceroute(testlink_ID:624_2)
    def test_007_ipv4traceroute_special(self):
        u"""Target输入框内容为特殊地址--选择IPv4 Traceroute(testlink_ID:624_2)"""
        log.debug("007")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Traceroute","255.255.255.255")
        time.sleep(60)
        #获取输出的结果
        result = tmp.get_ping_output()
        assert (result != "") and (("bad address" or "can't connect to remote host") \
                    not in result),"ipv4 traceroute special,test fail!"
        print "ipv4 ping traceroute,test pass!"

    #Target输入框内容为正确的IPv4地址--ping网关IP(testlink_ID:625_1)
    def test_008_ping_network_gateway_v4(self):
        u"""Target输入框内容为正确的IPv4地址--ping网关IP(testlink_ID:625_1)"""
        log.debug("008")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Ping",data_basic['7000_ip'])
        #获取输出的结果
        result = tmp.get_ping_output()
        assert "0% packet loss" in result,"ping network gateway ipv4,test fail!"
        print "ping network gateway ipv4,test pass!"

    #Target输入框内容为正确的IPv4地址--traceroute网关IP(testlink_ID:625_2)
    def test_009_traceroute_network_gateway_v4(self):
        u"""Target输入框内容为正确的IPv4地址--ping网关IP(testlink_ID:625_2)"""
        log.debug("009")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Traceroute",data_basic['7000_ip'])
        time.sleep(60)
        #获取输出的结果
        result = tmp.get_ping_output()
        assert (result != "") and (("bad address" or "can't connect to remote host") \
                    not in result),"traceroute network gateway ipv4,test fail!"
        print "traceroute network gateway ipv4,test pass!"

    #DUT能访问外网--选择IPv4 Ping(testlink_ID:627_1)
    def test_010_ping_baidu_v4(self):
        u"""DUT能访问外网--选择IPv4 Ping(testlink_ID:627_1)"""
        log.debug("010")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Ping","www.baidu.com")
        #获取输出的结果
        result = tmp.get_ping_output()
        assert "0% packet loss" in result,"ping baidu,test fail!"
        print "ping baidu,test pass!"

    #DUT能访问外网--选择IPv4 Traceroute(testlink_ID:627_2)
    def test_011_traceroute_baidu_v4(self):
        u"""DUT能访问外网--选择IPv4 Traceroute(testlink_ID:627_2)"""
        log.debug("011")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv4 Traceroute","www.baidu.com")
        time.sleep(60)
        #获取输出的结果
        result = tmp.get_ping_output()
        assert  "traceroute to www.baidu.com" in result,"traceroute baidu,test fail!"
        print "traceroute baidu,test pass!"

    #DUT能访问7000ipv6--选择IPv6 Ping(testlink_ID:627_3)--bug83333
    def test_012_ping_baidu_v6(self):
        u"""DUT能访问7000ipv6--选择IPv6 Ping(testlink_ID:627_3)--bug83333"""
        log.debug("012")
        #取出7000的lan口的ipv6的地址
        s = SSH(data_basic['7000_ip'],data_login['all'])
        result1 = s.ssh_cmd(data_basic['sshUser'],"ifconfig eth0.1 | grep inet6")
        result2 = result1.split(" ")
        ipv6_7000 = result2[-2][0:-3]
        print "IPv6 of GWN7000 is %s"%ipv6_7000
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv6 Ping",ipv6_7000)
        #获取输出的结果
        result = tmp.get_ping_output()
        assert "0% packet loss" in result,"ping 7000 ipv6,test fail!"
        print "ping 7000 ipv6,test pass!"

    #DUT能访问外网--选择IPv6 traceroute(testlink_ID:627_4)--bug83333
    def test_013_traceroute_baidu_v6(self):
        u"""DUT能访问外网--选择IPv6 traceroute(testlink_ID:627_4)--bug83333"""
        log.debug("013")
        tmp = PingBusiness(self.driver)
        #输入目标地址，点击开始
        tmp.run_ping("IPv6 Traceroute",data_AP['BY_ipv6_1'])
        time.sleep(60)
        #获取输出的结果
        result = tmp.get_ping_output()
        print "result=%s"%result
        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("Debug")
        assert "traceroute to %s"%data_AP['BY_ipv6_1'] in result,"traceroute internet ipv6,test fail!"
        print "traceroute internet ipv6,test pass!"

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
