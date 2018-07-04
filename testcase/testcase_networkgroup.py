#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：用例集，调用networkgroup_business

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
log = Log("Networkgroup")
class TestNetworkGroup(unittest.TestCase):
    u"""测试网络组的用例集(runtime:11h)"""
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

    ####################################################################
    ##################以下是Network Group-Basic的测试用例##################
    ####################################################################
    #创建Network Group是否会出现对话框(testlink_ID:900_1)
    def test_002_check_create_dialog(self):
        u"""创建Network Group是否会出现对话框(testlink_ID:900_1)"""
        log.debug("002")
        #点击添加，检查页面上是否有添加对话框
        tmp = NGBusiness(self.driver)
        result = tmp.check_create_dialog()
        assert result,"check dialog after clicking add NG,test fail!"
        print "check dialog after clicking add NG,test pass!"

    #修改Network Group是否会出现对话框(testlink_ID:901)
    def test_003_check_edit_dialog(self):
        u"""修改Network Group是否会出现对话框(testlink_ID:901)"""
        log.debug("003")
        #点击编辑，检查页面上是否有添加对话框
        tmp = NGBusiness(self.driver)
        result = tmp.check_edit_dialog()
        assert result,"check dialog after clicking edit NG,test fail!"
        print "check dialog after clicking edit NG,test pass!"

    #点击网络组，添加一个新的网络组NG2(testlink_ID:900_2)
    def test_004_add_NG2(self):
        u"""测试添加一个新的网络组NG2(testlink_ID:900_2)"""
        log.debug("004")
        NG2_name = "%s-2"%data_ng["NG2_name"]
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        Add = NGBusiness(self.driver)
        Add.new_network_group(NG2_name,\
                NG2_ssid,data_wireless["short_wpa"])
        result = Add.check_new_NG(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'],NG2_name)
        print result
        assert result,"add a new network group,test fail!"
        print "add a new network group,test pass!"

    #删除新增的网络组NG2，并检查是否有提示框，判断是否删除成功(testlink_ID:902)
    def test_005_remove_NG2(self):
        u"""删除新增的网络组NG2，并检查是否有提示框，判断是否删除成功(testlink_ID:902)"""
        log.debug("005")
        NG2_name = "%s-2"%data_ng["NG2_name"]
        tmp = NGBusiness(self.driver)
        result1 = tmp.del_first_NG()
        result2 = tmp.check_new_NG(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'],NG2_name)
        print result1,result2
        assert result1 and (result2 == False),"remove a new network group,test fail!"
        print "remove a new network group,test pass!"

    #删除默认Network Group(testlink_ID:903)
    def test_006_del_group0(self):
        u"""删除默认Network Group(testlink_ID:903)"""
        log.debug("006")
        tmp = NGBusiness(self.driver)
        #删除默认的网络组
        result1,result2 = tmp.del_group0()
        assert result1 and (result2 == False),"delete default network group,test fail!"
        print "delete default network group,test pass!"

    #点击网络组，添加到最大16个网络组(testlink_ID:923)
    def test_007_add_NG_max(self):
        u"""测试点击网络组，添加到最大16个网络组(testlink_ID:904)"""
        log.debug("007")
        tmp = NGBusiness(self.driver)
        result = tmp.add_NG_max(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'],data_wireless["short_wpa"])
        assert result,"add the max number network group(16),test fail!"
        print "add the max number network group(16),test pass!"

     #16个Network Group配置可以正确配置于MasterAP(testlink_ID:921)--bug86448
    def test_008_check_master_maxNG_config(self):
        u"""16个Network Group配置可以正确配置于MasterAP(testlink_ID:921)--bug86448"""
        #将master ap加入所有的网络组
        tmp1 = APSBusiness(self.driver)
        tmp1.add_master_to_all_NG()
        time.sleep(600)
        #验证AP加入16个网络组后，配置是否生效
        tmp2 = NGBusiness(self.driver)
        result1,result2 = tmp2.check_maxNG_config(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'])
        #将master ap加入默认网络组
        tmp1.add_master_to_gourp0()
        assert ("HWaddr" in result1) and ("HWaddr" in result2),\
            "check Configuration after Master AP adding to 16 NG,test fail!"
        print "check Configuration after Master AP adding to 16 NG,test pass!"

    #16个Network Group配置可以正确同步于SlaveAP(testlink_ID:922)--bug86448
    def test_009_check_slave_maxNG_config(self):
        u"""16个Network Group配置可以正确同步于SlaveAP(testlink_ID:922)--bug86448"""
        #搜索-配对-slave加入所有的网络组
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add_to_all_NG(data_AP['slave:mac2'])
        time.sleep(600)
        #验证AP加入16个网络组后，配置是否生效
        tmp2 = NGBusiness(self.driver)
        result1,result2 = tmp2.check_maxNG_config(data_basic['slave_ip2'],data_basic['sshUser'],\
                               data_login['all'])
        #slave加入特定网络组
        self.driver.refresh()
        time.sleep(15)
        tmp1.add_slave_to_NG(data_AP['slave:mac2'],1)
        assert  ("HWaddr" in result1) and ("HWaddr" in result2),\
            "check Configuration after slave AP adding to 16 NG,test fail!"
        print "check Configuration after slave AP adding to 16 NG,test pass!"

    #Network Group 显示(testlink_ID:904)
    def test_010_check_all_display(self):
        u"""Network Group 显示(testlink_ID:904)"""
        tmp = NGBusiness(self.driver)
        #选择特定的一个网络组，disable网络组和wifi
        tmp.disable_NG_wifi(2)
        #验证16个网络组在页面的显示情况
        result1,result2,result3 = tmp.check_max_disaplay()
        assert (False not in result1) and (result2 == 30) and (result3 == 2),\
            "check max network group display,test fail!"
        print "check max network group display,test pass!"

    #删除所有网络组(testlink_ID:902)
    def test_011_del_NG_max(self):
        u"""删除所有网络组(testlink_ID:902)"""
        NG2_name = "%s-1"%data_ng["NG2_name"]
        tmp = NGBusiness(self.driver)
        tmp.del_all_NG()
        #检查master ap的网络组
        result1 = tmp.check_new_NG(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'],NG2_name)
        #检查slave ap的网络组
        result2 = tmp.check_new_NG(data_basic['slave_ip2'],data_basic['sshUser'],\
                               data_login['all'],NG2_name)
        #解除最后一个slave AP的配对
        tmp1 = APSBusiness(self.driver)
        tmp1.unpair_last_slave_ap(1)
        assert (result1 == False) and (result2 == False), "delete all network group,test fail!"
        print "delete all network group,test pass!"

    #Network Group 缺省名字(testlink_ID:906)
    def test_012_group0_name(self):
        u"""Network Group 缺省名字(testlink_ID:906)"""
        tmp = NGBusiness(self.driver)
        tmp.NG_menu()
        #获取所有的网络组名和SSID名
        result = tmp.get_titlediv()
        print result
        assert "group0" in result,"check default network gourp name,test fail!"
        print "check default network gourp name,test pass!"

    #新增Network Group 缺省名字(testlink_ID:907)
    def test_013_new_gourp_name(self):
        u"""新增Network Group 缺省名字(testlink_ID:907)"""
        tmp = NGBusiness(self.driver)
        #添加一个新网络组，不输入任何参数
        tmp.new_default()
        #获取所有的网络组名和SSID名
        result = tmp.get_titlediv()
        #删除所有网络组
        tmp.del_all_NG()
        print result
        assert "group1" in result,"check default new network gourp name,test fail!"
        print "check default new network gourp name,test pass!"

    #自定义组名字(合法名字）(testlink_ID:908)
    def test_014_check_legal_name(self):
        u"""自定义组名字(合法名字）(testlink_ID:908)"""
        NG_name = data_ng['NG_name32']
        NG_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = NGBusiness(self.driver)
        tmp.new_network_group(NG_name,NG_ssid,data_wireless["short_wpa"])
        result = tmp.check_new_NG(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'],NG_name)
        #删除所有网络组
        tmp.del_all_NG()
        print result
        assert result,"check 32bit legal name,test fail!"
        print "check 32bit legal name,test pass!"

    #自定义组名字(非法名字检测）(testlink_ID:909)
    def test_015_check_illegal_name(self):
        u"""自定义组名字(非法名字检测）(testlink_ID:909)"""
        NG_name = data_ng['NG_name40']
        NG_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = NGBusiness(self.driver)
        tmp.new_network_group(NG_name,NG_ssid,data_wireless["short_wpa"])
        result = len(tmp.get_NG_name(1))
        print result
        #删除所有网络组
        tmp.del_all_NG()
        assert result == 32,"check 40bit illegal name,test fail!"
        print "check 40bit illegal name,test pass!"

    #Vlan 启用(testlink_ID:910)
    def test_016_check_VLAN_enable(self):
        u"""Vlan 启用(testlink_ID:910)"""
        tmp = NGBusiness(self.driver)
        #添加网络组时，检查VLAN是否启用
        result1,result2,result3 = tmp.check_VLAN_enable()
        assert result1 and (result2 > 1) and result3,"check VLAN enable,test fail!"
        print "check VLAN enable,test pass!"

    #VLAN ID 的合法范围(2-4093)(testlink_ID:911)
    def test_017_check_VID_range(self):
        u"""VLAN ID 的合法范围(2-4093)(testlink_ID:911)"""
        VID = data_ng["all_VID"]
        tmp = NGBusiness(self.driver)
        #添加网络组时,检查VID的合理范围
        result1,result2 = tmp.check_VID_range(VID,data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_login['all'])
        assert (result1 == [True,True]) and (result2 == [True,True]),"check VID range,test fail!"
        print "check VID range,test pass!"

    #Network group 之间不能配置相同的VLAN ID(testlink_ID:912)
    def test_018_check_same_VID(self):
        u"""Network group 之间不能配置相同的VLAN ID(testlink_ID:912)"""
        tmp = NGBusiness(self.driver)
        #设置相同的VID的情况
        result = tmp.check_same_VID()
        #删除所有网络组
        tmp.del_all_NG()
        assert result,"check same VID,test fail!"
        print "check same VID,test pass!"

    #Network Group保存(testlink_ID:926)
    def test_019_check_config(self):
        u"""Network Group保存(testlink_ID:926)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check save network group configuration,test fail!"
        print "check save network group configuration,test pass!"

    #Network Group重启不会丢失或者篡改(testlink_ID:927)
    def test_020_check_reboot_config(self):
        u"""Network Group重启不会丢失或者篡改(testlink_ID:927)"""
        #新增一个网络组NG2
        NG2_name = "%s-2"%data_ng["NG2_name"]
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        Add = NGBusiness(self.driver)
        Add.new_network_group(NG2_name,\
                NG2_ssid,data_wireless["short_wpa"])
        #多个网络组时，搜索-配对-加入网络组
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add(2,data_AP['slave:mac2'])

        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        # time.sleep(90)
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(NG2_ssid,data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and \
            (NG2_ssid in result2),"check configuration after rebootting,test fail!"
        print "check configuration after rebootting,test pass!"

    #Network Group降级后不会丢失或者篡改(testlink_ID:928_1)
    def test_021_check_downgrade_config(self):
        u"""Network Group降级后不会丢失或者篡改(testlink_ID:928_1)"""
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行降级固件
        result1 = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['old_version'],data_basic['http_old_addr'],"HTTP")
        # time.sleep(90)
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        result3 = tmp.connect_WPA_AP(NG2_ssid,data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        print result1
        assert result1 and (data_wireless['all_ssid'] in result2) and \
            (NG2_ssid in result3),"check configuration after downupgrade,test fail!"
        print "check configuration after downgrade,test pass!"

    #Network Group升级后不会丢失或者篡改(testlink_ID:928_2)
    def test_022_check_upgrade_config(self):
        u"""Network Group升级后不会丢失或者篡改(testlink_ID:928_2)"""
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行升级固件
        result1 = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['version'],data_basic['http_new_addr'],"HTTP")
        # time.sleep(90)
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        result3 = tmp.connect_WPA_AP(NG2_ssid,data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        print result1
        assert result1 and (data_wireless['all_ssid'] in result2) and \
            (NG2_ssid in result3),"check configuration after upgrade,test fail!"
        print "check configuration after upgrade,test pass!"

    ##################################################################
    #################以下是SSID and Hide SSID的测试用例##################
    ##################################################################
    #SSID对英文的支持(testlink_ID:930_1)
    def test_023_check_SSID_letter(self):
        u"""SSID对英文的支持(testlink_ID:930_1)"""
        tmp = NGBusiness(self.driver)
        #删除所有网络组
        tmp.del_all_NG()
        #将slave ap解除配对
        tmp1 = APSBusiness(self.driver)
        tmp1.unpair_last_slave_ap(1)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['letter_ssid'],data_wireless["short_wpa"])
        result = tmp.ssid_scan_result_backup(data_wireless['letter_ssid'],data_basic["wlan_pc"])
        assert result,"Check letter SSID,test fail!"
        print "Check letter SSID,test pass!"

    #SSID对数字的支持(testlink_ID:930_2)
    def test_024_check_SSID_digital(self):
        u"""SSID对数字的支持(testlink_ID:930_2)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['digital_ssid'],data_wireless["short_wpa"])
        result = tmp.ssid_scan_result_backup(data_wireless['digital_ssid'],data_basic["wlan_pc"])
        assert result,"Check digital SSID,test fail!"
        print "Check digital SSID,test pass!"

    #SSID对英文+数字的支持(testlink_ID:930_3)
    def test_025_check_SSID_letter_digital(self):
        u"""SSID对英文+数字的支持(testlink_ID:930_3)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['digital_letter_ssid'],data_wireless["short_wpa"])
        result = tmp.ssid_scan_result_backup(data_wireless['digital_letter_ssid'],data_basic["wlan_pc"])
        assert result,"Check letter+digital SSID,test fail!"
        print "Check letter+digital SSID,test pass!"

    #SSID对ASCII的支持(testlink_ID:930_4)
    def test_026_check_SSID_ASCII(self):
        u"""SSID对ASCII的支持(testlink_ID:930_4)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['ascii_ssid'],data_wireless["short_wpa"])
        #获取所有的网络组名和SSID名
        result = tmp.get_titlediv()
        print result
        assert data_wireless['ascii_ssid'] in result,"Check ASCII SSID,test fail!"
        print "Check ASCII SSID,test pass!"

    #中文SSID的正常配置(testlink_ID:931)
    def test_027_check_SSID_CN(self):
        u"""中文SSID的正常配置(testlink_ID:931)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['CN_ssid'],data_wireless["short_wpa"])
        #获取所有的网络组名和SSID名
        result = tmp.get_titlediv()
        print result
        assert data_wireless['CN_ssid'] in result,"Check CN SSID,test fail!"
        print "Check CN SSID,test pass!"

    #特殊符号的SSID配置(testlink_ID:933)
    def test_028_check_SSID_special(self):
        u"""特殊符号的SSID配置(testlink_ID:933)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['special_ssid'],data_wireless["short_wpa"])
        #获取所有的网络组名和SSID名
        result = tmp.get_titlediv()
        print result
        assert data_wireless['special_ssid'] in result,"Check special SSID,test fail!"
        print "Check specail SSID,test pass!"

    #修改已配置的SSID(testlink_ID:934)
    def test_029_change_SSID(self):
        u"""修改已配置的SSID(testlink_ID:934)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid为全英文
        tmp.change_wifi_ssid_key(data_wireless['letter_ssid'],data_wireless["short_wpa"])
        result1 = tmp.connect_WPA_AP(data_wireless['letter_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert (data_wireless['letter_ssid'] in result1) and (data_wireless['all_ssid'] in result2),\
            "Check change SSID,test fail!"
        print "Check change SSID,test pass!"

    #验证SSID的字符长度限制(testlink_ID:935)
    def test_030_SSID_max(self):
        u"""验证SSID的字符长度限制(testlink_ID:935)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid为32位加abc的字符
        tmp.change_wifi_ssid_key(data_wireless['long_ssid']+"abc",data_wireless["short_wpa"])
        #获取所有的网络组名和SSID名
        result1 = tmp.get_titlediv()
        print result1
        result2 = tmp.connect_WPA_AP(data_wireless['long_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert ((data_wireless['long_ssid']+"abc") not in result1) and (data_wireless['long_ssid'] in result1) \
            and ((data_wireless['long_ssid']+"abc") not in result2) and (data_wireless['long_ssid'] in result2),\
            "Check max SSID,test fail!"
        print "Check max SSID,test pass!"

    #Name里含有空格的SSID(testlink_ID:936)
    def test_031_SSID_blank(self):
        u"""Name里含有空格的SSID(testlink_ID:936)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid为带空格的SSID
        ssid = data_wireless['letter_ssid']+" "+data_wireless['digital_ssid']
        tmp.change_wifi_ssid_key(ssid,data_wireless["short_wpa"])
        #获取所有的网络组名和SSID名
        result1 = tmp.get_titlediv()
        print result1
        result2 = tmp.connect_WPA_AP(ssid,data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert (ssid in result1) and (ssid in result2),"Check SSID contain blank,test fail!"
        print "Check SSID contain blank,test pass!"

    #关闭开启WIFI对连接在SSID无线终端的影响(testlink_ID:937)
    def test_032_disable_enable_wifi(self):
        u"""关闭开启WIFI对连接在SSID无线终端的影响(testlink_ID:937)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        #禁用默认网络组的wifi
        tmp.disable_enable_wifi()
        result2 = tmp.get_client_cmd_result("iw dev %s link"%data_basic['wlan_pc'])
        #启用默认网络组的wifi
        tmp.disable_enable_wifi()
        result3 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        #断开无线网络
        tmp.disconnect_ap()
        assert (data_wireless['all_ssid'] in result1) and ("Not connected" in result2)\
            and (data_wireless['all_ssid'] in result3),"Check client status after disable/enable wifi,test fail!"
        print "Check client status after disable/enable wifi,test pass!"

    #测试隐藏无线ssid(testlink_ID:938_1)
    def test_033_enable_hidden(self):
        u"""测试隐藏无线ssid(testlink_ID:938_1)"""
        tmp = NGBusiness(self.driver)
        #隐藏ssid
        tmp.hidden_ssid()
        #无线扫描，无法扫描到
        result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result2 = tmp.check_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result1,result2
        assert result2,"test hidden ssid,test fail!"
        print "test hidden ssid,test pass!"

    #重启后测试隐藏无线ssid是否依然生效(testlink_ID:938_2)
    def test_034_reboot_hidden_SSID(self):
        u"""重启后测试隐藏无线ssid是否依然生效(testlink_ID:938_2)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #无线扫描，无法扫描到
        result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result1,result2
        assert (data_wireless['all_ssid'] in result2),"test hidden ssid after rebootting,test fail!"
        print "test hidden ssid after rebootting,test pass!"

    #Hide SSID 的状态下修改SSID(testlink_ID:940)
    def test_035_modify_hidden_SSID(self):
        u"""Hide SSID 的状态下修改SSID(testlink_ID:940)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['letter_ssid'],data_wireless['short_wpa'])
        result = tmp.check_WPA_hiddenssid_AP(data_wireless['letter_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result,"test modify hidden ssid,test fail!"
        print "test modify hidden ssid,test pass!"

    #关闭、开启WIFI对连接在 Hide SSID 无线终端的影响(testlink_ID:941)
    def test_036_disable_hidden_wifi(self):
        u"""关闭、开启WIFI对连接在 Hide SSID 无线终端的影响(testlink_ID:941)"""
        tmp = NGBusiness(self.driver)
        #禁用默认网络组的wifi
        tmp.disable_enable_wifi()
        result1 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['letter_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        #启用默认网络组的wifi
        tmp.disable_enable_wifi()
        result2 = tmp.check_WPA_hiddenssid_AP(data_wireless['letter_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ("Not connected" in result1) and result2,"test disable/enable wifi on hidden ssid,test fail!"
        print "test disable/enable wifi on hidden ssid,test pass!"

    #Hide SSID 与 OPEN 加密模式的结合使用验证(testlink_ID:943)
    def test_037_OPEN_hidden_SSID(self):
        u"""Hide SSID 与 OPEN 加密模式的结合使用验证(testlink_ID:943)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为非加密
        tmp.wifi_None_encryption()
        result = tmp.connect_NONE_hiddenssid_AP(data_wireless['letter_ssid'],data_basic['wlan_pc'])
        #设置默认网络组无线为wpa/wpa2加密
        tmp.wifi_wpa_encryption(3,0,data_wireless['short_wpa'])
        assert data_wireless['letter_ssid'] in result,"test OPEN encryption hidden ssid,test fail!"
        print "test OPEN encryption hidden ssid,test pass!"

    #Hide SSID 与 Mac filter 结合使用验证(testlink_ID:944)
    def test_038_mac_filter_hidden_SSID(self):
        u"""Hide SSID 与 Mac filter 结合使用验证(testlink_ID:944)"""
        tmp = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        #添加一个只有一个mac地址的访问列表
        tmp.add_accesslist_onemac(mac)
        tmp1 = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的黑名单
        tmp1.wifi_blacklist()
        #无线连接这个的hidden AP
        result = tmp1.connect_WPA_hiddenssid_AP_backup(data_wireless['letter_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #禁用默认网络组的无线过滤
        tmp1.disable_macfilter(1)
        assert 'Not connected' in result,"test mac filter on hidden SSID,test fail!"
        print "test mac filter on hidden SSID,test pass!"

    #测试取消隐藏无线ssid(testlink_ID:942)
    def test_039_disable_hidden(self):
        u"""测试取消隐藏无线ssid(testlink_ID:942)"""
        tmp = NGBusiness(self.driver)
        #取消隐藏ssid
        tmp.hidden_ssid()
        #无线扫描，能够扫描到
        result1 = tmp.ssid_scan_result_backup(data_wireless['letter_ssid'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['letter_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result1
        assert result1 and (data_wireless['letter_ssid'] in result2) ,"test cancel hidden ssid,test fail!"
        print "test cancel hidden ssid,test pass!"

    #AP 2.4G和5G可以同时广播相同SSID(testlink_ID:945)
    def test_040_dual_band(self):
        u"""AP 2.4G和5G可以同时广播相同SSID(testlink_ID:945)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        #确认有两个无线接口
        tmp1 = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath0 | grep ESSID")
        result2 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath1 | grep ESSID")
        assert (data_wireless['all_ssid'] in result1) \
            and (data_wireless['all_ssid'] in result2),"test SSID broadcast of 2.4G and 5G,test fail!"
        print "test SSID broadcast of 2.4G and 5G,test pass!"

    #AP 2.4G和5G BSSID不相同(testlink_ID:946)
    def test_041_BSSID(self):
        u"""AP 2.4G和5G BSSID不相同(testlink_ID:946)"""
        tmp = SSH(data_basic['DUT_ip'],data_login['all'])
        #取2.4G的BSSID
        BSSID_2g4_tmp = tmp.ssh_cmd(data_basic['sshUser'],"iwconfig ath0 | grep Access")
        BSSID_2g4 = BSSID_2g4_tmp.strip("\n\t")[-21:-4]
        #取5G的BSSID
        BSSID_5g_tmp = tmp.ssh_cmd(data_basic['sshUser'],"iwconfig ath1 | grep Access")
        BSSID_5g = BSSID_5g_tmp.strip("\n\t")[-21:-4]
        print BSSID_2g4,BSSID_5g
        assert BSSID_2g4 != BSSID_5g,"test BSSID of 2.4G and 5G,test fail!"
        print "test BSSID of 2.4G and 5G,test pass!"

    ####################################################################
    ##################以下是加密的测试用例#################################
    ####################################################################
    #测试网络组中2.4g的无线加密-为不加密时(testlink_ID:949)
    def test_042_None_encryption(self):
        u"""测试网络组中2.4g的无线加密-为不加密时"""
         #切换2.4G频段
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("2.4GHz")

        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为非加密
        tmp.wifi_None_encryption()
        #无线连接这个非加密的无线
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test None encryption of wifi,test fail!"
        print "test None encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为5位wep64时(testlink_ID:950_1)
    def test_043_5wep64_encryption(self):
        u"""测试网络组中2.4g的无线加密-为5位wep64时(testlink_ID:950_1)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 5bits wep64 encryption of wifi,test fail!"
        print "test 5bits wep64 encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为10位wep64时(testlink_ID:950_2)
    def test_044_10wep64_encryption(self):
        u"""测试网络组中2.4g的无线加密-为10位wep64时(testlink_ID:950_2)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(0,data_wireless['wep64-10'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep64-10'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 10bits wep64 encryption of wifi,test fail!"
        print "test 10bits wep64 encryption of wifi,test pass!"

    #2.4g的WEP64bit参数校验1(testlink_ID:951_1)
    def test_045_abnormal1_wep(self):
        u"""2.4g的WEP64bit参数校验1(testlink_ID:951_1)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep64 abnormal1 encryption,test fail!"
        print "test wep64 abnormal1 encryption,test pass!"

    #2.4g的WEP64bit参数校验2(testlink_ID:951_2)
    def test_046_abnormal2_wep(self):
        u"""2.4g的WEP64bit参数校验2(testlink_ID:951_2)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep64 abnormal2 encryption,test fail!"
        print "test wep64 abnormal2 encryption,test pass!"

    #测试网络组中2.4g的无线加密-为13位wep128时(testlink_ID:952_1)
    def test_047_13wep128_encryption(self):
        u"""测试网络组中2.4g的无线加密-为13位wep128时(testlink_ID:952_1)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 13bits wep128 encryption of wifi,test fail!"
        print "test 13bits wep128 encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为26位wep128时(testlink_ID:952_2)
    def test_048_26wep128_encryption(self):
        u"""测试网络组中2.4g的无线加密-为26位wep128时(testlink_ID:952_2)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(0,data_wireless['wep128-26'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep128-26'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 26bits wep128 encryption of wifi,test fail!"
        print "test 26bits wep128 encryption of wifi,test pass!"

    #2.4g的WEP128bit参数校验1(testlink_ID:953_1)
    def test_049_abnormal1_wep(self):
        u"""2.4g的WEP128bit参数校验1(testlink_ID:953_1)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep128 abnormal1 encryption,test fail!"
        print "test wep128 abnormal1 encryption,test pass!"

    #2.4g的WEP128bit参数校验2(testlink_ID:953_2)
    def test_050_abnormal2_wep(self):
        u"""2.4g的WEP128bit参数校验2(testlink_ID:953_2)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep128 abnormal2 encryption,test fail!"
        print "test wep128 abnormal2 encryption,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-AES时(testlink_ID:954)
    def test_051_wpa_mixed_AES_encryption(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-AES时(testlink_ID:954)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-AES encryption of wifi,test pass!"

    #2.4g的WPA/WPA2-PSK AES参数校验(testlink_ID:956)
    def test_052_check_AES_arguments(self):
        u"""2.4g的WPA/WPA2-PSK AES参数校验(testlink_ID:956)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check AES arguments,test fail!"
        print "check AES arguments,test pass!"

    #2.4g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:958)
    def test_053_wpa_mixed_AES_max(self):
        u"""2.4g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:958)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK AES max length ,test fail!"
        print "check WPA/WPA2-PSK AES max length,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:959)
    def test_054_wpa_mixed_TKIP_encryption(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:959)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-TKIP的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-TKIP encryption of wifi,test fail!"
        print "test wpa/wpa2-TKIP encryption of wifi,test pass!"

    #2.4g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:960)
    def test_055_check_TKIP_arguments(self):
        u"""2.4g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:960)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check TKIP/AES arguments,test fail!"
        print "check TKIP/AES arguments,test pass!"

    #2.4g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:958)
    def test_056_wpa_mixed_TKIP_AES_max(self):
        u"""2.4g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:958)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK TKIP/AES max length ,test fail!"
        print "check WPA/WPA2-PSK TKIP/AES max length,test pass!"

    #测试网络组中2.4g的无线加密-为wpa2-AES时(testlink_ID:964)
    def test_057_wpa2_AES_encryption(self):
        u"""测试网络组中2.4g的无线加密-为wpa2-AES时(testlink_ID:964)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    #2.4g的wpa2-AES参数校验(testlink_ID:968)
    def test_058_check_WPA2_AES_arguments(self):
        u"""2.4g的wpa2-AES参数校验(testlink_ID:968)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES arguments,test fail!"
        print "check wpa2-AES arguments,test pass!"

    #2.4g的wpa2-AES 密钥长度限制验证(testlink_ID:973)
    def test_059_wpa2_AES_max(self):
        u"""2.4g的wpa2-AES 密钥长度限制验证(testlink_ID:973)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES max length ,test fail!"
        print "check wpa2-AES max length,test pass!"

    #测试网络组中2.4g的无线加密-为wpa2-TKIP/AES时(testlink_ID:966)
    def test_060_wpa2_TKIP_AES_encryption(self):
        u"""测试网络组中2.4g的无线加密-为wpa2-TKIP/AES时(testlink_ID:966)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-TKIP/AES encryption of wifi,test pass!"

    #2.4g的wpa2-TKIP/AES参数校验(testlink_ID:970)
    def test_061_check_WPA2_TKIP_AES_arguments(self):
        u"""2.4g的wpa2-TKIP/AES参数校验(testlink_ID:970)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AESAES arguments,test fail!"
        print "check wpa2-TKIP/AESAES arguments,test pass!"

    #2.4g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:973)
    def test_062_wpa2_TKIP_AES_max(self):
        u"""2.4g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:973)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AES max length ,test fail!"
        print "check wpa2-TKIP/AES max length,test pass!"

    #测试网络组中2.4g的无线加密-为wpa2-802.1x-TKIP/AES时
    def test_063_wpa2_802_1x_TKIP_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa2-802.1x-TKIP/AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-TKIP/AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa2-802.1x-AES时
    def test_064_wpa2_802_1x_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa2-802.1x-AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-AES时
    def test_065_wpa_mixed_802_1x_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(3,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时
    def test_066_wpa_mixed_802_1x_TKIP_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"


    #测试网络组中2.4g的无线加密再次改为wpa2-AES时(testlink_ID:964)
    def test_067_wpa_mixed_AES_encryption(self):
        u"""测试网络组中2.4g的无线加密再次改为wpa2-AES时(testlink_ID:964)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"







    #测试网络组中5g的无线加密-为不加密时(testlink_ID:949)
    def test_068_None_encryption(self):
        u"""测试网络组中5g的无线加密-为不加密时(testlink_ID:949)"""
        #切换仅5G频段
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("5GHz")

        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为非加密
        tmp.wifi_None_encryption()
        #无线连接这个非加密的无线
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test None encryption of wifi,test fail!"
        print "test None encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为5位wep64时(testlink_ID:950_1)
    def test_069_5wep64_encryption(self):
        u"""测试网络组中5g的无线加密-为5位wep64时(testlink_ID:950_1)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 5bits wep64 encryption of wifi,test fail!"
        print "test 5bits wep64 encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为10位wep64时(testlink_ID:950_2)
    def test_070_10wep64_encryption(self):
        u"""测试网络组中5g的无线加密-为10位wep64时(testlink_ID:950_2)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(0,data_wireless['wep64-10'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep64-10'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 10bits wep64 encryption of wifi,test fail!"
        print "test 10bits wep64 encryption of wifi,test pass!"

    #5g的WEP64bit参数校验1(testlink_ID:951_1)
    def test_071_abnormal1_wep(self):
        u"""5g的WEP64bit参数校验1(testlink_ID:951_1)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep64 abnormal1 encryption,test fail!"
        print "test wep64 abnormal1 encryption,test pass!"

    #5g的WEP64bit参数校验2(testlink_ID:951_2)
    def test_072_abnormal2_wep(self):
        u"""5g的WEP64bit参数校验2(testlink_ID:951_2)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep64 abnormal2 encryption,test fail!"
        print "test wep64 abnormal2 encryption,test pass!"

    #测试网络组中5g的无线加密-为13位wep128时(testlink_ID:952_1)
    def test_073_13wep128_encryption(self):
        u"""测试网络组中5g的无线加密-为13位wep128时(testlink_ID:952_1)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 13bits wep128 encryption of wifi,test fail!"
        print "test 13bits wep128 encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为26位wep128时(testlink_ID:952_2)
    def test_074_26wep128_encryption(self):
        u"""测试网络组中5g的无线加密-为26位wep128时(testlink_ID:952_2)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(0,data_wireless['wep128-26'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep128-26'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 26bits wep128 encryption of wifi,test fail!"
        print "test 26bits wep128 encryption of wifi,test pass!"

    #5g的WEP128bit参数校验1(testlink_ID:953_1)
    def test_075_abnormal1_wep(self):
        u"""5g的WEP128bit参数校验1(testlink_ID:953_1)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep128 abnormal1 encryption,test fail!"
        print "test wep128 abnormal1 encryption,test pass!"

    #5g的WEP128bit参数校验2(testlink_ID:953_1)
    def test_076_abnormal2_wep(self):
        u"""5g的WEP128bit参数校验2(testlink_ID:953_1)"""
        tmp = NGBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep128 abnormal2 encryption,test fail!"
        print "test wep128 abnormal2 encryption,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-AES时(testlink_ID:954)
    def test_077_wpa_mixed_AES_encryption(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-AES时(testlink_ID:954)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-AES encryption of wifi,test pass!"

    #5g的WPA/WPA2-PSK AES参数校验(testlink_ID:956)
    def test_078_check_AES_arguments(self):
        u"""5g的WPA/WPA2-PSK AES参数校验(testlink_ID:956)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check AES arguments,test fail!"
        print "check AES arguments,test pass!"

    #5g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:958)
    def test_079_wpa_mixed_AES_max(self):
        u"""5g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:958)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK AES max length ,test fail!"
        print "check WPA/WPA2-PSK AES max length,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:959)
    def test_080_wpa_mixed_TKIP_encryption(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:959)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-TKIP的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-TKIP encryption of wifi,test fail!"
        print "test wpa/wpa2-TKIP encryption of wifi,test pass!"

    #5g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:960)
    def test_081_check_TKIP_arguments(self):
        u"""5g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:960)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check TKIP/AES arguments,test fail!"
        print "check TKIP/AES arguments,test pass!"

    #5g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:958)
    def test_082_wpa_mixed_TKIP_AES_max(self):
        u"""5g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:958)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK TKIP/AES max length ,test fail!"
        print "check WPA/WPA2-PSK TKIP/AES max length,test pass!"

    #测试网络组中5g的无线加密-为wpa2-AES时(testlink_ID:964)
    def test_083_wpa2_AES_encryption(self):
        u"""测试网络组中5g的无线加密-为wpa2-AES时(testlink_ID:964)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    #5g的wpa2-AES参数校验(testlink_ID:968)
    def test_084_check_WPA2_AES_arguments(self):
        u"""5g的wpa2-AES参数校验(testlink_ID:968)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES arguments,test fail!"
        print "check wpa2-AES arguments,test pass!"

    #5g的wpa2-AES 密钥长度限制验证(testlink_ID:973)
    def test_085_wpa2_AES_max(self):
        u"""5g的wpa2-AES 密钥长度限制验证(testlink_ID:973)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES max length ,test fail!"
        print "check wpa2-AES max length,test pass!"

    #测试网络组中5g的无线加密-为wpa2-TKIP/AES时(testlink_ID:966)
    def test_086_wpa2_TKIP_AES_encryption(self):
        u"""测试网络组中5g的无线加密-为wpa2-TKIP/AES时(testlink_ID:966)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-TKIP/AES encryption of wifi,test pass!"

    #5g的wpa2-TKIP/AES参数校验(testlink_ID:967)
    def test_087_check_WPA2_TKIP_AES_arguments(self):
        u"""5g的wpa2-TKIP/AES参数校验(testlink_ID:967)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AESAES arguments,test fail!"
        print "check wpa2-TKIP/AESAES arguments,test pass!"

    #5g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:973)
    def test_088_wpa2_TKIP_AES_max(self):
        u"""5g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:973)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AES max length ,test fail!"
        print "check wpa2-TKIP/AES max length,test pass!"

    #测试网络组中5g的无线加密-为wpa2-802.1x-TKIP/AES时
    def test_089_wpa2_802_1x_TKIP_AES(self):
        u"""测试网络组中5g的无线加密-为wpa2-802.1x-TKIP/AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-TKIP/AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa2-802.1x-AES时
    def test_090_wpa2_802_1x_AES(self):
        u"""测试网络组中5g的无线加密-为wpa2-802.1x-AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-802.1x-AES时
    def test_091_wpa_mixed_802_1x_AES(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-802.1x-AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(3,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时
    def test_092_wpa_mixed_802_1x_TKIP_AES(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"


    #测试网络组中5g的无线加密再次改为wpa2-AES时(testlink_ID:964)
    def test_093_wpa2_AES_encryption(self):
        u"""测试网络组中5g的无线加密再次改为wpa2-AES时(testlink_ID:964)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #切换Dual-Band频段
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("Dual-Band")
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    ####################################################################
    ##################以下是Mac Filter的测试用例###########################
    ####################################################################
    #设置默认网络组的无线过滤的白名单,添加本机无线mac地址，并判断无线是否能够连接成功(testlink_ID:986_1)
    def test_094_mac_whitelist_in(self):
        u"""设置默认网络组的无线过滤的白名单,添加本机无线mac地址，并判断无线是否能够连接成功(testlink_ID:986_1)"""
        tmp = NGBusiness(self.driver)
        #取本机无线mac地址
        #mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test mac in whitelist,test fail!"
        print "test mac in whitelist,test pass!"

    #设置默认网络组的无线过滤的白名单,添加随机mac，并判断本机无线是否能够连接成功(testlink_ID:986_2)
    def test_095_mac_whitelist_out(self):
        u"""设置默认网络组的无线过滤的白名单,添加随机mac，并判断本机无线是否能够连接成功(testlink_ID:986_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp.randomMAC()
        print random_mac
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert 'Not connected' in result,"test mac out whitelist,test fail!"
        print "test mac out whitelist,test pass!"

    #设置默认网络组的无线过滤的白名单,添加随机大写的mac地址(testlink_ID:981_1)
    def test_096_upper_mac_whitelist_out(self):
        u"""设置默认网络组的无线过滤的白名单,添加随机大写的mac地址(testlink_ID:981_1)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #mac地址改变为大写
        RANDON_MAC = random_mac.upper()
        print RANDON_MAC
        tmp.edit_accesslist_onemac(RANDON_MAC)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert 'Not connected' in result,"test upper mac out whitelist,test fail!"
        print "test upper mac out whitelist,test pass!"

    #设置默认网络组的无线过滤的白名单,添加随机小写的mac地址(testlink_ID:981_2)
    def test_097_lower_mac_whitelist_out(self):
        u"""设置默认网络组的无线过滤的白名单,添加随机小写的mac地址(testlink_ID:981_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        # tmp = NGBusiness(self.driver)
        # #设置默认网络组的无线过滤的白名单
        # tmp.wifi_whitelist(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test lower mac out whitelist,test fail!"
        print "test lower mac out whitelist,test pass!"

    #添加10条mac地址白名单，确认其有效性(testlink_ID:985)
    def test_098_many_mac_whitelist(self):
        u"""添加10条mac地址白名单，确认其有效性(testlink_ID:985)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        tmp1 = NGBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp1.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 10) and (data_wireless['all_ssid'] in result2),"test many mac_whitelist,test fail!"
        print "test many mac_whitelist,test pass!"

    #删除所有的mac地址白名单，仅保留PC本身的mac，确认其有效性(testlink_ID:982)
    def test_099_del_many_mac_whitelist(self):
        u"""删除所有的mac地址白名单，仅保留PC本身的mac，确认其有效性(testlink_ID:982)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        tmp1 = NGBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp1.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 1) and (data_wireless['all_ssid'] in result2),"test del all mac_whitelist,test fail!"
        print "test del all mac_whitelist,test pass!"

    #设置默认网络组的无线过滤的黑名单,添加本机mac地址，并判断无线不能连接成功(testlink_ID:984_1)
    def test_100_mac_blacklist_in(self):
        u"""设置默认网络组的无线过滤的黑名单,添加本机mad地址，并判断无线不能连接成功(testlink_ID:984_1)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test mac in blacklist,test fail!"
        print "test mac in blacklist,test pass!"

    #设置默认网络组的无线过滤的黑名单,添加随机mac，并判断本机无线能够连接成功(testlink_ID:984_2)
    def test_101_mac_blacklist_out(self):
        u"""设置默认网络组的无线过滤的黑名单,添加随机mac，并判断本机无线能够连接成功(testlink_ID:984_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp.randomMAC()
        print random_mac
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test mac out blacklist,test fail!"
        print "test mac out blacklist,test pass!"

    #添加10条mac地址黑名单，确认其有效性(testlink_ID:985)
    def test_102_many_mac_blacklist(self):
        u"""添加10条mac地址黑名单，确认其有效性(testlink_ID:985)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        tmp1 = NGBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp1.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 10) and (data_wireless['all_ssid'] in result2),"test many mac_blacklist,test fail!"
        print "test many mac_blacklist,test pass!"

    #删除所有的mac地址黑名单，仅保留PC本身的mac，确认其有效性(testlink_ID:983)
    def test_103_del_many_mac_blacklist(self):
        u"""删除所有的mac地址黑名单，仅保留PC本身的mac，确认其有效性(testlink_ID:983)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        tmp1 = NGBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，黑名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp1.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result1 == 1 and ('Not connected' in result2),"test del all mac_blacklist,test fail!"
        print "test del all mac_blacklist,test pass!"

    #禁用mac filter，并判断本机无线能够连接成功(testlink_ID:988)
    def test_104_mac_blacklist_out(self):
        u"""禁用mac filter，并判断本机无线能够连接成功(testlink_ID:988)"""
        #禁用默认网络组的无线过滤
        tmp = NGBusiness(self.driver)
        tmp.disable_macfilter(1)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test mac out blacklist,test fail!"
        print "test mac out blacklist,test pass!"

    #Blacklist 多 group环境应用功能验证1(testlink_ID:989_1)
    def test_105_manygroup_blacklist1(self):
        u"""Blacklist 多 group环境应用功能验证1(testlink_ID:989_1)"""
        #添加一个新的网络组NG2
        tmp = NGBusiness(self.driver)
        NG2_name = "%s-2"%data_ng["NG2_name"]
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp.new_network_group(NG2_name,NG2_ssid,data_wireless["short_wpa"])
        #有多个网络组时,设置第1个网络组(即NG2网络组)的无线过滤的黑名单
        tmp.groupn_wifi_blacklist(1)
        #搜索-配对-加入新的网络组NG2
        pair = APSBusiness(self.driver)
        pair.search_pair_add(2,data_AP['slave:mac2'])
        #连接group0的无线
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接新的网络组NG2的无线
        result2 = tmp.connect_WPA_AP_backup(NG2_ssid,data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "test blacklist item1 of many groups,test fail!"
        print "test blacklist item1 of many groups,test pass!"

    #Blacklist 多 group环境应用功能验证2(testlink_ID:989_2)
    def test_106_manygroup_blacklist2(self):
        u"""Blacklist 多 group环境应用功能验证2(testlink_ID:989_2)"""
        tmp = NGBusiness(self.driver)
        #有多个网络组时,设置gourp0的无线过滤的黑名单
        tmp.groupn_wifi_blacklist_backup(2)
        #有多个网络组时,禁用新的网络组NG2的无线过滤
        tmp.disable_macfilter(1)
        time.sleep(60)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接新的网络组NG2的无线
        result2 = tmp.connect_WPA_AP("%s-2"%data_ng["NG2_ssid"],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ("%s-2"%data_ng["NG2_ssid"] in result2),\
            "test blacklist item2 of many groups,test fail!"
        print "test blacklist item2 of many groups,test pass!"

    #Blacklist 多 group环境应用功能验证3(testlink_ID:989_3)
    def test_107_manygroup_blacklist3(self):
        u"""Blacklist 多 group环境应用功能验证3(testlink_ID:989_3)"""
        tmp = NGBusiness(self.driver)
        #mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        #有多个网络组时,设置新的网络组NG2的无线过滤的黑名单
        tmp.groupn_wifi_blacklist_backup(1)
        time.sleep(60)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接新的网络组NG2的无线
        result2 = tmp.connect_WPA_AP_backup("%s-2"%data_ng["NG2_ssid"],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ('Not connected' in result2),\
            "test blacklist item3 of many groups,test fail!"
        print "test blacklist item3 of many groups,test pass!"

    #Whitelist 多 group环境应用功能验证1(testlink_ID:990_1)
    def test_108_manygroup_whitelist1(self):
        u"""Whitelist 多 group环境应用功能验证1(testlink_ID:990_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp1.randomMAC()
        tmp1.edit_accesslist_onemac(random_mac)
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = NGBusiness(self.driver)
        #有多个网络组时,设置新的网络组NG2的无线过滤的白名单
        tmp.groupn_wifi_whitelist(1)
        #有多个网络组时,禁用gourp0的无线过滤
        tmp.disable_macfilter(2)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接新的网络组NG2的无线
        result2 = tmp.connect_WPA_AP_backup(NG2_ssid,data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "test Whitelist item1 of many groups,test fail!"
        print "test Whitelist item1 of many groups,test pass!"

    #Whitelist 多 group环境应用功能验证2(testlink_ID:990_2)
    def test_109_manygroup_whitelist2(self):
        u"""Whitelist 多 group环境应用功能验证2(testlink_ID:990_2)"""
        tmp = NGBusiness(self.driver)
        #有多个网络组时,设置gourp0的无线过滤的白名单
        tmp.groupn_wifi_whitelist_backup(2)
        #有多个网络组时,禁用新的网络组NG2的无线过滤
        tmp.disable_macfilter(1)
        time.sleep(60)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接新的网络组NG2的无线
        result2 = tmp.connect_WPA_AP("%s-2"%data_ng["NG2_ssid"],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ("%s-2"%data_ng["NG2_ssid"] in result2),\
            "test Whitelist item2 of many groups,test fail!"
        print "test Whitelist item2 of many groups,test pass!"

    #Whitelist 多 group环境应用功能验证3(testlink_ID:990_3)
    def test_110_manygroup_whitelist3(self):
        u"""Whitelist 多 group环境应用功能验证3(testlink_ID:990_3)"""
        tmp = NGBusiness(self.driver)
        #有多个网络组时,设置新的网络组NG2的无线过滤的白名单
        tmp.groupn_wifi_whitelist_backup(1)
        time.sleep(60)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接新的网络组NG2的无线
        result2 = tmp.connect_WPA_AP_backup("%s-2"%data_ng["NG2_ssid"],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ('Not connected' in result2),\
            "test Whitelist item3 of many groups,test fail!"
        print "test Whitelist item3 of many groups,test pass!"

    #Blacklist和whitelist在多 group环境里冲突时的功能验证1(testlink_ID:991_1)
    def test_111_manygroup_black_white1(self):
        u"""Blacklist和whitelist在多 group环境里冲突时的功能验证1(testlink_ID:991_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        #设置group0的黑名单
        tmp.groupn_wifi_blacklist_backup(2)
        # #设置NG2的白名单
        # tmp.groupn_wifi_whitelist(1)
        # tmp.groupn_wifi_whitelist(1)
        time.sleep(60)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接NG2的无线
        result2 = tmp.connect_WPA_AP(NG2_ssid,data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and (NG2_ssid in result2),\
            "test blacklist and whitelist item1 of many groups,test fail!"
        print "test blacklist and whitelist item1 of many groups,test pass!"

    #Blacklist和whitelist在多 group环境里冲突时的功能验证2(testlink_ID:991_2)
    def test_112_manygroup_black_white2(self):
        u"""Blacklist和whitelist在多 group环境里冲突时的功能验证2(testlink_ID:991_2)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp1.randomMAC()
        tmp1.edit_accesslist_onemac(random_mac)
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        result1 = tmp1.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接NG2的无线
        result2 = tmp1.connect_WPA_AP_backup(NG2_ssid,data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "test blacklist and whitelist item2 of many groups,test fail!"
        print "test blacklist and whitelist item2 of many groups,test pass!"

    #重启后检查Blacklist和whitelist在多 group环境里是否依然生效(testlink_ID:993)
    def test_113_reboot_manygroup_black_white(self):
        u"""重启后检查Blacklist和whitelist在多 group环境里是否依然生效(testlink_ID:993)"""
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        time.sleep(60)
        #连接group0的无线
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #连接NG2的无线
        result2 = tmp.connect_WPA_AP_backup(NG2_ssid,data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "test blacklist and whitelis of many groups after reboot,test fail!"
        print "test blacklist and whitelis of many groups after reboot,test pass!"


    ###################################################################
    #################以下是Random Passoword的测试用例##################
    ###################################################################

    #恢复出厂后默认SSID验证(testlink_ID:1252)
    def test_114_default_ssid(self):
        u"""恢复出厂后默认SSID验证(testlink_ID:1252)"""
        tmp = APSBusiness(self.driver)
        tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        #取得默认的ssid
        tmp1 = SWBusiness(self.driver)
        result = tmp1.check_default_ssid(data_AP['master:mac'])
        assert result,"after reset the AP check default ssid,fail!"
        print "after reset the AP check default ssid,pass!"

    #默认随机密码验证(testlink_ID:1253)
    def test_115_have_default_pwd(self):
        u"""默认随机密码验证(testlink_ID:1253)"""
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        #取出ap的2.4G的无线的默认密码
        default_pwd_2g4 = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath0.key')
        #取出ap的5G的无线的默认密码
        default_pwd_5g = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath1.key')
        assert ('wireless.ath0.key' in default_pwd_2g4) and ('wireless.ath1.key' in default_pwd_5g),\
            "after reset the AP have default pwd,fail!"
        print "after reset the AP have default pwd,pass!"

    #对比标签密码与实际密码(testlink_ID:1254)
    def test_116_default_pwd(self):
        u"""对比标签密码与实际密码(testlink_ID:1254)"""
        #登录路由后台取出初始配置的密码
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        pwd_str = ssh.ssh_cmd(data_basic['sshUser'],'cat /proc/gxp/dev_info/security/ssid_password')
        pwd = pwd_str.strip("\r\n")
        #取出ap的2.4G的无线的默认密码
        default_pwd_2g4 = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath0.key')
        #取出ap的5G的无线的默认密码
        default_pwd_5g = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath1.key')
        assert (pwd in default_pwd_2g4) and (pwd in default_pwd_5g),\
            "after reset the AP check default pwd,fail!"
        print "after reset the AP check default pwd,pass!"

    #默认wifi状态(testlink_ID:1255)
    def test_117_default_wifi_status(self):
        u"""默认wifi状态(testlink_ID:1255)"""
        tmp = SWBusiness(self.driver)
        result = tmp.wifi_status()
        print result
        assert result == 'true',"test defalut wifi status,test fail!"
        print "test defalut wifi status,test pass!"

    #随机密码真实性验证(testlink_ID:1256)
    def test_118_check_default_pwd(self):
        u"""随机密码真实性验证(testlink_ID:1256)"""
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
        assert ssid in result1,"test check default pwd,test fail!"
        print "test check default pwd,test pass!"

    #SSID与wifi密码修改(testlink_ID:1257)
    def test_119_change_ssid_pwd(self):
        u"""SSID与wifi密码修改(testlink_ID:1257)"""
        #修改默认网络组的ssid和密码
        tmp1 = NGBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        #使用无线网卡连接该AP
        result = tmp1.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                     data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"change default ssid and pwd,test fail!"
        print "change default ssid and pwd,test pass!"

    #重启后检查SSID与wifi密码(testlink_ID:1260)
    def test_120_reboot_check_ssid_pwd(self):
        u"""重启后检查SSID与wifi密码(testlink_ID:1260)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #使用无线网卡连接该AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                     data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"reboot ap after change default ssid and pwd,test fail!"
        print "reboot ap after change default ssid and pwd,test pass!"

    #配对后slave ap的ssid和密码(testlink_ID:1257_1)
    def test_121_slaveAP_ssid_pwd(self):
        u"""配对后slave ap的ssid和密码(testlink_ID:1257_1)"""
        #搜索AP并配对
        tmp = APSBusiness(self.driver)
        tmp.search_pair_AP(data_AP['slave:mac1'],data_AP['slave:mac2'])
        #登录路由后台取出ssid和密码
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        ssid_2g4 = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath0.ssid')
        ssid_5g = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath1.ssid')
        pwd_2g4 = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath0.key')
        pwd_5g = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath1.key')
        #将slave ap解除配对
        tmp.unpair_last_slave_ap(2)
        assert (data_wireless['all_ssid'] in ssid_2g4) and (data_wireless['all_ssid'] in ssid_5g) \
            and (data_wireless["short_wpa"] in pwd_2g4) and (data_wireless["short_wpa"] in pwd_5g),\
            "after pair slave ap check ssid and pwd,test fail!"
        print "after pair slave ap check ssid and pwd,test pass!"



    ####################################################################
    ##################以下是Client Isolation的测试用例##################
    ####################################################################
    #Gateway MAC Address为空的配置验证(testlink_ID:1534)
    def test_122_check_wifi_isolation_gateway_mac_blank(self):
        u"""Gateway MAC Address为空的配置验证(testlink_ID:1534)"""
        tmp = NGBusiness(self.driver)
        #配置group0的客户端隔离的网关mac为错误的测试
        result1,result2 = tmp.check_wifi_isolation_gateway_mac_err("")
        assert (result1 and result2) == True,"check gateway mac is blank,test fail!"
        print "check gateway mac is blank,test pass!"

    #单环境下client isolation功能验证radio--这里只验证后台规则生效(testlink_ID:1518_1)
    def test_123_check_isolation_radio(self):
        u"""单环境下client isolation功能验证radio--这里只验证后台规则生效(testlink_ID:1518_1)"""
        tmp = NGBusiness(self.driver)
        #配置group0的客户端隔离的无线模式
        tmp. wifi_isolation("radio")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result1) and ("radio" in result2),\
            "check isolation radio,test fail!"
        print "check isolation radio,test pass!"

    #单环境下client isolation功能验证internet(testlink_ID:1518_2)
    def test_124_check_isolation_internet(self):
        u"""单环境下client isolation功能验证internet(testlink_ID:1518_2)"""
        tmp = NGBusiness(self.driver)
        #配置group0的客户端隔离的互联网模式
        tmp. wifi_isolation_backup("internet")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        result3,result4 = tmp.check_isolation(data_wireless['all_ssid'],data_wireless["short_wpa"])
        assert ("1" in result1) and ("internet" in result2) and \
               (result3 != 0) and (result4 == 0), \
            "check isolation internet,test fail!"
        print "check isolation internet,test pass!"

    #单环境下client isolation功能验证gatewaymac(testlink_ID:1518_3)
    def test_125_check_isolation_gatewaymac(self):
        u"""单环境下client isolation功能验证gatewaymac(testlink_ID:1518_3)"""
        tmp = NGBusiness(self.driver)
        #配置group0的客户端隔离的网关mac模式
        #获取7000的mac地址
        route_mac = tmp.get_router_mac(data_basic['7000_ip'],data_basic['sshUser'],data_login['all'])
        print route_mac
        tmp.wifi_isolation_gateway_mac_backup(route_mac)
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.gateway_mac")
        result4,result5 = tmp.check_isolation(data_wireless['all_ssid'],data_wireless["short_wpa"])
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #配置group0的客户端隔离的无线模式
        tmp. wifi_isolation_backup("radio")
        assert ("1" in result1) and ("gateway_mac" in result2) and (route_mac.upper() in result3) and \
            (result4 == 0) and (result5 == 0), \
            "check isolation gateway mac,test fail!"
        print "check isolation gateway mac,test pass!"

    #重启查看client isolation是否依然生效(testlink_ID:1519)
    def test_126_check_reboot_isolation(self):
        u"""重启查看client isolation是否依然生效(testlink_ID:1519)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result1) and ("radio" in result2),\
            "check isolation radio after rebooting,test fail!"
        print "check isolation radio after rebooting,test pass!"



    ####################################################################
    ##################以下是最小RSSI的测试用例##################
    ####################################################################
    #enableRSSI 配置验证并检查(testlink_ID:1015_1)
    def test_127_check_enable_rssi(self):
        u"""enableRSSI 配置验证并检查(testlink_ID:1015_1)"""
        #取消group0的客户端隔离的模式
        tmp = NGBusiness(self.driver)
        tmp.cancel_wifi_isolation()
        #enableRSSI 配置验证并检查
        result = tmp.check_enable_rssi()
        assert result=="-94","check enable RSSI,test fail!"
        print "check enable RSSI,test pass!"

    #disableRSSI 配置验证并检查(testlink_ID:1015_2)
    def test_128_check_disable_rssi(self):
        u"""disableRSSI 配置验证并检查(testlink_ID:1015_2)"""
        tmp = NGBusiness(self.driver)
        #disableRSSI 配置验证并检查
        result1,result2 = tmp.check_disable_rssi()
        assert (result1 == None) and (result2=="-94"),"check disable RSSI,test fail!"
        print "check disable RSSI,test pass!"

    #enable rssi,Minimum RSSI (dBm)为空格的配置验证(testlink_ID:1017_1)
    def test_129_check_min_rssi_blank(self):
        u"""enable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:1017_1)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(" ")
        assert result1 and result2,"enable rssi when min rssi is blank,test fail!"
        print "enable rssi when min rssi is blank,test pass!"

    #disable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:1017_2)
    def test_130_check_min_rssi_blank(self):
        u"""disable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:1017_2)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_disable_min_rssi_error("")
        assert (result1==False) and (result2==False),"disable rssi when min rssi is blank,test fail!"
        print "disable rssi when min rssi is blank,test pass!"

    #在Minimum RSSI (dBm)处输入大于-1的整数(testlink_ID:1016_1)
    def test_131_check_min_rssi_more_than_negative1(self):
        u"""在Minimum RSSI (dBm)处输入大于-1的整数(testlink_ID:1016_1)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("0")
        assert result1 and result2,"when min rssi more than nagative 1,test fail!"
        print "when min rssi more than nagative 1,test pass!"

    #在Minimum RSSI (dBm)处输入小于-94的整数(testlink_ID:1016_2)
    def test_132_check_min_rssi_less_than_negative94(self):
        u"""在Minimum RSSI (dBm)处输入小于-94的整数(testlink_ID:1016_2)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("-95")
        assert result1 and result2,"when min rssi less than nagative 95,test fail!"
        print "when min rssi less than nagative 95,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:1017_3)
    def test_133_check_min_rssi_chinese(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如中文(testlink_ID:1017_3)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['CN_ssid'])
        assert result1 and result2,"when min rssi is chinese,test fail!"
        print "when min rssi is chinese,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:1017_4)
    def test_134_check_min_rssi_ascii(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如ASCII码(testlink_ID:1017_4)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['ascii_ssid'])
        assert result1 and result2,"when min rssi is ascii,test fail!"
        print "when min rssi is ascii,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:1017_5)
    def test_135_check_min_rssi_decimals(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如小数(testlink_ID:1017_5)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("-50.5")
        assert result1 and result2,"when min rssi is decimals,test fail!"
        print "when min rssi is decimals,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:1017_6)
    def test_136_check_min_rssi_special(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如特殊字符(testlink_ID:1017_6)"""
        tmp = NGBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['special_ssid'])
        assert result1 and result2,"when min rssi is special,test fail!"
        print "when min rssi is special,test pass!"

    #在Minimum RSSI (dBm)处输入-1(testlink_ID:1018_1)
    def test_137_check_min_rssi_negative1(self):
        u"""在Minimum RSSI (dBm)处输入-1(testlink_ID:1018_1)"""
        tmp = NGBusiness(self.driver)
        #enableRSSI
        tmp.check_enable_rssi()
        #设置最小RSSI值，并检查是否正确
        result = tmp.check_min_rssi("-1")
        assert result == "-1","when min rssi is -1,test fail!"
        print "when min rssi is -1,test pass!"

    #RSSI功能验证-范围验证-1(testlink_ID:1018_2)
    def test_138_check_min_rssi_negative1_validity(self):
        u"""RSSI功能验证-范围验证-1(testlink_ID:1018_2)"""
        tmp = NGBusiness(self.driver)
        tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在1分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        print "result = %s"%result
        assert "Not connected.\n" in result,"check min rssi is -1 validity,test fail!"
        print "check min rssi is -1 validity,test pass!"

    #在Minimum RSSI (dBm)处输入-94(testlink_ID:1018_3)
    def test_139_check_min_rssi_negative94(self):
        u"""在Minimum RSSI (dBm)处输入-94(testlink_ID:1018_3)"""
        tmp = NGBusiness(self.driver)
        result = tmp.check_min_rssi("-94")
        print "result = %s"%result
        assert result == "-94","when min rssi is -94,test fail!"
        print "when min rssi is -94,test pass!"

    #RSSI功能验证-范围验证-94(testlink_ID:1018_4)
    def test_140_check_min_rssi_negative94_validity(self):
        u"""RSSI功能验证-范围验证-94(testlink_ID:1018_4)"""
        tmp = NGBusiness(self.driver)
        tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在1分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        assert "Not connected.\n" not in result,"check min rssi is -94 validity,test fail!"
        print "check min rssi is -94 validity,test pass!"

    #在Minimum RSSI (dBm)处输入-10(testlink_ID:1018_5)
    def test_141_check_min_rssi_negative10(self):
        u"""在Minimum RSSI (dBm)处输入-10(testlink_ID:1018_5)"""
        tmp = NGBusiness(self.driver)
        result = tmp.check_min_rssi("-10")
        assert result == "-10","when min rssi is -10,test fail!"
        print "when min rssi is -10,test pass!"

    #RSSI功能验证-范围验证-10(testlink_ID:1018_6)
    def test_142_check_min_rssi_negative10_validity(self):
        u"""RSSI功能验证-范围验证-10(testlink_ID:1018_6)"""
        tmp = NGBusiness(self.driver)
        tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在1分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        #关闭RSSI
        tmp.check_disable_rssi()
        assert "Not connected.\n" in result,"check min rssi is -10 validity,test fail!"
        print "check min rssi is -10 validity,test pass!"

    ####################################################################
    ##################以下是WIFI功能混合测试的测试用例##################
    ####################################################################
    #WEP 64bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1021_1)
    def test_143_wep64_1_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1021_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #添加一个只有一个mac地址的访问列表
        tmp1.add_accesslist_onemac(mac)

        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WEP64bit,test fail!"
        print "test one mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1021_2)
    def test_144_wep64_many_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1021_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WEP64bit,test fail!"
        print "test many mac in blacklist with WEP64bit,test pass!"


    #WEP 64bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1021_3)
    def test_145_wep64_1_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1021_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in blacklist with WEP64bit,test fail!"
        print "test one mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1021_4)
    def test_146_wep64_many_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1021_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in blacklist with WEP64bit,test fail!"
        print "test many mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:1022_1)
    def test_147_wep64_1_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:1022_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WEP64bit,test fail!"
        print "test one mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1022_2)
    def test_148_wep64_many_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1022_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in whitelist with WEP64bit,test fail!"
        print "test many mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1022_3)
    def test_149_wep64_1_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1022_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WEP64bit,test fail!"
        print "test one mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1022_4)
    def test_150_wep64_many_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1022_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WEP64bit,test fail!"
        print "test many mac in whitelist with WEP64bit,test pass!"



    #WEP 128bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1023_1)
    def test_151_wep128_1_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1023_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WEP128bit,test fail!"
        print "test one mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1023_2)
    def test_152_wep128_many_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1023_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WEP128bit,test fail!"
        print "test many mac in blacklist with WEP128bit,test pass!"


    #WEP 128bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1023_3)
    def test_153_wep128_1_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1023_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in blacklist with WEP128bit,test fail!"
        print "test one mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1023_4)
    def test_154_wep128_many_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1023_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in blacklist with WEP128bit,test fail!"
        print "test many mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:1024_1)
    def test_155_wep128_1_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:1024_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)

        tmp = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WEP128bit,test fail!"
        print "test one mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1024_2)
    def test_156_wep128_many_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1024_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in whitelist with WEP128bit,test fail!"
        print "test many mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1024_3)
    def test_157_wep128_1_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1024_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WEP128bit,test fail!"
        print "test one mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1024_4)
    def test_158_wep128_many_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1024_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WEP128bit,test fail!"
        print "test many mac in whitelist with WEP128bit,test pass!"


    #WPA 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1025_1)
    def test_159_WPA_1_blacklist(self):
        u"""WPA 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1025_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1025_2)
    def test_160_WPA_many_blacklist(self):
        u"""WPA 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1025_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WPA,test fail!"
        print "test many mac in blacklist with WPA,test pass!"


    #WPA 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1025_3)
    def test_161_WPA_1_blacklist(self):
        u"""WPA 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1025_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1025_4)
    def test_162_WPA_many_blacklist(self):
        u"""WPA 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1025_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in blacklist with WPA,test fail!"
        print "test many mac in blacklist with WPA,test pass!"

    #WPA 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:1026_1)
    def test_163_WPA_1_whitelist(self):
        u"""WPA 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:1026_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WPA,test fail!"
        print "test one mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1026_2)
    def test_164_WPA_many_whitelist(self):
        u"""WPA 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1026_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in whitelist with WPA,test fail!"
        print "test many mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1026_3)
    def test_165_WPA_1_whitelist(self):
        u"""WPA 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1026_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WPA,test fail!"
        print "test one mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1026_4)
    def test_166_WPA_many_whitelist(self):
        u"""WPA 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1026_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WPA,test fail!"
        print "test many mac in whitelist with WPA,test pass!"





    #WPA2 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1027_1)
    def test_167_WPA2_1_blacklist(self):
        u"""WPA2 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1027_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WPA2,test fail!"
        print "test one mac in blacklist with WPA2,test pass!"

    #WPA2 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1027_2)
    def test_168_WPA2_many_blacklist(self):
        u"""WPA2 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1027_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WPA2,test fail!"
        print "test many mac in blacklist with WPA2,test pass!"


    #WPA2 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1027_3)
    def test_169_WPA2_1_blacklist(self):
        u"""WPA2 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1027_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA2 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1027_4)
    def test_170_WPA2_many_blacklist(self):
        u"""WPA2 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1027_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in blacklist with WPA,test fail!"
        print "test many mac in blacklist with WPA,test pass!"

    #WPA2 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:1028_1)
    def test_171_WPA2_1_whitelist(self):
        u"""WPA2 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:1028_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WPA2,test fail!"
        print "test one mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1028_2)
    def test_172_WPA2_many_whitelist(self):
        u"""WPA2 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1028_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in whitelist with WPA2,test fail!"
        print "test many mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1028_3)
    def test_173_WPA2_1_whitelist(self):
        u"""WPA2 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1028_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WPA2,test fail!"
        print "test one mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1028_4)
    def test_174_WPA2_many_whitelist(self):
        u"""WPA2 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1028_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WPA2,test fail!"
        print "test many mac in whitelist with WPA2,test pass!"





    #open 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1029_1)
    def test_175_open_1_blacklist(self):
        u"""open 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:1029_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为不加密
        tmp.wifi_None_encryption()
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with open,test fail!"
        print "test one mac in blacklist with open,test pass!"

    #open 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1029_2)
    def test_176_open_many_blacklist(self):
        u"""open 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:1029_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with open,test fail!"
        print "test many mac in blacklist with open,test pass!"


    #open 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1029_3)
    def test_177_open_1_blacklist(self):
        u"""open 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:1029_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in blacklist with open,test fail!"
        print "test one mac in blacklist with open,test pass!"

    #open 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1029_4)
    def test_178_open_many_blacklist(self):
        u"""open 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:1029_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in blacklist with open,test fail!"
        print "test many mac in blacklist with open,test pass!"

    #open 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:1029_5)
    def test_179_open_1_whitelist(self):
        u"""open 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:1029_5)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = NGBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with open,test fail!"
        print "test one mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1029_6)
    def test_180_open_many_whitelist(self):
        u"""open 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:1029_6)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['all_ssid'] in result,"test many mac in whitelist with open,test fail!"
        print "test many mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1029_7)
    def test_181_open_1_whitelist(self):
        u"""open 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:1029_7)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with open,test fail!"
        print "test one mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1029_8)
    def test_182_open_many_whitelist(self):
        u"""open 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:1029_8)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with open,test fail!"
        print "test many mac in whitelist with open,test pass!"




    #多功能混合验证 client isolation + encrypted  (open mode)(testlink_ID:1030)
    def test_183_check_open_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (open mode)(testlink_ID:1030)"""
        tmp = NGBusiness(self.driver)
        #禁用第n个网络组的无线过滤
        tmp.disable_macfilter(1)
        #配置group0的客户端隔离的模式
        tmp.wifi_isolation("radio")
        #无线连接这个的AP
        result1 = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check open encryption and isolation radio,test fail!"
        print "check open encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WEP 64bit  mode)(testlink_ID:1031)
    def test_184_check_wep64_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WEP 64bit  mode)(testlink_ID:1031)"""
        tmp = NGBusiness(self.driver)
        #设置wep64加密
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个的AP
        result1 = tmp.connect_WEP_AP(data_wireless['all_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wep64bit encryption and isolation radio,test fail!"
        print "check wep64bit encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WEP 128bit  mode)(testlink_ID:1032)
    def test_185_check_wep128_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WEP 128bit  mode)(testlink_ID:1032)"""
        tmp = NGBusiness(self.driver)
        #设置wep128加密
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个的AP
        result1 = tmp.connect_WEP_AP(data_wireless['all_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wep128bit encryption and isolation radio,test fail!"
        print "check wep128bit encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES mode)(testlink_ID:1033)
    def test_186_check_wpa2_mix_AES_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES mode)(testlink_ID:1033)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2 mix-AES encryption and isolation radio,test fail!"
        print "check wpa2 mix-AES encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES/TKIP mode)(testlink_ID:1034)
    def test_187_check_wpa2_mix_AESTKIP_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES/TKIP mode)(testlink_ID:1034)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2 mix-AES/TKIP encryption and isolation radio,test fail!"
        print "check wpa2 mix-AES/TKIP encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA2  AES mode)(testlink_ID:1035)
    def test_188_check_wpa2_AES_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA2  AES mode)(testlink_ID:1035)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2-AES encryption and isolation radio,test fail!"
        print "check wpa2-AES encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA2  AES/TKIP mode)(testlink_ID:1036)
    def test_189_check_wpa2_AESTKIP_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA2  AES/TKIP mode)(testlink_ID:1036)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2-AES/TKIP encryption and isolation radio,test fail!"
        print "check wpa2-AES/TKIP encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + hide SSID(testlink_ID:1037)
    def test_190_check_hideSSID_isolation(self):
        u"""多功能混合验证 client isolation + hide SSID(testlink_ID:1037)"""
        tmp = NGBusiness(self.driver)
        #设置group0是否隐藏
        tmp.hidden_ssid()
        result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        #取消group0是否隐藏
        tmp.hidden_ssid()
        assert (result1 == False) and ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check hide SSID and isolation radio,test fail!"
        print "check hide SSID and isolation radio,test pass!"

    #多功能混合验证 client isolation + mac filter(testlink_ID:1038)
    def test_191_check_macfilter_isolation(self):
        u"""多功能混合验证 client isolation + mac filter(testlink_ID:1038)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)

        tmp = NGBusiness(self.driver)
        tmp.wifi_whitelist_backup()
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and ("1" in result2) \
                and ("radio" in result3),\
                "check mac filter and isolation radio,test fail!"
        print "check mac filter and isolation radio,test pass!"

    #hide SSID、WPA2、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1049)
    def test_192_WPA2_all_mixed_whitelist(self):
        u"""hide SSID、WPA2、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1049)"""
        tmp = NGBusiness(self.driver)
        #设置group0是否隐藏
        tmp.hidden_ssid()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WPA2 in all mixed whitelist,test fail!"
        print "check WPA2 in all mixed whitelist,test pass!"

    #hide SSID、OPEN、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1045)
    def test_193_open_all_mixed_whitelist(self):
        u"""hide SSID、OPEN、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1045)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为不加密
        tmp.wifi_None_encryption()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_NONE_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert  ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check OPEN in all mixed whitelist,test fail!"
        print "check OPEN in all mixed whitelist,test pass!"

    #hide SSID、WEP64、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1046)
    def test_194_WEP64_all_mixed_whitelist(self):
        u"""hide SSID、WEP64、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1046)"""
        tmp = NGBusiness(self.driver)
        #先禁用mac地址过滤
        #tmp.disable_macfilter(1)
        #设置默认网络组无线为WEP64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #设置group0的无线过滤的白名单
        #mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #tmp.wifi_whitelist(mac)
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WEP64 in all mixed whitelist,test fail!"
        print "check WEP64 in all mixed whitelist,test pass!"

    #hide SSID、WEP128、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1047)
    def test_195_WEP128_all_mixed_whitelist(self):
        u"""hide SSID、WEP128、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1047)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为WEP128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WEP128 in all mixed whitelist,test fail!"
        print "check WEP128 in all mixed whitelist,test pass!"

    #hide SSID、WPA、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1048)
    def test_196_WPA_all_mixed_whitelist(self):
        u"""hide SSID、WPA、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:1048)"""
        tmp = NGBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WPA in all mixed whitelist,test fail!"
        print "check WPA in all mixed whitelist,test pass!"

    #hide SSID、WPA、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1043)
    def test_197_WPA_all_mixed_blacklist(self):
        u"""hide SSID、WPA、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1043)"""
        tmp = NGBusiness(self.driver)
        tmp.wifi_blacklist_backup()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check WPA in all mixed blacklist,test fail!"
        print "check WPA in all mixed blacklist,test pass!"

    #hide SSID、open、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1040)
    def test_198_open_all_mixed_blacklist(self):
        u"""hide SSID、open、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1040)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为不加密
        tmp.wifi_None_encryption()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_NONE_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check open in all mixed blacklist,test fail!"
        print "check open in all mixed blacklist,test pass!"

    #hide SSID、wep64、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1041)
    def test_199_wep64_all_mixed_blacklist(self):
        u"""hide SSID、wep64、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1041)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为WEP64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wep64 in all mixed blacklist,test fail!"
        print "check wep64 in all mixed blacklist,test pass!"

    #hide SSID、wep128、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1042)
    def test_200_wep128_all_mixed_blacklist(self):
        u"""hide SSID、wep128、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1042)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为WEP128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wep128 in all mixed blacklist,test fail!"
        print "check wep128 in all mixed blacklist,test pass!"

    #hide SSID、wpa2、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1044)
    def test_201_wpa2_all_mixed_blacklist(self):
        u"""hide SSID、wpa2、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:1044)"""
        tmp = NGBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(2,0,data_wireless['short_wpa'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wpa2 in all mixed blacklist,test fail!"
        print "check wpa2 in all mixed blacklist,test pass!"






    ####################################################################
    ##################以下是Network-组成员的测试用例##################
    ####################################################################

    #恢复出厂后Master AP 默认属于Group0(testlink_ID:1050)
    def test_202_default_ssid(self):
        u"""恢复出厂后Master AP 默认属于Group0(testlink_ID:1050)"""
        tmp = APSBusiness(self.driver)
        tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        #取得master ap的mac并去掉冒号
        mac1 = tmp.mac_drop(data_AP['master:mac'])
        mac = mac1.lower()
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.%s.zones"%mac)
        assert "zone0" in result,"after reset the AP check default master ap's group,fail!"
        print "after reset the AP check default master ap's group,pass!"

    #一次从一个Group可以移除多个AP(testlink_ID:1055)
    def test_203_del_manyap_to_1group(self):
        u"""一次从一个Group可以移除多个AP(testlink_ID:1055)"""
        #修改默认网络组的ssid和密码
        tmp1 = NGBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        #只有默认时，搜索-配对-加入网络组
        tmp2 = APSBusiness(self.driver)
        tmp2.search_pair_add_default(data_AP['slave:mac2'])
        #将所有已添加的设备删除
        tmp = NGBusiness(self.driver)
        tmp.del_all_ap()
        #确定master ap 和slave ap都不在默认网络组
        master_mac1 = tmp.mac_drop(data_AP['master:mac'])
        master_mac = master_mac1.lower()
        slave_mac2 = tmp.mac_drop(data_AP['slave:mac2'])
        slave_mac = slave_mac2.lower()
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.%s.zones"%master_mac)
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.%s.zones"%slave_mac)
        assert ("zone0"  not in result1) and ("zone0"  not in result2),"del many aps from one group,test fail!"
        print "del many aps from one group,test pass!"

    #一次可以加入多个AP到一个Group(testlink_ID:1054)
    def test_204_add_manyAP_to_1group(self):
        u"""一次可以加入多个AP到一个Group(testlink_ID:1054)"""
        #将所有可添加的设备添加
        tmp = NGBusiness(self.driver)
        tmp.add_all_ap()
        #确定master ap 和slave ap都加入第二个网络组
        master_mac1 = tmp.mac_drop(data_AP['master:mac'])
        master_mac = master_mac1.lower()
        slave_mac2 = tmp.mac_drop(data_AP['slave:mac2'])
        slave_mac = slave_mac2.lower()
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.%s.zones"%master_mac)
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.%s.zones"%slave_mac)
        assert ("zone0" in result1) and ("zone0" in result2),"add many aps to one group,test fail!"
        print "add many aps to one group,test pass!"



    #slave AP加入Group后会产生相应的网络接口(testlink_ID:1057)
    def test_205_check_interface(self):
        u"""slave AP加入Group后会产生相应的网络接口(testlink_ID:1057)"""
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"ifconfig")
        assert ("br-lan0_zone0" and "ath0" and "ath1") in result,\
            "check interface after adding group,test fail!"
        print "check interface after adding group,test pass!"

    #AP自动同步并应用其加入的单个Group的配置(testlink_ID:1058)
    def test_206_check_config_1gourp(self):
        u"""AP自动同步并应用其加入的单个Group的配置(testlink_ID:1058)"""
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"cat /etc/config/grandstream")
        assert (data_login['all'] and data_wireless['all_ssid']) in result,\
            "check config after adding 1 group,test fail!"
        print "check config after adding 1 group,test pass!"

    #AP自动同步并应用其加入的多个Group的配置(testlink_ID:1059)
    def test_207_check_config_manygourp(self):
        u"""AP自动同步并应用其加入的多个Group的配置(testlink_ID:1059)"""
        NG_name = data_ng["NG2_name"]+"-2"
        NG_ssid = data_ng["NG2_ssid"]+"-2"
        tmp1 = NGBusiness(self.driver)
        tmp1.new_network_group(NG_name,NG_ssid,data_wireless["short_wpa"])
        #slave加入所有的网络组
        tmp = APSBusiness(self.driver)
        tmp.add_slave_to_all_NG()

        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"cat /etc/config/grandstream")
        assert (data_login['all'] and data_wireless['all_ssid'] and \
                NG_name and NG_ssid) in result,\
            "check config after adding many groups,test fail!"
        print "check config after adding many groups,test pass!"

    #AP移除Group后，相应的组配置也会被删除(testlink_ID:1060)
    def test_208_del_config(self):
        u"""AP移除Group后，相应的组配置也会被删除(testlink_ID:1060)"""
        tmp = APSBusiness(self.driver)
        tmp.add_slave_to_NG(data_AP['slave:mac2'],1)
        NG_name = data_ng["NG2_name"]+"-2"
        NG_ssid = data_ng["NG2_ssid"]+"-2"
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"cat /etc/config/grandstream")
        assert ((data_login['all'] and data_wireless['all_ssid']) in result) \
               and ((NG_name or NG_ssid) not in result),\
            "check config after deling many groups,test fail!"
        print "check config after deling many groups,test pass!"

    #修改Group的配置，检查Group成员AP的状态(testlink_ID:1061)
    def test_209_check_AP_status1(self):
        u"""修改Group的配置，检查Group成员AP的状态(testlink_ID:1061)"""
        #slave ap加入网络组2
        tmp = APSBusiness(self.driver)
        tmp.add_slave_to_NG(data_AP['slave:mac2'],2)
        #修改网络组2的ssid
        NG_ssid = data_ng["NG2_ssid"]
        tmp1 = NGBusiness(self.driver)
        tmp1.change_specail_wifi_ssid_key(1,NG_ssid+"-3",data_wireless["short_wpa"])
        time.sleep(60)
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")
        assert (NG_ssid+"-3") in result,\
            "check AP status after modify group,test fail!"
        print "check AP status after modify group,test pass!"

    #Master AP 重启，不会影响Group配置(testlink_ID:1063)
    def test_210_master_reboot(self):
        u"""Master AP 重启，不会影响Group配置(testlink_ID:1063)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        NG_ssid = data_ng["NG2_ssid"]
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")
        assert (data_wireless['all_ssid'] in result1) and \
               ((NG_ssid+"-3") in result2),"check config after reboot master ap,test fail!"
        print "check config after reboot master ap,test pass!"

    #Slave AP 重启，不会影响Group配置(testlink_ID:1064)
    def test_211_slave_reboot(self):
        u"""Slave AP 重启，不会影响Group配置(testlink_ID:1064)"""
        tmp = APSBusiness(self.driver)
        tmp.reboot_slave_ap1()
        NG_ssid = data_ng["NG2_ssid"]
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")
        assert (data_wireless['all_ssid'] in result1) and \
               ((NG_ssid+"-3") in result2),"check config after reboot slave ap,test fail!"
        print "check config after reboot slave ap,test pass!"

    #删除Group的配置，检查Group成员AP的状态(testlink_ID:1062)
    def test_212_check_AP_status2(self):
        u"""删除Group的配置，检查Group成员AP的状态(testlink_ID:1062)"""
        tmp = NGBusiness(self.driver)
        tmp.del_first_NG()
        ssh = SSH(data_basic['slave_ip2'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")

        #解除slave ap2的配对
        tmp1 = APSBusiness(self.driver)
        tmp1.unpair_special_slave_AP(data_AP['slave:mac2'])

        assert ("ath0" or "ath1") not in result,"check AP status after del group,test fail!"
        print "check AP status after del group,test pass!"


    ####################################################################
    ##################以下是fallback IP的测试用例##################
    ####################################################################
    #disable/enable dhcp server when GWN76xx is in unpaired status,fallback IP works fine
    def test_213_check_fallback_IP_function(self):
        u"""disable/enable dhcp server when GWN76xx is in unpaired status,fallback IP works fine(testlink_ID:2335,2343)"""
        #修改7000网络组的dhcp ipv4的租期时间为2分钟
        tmp = NGBusiness(self.driver)
        tmp.wlan_disable(data_basic['wlan_pc'])
        tmp.mixed_7000_dhcp_lease_time("2m")
        #先退出7000的登录
        tmp2 = NavbarBusiness(self.driver)
        tmp2.logout()

        #打开master ap的web页面
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(10)
        time.sleep(10)
        #在页面上把master AP恢复出厂设置
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_factory_reset_backup(data_basic['DUT_ip'])
        #disable/enable dhcp server when GWN76xx is in unpaired status,fallback IP works fine
        result1,result2 = tmp.check_fallback_IP_function("192.168.1.2",
            data_basic['DUT_ip'],data_basic['sshUser'],data_basic["super_defalut_pwd"])

        #先退出7000的登录
        tmp2.logout()
        #修改7000网络组的dhcp ipv4的租期时间为12h
        tmp.mixed_7000_dhcp_lease_time("12h")
        #pc有线网卡释放ip
        tmp.dhcp_release_wlan(data_basic['lan_pc'])
        #pc有线网卡重新获取ip
        tmp.dhcp_wlan(data_basic['lan_pc'])

        #测试完毕，禁用无线网卡，使pc够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("NetworkGroup")

        self.assertTrue(result1)
        self.assertTrue(result2), "dis/enable dhcp server,check fallback ip,test fail!"
        print "dis/enable dhcp server,check fallback ip,test pass!"

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
