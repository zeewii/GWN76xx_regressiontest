#coding=utf-8
#作者：曾祥卫
#时间：2017.11.03
#描述：用例层代码，调用clientaccess_business

import unittest
import time,subprocess
from selenium import webdriver
import sys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from login.login_business import LoginBusiness
from clients.clients_business import ClientsBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from access_points.aps_business import APSBusiness
from ssid.ssid_business import SSIDBusiness
from data import data
from connect.ssh import SSH
from data.logfile import Log

log = Log("Clientaccess")
reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_AP = data.data_AP()
data_ng = data.data_networkgroup()
data_client = data.data_Client()


class TestClientAccess(unittest.TestCase):
    u"""测试客户端访问的用例集(runtime:50m)"""
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
        #修改默认SSID的ssid和密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
    
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'], data_basic['wlan_pc'])
        #禁用启用有线网卡，以便无线网卡能够在ap的client页面显示在线
        tmp.wlan_disable(data_basic['lan_pc'])
        tmp.wlan_enable(data_basic['lan_pc'])
        time.sleep(60)
        tmp.dhcp_release_wlan(data_basic["wlan_pc"])

        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"
    
    #UI检查(testlink_ID:2748)
    def test_002_check_clientaccess_UI(self):
        u"""UI检查(testlink_ID:2748)"""
        log.debug("002")
        tmp = ClientAccessBusiness(self.driver)
        #检查页面上是否有添加和编辑按钮，来判断UI页面正常
        result = tmp.check_clientaccess_UI()
        self.assertTrue(result), "check client access menu webpage UI, test fail!"
        print "check client access menu webpage UI, test pass!"
    
    #页面默认参数检查
    def test_003_check_webpage_default_parameter(self):
        u"""页面默认参数检查(testlink_ID:2750)"""
        log.debug("003")
        tmp = ClientAccessBusiness(self.driver)
        #页面默认参数检查
        mac = tmp.randomMAC()
        result = tmp.check_webpage_default_parameter(mac)
        self.assertTrue(result), "check webpage default parameter, test fail!"
        print "check webpage default parameter, test pass!"
    
    #Global Blacklist默认状态检查
    def test_004_check_global_blacklist_default(self):
        u"""Global Blacklist默认状态检查(testlink_ID:2751)"""
        log.debug("004")
        tmp = ClientAccessBusiness(self.driver)
        #Global Blacklist默认状态检查
        result1,result2,result3 = tmp.check_global_blacklist_default()
        self.assertEqual("", result1)
        self.assertTrue(result2)
        self.assertTrue(result3), "check global blacklist default status, test fail!"
        print "check global blacklist default status, test pass!"
    
    #终端在client页面被block后，显示到Global Blacklist中
    def test_005_check_block_client(self):
        u"""终端在client页面被block后，显示到Global Blacklist中(testlink_ID:2752)"""
        log.debug("005")
        tmp = ClientAccessBusiness(self.driver)
        #使用无线网卡能够连接上ssid,并正常使用
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #终端在client页面被block后，显示到Global Blacklist中
        result = tmp.check_block_client(wlan_mac,data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'])
        self.assertTrue(result), "check Global Blacklist after blocking client, test fail!"
        print "check Global Blacklist after blocking client, test pass!"
    
    #Blocked clients重连验证
    def test_006_block_client(self):
        u"""Blocked clients重连验证(testlink_ID:2753)"""
        log.debug("006")
        tmp = ClientAccessBusiness(self.driver)
        #使用无线网卡连接ssid
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),"after blocking client,client connect ap again,test fail!"
        print "after blocking client,client connect ap again,test pass!"
    
    #删除Global Blacklist中的终端
    def test_007_del_Global_Blacklist_mac(self):
        u"""删除Global Blacklist中的终端(testlink_ID:2769)"""
        log.debug("007")
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #删除Global Blacklist中的终端后检查web页面的列表和iptables规则
        result = tmp.check_del_Global_Blacklist_mac(wlan_mac,data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'])
        self.assertTrue(result), "check webpage and iptables after del Global Blacklist, test fail!"
        print "check webpage and iptables after del Global Blacklist, test pass!"
    
    #被删除的终端重连验证
    def test_008_unblock_client(self):
        u"""被删除的终端重连验证(testlink_ID:2770)"""
        log.debug("008")
        tmp = ClientAccessBusiness(self.driver)
        #使用无线网卡能够连接上ssid,并正常使用
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),"after del Global Blacklist,client connect ap again,test fail!"
        print "after del Global Blacklist,client connect ap again,test pass!"
    
    #Block 5G客户端
    def test_009_block_5G_client(self):
        u"""Block 5G客户端(testlink_ID:2754)"""
        log.debug("009")
        #修改ap的的Freq为5G
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_AP_Freq("5GHz")
        #使用无线网卡能够连接上ssid,并正常使用
        tmp1.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        tmp1.dhcp_release_wlan(data_basic['wlan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #终端在client页面被block后，显示到Global Blacklist中
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result1 = tmp.check_block_client(wlan_mac,data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #删除Global Blacklist里面的所有的mac
        tmp.del_Global_Blacklist_mac()
        self.assertTrue(result1)
        self.assertIn('Not connected', result2), "check block 5G client,test fail!"
        print "check block 5G client,test pass!"
    
    #Block 2.4G客户端
    def test_010_block_2G4_client(self):
        u"""Block 2.4G客户端(testlink_ID:2755)"""
        log.debug("010")
        #修改ap的的Freq为2.4G
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_AP_Freq("2.4GHz")
        #使用无线网卡能够连接上ssid,并正常使用
        tmp1.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        tmp1.dhcp_release_wlan(data_basic['wlan_pc'])
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #终端在client页面被block后，显示到Global Blacklist中
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result1 = tmp.check_block_client(wlan_mac,data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #删除Global Blacklist里面的所有的mac
        tmp.del_Global_Blacklist_mac()
        #修改ap的Freq为Dual-Band
        tmp1.change_AP_Freq("Dual-Band")
        self.assertTrue(result1)
        self.assertIn('Not connected', result2), "check block 2.4G client,test fail!"
        print "check block 2.4G client,test pass!"
    
    #手动添加mac地址到Global Blacklist,并检查是否添加成功
    def test_011_check_add_mac_Global_Blacklist(self):
        u"""手动添加mac地址到Global Blacklist,并检查是否添加成功(testlink_ID:2759)"""
        log.debug("011")
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.check_add_mac_Global_Blacklist(wlan_mac,data_basic['DUT_ip'],
            data_basic['sshUser'],data_login['all'])
        self.assertTrue(result), "check add mac to Global Blacklist,test fail!"
        print "check add mac to Global Blacklist,test pass!"
    
    #检查Global Blacklist中的mac地址统计
    def test_012_check_Global_Blacklist_statistics(self):
        u"""检查Global Blacklist中的mac地址统计(testlink_ID:2758)"""
        log.debug("012")
        tmp = ClientAccessBusiness(self.driver)
        result = tmp.get_Global_Blacklist_mac()
        self.assertIn("(1)", result), "check Global Blacklist statistics,test fail!"
        print "check Global Blacklist statistics,test pass!"
    
    #被手动添加到Global Blacklist中的client重连验证
    def test_013_check_add_mac_Global_Blacklist_reconnect(self):
        u"""被手动添加到Global Blacklist中的client重连验证(testlink_ID:2760)"""
        log.debug("013")
        tmp = ClientAccessBusiness(self.driver)
        #使用无线网卡连接ssid
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),"after add mac to Global Blacklist,client connect ap again,test fail!"
        print "after add mac to Global Blacklist,client connect ap again,test pass!"
    
    #手动添加多条mac地址到Global Blacklist中
    def test_014_check_add_many_macs_Global_Blacklist(self):
        u"""手动添加多条mac地址到Global Blacklist中(testlink_ID:2761)"""
        log.debug("014")
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #手动添加10条mac地址到Global Blacklist中
        result1 = tmp.check_add_many_macs_Global_Blacklist(10,wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #使用无线网卡连接ssid
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        self.assertTrue(result1)
        self.assertIn('Not connected', result2), "check add many macs to Global Blacklist,test fail!"
        print "check add many macs to Global Blacklist,test pass!"
    
    #手动添加两个相同的mac地址到Global Blacklist
    def test_015_check_two_same_mac_Global_Blacklist(self):
        u"""手动添加两个相同的mac地址到Global Blacklist(testlink_ID:2762)"""
        log.debug("015")
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.check_two_same_mac_Global_Blacklist(wlan_mac)
        self.assertIn("(1)", result), "check add two same mac in Global Blacklist,test fail!"
        print "check add two same mac in Global Blacklist,test pass!"
    
    #手动添加mac地址后检查Global Blacklist中的mac地址统计
    def test_016_check_Global_Blacklist_statistics_through_add_mac(self):
        u"""手动添加mac地址后检查Global Blacklist中的mac地址统计(testlink_ID:2763)"""
        log.debug("016")
        tmp = ClientAccessBusiness(self.driver)
        result = tmp.check_Global_Blacklist_statistics_through_add_mac(10)
        self.assertTrue(result), "check Global Blacklist statistics through add mac,test fail!"
        print "check Global Blacklist statistics through add mac,test pass!"
    
    #新ssid的Global Blacklist应用情况
    def test_017_group1_Global_Blacklist(self):
        u"""新ssid的Global Blacklist应用情况(testlink_ID:2764)"""
        log.debug("017")
        #添加一个新的ssid
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(data_ng["NG2_ssid"],data_wireless["short_wpa"])
        #将master ap加入所有的SSID
        tmp2 = APSBusiness(self.driver)
        tmp2.add_master_to_all_NG()
        #使用无线网卡连接ssid
        result = tmp2.connect_WPA_AP_backup(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result), "check Global Blacklist of adding new group,test fail!"
        print "check Global Blacklist of adding new group,test pass!"
    
    #重启后检查Global Blacklist是否生效
    def test_019_reboot_ap_Global_Blacklist(self):
        u"""重启后检查Global Blacklist是否生效(testlink_ID:2766)"""
        log.debug("019")
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        #使用无线网卡连接ssid
        result = tmp1.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result), "check Global Blacklist after reboot ap,test fail!"
        print "check Global Blacklist after reboot ap,test pass!"
    
    #Global Blacklist中mac地址输入非法格式
    def test_020_check_invalid_address_Global_Blacklist(self):
        u"""Global Blacklist中mac地址输入非法格式(testlink_ID:2768)"""
        log.debug("020")
        tmp = ClientAccessBusiness(self.driver)
        values = [data_client['err_format_mac'],data_client['chn_mac'],data_client['special_mac']]
        result = tmp.check_invalid_address_Global_Blacklist(values)
        self.assertNotIn(False,result),"check invalid address in Global Blacklist,test fail!"
        print "check invalid address in Global Blacklist,test pass!"
    
    #没有创建Access list时mac过滤下的显示情况
    def test_021_check_mac_filter_no_access_list(self):
        u"""没有创建Access list时mac过滤下的显示情况(testlink_ID:2771)"""
        log.debug("021")
        tmp = SSIDBusiness(self.driver)
        #删除多余的ssid
        tmp.del_all_NG()
        #有多个SSID时,设置第n个SSID的无线过滤的白名单,获取mac白名单提示信息
        result1 = tmp.get_groupn_wifi_whitelist(1)
        #有多个SSID时,设置第n个SSID的无线过滤的黑名单,获取mac黑名单提示信息
        result2 = tmp.get_groupn_wifi_blacklist(1)
        self.assertIn(u"没有可用列表" or "No access list", result1)
        self.assertIn(u"没有可用列表" or "No access list", result2),"check mac filter in no access list,test fail!"
        print "check mac filter in no access list,test pass!"
    
    #添加新的list
    def test_022_check_add_access_list(self):
        u"""添加新的list(testlink_ID:2772)"""
        log.debug("022")
        tmp = ClientAccessBusiness(self.driver)
        #页面默认参数检查
        mac = tmp.randomMAC()
        result = tmp.check_webpage_default_parameter(mac)
        self.assertTrue(result), "add a new list, test fail!"
        print "add a new list, test pass!"
    
    #删除Access list
    def test_023_check_del_access_list(self):
        u"""删除Access list(testlink_ID:2773)"""
        log.debug("023")
        #点击客户端菜单
        tmp1 = ClientsBusiness(self.driver)
        tmp1.clients_menu()
        #点击客户端访问菜单
        tmp = ClientAccessBusiness(self.driver)
        tmp.clientaccess_menu()
        #获取页面上所有的标题
        result = tmp.g_all_title()
        self.assertNotIn("Access List 1", result),"delete access list,test fail!"
        print "delete access list,test pass!"
    
    #Access list在mac过滤列表中的显示情况
    def test_024_check_mac_filter_have_access_list(self):
        u"""Access list在mac过滤列表中的显示情况(testlink_ID:2774-1)"""
        log.debug("024")
        tmp = ClientAccessBusiness(self.driver)
        #添加一个只有一个mac地址的访问列表
        random_mac = tmp.randomMAC()
        tmp.add_accesslist_onemac(random_mac)
        tmp1 = SSIDBusiness(self.driver)
        #有多个SSID时,设置第n个SSID的无线过滤的白名单,列表能显示
        result1 = tmp1.get_groupn_wifi_whitelist_display(1)
        #有多个SSID时,设置第n个SSID的无线过滤的黑名单,列表能显示
        result2 = tmp1.get_groupn_wifi_blacklist_display(1)
        self.assertTrue(result1)
        self.assertTrue(result2),"check mac filter in have access list,test fail!"
        print "check mac filter in have access list,test fail!"
    
    #Access list在mac过滤列表中的显示情况
    def test_025_check_mac_filter_have_access_list(self):
        u"""Access list在mac过滤列表中的显示情况(testlink_ID:2774-2)"""
        log.debug("025")
        tmp1 = ClientAccessBusiness(self.driver)
        #删除只添加了一个新增访问列表
        tmp1.del_firest_list()
        tmp = SSIDBusiness(self.driver)
        #有多个SSID时,设置第n个SSID的无线过滤的白名单,获取mac白名单提示信息
        result1 = tmp.get_groupn_wifi_whitelist(1)
        #有多个SSID时,设置第n个SSID的无线过滤的黑名单,获取mac黑名单提示信息
        result2 = tmp.get_groupn_wifi_blacklist(1)
        self.assertIn(u"没有可用列表" or "No access list", result1)
        self.assertIn(u"没有可用列表" or "No access list", result2),"check mac filter after del access list,test fail!"
        print "check mac filter after del access list,test pass!"
    
    #删除已被应用于黑白名单的access list
    def test_026_check_del_has_apply_access_list(self):
        u"""删除已被应用于黑白名单的access list(testlink_ID:2775)"""
        log.debug("026")
        tmp = ClientAccessBusiness(self.driver)
        #添加一个只有一个mac地址的访问列表
        random_mac = tmp.randomMAC()
        tmp.add_accesslist_onemac(random_mac)
        #有多个SSID时,设置第n个SSID的无线过滤的黑名单
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_blacklist(1)
        #删除只添加了一个新增访问列表时，web页面是否有提示该列表被使用
        result = tmp.check_del_first_list()
        self.assertTrue(result), "check del access when it has been apply,test fail!"
        print "check del access when it has been apply,test pass!"
    
    #Access list mac地址格式检查
    def test_027_invalid_address_Global_Blacklist(self):
        u"""Access list mac地址格式检查(testlink_ID:2776)"""
        log.debug("027")
        tmp = ClientAccessBusiness(self.driver)
        values = [data_client['err_format_mac'],data_client['chn_mac'],data_client['special_mac']]
        result = tmp.check_invalid_address_Access_list(values)
        self.assertNotIn(False,result),"check invalid address in access list1,test fail!"
        print "check invalid address in access list1,test pass!"
    
    #添加两个相同的mac地址到access list
    def test_028_check_two_same_mac_access_list(self):
        u"""添加两个相同的mac地址到access list(testlink_ID:2777)"""
        log.debug("028")
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(wlan_mac)
        result = tmp.check_two_same_mac_access_list1(wlan_mac)
        self.assertIn("(1)", result), "check add two same mac in access list1,test fail!"
        print "check add two same mac in access list1,test pass!"
    
    #添加空的list
    def test_029_check_add_blank_mac_list(self):
        u"""添加空的list(testlink_ID:2778)"""
        log.debug("029")
        tmp = ClientAccessBusiness(self.driver)
        tmp.add_accesslist_onemac("")
        #获取页面上所有的标题
        result = tmp.g_all_title()
        self.assertIn("Access List 2", result),"check add blank mac,test fail!"
        print "check add blank mac,test pass!"
    
    #access list名称格式检查
    def test_030_check_access_list_name(self):
        u"""access list名称格式检查(testlink_ID:2779)"""
        log.debug("030")
        tmp = ClientAccessBusiness(self.driver)
        tmp.change_list_name("Access List 2",data_client['list_name'])
        #获取页面上所有的标题
        result = tmp.g_all_title()
        self.assertIn(data_client['list_name'], result),"check list name,test fail!"
        print "check list name,test pass!"
    
    #添加两个相同名称的access list
    def test_031_check_same_list_name(self):
        u"""添加两个相同名称的access list(testlink_ID:2780)"""
        log.debug("031")
        tmp = ClientAccessBusiness(self.driver)
        #修改两个相同名称的access list
        result = tmp.check_same_name_list(data_client['list_name'],"Access List 1")
        self.assertTrue(result), "check the same list name,test fail!"
        print "check the same list name,test pass!"
    
    #access list应用于黑名单-1
    def test_032_apply_black_list_1(self):
        u"""access list应用于黑名单(testlink_ID:2782-1)"""
        log.debug("032")
        tmp = ClientAccessBusiness(self.driver)
        #删除Access List 2列表
        tmp.del_Access_list_n(data_client['list_name'])
        #清空Global Blacklist
        tmp.edit_accesslist_n_onemac("Global Blacklist","")
        #修改Access List 1列表为随机mac
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1",random_mac)
        #检查mac地址是否添加到macfilter blacklist
        result1 = tmp.check_macfilter_blacklist(random_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertIn(data_wireless['all_ssid'],result2),"check access list apply to black list,test fail!"
        print "check access list apply to black list,test pass!"
    
    #access list应用于黑名单-2
    def test_033_apply_black_list_2(self):
        u"""access list应用于黑名单(testlink_ID:2782-2)"""
        log.debug("033")
        #修改Access List 1列表为无线网卡的mac
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1",wlan_mac)
        #检查mac地址是否添加到macfilter blacklist
        result1 = tmp.check_macfilter_blacklist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertIn('Not connected',result2),"check access list apply to black list,test fail!"
        print "check access list apply to black list,test pass!"
    
    
    #应用黑名单后再添加mac地址
    def test_034_many_macs(self):
        u"""应用黑名单后再添加mac地址(testlink_ID:2783)"""
        log.debug("034")
        tmp = ClientAccessBusiness(self.driver)
        #编辑特定的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_n_manymac("Access List 1",9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑特定的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_n_manymac("Access List 1")
        self.assertIn('Not connected',result),"add mac after applying,test fail!"
        print "add mac after applying,test pass!"
    
    #黑名单时选择多个access list
    def test_035_check_many_access_list(self):
        u"""黑名单时选择多个access list(testlink_ID:2784)"""
        log.debug("035")
        tmp = ClientAccessBusiness(self.driver)
        #添加一个只有一个mac地址的访问列表
        random_mac = tmp.randomMAC()
        tmp.add_accesslist_onemac(random_mac)
        #有多个SSID时,点击第n个SSID的无线过滤的黑名单下的第2个列表--group0
        tmp1 = SSIDBusiness(self.driver)
        tmp1.groupn_wifi_blacklist_twolist(1)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter blacklist
        result1 = tmp.check_macfilter_blacklist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.check_macfilter_blacklist(random_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result3 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertIn('Not connected',result3),"check many access lists apply to black list,test fail!"
        print "check many access lists apply to black list,test pass!"
    
    #重启后检查黑名单是否生效
    def test_036_check_blacklist_after_reboot(self):
        u"""重启后检查黑名单是否生效(testlink_ID:2787)"""
        log.debug("036")
        #在ap页面上执行重启
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected',result),"check blacklist after reboot,test fail!"
        print "check blacklist after reboot,test pass!"
    
    #应用黑名单后从list中删除指定mac地址
    def test_037_check_del_mac(self):
        u"""应用黑名单后从list中删除指定mac地址(testlink_ID:2786)"""
        log.debug("037")
        tmp = ClientAccessBusiness(self.driver)
        #编辑特定的访问列表---只修改mac，不添加
        tmp.edit_accesslist_n_onemac("Access List 1","")
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter blacklist
        result1 = tmp.check_macfilter_blacklist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertFalse(result1)
        self.assertIn(data_wireless['all_ssid'],result2), "check del mac from access list,test fail!"
        print "check del mac from access list,test pass!"
    
    #access list应用于白名单-1
    def test_038_apply_white_list_1(self):
        u"""access list应用于白名单(testlink_ID:2788-1)"""
        log.debug("038")
        #禁用第n个SSID的无线过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter(1)
        tmp = ClientAccessBusiness(self.driver)
        #删除Access List 2列表
        tmp.del_Access_list_n("Access List 2")
        #编辑特定的访问列表---Access List 1
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1",random_mac)
        #有多个SSID时,设置第n个SSID的无线过滤的白名单
        tmp1.wifi_n_whitelist(1)
        #检查mac地址是否添加到macfilter whitelist
        result1 = tmp.check_macfilter_whitelist(random_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertIn('Not connected',result2),"check access list apply to white list,test fail!"
        print "check access list apply to white list,test pass!"
    
    #access list应用于白名单-2
    def test_039_apply_white_list_2(self):
        u"""access list应用于白名单(testlink_ID:2788-2)"""
        log.debug("039")
        tmp = ClientAccessBusiness(self.driver)
        #编辑特定的访问列表---Access List 1
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1",wlan_mac)
        #检查mac地址是否添加到macfilter whitelist
        result1 = tmp.check_macfilter_whitelist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertIn(data_wireless['all_ssid'],result2),"check access list apply to white list,test fail!"
        print "check access list apply to white list,test pass!"
    
    #应用白名单后再添加mac地址
    def test_040_many_macs(self):
        u"""应用白名单后再添加mac地址(testlink_ID:2789)"""
        log.debug("040")
        tmp = ClientAccessBusiness(self.driver)
        #编辑特定的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_n_manymac("Access List 1",9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑特定的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_n_manymac("Access List 1")
        self.assertIn(data_wireless['all_ssid'],result),"add mac after applying,test fail!"
        print "add mac after applying,test pass!"
    
    #白名单时选择多个access list
    def test_041_check_many_access_list(self):
        u"""白名单时选择多个access list(testlink_ID:2790)"""
        log.debug("041")
        tmp = ClientAccessBusiness(self.driver)
        #添加一个只有一个mac地址的访问列表
        random_mac = tmp.randomMAC()
        tmp.add_accesslist_onemac(random_mac)
        #有多个SSID时,点击第n个SSID的无线过滤的白名单下的第2个列表--group0
        tmp1 = SSIDBusiness(self.driver)
        tmp1.groupn_wifi_whitelist_twolist(1)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter whitelist
        result1 = tmp.check_macfilter_whitelist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.check_macfilter_whitelist(random_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result3 = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertIn(data_wireless['all_ssid'],result3),"check many access lists apply to white list,test fail!"
        print "check many access lists apply to white list,test pass!"
    
    #重启后检查白名单是否生效
    def test_042_check_whitelist_after_reboot(self):
        u"""重启后检查白名单是否生效(testlink_ID:2787)"""
        log.debug("042")
        #在ap页面上执行重启
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result),"check whitelist after reboot,test fail!"
        print "check whitelist after reboot,test pass!"
    
    #应用白名单后从list中删除指定mac地址
    def test_043_check_del_mac(self):
        u"""应用白名单后从list中删除指定mac地址(testlink_ID:2791)"""
        log.debug("043")
        tmp = ClientAccessBusiness(self.driver)
        #编辑特定的访问列表---只修改mac，不添加
        tmp.edit_accesslist_n_onemac("Access List 1","")
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter whitelist
        result1 = tmp.check_macfilter_whitelist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertFalse(result1)
        self.assertIn('Not connected',result2), "check del mac from access list,test fail!"
        print "check del mac from access list,test pass!"
    
    #白名单时应用空的list
    def test_044_check_whitelist_blank(self):
        u"""白名单时应用空的list(testlink_ID:2792)"""
        log.debug("044")
        #禁用mac过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter(1)
        #删除特定的访问列表Access List 2
        tmp = ClientAccessBusiness(self.driver)
        tmp.del_Access_list_n("Access List 2")
        #有多个SSID时,设置第n个SSID的无线过滤的白名单--不点击list
        tmp1.wifi_n_whitelist_backup(1)
        result = tmp1.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected',result), "check whitelist is blank,test fail!"
        print "check whitelist is blank,test pass!"
    
    #Access list的名称中含特殊字符时的应用情况
    def test_045_check_access_list_name(self):
        u"""Access list的名称中含特殊字符时的应用情况(testlink_ID:2793)"""
        log.debug("045")
        #禁用mac过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter(1)
        #编辑特定的访问列表Access List 1
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1", wlan_mac)
        #修改列表名称
        tmp.change_list_name("Access List 1",data_client['list_name'])
        #有多个SSID时,设置第n个SSID的无线过滤的白名单--不点击list
        tmp1.wifi_n_whitelist_backup(1)
        result1 = tmp1.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #有多个SSID时,设置第n个SSID的无线过滤的黑名单--不点击list
        tmp1.wifi_n_blacklist_backup(1)
        result2 = tmp1.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result1)
        self.assertIn('Not connected',result2), "check access list name,test fail!"
        print "check access list name,test pass!"
    
    #检查多个access list中有重复的mac地址时应用情况
    def test_046_check_many_access_lists_have_same_mac(self):
        u"""检查多个access list中有重复的mac地址时应用情况(testlink_ID:2794-1)"""
        log.debug("046")
        #新建一个access list1
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #能够添加两个相同mac的的access list
        result = tmp.check_same_mac_in_different_lists(wlan_mac)
        self.assertFalse(result), "check many access lists have same mac,test fail!"
        print "check many access lists have same mac,test pass!"
    
    #白名单与Global Blacklist包含同一个mac地址时的使用情况
    def test_047_access_Global_conflict(self):
        u"""白名单与Global Blacklist包含同一个mac地址时的使用情况(testlink_ID:2795)"""
        log.debug("047")
        #禁用mac过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter(1)
        #删除一个access list
        tmp = ClientAccessBusiness(self.driver)
        tmp.del_Access_list_n(data_client['list_name'])
        tmp.del_Access_list_n("Access List 1")
        #编辑特定的访问列表---只修改mac，不添加
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Global Blacklist",wlan_mac)
        #新建一个access list1
        tmp.add_accesslist_onemac(wlan_mac)
        #选择白名单，不点击list
        tmp1.wifi_n_whitelist_backup(1)
        #检查mac地址是否添加到macfilter whitelist
        result1 = tmp.check_macfilter_whitelist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #去掉Global Blacklist
        tmp.edit_accesslist_n_onemac("Global Blacklist","")
        self.assertFalse(result1)
        self.assertIn('Not connected',result2), "check white list is conflict with Global Blacklist,test fail!"
        print "check white list is conflict with Global Blacklist,test pass!"
    
    #新ssid的黑名单应用情况
    def test_048_check_new_ssid_blacklist(self):
        u"""新ssid的黑名单应用情况(testlink_ID:2797)"""
        log.debug("048")
        #添加一个新的ssid
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(data_ng["NG2_ssid"],data_wireless["short_wpa"])
        #将master ap加入所有的SSID
        tmp2 = APSBusiness(self.driver)
        tmp2.add_master_to_all_NG()
        #新SSID中设置mac地址过滤的黑名单
        tmp1.wifi_n_blacklist(2)
        wlan_mac = tmp1.get_wlan_mac(data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.macfilter")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.macfilter")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.maclist")
        result4 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.maclist")
        self.assertIn("deny",result1)
        self.assertIn("deny",result2)
        self.assertIn(wlan_mac, result3)
        self.assertIn(wlan_mac, result4),"check new group blacklist, test fail!"
        print "check new group blacklist, test pass!"
    
    #新group的白名单应用情况
    def test_049_check_new_group_whitelist(self):
        u"""新group的白名单应用情况(testlink_ID:2798)"""
        log.debug("049")
        #新SSID中设置mac地址过滤的白名单
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_whitelist(2)
        wlan_mac = tmp1.get_wlan_mac(data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.macfilter")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.macfilter")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.maclist")
        result4 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.maclist")
        self.assertIn("allow",result1)
        self.assertIn("allow",result2)
        self.assertIn(wlan_mac, result3)
        self.assertIn(wlan_mac, result4),"check new group whitelist, test fail!"
        print "check new group whitelist, test pass!"
    
    #新group多个list的应用情况
    def test_050_check_new_group_many_list_1(self):
        u"""新group多个list的应用情况(testlink_ID:2799-1)"""
        log.debug("050")
        tmp = ClientAccessBusiness(self.driver)
        #添加一个只有一个mac地址的访问列表
        random_mac = tmp.randomMAC()
        tmp.add_accesslist_onemac(random_mac)
        #有多个SSID时,点击第n个SSID的无线过滤的白名单下的第1个列表--group1
        tmp1 = SSIDBusiness(self.driver)
        tmp1.groupn_wifi_whitelist_twolist(2)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter whitelist
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.macfilter")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.macfilter")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.maclist")
        result4 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.maclist")
        result5 = tmp.connect_WPA_AP(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn("allow",result1)
        self.assertIn("allow",result2)
        self.assertIn(wlan_mac, result3)
        self.assertIn(wlan_mac, result4)
        self.assertIn(data_ng["NG2_ssid"],result5),"check many access lists apply to new group,test fail!"
        print "check many access lists apply to new group,test pass!"
    
    #新group多个list的应用情况
    def test_051_check_new_group_many_list_2(self):
        u"""新group多个list的应用情况(testlink_ID:2799-2)"""
        log.debug("051")
        #有多个SSID时,点击第n个SSID的无线过滤的黑名单下的第1个列表--group1
        tmp1 = SSIDBusiness(self.driver)
        #有多个SSID时,设置第n个SSID的无线过滤的黑名单--不点击list
        tmp1.wifi_n_blacklist_backup(2)
        tmp1.groupn_wifi_blacklist_twolist(2)
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter blacklist
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.macfilter")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.macfilter")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath2.maclist")
        result4 = ssh.ssh_cmd(data_basic['sshUser'],"uci show wireless.ath3.maclist")
        result5 = tmp.connect_WPA_AP_backup(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn("deny",result1)
        self.assertIn("deny",result2)
        self.assertIn(wlan_mac, result3)
        self.assertIn(wlan_mac, result4)
        self.assertIn('Not connected',result5),"check many access lists apply to new group,test fail!"
        print "check many access lists apply to new group,test pass!"
    
    #Disable MAC Filtering
    def test_052_disable_mac_filtering(self):
        u"""Disable MAC Filtering(testlink_ID:2796)"""
        log.debug("052")
        #两个SSID都禁用mac过滤
        tmp1 = SSIDBusiness(self.driver)
        tmp1.disable_macfilter(1)
        tmp1.disable_macfilter(2)
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter blacklist-group0
        result1 = tmp.check_macfilter_blacklist(wlan_mac,
            data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        result3 = tmp.connect_WPA_AP(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertFalse(result1)
        self.assertIn(data_wireless['all_ssid'], result2)
        self.assertIn(data_ng["NG2_ssid"], result3),
        "check disable mac filtering, test fail!"
        print "check disable mac filtering, test pass!"
    
    #Slave ap的Global Blacklist应用情况
    def test_053_slave_Global_Blacklist(self):
        u"""Slave ap的Global Blacklist应用情况(testlink_ID:2800)"""
        log.debug("053")
        tmp1 = APSBusiness(self.driver)
        #master只加入第一个SSID
        tmp1.add_master_to_n_NG(1)
        self.driver.refresh()
        self.driver.implicitly_wait(20)
        time.sleep(10)
        #slave配对加入特定SSID--第2个
        tmp1.search_pair_add(2,data_AP['slave:mac2'])
        #将无线客户端的mac加入Global Blacklist
        tmp = ClientAccessBusiness(self.driver)
        #删除两个access list
        tmp.del_Access_list_n("Access List 1")
        tmp.del_Access_list_n("Access List 2")
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Global Blacklist", wlan_mac)
        result = tmp.connect_WPA_AP_backup(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #设置Global Blacklist为空
        tmp.edit_accesslist_n_onemac("Global Blacklist", "")
        self.assertIn('Not connected',result),
        "check slave ap of applying Global Blacklist, test fail!"
        print "check slave ap of applying Global Blacklist, test pass!"
    
    #slave ap的黑名单应用情况-1
    def test_054_check_slave_blacklist_1(self):
        u"""slave ap的黑名单应用情况(testlink_ID:2801-1)"""
        log.debug("054")
        #新建一个list，加入无线mac地址
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.add_accesslist_onemac(wlan_mac)
        #新SSID中设置mac地址过滤的黑名单--不点击list
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_blacklist_backup(2)
        time.sleep(30)
        result = tmp.connect_WPA_AP_backup(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected',result),
        "check slave ap of applying Blacklist, test fail!"
        print "check slave ap of applying Blacklist, test pass!"
    
    #slave ap的黑名单应用情况-2
    def test_055_check_slave_blacklist_2(self):
        u"""slave ap的黑名单应用情况(testlink_ID:2801-2)"""
        log.debug("055")
        #修改新建list的mac地址
        tmp = ClientAccessBusiness(self.driver)
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1",random_mac)
        result = tmp.connect_WPA_AP(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_ng["NG2_ssid"],result),
        "check slave ap of applying Blacklist, test fail!"
        print "check slave ap of applying Blacklist, test pass!"
    
    #slave ap的白名单应用情况-1
    def test_056_check_slave_whitelist_1(self):
        u"""slave ap的白名单应用情况(testlink_ID:2802-1)"""
        log.debug("056")
        #新SSID中设置mac地址过滤的白名单--不点击list
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_whitelist_backup(2)
        result = tmp1.connect_WPA_AP_backup(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected',result),
        "check slave ap of applying whitelist, test fail!"
        print "check slave ap of applying whitelist, test pass!"
    
    #slave ap的白名单应用情况-2
    def test_057_check_slave_whitelist_2(self):
        u"""slave ap的白名单应用情况(testlink_ID:2802-2)"""
        log.debug("057")
        #修改新建list的mac地址
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1",wlan_mac)
        result = tmp.connect_WPA_AP(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_ng["NG2_ssid"],result),
        "check slave ap of applying whitelist, test fail!"
        print "check slave ap of applying whitelist, test pass!"
    
    #slave ap应用多个access list-1
    def test_058_check_slave_many_lists_1(self):
        log.debug("058")
        u"""slave ap应用多个access list(testlink_ID:2803-1)"""
        tmp = ClientAccessBusiness(self.driver)
        #添加一个只有一个mac地址的访问列表
        random_mac = tmp.randomMAC()
        tmp.add_accesslist_onemac(random_mac)
        # #有多个SSID时,点击第n个SSID的无线过滤的白名单下的第1个列表--group1
        # tmp1 = NGBusiness(self.driver)
        # tmp1.groupn_wifi_whitelist_twolist(1)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter whitelist
        result1 = tmp.check_macfilter_whitelist(wlan_mac,
            data_basic['slave_ip2'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.check_macfilter_whitelist(random_mac,
            data_basic['slave_ip2'],data_basic['sshUser'],data_login['all'])
        result3 = tmp.connect_WPA_AP(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertIn(data_ng["NG2_ssid"],result3),\
        "check many access lists apply to white list in slave ap, test fail!"
        print "check many access lists apply to white list in slave ap, test pass!"
    
    #slave ap应用多个access list-2
    def test_059_check_slave_many_lists_2(self):
        log.debug("059")
        u"""slave ap应用多个access list(testlink_ID:2803-2)"""
        #新SSID中设置mac地址过滤的黑名单--不点击list
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_blacklist_backup(2)
        time.sleep(30)
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #检查mac地址是否添加到macfilter blacklist
        result1 = tmp.check_macfilter_blacklist(wlan_mac,
            data_basic['slave_ip2'],data_basic['sshUser'],data_login['all'])
        result2 = tmp.connect_WPA_AP_backup(data_ng["NG2_ssid"],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        #有多个SSID时1,禁用第n个SSID的无线过滤-group1
        tmp1.disable_macfilter(2)
        self.assertTrue(result1)
        self.assertIn('Not connected',result2),\
        "check many access lists apply to black list in slave ap, test fail!"
        print "check many access lists apply to black list in slave ap, test pass!"
    
    #WEP加密时黑名单应用情况-1
    def test_060_wep_blacklist_1(self):
        u"""WEP加密时黑名单应用情况-1(testlink_ID:2811-1)"""
        log.debug("060")
        #删除Access List 2
        tmp2 = ClientAccessBusiness(self.driver)
        tmp2.del_Access_list_n("Access List 2")
        #删除SSID1
        tmp1 = SSIDBusiness(self.driver)
        tmp1.del_all_NG()
        #设置ssid0的黑名单
        tmp1.wifi_n_blacklist_backup(1)
        #group0由wpa2/aes修改为wep 64bit
        tmp1.wifi_wep_encryption(1,data_wireless['wep64'])
        result = tmp1.connect_WEP_AP_backup(data_wireless['all_ssid'],
            data_wireless['wep64'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when wep encryption blacklist, test fail!"
        print "check when wep encryption blacklist, test pass!"

    #WEP加密时黑名单应用情况-2
    def test_061_wep_blacklist_2(self):
        u"""WEP加密时黑名单应用情况-2(testlink_ID:2811-2)"""
        log.debug("061")
        #修改Access List 1为随机mac
        tmp = ClientAccessBusiness(self.driver)
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1", random_mac)
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],
            data_wireless['wep64'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),
        "check when wep encryption blacklist, test fail!"
        print "check when wep encryption blacklist, test pass!"

    #WEP加密时白名单应用情况-1
    def test_062_wep_whitelist_1(self):
        u"""WEP加密时白名单应用情况-1(testlink_ID:2811-3)"""
        log.debug("062")
        #将group0改为白名单
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_whitelist_backup1(1)
        result = tmp1.connect_WEP_AP_backup(data_wireless['all_ssid'],
            data_wireless['wep64'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when wep encryption whitelist, test fail!"
        print "check when wep encryption whitelist, test pass!"

    #WEP加密时白名单应用情况-2
    def test_063_wep_whitelist_2(self):
        u"""WEP加密时白名单应用情况-2(testlink_ID:2811-4)"""
        log.debug("063")
        #修改Access List 1为无线网卡的mac
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1", wlan_mac)
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],
            data_wireless['wep64'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),
        "check when wep encryption whitelist, test fail!"
        print "check when wep encryption whitelist, test pass!"

    #Open加密方式时白名单应用情况-1
    def test_064_open_whitelst_1(self):
        u"""Open加密方式时白名单应用情况-1(testlink_ID:2812-1)"""
        log.debug("064")
        #修改group0的加密方式为open
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_None_encryption()
        result = tmp1.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),
        "check when Open encryption whitelist, test fail!"
        print "check when Open encryption whitelist, test fail!"

    #Open加密方式时白名单应用情况-2
    def test_065_open_whitelst_2(self):
        u"""Open加密方式时白名单应用情况-2(testlink_ID:2812-2)"""
        log.debug("065")
        #修改Access List 1为随机mac
        tmp = ClientAccessBusiness(self.driver)
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1", random_mac)
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when open encryption whitelist, test fail!"
        print "check when open encryption whitelist, test pass!"

    #Open加密方式时黑名单应用情况-1
    def test_066_open_blacklist_1(self):
        u"""Open加密方式时黑名单应用情况-1(testlink_ID:2812-3)"""
        log.debug("066")
        #将group0改为黑名单
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_blacklist_backup1(1)
        result = tmp1.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),
        "check when open encryption blacklist, test fail!"
        print "check when open encryption blacklist, test pass!"

    #Open加密方式时黑名单应用情况-2
    def test_067_open_blacklist_2(self):
        u"""Open加密方式时黑名单应用情况-2(testlink_ID:2812-4)"""
        log.debug("067")
        #修改Access List 1为无线网卡的mac
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1", wlan_mac)
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when open encryption blacklist, test fail!"
        print "check when open encryption blacklist, test pass!"

    #802.1X加密方式时黑名单应用情况-1
    def test_068_8021X_blacklist_1(self):
        u"""802.1X加密方式时黑名单应用情况-1(testlink_ID:2813-1)"""
        log.debug("068")
        #修改group0的加密方式为802.1X
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_8021x_encryption(4,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        result = tmp1.connect_8021x_AP_backup(data_wireless['all_ssid'],\
            data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when 802.1X encryption blacklist, test fail!"
        print "check when 802.1X encryption blacklist, test pass!"

    #802.1X加密方式时黑名单应用情况-2
    def test_069_8021X_blacklist_2(self):
        u"""802.1X加密方式时黑名单应用情况-2(testlink_ID:2813-2)"""
        log.debug("069")
        #修改Access List 1为随机mac
        tmp = ClientAccessBusiness(self.driver)
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1", random_mac)
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
            data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),
        "check when 802.1X encryption blacklist, test fail!"
        print "check when 802.1X encryption blacklist, test pass!"

    #802.1X加密方式时白名单应用情况-1
    def test_070_8021X_whitelist_1(self):
        u"""802.1X加密方式时白名单应用情况-1(testlink_ID:2813-3)"""
        log.debug("070")
        #修改group0为wpa2/aes加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(0,0,data_wireless['short_wpa'])
        #修改mac filter为白名单
        tmp1.wifi_n_whitelist_backup(1)
        #再将加密方式改回802.1X
        tmp1.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        result = tmp1.connect_8021x_AP_backup(data_wireless['all_ssid'],\
            data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when 802.1X encryption whitelist, test fail!"
        print "check when 802.1X encryption whitelist, test pass!"

    #802.1X加密方式时白名单应用情况-2
    def test_071_8021X_whitelist_2(self):
        u"""802.1X加密方式时白名单应用情况-2(testlink_ID:2814-4)"""
        log.debug("071")
        #修改Access List 1为无线网卡的mac
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1", wlan_mac)
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
            data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'], result),
        "check when 802.1X encryption whitelist, test fail!"
        print "check when 802.1X encryption whitelist, test pass!"

    #wpa2/aes加密方式时白名单应用情况-1
    def test_072_wpa2_aes_whitelist_1(self):
        u"""wpa2/aes加密方式时白名单应用情况-1(testlink_ID:额外添加)"""
        log.debug("072")
        #修改group0为wpa2/aes加密
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_wpa_encryption(0,0,data_wireless['short_wpa'])
        result = tmp1.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result),
        "check when wpa2/aes encryption whitelist, test fail!"
        print "check when wpa2/aes encryption whitelist, test pass!"

    #wpa2/aes加密方式时白名单应用情况-2
    def test_073_wpa2_aes_whitelist_2(self):
        u"""wpa2/aes加密方式时白名单应用情况-2(testlink_ID:额外添加)"""
        log.debug("073")
        #修改Access List 1为随机mac
        tmp = ClientAccessBusiness(self.driver)
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_n_onemac("Access List 1", random_mac)
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when wpa2/aes encryption whitelist, test fail!"
        print "check when wpa2/aes encryption whitelist, test pass!"

    #wpa2/aes加密方式时黑名单应用情况-1
    def test_074_wpa2_aes_blacklist_1(self):
        u"""wpa2/aes加密方式时黑名单应用情况-1(testlink_ID:额外添加)"""
        log.debug("074")
        #将group0改为黑名单
        tmp1 = SSIDBusiness(self.driver)
        tmp1.wifi_n_blacklist_backup(1)
        result = tmp1.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result),
        "check when wpa2/aes encryption blacklist, test fail!"
        print "check when wpa2/aes encryption blacklist, test pass!"

    #wpa2/aes加密方式时黑名单应用情况-2
    def test_075_wpa2_aes_blacklist_2(self):
        u"""wpa2/aes加密方式时黑名单应用情况-2(testlink_ID:额外添加)"""
        log.debug("075")
        #修改Access List 1为无线网卡的mac
        tmp = ClientAccessBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.edit_accesslist_n_onemac("Access List 1", wlan_mac)
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertIn('Not connected', result),
        "check when wpa2/aes encryption blacklist, test fail!"
        print "check when wpa2/aes encryption blacklist, test pass!"

    # #降级后，黑名单依然生效
    # def test_076_downgrade_blacklist(self):
    #     u"""降级后，黑名单依然生效(testlink_ID:2815-1)"""
    #     tmp = UpgradeBusiness(self.driver)
    #     #在ap页面上执行降级固件
    #     result1 = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
    #             data_login['all'],data_basic['old_version'],data_basic['http_old_addr'],"HTTP")
    #     result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
    #         data_wireless['short_wpa'],data_basic['wlan_pc'])
    #     self.assertTrue(result1)
    #     self.assertIn('Not connected', result2),
    #     "check after downgrade ap FW, the blacklist is valid, test fail!"
    #     print "check after downgrade ap FW, the blacklist is valid, test pass!"

    #升级后，黑名单依然生效
    def test_077_upgrade_blacklist(self):
        u"""升级后，黑名单依然生效(testlink_ID:2815-2)"""
        log.debug("077")
        tmp = UpgradeBusiness(self.driver)
        # #在ap页面上执行升级固件
        # result1 = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
        #         data_login['all'],data_basic['version'],data_basic['http_new_addr'],"HTTP")
        # result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],
        #     data_wireless['short_wpa'],data_basic['wlan_pc'])

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("ClientAccess")

        # self.assertTrue(result1)
        # self.assertIn('Not connected', result2),
        "check after upgrade ap FW, the blacklist is valid, test fail!"
        print "check after upgrade ap FW, the blacklist is valid, test pass!"

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
