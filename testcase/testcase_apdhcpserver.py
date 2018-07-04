#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：用例集，调用APdhcpserver_business

import unittest,subprocess
import time
from selenium import webdriver
import sys
from navbar.navbar_business import NavbarBusiness
from login.login_business import LoginBusiness
from network_group.networkgroup_business import NGBusiness
from access_points.aps_business import APSBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from setupwizard.setupwizard_business import SWBusiness
from clients.client_access.clientaccess_business import ClientAccessBusiness
from data import data
from connect.ssh import SSH
from data.logfile import Log
reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
log = Log("APdhcpserver")
class TestAPDhcpServer(unittest.TestCase):
    u"""测试AP DHCP Server的用例集(runtime:2h)"""
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

        #关闭7000的dhcp server
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_ip4_dhcp_server()

        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"


    ####################################################################
    ##################以下是AP DHCP Server的测试用例##################
    ####################################################################
    #验证dhcp开启功能生效
    def test_002_open_ap_dhcp(self):
        u"""验证dhcp开启功能生效(testlink_ID:2457)"""
        log.debug("002")
        tmp1 = APSBusiness(self.driver)
        #指定master ap为静态ip
        tmp1.set_ap_fixed_ip(data_AP['master:mac'],
            data_basic['DUT_ip'],data_AP['fixed_netmask'],
            data_basic['7000_ip'])
        #开启master ap的dhcp server
        tmp = NGBusiness(self.driver)
        tmp.click_ip4_dhcp_server(data_basic['7000_ip'])
        #检查是否勾选
        result = tmp.check_ap_dhcp_server()
        self.assertTrue(result), "check ap dhcp server open in webpage,test fail!"
        print "check ap dhcp server open in webpage,test pass!"

    #验证dhcp关闭功能生效
    def test_003_close_ap_dhcp(self):
        u"""验证dhcp关闭功能生效(testlink_ID:2458)"""
        log.debug("003")
        #关闭master ap的dhcp server
        tmp = NGBusiness(self.driver)
        tmp.click_ip4_dhcp()
        #检查是否勾选
        result = tmp.check_ap_dhcp_server()
        self.assertIsNone(result), "check ap dhcp server close in webpage,test fail!"
        print "check ap dhcp server close in webpage,test pass!"

    #验证不可设置非法的开始地址
    def test_004_check_dhcp_start_invalid(self):
        u"""验证不可设置非法的开始地址(testlink_ID:2459)"""
        log.debug("004")
        #验证不可设置非法的开始地址
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_start_valid("1.1.1.256")
        result2 = tmp.check_dhcp_start_valid(u"192。168.1.2")
        self.assertTrue(result1)
        self.assertTrue(result2), "check ipv4 dhcp start address,test fail!"
        print "check ipv4 dhcp start address,test pass!"

    #验证可设置合法的开始地址
    def test_005_check_dhcp_start_valid(self):
        u"""验证可设置合法的开始地址(testlink_ID:2460)"""
        log.debug("005")
        #验证可设置合法的开始地址
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_start_valid("10.10.10.1")
        result2 = tmp.check_dhcp_start_valid("172.168.1.1")
        result3 = tmp.check_dhcp_start_valid("192.168.1.1")
        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertFalse(result3), "check ipv4 dhcp start address,test fail!"
        print "check ipv4 dhcp start address,test pass!"

    #验证不可设置非法的结束地址
    def test_006_check_dhcp_end_invalid(self):
        u"""验证不可设置非法的结束地址(testlink_ID:2461)"""
        log.debug("006")
        #验证不可设置非法的结束地址
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_end_valid("1.1.1.256")
        result2 = tmp.check_dhcp_end_valid(u"192。168.1.2")
        self.assertTrue(result1)
        self.assertTrue(result2), "check ipv4 dhcp end address,test fail!"
        print "check ipv4 dhcp end address,test pass!"

    #验证可设置合法的结束地址
    def test_007_check_dhcp_end_valid(self):
        u"""验证可设置合法的结束地址(testlink_ID:2462)"""
        log.debug("007")
        #验证可设置合法的结束地址
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_end_valid("10.10.10.1")
        result2 = tmp.check_dhcp_end_valid("172.168.1.1")
        result3 = tmp.check_dhcp_end_valid("192.168.1.1")
        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertFalse(result3), "check ipv4 dhcp end address,test fail!"
        print "check ipv4 dhcp end address,test pass!"

    #验证不可设置开始地址大于结束地址
    def test_008_check_dhcp_start_more_end(self):
        u"""验证不可设置开始地址大于结束地址(testlink_ID:2463)"""
        log.debug("008")
        #开始地址大于结束地址是否合法
        tmp = NGBusiness(self.driver)
        result = tmp.check_dhcp_start_more_end("192.168.1.100","192.168.1.99")
        self.assertTrue(result), "check ipv4 dhcp start address more than end address,test fail!"
        print "check ipv4 dhcp start address more than end address,test pass!"

    #验证不可设置dhcp地址池与接口地址非同一网段
    def test_009_check_dhcp_different_net(self):
        u"""dhcp地址池与接口地址非同一网段(testlink_ID:2464)"""
        log.debug("009")
        #dhcp地址池与接口地址非同一网段
        tmp = NGBusiness(self.driver)
        result = tmp.check_dhcp_start_more_end("192.168.2.1","192.168.2.254")
        self.assertTrue(result), "check ipv4 dhcp is different net,test fail!"
        print "check ipv4 dhcp is different net,test pass!"

    #验证不可设置非法格式的dhcp租约
    def test_010_check_dhcp_lease_time_invalid(self):
        u"""验证不可设置非法格式的dhcp租约(testlink_ID:2465)"""
        log.debug("010")
        #非法格式的dhcp的租约
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_lease_time("12")
        result2 = tmp.check_dhcp_lease_time("12H")
        result3 = tmp.check_dhcp_lease_time("12M")
        result4 = tmp.check_dhcp_lease_time("12d")
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertTrue(result4), "check dhcp invalid lease time, test fail!"
        print "check dhcp invalid lease time, test pass!"

    #验证可设置合法格式的dhcp租约
    def test_011_check_dhcp_lease_time_valid(self):
        u"""验证可设置合法格式的dhcp租约(testlink_ID:2466)"""
        log.debug("011")
        #合法格式的dhcp的租约
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_lease_time("2m")
        result2 = tmp.check_dhcp_lease_time("12h")
        result3 = tmp.check_dhcp_lease_time("1193046h")
        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertFalse(result3), "check dhcp valid lease time, test fail!"
        print "check dhcp valid lease time, test pass!"

    #验证不可设置非法格式网关地址
    def test_012_check_dhcp_gateway_invalid(self):
        u"""验证不可设置非法格式网关地址(testlink_ID:2467)"""
        log.debug("012")
        #验证不可设置非法格式网关地址
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_gateway("1.1.1.256")
        result2 = tmp.check_dhcp_gateway(u"192。168.1.2")
        self.assertTrue(result1)
        self.assertTrue(result2), "check ipv4 dhcp gateway address,test fail!"
        print "check ipv4 dhcp gateway address,test pass!"

    #验证可设置合法格式网关地址
    def test_013_check_dhcp_gateway_valid(self):
        u"""验证可设置合法格式网关地址(testlink_ID:2468)"""
        log.debug("013")
        #验证可设置合法格式网关地址
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_gateway("10.10.10.1")
        result2 = tmp.check_dhcp_gateway("172.168.1.1")
        result3 = tmp.check_dhcp_gateway("192.168.1.1")
        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertFalse(result3), "check ipv4 dhcp gateway address,test fail!"
        print "check ipv4 dhcp gateway address,test pass!"

    #验证网关与接口地址不在同一网段，设置失败
    def test_014_check_dhcp_gateway_different_ip(self):
        u"""验证网关与接口地址不在同一网段，设置失败(testlink_ID:2469)"""
        log.debug("014")
        tmp = NGBusiness(self.driver)
        result =tmp.check_dhcp_gateway_different_ip("192.168.2.1")
        self.assertTrue(result), "check dhcp gateway is different from ap ip, test fail!"
        print "check dhcp gateway is different from ap ip, test pass!"

    #验证不可设置非法格式的dns
    def test_015_check_dhcp_dns_invalid(self):
        u"""验证不可设置非法格式的dns(testlink_ID:2470)"""
        log.debug("015")
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_dns("1.1.1.256")
        result2 = tmp.check_dhcp_dns(u"192。168.1.2")
        self.assertTrue(result1)
        self.assertTrue(result2), "check ipv4 dhcp dns,test fail!"
        print "check ipv4 dhcp dns,test pass!"

    #验证可设置合法格式的dns
    def test_016_check_dhcp_dns_valid(self):
        u"""验证可设置合法格式的dns(testlink_ID:2471)"""
        log.debug("016")
        tmp = NGBusiness(self.driver)
        result1 = tmp.check_dhcp_dns("8.8.8.8")
        result2 = tmp.check_dhcp_dns("114.114.114.114")
        self.assertFalse(result1)
        self.assertFalse(result2), "check ipv4 dhcp dns,test fail!"
        print "check ipv4 dhcp dns,test pass!"

    #验证首选和次选dns可设置相同
    def test_017_check_ap_dhcp_dns1_dns2(self):
        u"""验证首选和次选dns可设置相同(testlink_ID:2472)"""
        log.debug("017")
        tmp = NGBusiness(self.driver)
        dns = "180.76.76.76"
        #设置首选dns和次选dns
        tmp.set_ap_dhcp_dns1_dns2(dns,dns)
        #验证首选dns和次选dns是否设置成功
        result1,result2 = tmp.check_ap_dhcp_dns1_dns2()
        self.assertEqual(dns, result1)
        self.assertEqual(dns, result2), "check dns1 and dns2 can set same, test fail!"
        print "check dns1 and dns2 can set same, test fail!"

    #验证默认group0的dhcp功能生效
    def test_018_check_group0_dhcp_server(self):
        u"""验证默认group0的dhcp功能生效(testlink_ID:2489)"""
        log.debug("018")
        tmp = NGBusiness(self.driver)
        #修改group0的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        #无线连接mater ap
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        result = tmp.get_localIp(data_basic['wlan_pc'])
        #无线网卡释放ip
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertIn("192.168.1", result), "check dhcp server function of group0, test fail!"
        print "check dhcp server function of group0, test pass!"

    #验证有线终端可通过dhcp获取ip
    def test_019_check_wire_client(self):
        u"""验证有线终端可通过dhcp获取ip(testlink_ID:2491)"""
        log.debug("019")
        tmp = NGBusiness(self.driver)
        #pc有线网卡释放ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        #pc有线网卡重新获取ip
        tmp.dhcp_wlan(data_basic['lan_pc'])
        #获取有线网卡的ip
        result = tmp.get_localIp(data_basic['lan_pc'])
        self.assertIn("192.168.1", result), "check wire client can get ip, test fail!"
        print "check wire client can get ip, test pass!"

    #验证重启后，dhcp配置不会丢失
    def test_020_check_reboot_ap_dhcp_config(self):
        u"""验证重启后，dhcp配置不会丢失(testlink_ID:2473)"""
        log.debug("020")
        #重启并重新登录master ap
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #检查完整配置
        tmp = NGBusiness(self.driver)
        dhcp_checked,gateway,dns1,dns2 = tmp.check_all_config()
        self.assertTrue(dhcp_checked)
        self.assertEqual(gateway,data_basic['7000_ip'])
        self.assertEqual(dns1,"180.76.76.76")
        self.assertEqual(dns2,"180.76.76.76"), "check dhcp configuration after reboot master ap, test fail!"
        print "check dhcp configuration after reboot master ap, test pass!"

    #验证设置dhcp配置后，网络终端能动态获取正确的ip，掩码等信息
    def test_021_client_can_get_ip(self):
        u"""验证设置dhcp配置后，网络终端能动态获取正确的ip，掩码等信息(testlink_ID:2475)"""
        log.debug("021")
        tmp = NGBusiness(self.driver)
        #pc有线网卡释放ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        #pc有线网卡重新获取ip
        tmp.dhcp_wlan(data_basic['lan_pc'])
        #获取pc的有线网卡的ip，掩码等信息
        result = tmp.get_client_cmd_result("ifconfig %s | grep inet"%data_basic['lan_pc'])
        self.assertIn("192.168.1", result)
        self.assertIn(data_AP['fixed_netmask'], result), "check client can get new ip, test fail!"
        print "check client can get new ip, test pass!"

    #验证更改子网掩码后，网络终端重新获取新的正确掩码
    def test_022_client_update_netmask(self):
        u"""验证更改子网掩码后，网络终端重新获取新的正确掩码(testlink_ID:2476)"""
        log.debug("022")
        tmp1 = APSBusiness(self.driver)
        #指定master ap为子网掩码
        tmp1.set_ap_fixed_ip_backup(data_AP['master:mac'],
            data_basic['DUT_ip'],data_AP['fixed_netmask2'],
            data_basic['7000_ip'])
        #pc有线网卡释放ip
        tmp1.dhcp_release_wlan(data_basic['lan_pc'])
        #pc有线网卡重新获取ip
        tmp1.dhcp_wlan(data_basic['lan_pc'])
        #获取pc的有线网卡的ip，掩码等信息
        result = tmp1.get_client_cmd_result("ifconfig %s | grep inet"%data_basic['lan_pc'])
        self.assertIn(data_AP['fixed_netmask2'], result), "check client can get new netmask, test fail!"
        print "check client can get new netmask, test pass!"

    #验证默认租期为12小时，检查配置是否是12小时
    def test_023_dhcp_least_time_12h(self):
        u"""验证默认租期为12小时，检查配置是否是12小时(testlink_ID:2477)"""
        log.debug("023")
        tmp1 = APSBusiness(self.driver)
        #master ap为子网掩码改回
        tmp1.set_ap_fixed_ip_backup(data_AP['master:mac'],
            data_basic['DUT_ip'],data_AP['fixed_netmask'],
            data_basic['7000_ip'])
        tmp = NGBusiness(self.driver)
        #登录后台，检查租期时间
        result = tmp.check_ap_dhcp_lease_time(data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'],"12h")
        self.assertTrue(result), "check default lease time is 12h, test fail!"
        print "check default lease time is 12h, test pass!"

    #验证设置租期为2m，检查配置是否为2m
    def test_024_dhcp_least_time_2m(self):
        u"""验证设置租期为2m，检查配置是否为2m(testlink_ID:2479)"""
        log.debug("024")
        tmp = NGBusiness(self.driver)
        #仅仅设置租期为2m
        tmp.set_dhcp_lease_time("2m")
        #登录后台，检查租期时间
        result = tmp.check_ap_dhcp_lease_time(data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'],"2m")
        self.assertTrue(result), "check lease time is 2m, test fail!"
        print "check lease time is 2m, test pass!"

    #验证设置租期为1193046h，检查配置是否为1193046h
    def test_025_dhcp_least_time_1193046h(self):
        u"""验证设置租期为1193046h，检查配置是否为1193046h(testlink_ID:2480)"""
        log.debug("025")
        tmp = NGBusiness(self.driver)
        #仅仅设置租期为1193046h
        tmp.set_dhcp_lease_time("1193046h")
        #登录后台，检查租期时间
        result = tmp.check_ap_dhcp_lease_time(data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'],"1193046h")
        self.assertTrue(result), "check lease time is 1193046h, test fail!"
        print "check lease time is 1193046h, test pass!"

    #验证更改地址池后，网络终端重新获取新地址池中的ip
    def test_026_client_can_get_new_ip(self):
        u"""验证更改地址池后，网络终端重新获取新地址池中的ip(testlink_ID:2482)"""
        log.debug("026")
        #新建网络组，开启dhcp server和wifi
        tmp = NGBusiness(self.driver)
        tmp.new_group_open_dhcp_server(data_ng["NG2_name"]+"-2",
            "192.168.2.1","192.168.2.10","192.168.2.11",
            "192.168.2.2","180.76.76.76",
            data_ng["NG2_ssid"]+"-2",data_wireless["short_wpa"])
        #无线连接新的group
        tmp.connect_DHCP_WPA_AP(data_ng["NG2_ssid"]+"-2",
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        ip1 = tmp.get_localIp(data_basic['wlan_pc'])
        result1 = int(ip1.split(".")[-1])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        #更改新建网络组的起始ip和终止ip
        tmp.change_groupn_start_end_ip(1,"192.168.2.20","192.168.2.21")
        #无线再次连接新的group
        tmp.connect_DHCP_WPA_AP(data_ng["NG2_ssid"]+"-2",
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        ip2 = tmp.get_localIp(data_basic['wlan_pc'])
        result2 = int(ip2.split(".")[-1])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        print result1,result2
        self.assertLessEqual(result1, 11)
        self.assertGreaterEqual(result1, 10)
        self.assertLessEqual(result2, 21)
        self.assertGreaterEqual(result2, 20), "check client can get new ip of address range , test fail!"
        print "check client can get new ip of address range , test pass!"

    #验证关闭dhcp功能后，网络终端无法获取ip
    def test_027_dhcp_close_function(self):
        u"""验证关闭dhcp功能后，网络终端无法获取ip(testlink_ID:2484)"""
        log.debug("027")
        tmp = NGBusiness(self.driver)
        #关闭新建网络组的dhcp server
        tmp.click_groupn_dhcp_server(1)
        #无线网卡重新获取ip
        tmp.dhcp_wlan(data_basic['wlan_pc'])
        #ping 网关
        result = tmp.get_ping("192.168.2.1")
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertNotEqual(result,0),"disable dhcp server,test fail!"
        print "disable dhcp server,test pass!"

    #验证关闭dhcp功能后，不影响其他group的dhcp功能
    def test_028_close_dhcp_other_group(self):
        u"""验证关闭dhcp功能后，不影响其他group的dhcp功能(testlink_ID:2485)"""
        log.debug("028")
        tmp = NGBusiness(self.driver)
        #无线连接group0
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        result = tmp.get_localIp(data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertIn("192.168.1", result), "disable dhcp server,check the other group,test fail!"
        print "disable dhcp server,check the other group,test pass!"

    #验证关闭dhcp功能后再开启，网络终端获取ip
    def test_029_open_dhcp_server_again(self):
        u"""验证关闭dhcp功能后再开启，网络终端获取ip(testlink_ID:2486)"""
        log.debug("029")
        tmp = NGBusiness(self.driver)
        #开启新建网络组的dhcp server
        tmp.click_groupn_dhcp_server(1)
        #无线连接新的group
        tmp.connect_DHCP_WPA_AP(data_ng["NG2_ssid"]+"-2",
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        result = tmp.get_localIp(data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertIn("192.168.2", result), "open dhcp server again,test fail!"
        print "open dhcp server again,test pass!"

    #验证非group0的dhcp功能生效
    def test_030_groupn_dhcp_server(self):
        u"""验证非group0的dhcp功能生效(testlink_ID:2490)"""
        log.debug("030")
        tmp = NGBusiness(self.driver)
        #获取无线网卡的ip
        tmp.dhcp_wlan(data_basic['wlan_pc'])
        result = tmp.get_localIp(data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertIn("192.168.2", result), "check not group0 dhcp server,test fail!"
        print "check not group0 dhcp server,test pass!"

    #验证关闭ipv4功能，网络终端获取不到ip
    def test_031_ipv4_close_function(self):
        u"""验证关闭ipv4功能，网络终端获取不到ip(testlink_ID:2487)"""
        log.debug("031")
        tmp = NGBusiness(self.driver)
        #关闭新建网络组的ipv4
        tmp.click_groupn_ipv4(1)
        #无线网卡重新获取ip
        tmp.dhcp_wlan(data_basic['wlan_pc'])
        #ping 网关
        result = tmp.get_ping("192.168.2.1")
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertNotEqual(result,0),"disable ipv4,test fail!"
        print "disable ipv4,test pass!"

    #验证关闭ipv4功能后，不影响其他group的dhcp功能
    def test_032_close_dhcp_other_group(self):
        u"""验证关闭ipv4功能后，不影响其他group的dhcp功能(testlink_ID:2488)"""
        log.debug("032")
        tmp = NGBusiness(self.driver)
        #无线连接group0
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        result = tmp.get_localIp(data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertIn("192.168.1", result), "disable dhcp server,check the other group,test fail!"
        print "disable dhcp server,check the other group,test pass!"

    #验证无线网络终端通过2.4G频段可通过dhcp获取ip
    def test_033_wifi_2g4_dhcp_server(self):
        u"""验证无线网络终端通过2.4G频段可通过dhcp获取ip(testlink_ID:2492)"""
        log.debug("033")
        tmp = NGBusiness(self.driver)
        #开启新建网络组的ipv4
        tmp.click_groupn_ipv4(1)
        #修改master ap为2.4G
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("2.4GHz")
        #无线连接新的group
        tmp.connect_DHCP_WPA_AP(data_ng["NG2_ssid"]+"-2",
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        result = tmp.get_localIp(data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertIn("192.168.2", result), "check 2.4G can get ip,test fail!"
        print "check 2.4G can get ip,test pass!"

    #验证无线网络终端通过5G频段可通过dhcp获取ip
    def test_034_wifi_5g_dhcp_server(self):
        u"""验证无线网络终端通过5G频段可通过dhcp获取ip(testlink_ID:2493)"""
        log.debug("034")
        #修改master ap为5G
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("5GHz")
        #无线连接新的group
        tmp1.connect_DHCP_WPA_AP(data_ng["NG2_ssid"]+"-2",
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #获取无线网卡的ip
        result = tmp1.get_localIp(data_basic['wlan_pc'])
        tmp1.dhcp_release_wlan(data_basic['wlan_pc'])
        #改回双频
        tmp1.change_AP_Freq("Dual-Band")
        self.assertIn("192.168.2", result), "check 5G can get ip,test fail!"
        print "check 5G can get ip,test pass!"

    #验证group0的dhcp配置是不会下发到slave
    def test_035_group0_dhcp_send_to_slave(self):
        u"""验证group0的dhcp配置是不会下发到slave(testlink_ID:2495,2496)"""
        log.debug("035")
        tmp1 = APSBusiness(self.driver)
        #slave ap2配对并加入所有网络组
        tmp1.search_pair_add_to_all_NG(data_AP['slave:mac2'])
        time.sleep(60)
        #获取slave ap2的新的ip
        slave2_ip = tmp1.g_special_AP_ip(data_AP['slave:mac2'])
        #登录slave ap2的后台查看dhcp配置
        ssh = SSH(slave2_ip,data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"cat /var/etc/dnsmasq.conf")
        self.assertNotIn(data_basic['7000_ip'],result)
        self.assertNotIn("192.168.2.1",result), "check slave haven't group0 and group1's dhcp server configuration,test fail!"
        print "check slave haven't group0 and group1's dhcp server configuration,test pass!"

    #验证填写不存在的网关地址，终端无法上网
    def test_036_check_noexist_gateway(self):
        u"""验证填写不存在的网关地址，终端无法上网(testlink_ID:2500)"""
        log.debug("036")
        tmp = NGBusiness(self.driver)
        #无线连接新的group
        tmp.connect_DHCP_WPA_AP(data_ng["NG2_ssid"]+"-2",
            data_wireless["short_wpa"],data_basic['wlan_pc'])
        #down掉pc有线
        tmp.wlan_disable(data_basic['lan_pc'])
        result = tmp.get_ping("www.qq.com")
        #up pc有线
        tmp.wlan_enable(data_basic['lan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertNotEqual(result,0),"check no exist gateway,client can't access internet,test fail!"
        print "check no exist gateway,client can't access internet,test pass!"

    #验证填写正确的网关地址，客户端可以上网
    def test_037_check_right_gateway(self):
        u"""验证填写正确的网关地址，客户端可以上网(testlink_ID:2501)"""
        log.debug("037")
        tmp = NGBusiness(self.driver)
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        result = tmp.get_ping("www.qq.com")
        #解除slave ap2的配对
        tmp1 = APSBusiness(self.driver)
        tmp1.unpair_special_slave_AP(data_AP['slave:mac2'])
        #删除多余的网络组
        tmp.del_all_NG()
        self.assertEqual(result,0),"check right gateway,client can access internet,test fail!"
        print "check right gateway,client can access internet,test pass!"

    #验证只填写有效的首选dns后，客户端可以访问网站
    def test_038_check_dns1_valid(self):
        u"""验证只填写有效的首选dns后，客户端可以访问网站(testlink_ID:2502)"""
        log.debug("038")
        tmp = NGBusiness(self.driver)
        #设置首选dns和次选dns-不点击dhcp server
        tmp.set_ap_dns1_dns2("180.76.76.76","")
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        result = tmp.get_ping("www.qq.com")
        self.assertEqual(result,0),"check only dns1,test fail!"
        print "check only dns1,test pass!"

    #验证只填写有效的次选dns后，客户端可以访问网站
    def test_039_check_dns2_valid(self):
        u"""验证只填写有效的次选dns后，客户端可以访问网站(testlink_ID:2504)"""
        log.debug("039")
        tmp = NGBusiness(self.driver)
        #设置首选dns和次选dns-不点击dhcp server
        tmp.set_ap_dns1_dns2("","223.5.5.5")
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        result = tmp.get_ping("www.qq.com")
        self.assertEqual(result,0),"check only dns2,test fail!"
        print "check only dns2,test pass!"

    #验证填写有效的首选次选dns后，客户端可以访问网站
    def test_040_check_dns12_valid(self):
        u"""验证填写有效的首选次选dns后，客户端可以访问网站(testlink_ID:2506)"""
        log.debug("040")
        tmp = NGBusiness(self.driver)
        #设置首选dns和次选dns-不点击dhcp server
        tmp.set_ap_dns1_dns2("180.76.76.76","223.5.5.5")
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        result = tmp.get_ping("www.qq.com")
        self.assertEqual(result,0),"check only dns1,2,test fail!"
        print "check only dns1,2,test pass!"

    #验证dns填写网关的地址，客户端可以访问网站
    def test_041_check_dns_gateway(self):
        u"""验证dns填写网关的地址，客户端可以访问网站(testlink_ID:2507)"""
        log.debug("041")
        tmp = NGBusiness(self.driver)
        #设置首选dns和次选dns-不点击dhcp server
        tmp.set_ap_dns1_dns2(data_basic['7000_ip'],"")
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        result = tmp.get_ping("www.qq.com")
        tmp.set_ap_dns1_dns2("180.76.76.76","223.5.5.5")
        self.assertEqual(result,0),"check set dsn to gateway,test fail!"
        print "check set dsn to gateway,test pass!"

    #验证重启后，dhcp功能正常
    def test_042_check_reboot_dhcp_function(self):
        u"""验证重启后，dhcp功能正常(testlink_ID:2508)"""
        log.debug("042")
        #重启并重新登录master ap
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        #release,renew 有线网卡
        tmp1.dhcp_release_wlan(data_basic['lan_pc'])
        tmp1.dhcp_wlan(data_basic['lan_pc'])
        #有线网卡得到ip
        result = tmp1.get_localIp(data_basic['lan_pc'])
        self.assertIn("192.168.1", result), "check dhcp function after rebooting,,test fail!"
        print "check dhcp function after rebooting,test pass!"

    #验证关闭dhcp功能后，网络终端有线无法获取ip
    def test_043_close_ap_dhcp(self):
        u"""验证关闭dhcp功能后，网络终端有线无法获取ip(testlink_ID:2484)"""
        log.debug("043")
        tmp = NGBusiness(self.driver)
        #关闭master ap的dhcp server
        tmp.click_ip4_dhcp()

        #master ap搜索并配对slave ap1,slave ap2
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_AP(data_AP['slave:mac1'],data_AP['slave:mac2'])

        #有线网卡重新获取ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        tmp.dhcp_wlan(data_basic['lan_pc'])
        #ping 网关
        result = tmp.get_ping("192.168.1.1")
        #指定pc有线网卡为静态ip
        subprocess.call("echo %s | sudo -S ifconfig %s %s"%(data_basic['PC_pwd'],data_basic['lan_pc'],data_basic['PC_ip']),shell=True)

        self.assertNotEqual(result,0), "close ap dhcp server,test fail!"
        print "close ap dhcp server,test pass!"

    #ap dhcp server测试完成后，恢复工作
    def test_044_restore(self):
        u"""ap dhcp server测试完成后，恢复工作"""
        log.debug("044")
        tmp = NGBusiness(self.driver)
        #开启7000的dhcp server
        tmp.mixed_7000_ip4_dhcp_server()
        #重启7000
        tmp3 = UpgradeBusiness(self.driver)
        tmp3.web_reboot_backup()
        #release,renew 有线网卡
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        time.sleep(200)
        tmp.dhcp_wlan(data_basic['lan_pc'])
        #再回来复位master ap
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(10)
        self.driver.refresh()
        time.sleep(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #复位master ap
        tmp1 = APSBusiness(self.driver)
        result = tmp1.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])

        #测试完毕，禁用无线网卡，使pc够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("APdhcpserver")

        self.assertTrue(result), "restore all configuration after testing ap dhcp server,test fail!"
        print "restore all configuration after testing ap dhcp server,test pass!"





    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()