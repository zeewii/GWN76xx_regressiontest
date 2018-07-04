#coding=utf-8
#作者：曾祥卫
#时间：2018.01.22
#描述：用例集，调用ssid_business

import unittest,time
from system_settings.mesh.mesh_business import MeshBusiness
from selenium import webdriver
import sys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from login.login_business import LoginBusiness
from setupwizard.setupwizard_business import SWBusiness
from ssid.ssid_business import SSIDBusiness
from access_points.aps_business import APSBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
# from network_group.networkgroup_business import NGBusiness
from connect.ssh import SSH
from data import data
from captive_portal.captiveportal_business import CPBusiness
from network_group.networkgroup_business import NGBusiness
from data.logfile import Log

reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
log = Log("SSID")

class TestSSID(unittest.TestCase):
    u"""测试ssid的用例集(runtime:10h)"""
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
        # #描述：启用无线网卡
        tmp.wlan_enable(data_basic['wlan_pc'])
        # rsyslog服务器准备
        tmp.ready_rsyslog()
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"



    ###################################################################
    #################以下是Random Passoword的测试用例##################
    ###################################################################

    #恢复出厂后默认SSID验证(testlink_ID:1252)
    def test_002_default_ssid(self):
        u"""恢复出厂后默认SSID验证(testlink_ID:1252)"""
        log.debug("002")
        #取得默认的ssid
        tmp1 = SWBusiness(self.driver)
        result = tmp1.check_default_ssid(data_AP['master:mac'])
        assert result,"after reset the AP check default ssid,fail!"
        print "after reset the AP check default ssid,pass!"

    #默认随机密码验证(testlink_ID:1253)
    def test_003_have_default_pwd(self):
        u"""默认随机密码验证(testlink_ID:1253)"""
        log.debug("003")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        #取出ap的2.4G的无线的默认密码
        default_pwd_2g4 = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath0.key')
        #取出ap的5G的无线的默认密码
        default_pwd_5g = ssh.ssh_cmd(data_basic['sshUser'],'uci show wireless.ath1.key')
        assert ('wireless.ath0.key' in default_pwd_2g4) and ('wireless.ath1.key' in default_pwd_5g),\
            "after reset the AP have default pwd,fail!"
        print "after reset the AP have default pwd,pass!"

    #对比标签密码与实际密码(testlink_ID:1254)
    def test_004_default_pwd(self):
        u"""对比标签密码与实际密码(testlink_ID:1254)"""
        log.debug("004")
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
    def test_005_default_wifi_status(self):
        u"""默认wifi状态(testlink_ID:1255)"""
        log.debug("005")
        tmp = SWBusiness(self.driver)
        result = tmp.wifi_status()
        print result
        assert result == 'true',"test defalut wifi status,test fail!"
        print "test defalut wifi status,test pass!"

    #随机密码真实性验证(testlink_ID:1256)
    def test_006_check_default_pwd(self):
        u"""随机密码真实性验证(testlink_ID:1256)"""
        log.debug("006")
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
    def test_007_change_ssid_pwd(self):
        u"""SSID与wifi密码修改(testlink_ID:1257)"""
        log.debug("007")
        #修改默认SSID的ssid和密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        #使用无线网卡连接该AP
        result = tmp1.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                     data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"change default ssid and pwd,test fail!"
        print "change default ssid and pwd,test pass!"

    #重启后检查SSID与wifi密码(testlink_ID:1260)
    def test_008_reboot_check_ssid_pwd(self):
        u"""重启后检查SSID与wifi密码(testlink_ID:1260)"""
        log.debug("008")
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #使用无线网卡连接该AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                                     data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"reboot ap after change default ssid and pwd,test fail!"
        print "reboot ap after change default ssid and pwd,test pass!"

    #配对后slave ap的ssid和密码(testlink_ID:1257_1)
    def test_009_slaveAP_ssid_pwd(self):
        u"""配对后slave ap的ssid和密码(testlink_ID:1257_1)"""
        log.debug("009")
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

    #enable/disable SSID的正常配置(testlink_ID:300_2)
    def test_010_check_first_en_dis_status(self):
        u"""enable/disable SSID的正常配置(testlink_ID:300_2)"""
        log.debug("010")
        tmp = SSIDBusiness(self.driver)
        #enable/disable SSID的正常配置
        result1,result2 = tmp.check_first_en_dis_status()
        assert (result1 == "enableicon") and (result2 == "disableicon"),\
            "check enable/disable SSID config,test fail!"
        print "check enable/disable SSID config,test pass!"

    #enable/disable SSID的功能验证(testlink_ID:301)
    def test_011_check_en_dis_function(self):
        u"""enable/disable SSID的正常配置(testlink_ID:301)"""
        log.debug("011")
        tmp = SSIDBusiness(self.driver)
        #disable状态下，使用无线网卡扫描该ssid
        result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        #enable/disable first SSID
        tmp.en_dis_first()
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == False) and (data_wireless['all_ssid'] in result2),\
            "check enable/disable SSID function,test fail!"
        print "check enable/disable SSID function,test pass!"

    #SSID为空的配置验证(testlink_ID:302)
    def test_012_check_blank_ssid(self):
        u"""SSID为空的配置验证(testlink_ID:302)"""
        log.debug("012")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_blank_ssid()
        ##enable/disable first SSID
        tmp.en_dis_first()
        assert result1 and (result2 == "disableicon"),\
            "check blank ssid in SSID,test fail!"
        print "check blank ssid in SSID,test pass!"

    #英文/数字、英文+数字和ASCII标准符号的 SSID 的正常配置(testlink_ID:303)
    def test_013_check_ssid_config(self):
        u"""英文/数字、英文+数字和ASCII标准符号的 SSID 的正常配置(testlink_ID:303)"""
        log.debug("013")
        tmp = SSIDBusiness(self.driver)
        result1,result2,result3,result4 = tmp.check_ssid_config(data_wireless['letter_ssid'],\
                        data_wireless['digital_ssid'],data_wireless['digital_letter_ssid'],\
                        data_wireless['ascii_ssid'])
        assert (result1 == data_wireless['letter_ssid']) and (result2 == data_wireless['digital_ssid']) \
            and (result3 == data_wireless['digital_letter_ssid']) and (result4 == data_wireless['ascii_ssid']),\
            "check ssid config,test fail!"
        print "check ssid config,test pass!"

    #SSID 对英文的SSID 的支持(testlink_ID:304_1)
    def test_014_check_SSID_letter(self):
        u"""SSID 对英文的SSID 的支持(testlink_ID:304_1)"""
        log.debug("014")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['letter_ssid'])
        result = tmp.ssid_scan_result_backup(data_wireless['letter_ssid'],data_basic["wlan_pc"])
        assert result,"Check letter SSID,test fail!"
        print "Check letter SSID,test pass!"

    #SSID 对数字的SSID 的支持(testlink_ID:304_2)
    def test_015_check_SSID_digital(self):
        u"""SSID 对数字的SSID 的支持(testlink_ID:304_2)"""
        log.debug("015")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['digital_ssid'])
        result = tmp.ssid_scan_result_backup(data_wireless['digital_ssid'],data_basic["wlan_pc"])
        assert result,"Check digital SSID,test fail!"
        print "Check digital SSID,test pass!"

    #SSID 对英文+数字的SSID 的支持(testlink_ID:304_3)
    def test_016_check_SSID_letter_digital(self):
        u"""SSID 对英文+数字的SSID 的支持(testlink_ID:304_3)"""
        log.debug("016")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['digital_letter_ssid'])
        result = tmp.ssid_scan_result_backup(data_wireless['digital_letter_ssid'],data_basic["wlan_pc"])
        assert result,"Check letter+digital SSID,test fail!"
        print "Check letter+digital SSID,test pass!"

    #SSID对ASCII的支持(testlink_ID:304_4)
    def test_017_check_SSID_ASCII(self):
        u"""SSID对ASCII的支持(testlink_ID:304_4)"""
        log.debug("017")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['ascii_ssid'])
        #获取第一个ssid的名字
        result = tmp.get_first_ssid_name()
        assert data_wireless['ascii_ssid'] in result,"Check ASCII SSID,test fail!"
        print "Check ASCII SSID,test pass!"

    #中文SSID的正常配置(testlink_ID:305)
    def test_018_check_SSID_CN(self):
        u"""中文SSID的正常配置(testlink_ID:305)"""
        log.debug("018")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['CN_ssid'])
        #获取第一个ssid的名字
        result = tmp.get_first_ssid_name()
        assert data_wireless['CN_ssid'] in result,"Check CN SSID,test fail!"
        print "Check CN SSID,test pass!"

    #特殊符号的SSID配置(testlink_ID:307)
    def test_019_check_SSID_special(self):
        u"""特殊符号的SSID配置(testlink_ID:307)"""
        log.debug("019")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['special_ssid'])
        #获取第一个ssid的名字
        result = tmp.get_first_ssid_name()
        assert data_wireless['special_ssid'] in result,"Check special SSID,test fail!"
        print "Check specail SSID,test pass!"

    #修改已配置的SSID(testlink_ID:308)
    def test_020_change_SSID(self):
        u"""修改已配置的SSID(testlink_ID:308)"""
        log.debug("020")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid为全英文
        tmp.modify_ssid(data_wireless['letter_ssid'])
        result1 = tmp.connect_WPA_AP(data_wireless['letter_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        #修改第一个ssid的ssid为混合
        tmp.modify_ssid(data_wireless['all_ssid'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert (data_wireless['letter_ssid'] in result1) and (data_wireless['all_ssid'] in result2),\
            "Check change SSID,test fail!"
        print "Check change SSID,test pass!"

    #验证SSID的字符长度限制(testlink_ID:309)
    def test_021_SSID_max(self):
        u"""验证SSID的字符长度限制(testlink_ID:309)"""
        log.debug("021")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['long_ssid']+"abc")
        #获取第一个ssid的名字
        result1 = tmp.get_first_ssid_name()
        result2 = tmp.connect_WPA_AP(data_wireless['long_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert ((data_wireless['long_ssid']+"abc") not in result1) and (data_wireless['long_ssid'] in result1) \
            and ((data_wireless['long_ssid']+"abc") not in result2) and (data_wireless['long_ssid'] in result2),\
            "Check max SSID,test fail!"
        print "Check max SSID,test pass!"

    #Name里含有空格的SSID(testlink_ID:310)
    def test_022_SSID_blank(self):
        u"""Name里含有空格的SSID(testlink_ID:310)"""
        log.debug("022")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        ssid = data_wireless['letter_ssid']+" "+data_wireless['digital_ssid']
        tmp.modify_ssid(ssid)
        #获取第一个ssid的名字
        result1 = tmp.get_first_ssid_name()
        result2 = tmp.connect_WPA_AP(ssid,data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert (ssid in result1) and (ssid in result2),"Check SSID contain blank,test fail!"
        print "Check SSID contain blank,test pass!"

    #关闭开启WIFI对连接在SSID无线终端的影响(testlink_ID:311)
    def test_023_disable_enable_wifi(self):
        u"""关闭开启WIFI对连接在SSID无线终端的影响(testlink_ID:311)"""
        log.debug("023")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['all_ssid'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        #enable/disable first SSID
        tmp.en_dis_first()
        result2 = tmp.get_client_cmd_result("iw dev %s link"%data_basic['wlan_pc'])
        #enable/disable first SSID
        tmp.en_dis_first()
        result3 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ("Not connected" in result2)\
            and (data_wireless['all_ssid'] in result3),"Check client status after disable/enable wifi,test fail!"
        print "Check client status after disable/enable wifi,test pass!"

    #Enable Hide SSID 的配置、功能(testlink_ID:312)
    def test_024_enable_hidden(self):
        u"""测试隐藏无线ssid(testlink_ID:311)"""
        log.debug("024")
        tmp = SSIDBusiness(self.driver)
        #设置第一个ssid隐藏
        tmp.set_hide_ssid()
        #无线扫描，无法扫描到
        result2 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        #通过连接隐藏ssid的方法能够连接上该ssid
        result3 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        #断开无线连接
        tmp.disconnect_ap()
        assert (result2 == False) and\
               (data_wireless['all_ssid'] in result3),\
            "test hidden ssid,test fail!"
        print "test hidden ssid,test pass!"

    #重启后测试隐藏无线ssid是否依然生效(testlink_ID:319)
    def test_025_reboot_hidden_SSID(self):
        u"""重启后测试隐藏无线ssid是否依然生效(testlink_ID:319)"""
        log.debug("025")
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #通过连接隐藏ssid的方法能够连接上该ssid
        result2 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result2,\
            "test hidden ssid after rebootting,test fail!"
        print "test hidden ssid after rebootting,test pass!"

    #Hide 有终端连接的SSID(testlink_ID:313)
    def test_026_hidden_ssid_client_connected(self):
        u"""Hide 有终端连接的SSID(testlink_ID:313)"""
        log.debug("026")
        tmp = SSIDBusiness(self.driver)
        #设置取消第一个ssid隐藏
        tmp.set_hide_ssid()
        tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        #设置第一个ssid隐藏
        tmp.set_hide_ssid()
        #通过连接隐藏ssid的方法能够连接上该ssid
        result = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,\
            "test hidden ssid if this ssid has been connected,test fail!"
        print "test hidden ssid if this ssid has been connected,test pass!"

    #Hide SSID 的状态下修改SSID(testlink_ID:314)
    def test_027_modify_hidden_ssid(self):
        u"""Hide SSID 的状态下修改SSID(testlink_ID:314)"""
        log.debug("027")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['all_ssid']+"02")
        #通过连接隐藏ssid的方法能够连接上该ssid
        result = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid']+"02") in result,\
            "modify ssid if hidden ssid,test fail!"
        print "modify ssid if hidden ssid,test pass!"

    #关闭、开启WIFI对连接在 Hide SSID 无线终端的影响(testlink_ID:315)
    def test_028_disable_hidden_wifi(self):
        u"""关闭、开启WIFI对连接在 Hide SSID 无线终端的影响(testlink_ID:315)"""
        log.debug("028")
        tmp = SSIDBusiness(self.driver)
        #enable/disable first SSID
        tmp.en_dis_first()
        result1 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['all_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        #enable/disable first SSID
        tmp.en_dis_first()
        result2 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ("Not connected" in result1) and ((data_wireless['all_ssid']+"02") in result2),\
                "test disable/enable wifi on hidden ssid,test fail!"
        print "test disable/enable wifi on hidden ssid,test pass!"

    #Disable Hide SSID 的配置与功能验证(testlink_ID:316)
    def test_029_disable_hidden_ssid(self):
        u"""Disable Hide SSID 的配置与功能验证(testlink_ID:316)"""
        log.debug("029")
        tmp = SSIDBusiness(self.driver)
        #设置取消第一个ssid隐藏
        tmp.set_hide_ssid()
        #无线扫描，能够扫描到
        result2 = tmp.ssid_scan_result_backup(data_wireless['all_ssid']+"02",data_basic['wlan_pc'])
        #使用正常连接方式能够连接上
        result3 = tmp.connect_WPA_AP(data_wireless['all_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result2 == True) and\
               ((data_wireless['all_ssid']+"02") in result3),\
                "disable hidden ssid,test fail!"
        print "disable hidden ssid,test pass!"

    #Hide SSID 与 OPEN 加密模式的结合使用验证(testlink_ID:317)
    def test_030_OPEN_hidden_SSID(self):
        u"""Hide SSID 与 OPEN 加密模式的结合使用验证(testlink_ID:317)"""
        log.debug("030")
        tmp = SSIDBusiness(self.driver)
        #设置第一个ssid隐藏
        tmp.set_hide_ssid()
        #修改第一个ssid的ssid
        tmp.modify_ssid(data_wireless['all_ssid'])
        #设置默认SSID无线为非加密
        tmp.wifi_None_encryption()
        result = tmp.connect_NONE_hiddenssid_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        #设置默认SSID无线为wpa/wpa2加密
        tmp.wifi_wpa_encryption(3,0,data_wireless['short_wpa'])
        assert data_wireless['all_ssid'] in result,"test OPEN encryption hidden ssid,test fail!"
        print "test OPEN encryption hidden ssid,test pass!"

    #Hide SSID 与 Mac filter 结合使用验证(testlink_ID:318)
    def test_031_mac_filter_hidden_SSID(self):
        u"""Hide SSID 与 Mac filter 结合使用验证(testlink_ID:318)"""
        log.debug("031")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #添加一个只有一个mac地址的访问列表
        tmp1.add_accesslist_onemac(mac)

        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的黑名单
        tmp.wifi_blacklist()
        #无线连接这个的hidden AP
        result = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #禁用默认SSID的无线过滤
        tmp.disable_macfilter(1)
        #设置取消第一个ssid隐藏
        tmp.set_hide_ssid()
        assert 'Not connected' in result,"test mac filter on hidden SSID,test fail!"
        print "test mac filter on qshidden SSID,test pass!"

    #AP 2.4G和5G可以同时广播相同SSID
    def test_032_dual_band(self):
        u"""AP 2.4G和5G可以同时广播相同SSID"""
        log.debug("032")
        #确认有两个无线接口
        tmp1 = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath0 | grep ESSID")
        result2 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath1 | grep ESSID")
        assert (data_wireless['all_ssid'] in result1) \
            and (data_wireless['all_ssid'] in result2),"test SSID broadcast of 2.4G and 5G,test fail!"
        print "test SSID broadcast of 2.4G and 5G,test pass!"

    #AP 2.4G和5G BSSID不相同
    def test_033_BSSID(self):
        u"""AP 2.4G和5G BSSID不相同"""
        log.debug("033")
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
    #测试ssid中2.4g的无线加密-为不加密时(testlink_ID:320)
    def test_034_None_encryption(self):
        u"""测试ssid中2.4g的无线加密-为不加密时(testlink_ID:320)"""
        log.debug("034")
        #切换ssid的2.4G频段
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("2.4GHz")
        ##设置默认SSID无线为非加密
        tmp.wifi_None_encryption()
        #无线连接这个非加密的无线
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test None encryption of wifi,test fail!"
        print "test None encryption of wifi,test pass!"

    #测试ssid中2.4g的无线加密-为5位wep64时(testlink_ID:322_1)
    def test_035_5wep64_encryption(self):
        u"""测试ssid中2.4g的无线加密-为5位wep64时(testlink_ID:322_1)"""
        log.debug("035")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 5bits wep64 encryption of wifi,test fail!"
        print "test 5bits wep64 encryption of wifi,test pass!"

    #测试ssid中2.4g的无线加密-为10位wep64时(testlink_ID:322_2)
    def test_036_10wep64_encryption(self):
        u"""测试ssid中2.4g的无线加密-为10位wep64时(testlink_ID:322_2)"""
        log.debug("036")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wep64
        tmp.wifi_wep_encryption(0,data_wireless['wep64-10'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep64-10'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 10bits wep64 encryption of wifi,test fail!"
        print "test 10bits wep64 encryption of wifi,test pass!"

    #2.4g的WEP64bit参数校验1(testlink_ID:324_1)
    def test_037_abnormal1_wep(self):
        u"""2.4g的WEP64bit参数校验1(testlink_ID:324_1)"""
        log.debug("037")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep64 abnormal1 encryption,test fail!"
        print "test wep64 abnormal1 encryption,test pass!"

    #2.4g的WEP64bit参数校验2(testlink_ID:324_2)
    def test_038_abnormal2_wep(self):
        u"""2.4g的WEP64bit参数校验2(testlink_ID:324_2)"""
        log.debug("038")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep64 abnormal2 encryption,test fail!"
        print "test wep64 abnormal2 encryption,test pass!"

    #测试ssid中2.4g的无线加密-为13位wep128时(testlink_ID:323_1)
    def test_039_13wep128_encryption(self):
        u"""测试ssid中2.4g的无线加密-为13位wep128时(testlink_ID:323_1)"""
        log.debug("039")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 13bits wep128 encryption of wifi,test fail!"
        print "test 13bits wep128 encryption of wifi,test pass!"

    #测试ssid中2.4g的无线加密-为26位wep128时(testlink_ID:323_2)
    def test_040_26wep128_encryption(self):
        u"""测试ssid中2.4g的无线加密-为26位wep128时(testlink_ID:323_2)"""
        log.debug("040")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wep128
        tmp.wifi_wep_encryption(0,data_wireless['wep128-26'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep128-26'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 26bits wep128 encryption of wifi,test fail!"
        print "test 26bits wep128 encryption of wifi,test pass!"

    #2.4g的WEP128bit参数校验1(testlink_ID:325_1)
    def test_041_abnormal1_wep(self):
        u"""2.4g的WEP128bit参数校验1(testlink_ID:325_1)"""
        log.debug("041")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep128 abnormal1 encryption,test fail!"
        print "test wep128 abnormal1 encryption,test pass!"

    #2.4g的WEP128bit参数校验2(testlink_ID:325_2)
    def test_042_abnormal2_wep(self):
        u"""2.4g的WEP128bit参数校验2(testlink_ID:325_2)"""
        log.debug("042")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep128 abnormal2 encryption,test fail!"
        print "test wep128 abnormal2 encryption,test pass!"

    #测试ssid中2.4g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)
    def test_043_wpa_mixed_AES_encryption(self):
        u"""测试ssid中2.4g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)"""
        log.debug("043")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-AES encryption of wifi,test pass!"


    #2.4g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)
    def test_044_check_AES_arguments(self):
        u"""2.4g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)"""
        log.debug("044")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check AES arguments,test fail!"
        print "check AES arguments,test pass!"

    #2.4g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)
    def test_045_wpa_mixed_AES_max(self):
        u"""2.4g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)"""
        log.debug("045")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK AES max length ,test fail!"
        print "check WPA/WPA2-PSK AES max length,test pass!"

    #测试ssid中2.4g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)
    def test_046_wpa_mixed_TKIP_encryption(self):
        u"""测试ssid中2.4g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)"""
        log.debug("046")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-TKIP的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-TKIP encryption of wifi,test fail!"
        print "test wpa/wpa2-TKIP encryption of wifi,test pass!"

    #2.4g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)
    def test_047_check_TKIP_arguments(self):
        u"""2.4g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)"""
        log.debug("047")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check TKIP/AES arguments,test fail!"
        print "check TKIP/AES arguments,test pass!"

    #2.4g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)
    def test_048_wpa_mixed_TKIP_AES_max(self):
        u"""2.4g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)"""
        log.debug("048")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK TKIP/AES max length ,test fail!"
        print "check WPA/WPA2-PSK TKIP/AES max length,test pass!"

    #测试ssid中2.4g的无线加密-为wpa2-AES时(testlink_ID:337)
    def test_049_wpa2_AES_encryption(self):
        u"""测试ssid中2.4g的无线加密-为wpa2-AES时(testlink_ID:337)"""
        log.debug("049")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    #2.4g的wpa2-AES参数校验(testlink_ID:341)
    def test_050_check_WPA2_AES_arguments(self):
        u"""2.4g的wpa2-AES参数校验(testlink_ID:341)"""
        log.debug("050")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES arguments,test fail!"
        print "check wpa2-AES arguments,test pass!"

    #2.4g的wpa2-AES 密钥长度限制验证(testlink_ID:346)
    def test_051_wpa2_AES_max(self):
        u"""2.4g的wpa2-AES 密钥长度限制验证(testlink_ID:346)"""
        log.debug("051")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES max length ,test fail!"
        print "check wpa2-AES max length,test pass!"

    #测试ssid中2.4g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)
    def test_052_wpa2_TKIP_AES_encryption(self):
        u"""测试ssid中2.4g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)"""
        log.debug("052")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-TKIP/AES encryption of wifi,test pass!"

    #2.4g的wpa2-TKIP/AES参数校验(testlink_ID:343)
    def test_053_check_WPA2_TKIP_AES_arguments(self):
        u"""2.4g的wpa2-TKIP/AES参数校验(testlink_ID:343)"""
        log.debug("053")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AESAES arguments,test fail!"
        print "check wpa2-TKIP/AESAES arguments,test pass!"

    #2.4g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)
    def test_054_wpa2_TKIP_AES_max(self):
        u"""2.4g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)"""
        log.debug("054")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AES max length ,test fail!"
        print "check wpa2-TKIP/AES max length,test pass!"

    #测试ssid中2.4g的无线加密-为wpa2-802.1x-TKIP/AES时
    def test_055_wpa2_802_1x_TKIP_AES(self):
        u"""测试ssid中2.4g的无线加密-为wpa2-802.1x-TKIP/AES时"""
        log.debug("055")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-TKIP/AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa2-802.1x-AES时
    def test_056_wpa2_802_1x_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa2-802.1x-AES时"""
        log.debug("056")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-AES时
    def test_057_wpa_mixed_802_1x_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-AES时"""
        log.debug("057")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa/wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(3,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时
    def test_058_wpa_mixed_802_1x_TKIP_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时"""
        log.debug("058")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa/wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"


    #测试ssid中2.4g的无线加密再次改为wpa2-AES时(testlink_ID:337)
    def test_059_wpa_mixed_AES_encryption(self):
        u"""测试ssid中2.4g的无线加密再次改为wpa2-AES时(testlink_ID:337)"""
        log.debug("059")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    #测试ssid中5g的无线加密-为不加密时(testlink_ID:320)
    def test_060_None_encryption(self):
        u"""测试ssid中5g的无线加密-为不加密时(testlink_ID:320)"""
        log.debug("060")
        #切换ssid的5G频段
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("5GHz")
        ##设置默认SSID无线为非加密
        tmp.wifi_None_encryption()
        #无线连接这个非加密的无线
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test None encryption of wifi,test fail!"
        print "test None encryption of wifi,test pass!"

    #测试ssid中5g的无线加密-为5位wep64时(testlink_ID:322_1)
    def test_061_5wep64_encryption(self):
        u"""测试ssid中5g的无线加密-为5位wep64时(testlink_ID:322_1)"""
        log.debug("061")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 5bits wep64 encryption of wifi,test fail!"
        print "test 5bits wep64 encryption of wifi,test pass!"

    #测试ssid中5g的无线加密-为10位wep64时(testlink_ID:322_2)
    def test_062_10wep64_encryption(self):
        u"""测试ssid中5g的无线加密-为10位wep64时(testlink_ID:322_2)"""
        log.debug("062")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wep64
        tmp.wifi_wep_encryption(0,data_wireless['wep64-10'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep64-10'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 10bits wep64 encryption of wifi,test fail!"
        print "test 10bits wep64 encryption of wifi,test pass!"

    #5g的WEP64bit参数校验1(testlink_ID:324_1)
    def test_063_abnormal1_wep(self):
        u"""5g的WEP64bit参数校验1(testlink_ID:324_1)"""
        log.debug("063")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep64 abnormal1 encryption,test fail!"
        print "test wep64 abnormal1 encryption,test pass!"

    #5g的WEP64bit参数校验2(testlink_ID:324_2)
    def test_064_abnormal2_wep(self):
        u"""5g的WEP64bit参数校验2(testlink_ID:324_2)"""
        log.debug("064")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep64 abnormal2 encryption,test fail!"
        print "test wep64 abnormal2 encryption,test pass!"

    #测试ssid中5g的无线加密-为13位wep128时(testlink_ID:323_1)
    def test_065_13wep128_encryption(self):
        u"""测试ssid中5g的无线加密-为13位wep128时(testlink_ID:323_1)"""
        log.debug("065")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 13bits wep128 encryption of wifi,test fail!"
        print "test 13bits wep128 encryption of wifi,test pass!"

    #测试ssid中5g的无线加密-为26位wep128时(testlink_ID:323_1)
    def test_066_26wep128_encryption(self):
        u"""测试ssid中5g的无线加密-为26位wep128时(testlink_ID:323_1)"""
        log.debug("066")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wep128
        tmp.wifi_wep_encryption(0,data_wireless['wep128-26'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['all_ssid'],data_wireless['wep128-26'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test 26bits wep128 encryption of wifi,test fail!"
        print "test 26bits wep128 encryption of wifi,test pass!"

    #5g的WEP128bit参数校验1(testlink_ID:325_1)
    def test_067_abnormal1_wep(self):
        u"""5g的WEP128bit参数校验1(testlink_ID:325_1)"""
        log.debug("067")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep128 abnormal1 encryption,test fail!"
        print "test wep128 abnormal1 encryption,test pass!"

    #5g的WEP128bit参数校验2(testlink_ID:325_2)
    def test_068_abnormal2_wep(self):
        u"""5g的WEP128bit参数校验2(testlink_ID:325_2)"""
        log.debug("068")
        tmp = SSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep128 abnormal2 encryption,test fail!"
        print "test wep128 abnormal2 encryption,test pass!"

    #测试ssid中5g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)
    def test_069_wpa_mixed_AES_encryption(self):
        u"""测试ssid中5g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)"""
        log.debug("069")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-AES encryption of wifi,test pass!"


    #5g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)
    def test_070_check_AES_arguments(self):
        u"""5g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)"""
        log.debug("070")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check AES arguments,test fail!"
        print "check AES arguments,test pass!"

    #5g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)
    def test_071_wpa_mixed_AES_max(self):
        u"""5g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)"""
        log.debug("071")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK AES max length ,test fail!"
        print "check WPA/WPA2-PSK AES max length,test pass!"

    #测试ssid中5g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)
    def test_072_wpa_mixed_TKIP_encryption(self):
        u"""测试ssid中5g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)"""
        log.debug("072")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-TKIP的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-TKIP encryption of wifi,test fail!"
        print "test wpa/wpa2-TKIP encryption of wifi,test pass!"

    #5g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)
    def test_073_check_TKIP_arguments(self):
        u"""5g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)"""
        log.debug("073")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check TKIP/AES arguments,test fail!"
        print "check TKIP/AES arguments,test pass!"

    #5g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)
    def test_074_wpa_mixed_TKIP_AES_max(self):
        u"""5g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)"""
        log.debug("074")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check WPA/WPA2-PSK TKIP/AES max length ,test fail!"
        print "check WPA/WPA2-PSK TKIP/AES max length,test pass!"

    #测试ssid中5g的无线加密-为wpa2-AES时(testlink_ID:337)
    def test_075_wpa2_AES_encryption(self):
        u"""测试ssid中5g的无线加密-为wpa2-AES时(testlink_ID:331)"""
        log.debug("075")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"


    #5g的wpa2-AES参数校验(testlink_ID:341)
    def test_076_check_WPA2_AES_arguments(self):
        u"""5g的wpa2-AES参数校验(testlink_ID:341)"""
        log.debug("076")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES arguments,test fail!"
        print "check wpa2-AES arguments,test pass!"

    #5g的wpa2-AES 密钥长度限制验证(testlink_ID:346)
    def test_077_wpa2_AES_max(self):
        u"""5g的wpa2-AES 密钥长度限制验证(testlink_ID:346)"""
        log.debug("077")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-AES max length ,test fail!"
        print "check wpa2-AES max length,test pass!"

    #测试ssid中5g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)
    def test_078_wpa2_TKIP_AES_encryption(self):
        u"""测试ssid中5g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)"""
        log.debug("078")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-TKIP/AES encryption of wifi,test pass!"


    #5g的wpa2-TKIP/AES参数校验(testlink_ID:343)
    def test_079_check_WPA2_TKIP_AES_arguments(self):
        u"""5g的wpa2-TKIP/AES参数校验(testlink_ID:343)"""
        log.debug("079")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AESAES arguments,test fail!"
        print "check wpa2-TKIP/AESAES arguments,test pass!"

    #5g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)
    def test_080_wpa2_TKIP_AES_max(self):
        u"""5g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)"""
        log.debug("080")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"check wpa2-TKIP/AES max length ,test fail!"
        print "check wpa2-TKIP/AES max length,test pass!"

    #测试ssid中5g的无线加密-为wpa2-802.1x-TKIP/AES时
    def test_081_wpa2_802_1x_TKIP_AES(self):
        u"""测试ssid中5g的无线加密-为wpa2-802.1x-TKIP/AES时"""
        log.debug("081")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-TKIP/AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa2-802.1x-AES时
    def test_082_wpa2_802_1x_AES(self):
        u"""测试网络组中5g的无线加密-为wpa2-802.1x-AES时"""
        log.debug("082")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-802.1x-AES时
    def test_083_wpa_mixed_802_1x_AES(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-802.1x-AES时"""
        log.debug("083")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa/wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(3,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时
    def test_084_wpa_mixed_802_1x_TKIP_AES(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时"""
        log.debug("084")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wpa/wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['all_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试ssid中5g的无线加密再次改为wpa2-AES时(testlink_ID:337)
    def test_085_wpa_mixed_AES_encryption(self):
        u"""测试ssid中5g的无线加密再次改为wpa2-AES时(testlink_ID:337)"""
        log.debug("085")
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])

        #切换为Dual-Band频段
        tmp.change_AP_Freq("Dual-Band")

        assert data_wireless['all_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    ####################################################################
    ##################以下是Mac Filter的测试用例###########################
    ####################################################################
    #设置ssid的无线过滤的白名单,添加本机无线mac地址，并判断无线是否能够连接成功(testlink_ID:362)
    def test_086_mac_whitelist_in(self):
        u"""设置ssid的无线过滤的白名单,添加本机无线mac地址，并判断无线是否能够连接成功(testlink_ID:362)"""
        log.debug("086")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的白名单
        tmp.wifi_whitelist()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test mac in whitelist,test fail!"
        print "test mac in whitelist,test pass!"

    #设置无线过滤的白名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)
    def test_087_reboot_mac_whitelist_in(self):
        u"""设置无线过滤的白名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)"""
        log.debug("087")
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test mac in whitelist after reboot ap,test fail!"
        print "test mac in whitelist after reboot ap,test pass!"

    #刷新页面配置，显示是 whitelist 状态
    def test_088_mac_whitelist_display(self):
        u"""刷新页面配置，显示是 whitelist 状态"""
        log.debug("088")
        tmp = SSIDBusiness(self.driver)
        #点击ssid菜单
        tmp.SSID_menu()
        #获取第一个ssid的MAC过滤状态
        result = tmp.get_first_macfilter()
        assert result == (u"白名单" or "Whitelist"),"test mac filter display in whitelist,test fail!"
        print "test mac filter display in whitelist,test pass!"

    #设置ssid的无线过滤的白名单,添加随机mac，并判断本机无线是否能够连接成功(testlink_ID:362)
    def test_089_mac_whitelist_out(self):
        u"""设置ssid的无线过滤的白名单,添加随机mac，并判断本机无线是否能够连接成功(testlink_ID:362)"""
        log.debug("089")
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


    #设置ssid的无线过滤的白名单,添加随机小写的mac地址(testlink_ID:362)
    def test_090_lower_mac_whitelist_out(self):
        u"""设置ssid的无线过滤的白名单,添加随机小写的mac地址(testlink_ID:362)"""
        log.debug("090")
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test lower mac out whitelist,test fail!"
        print "test lower mac out whitelist,test pass!"

    #添加10条mac地址白名单，确认其有效性(testlink_ID:363)
    def test_091_many_mac_whitelist(self):
        u"""添加10条mac地址白名单，确认其有效性(testlink_ID:363)"""
        log.debug("091")
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        tmp = SSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 10) and (data_wireless['all_ssid'] in result2),"test many mac_whitelist,test fail!"
        print "test many mac_whitelist,test pass!"

    #删除所有的mac地址白名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)
    def test_092_del_many_mac_whitelist(self):
        u"""删除所有的mac地址白名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)"""
        log.debug("092")
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        tmp1 = SSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result1 == 1 and (data_wireless['all_ssid'] in result2),"test del all mac_whitelist,test fail!"
        print "test del all mac_whitelist,test pass!"

    #设置ssid的无线过滤的黑名单,添加本机mac地址，并判断无线不能连接成功(testlink_ID:360)
    def test_093_mac_blacklist_in(self):
        u"""设置ssid的无线过滤的黑名单,添加本机mad地址，并判断无线不能连接成功(testlink_ID:360)"""
        log.debug("093")
        tmp = SSIDBusiness(self.driver)
        #设置ssid的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test mac in blacklist,test fail!"
        print "test mac in blacklist,test pass!"

    #刷新页面配置，显示是 blacklist 状态
    def test_094_mac_blacklist_display(self):
        u"""刷新页面配置，显示是 blacklist 状态"""
        log.debug("094")
        tmp = SSIDBusiness(self.driver)
        #点击ssid菜单
        tmp.SSID_menu()
        #获取第一个ssid的MAC过滤状态
        result = tmp.get_first_macfilter()
        assert result == (u"黑名单" or "Blacklist"),"test mac filter display in blacklist,test fail!"
        print "test mac filter display in blacklist,test pass!"

    #设置无线过滤的黑名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)
    def test_095_reboot_mac_blacklist_in(self):
        u"""设置无线过滤的黑名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)"""
        log.debug("095")
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test mac in blacklist after reboot ap,test fail!"
        print "test mac in blacklist after reboot ap,test pass!"

    #设置ssid的无线过滤的黑名单,添加随机mac，并判断本机无线能够连接成功(testlink_ID:362)
    def test_096_mac_blacklist_out(self):
        u"""设置ssid的无线过滤的黑名单,添加随机mac，并判断本机无线能够连接成功(testlink_ID:362)"""
        log.debug("096")
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

    #添加10条mac地址黑名单，确认其有效性(testlink_ID:361)
    def test_097_many_mac_blacklist(self):
        u"""添加10条mac地址黑名单，确认其有效性(testlink_ID:361)"""
        log.debug("097")
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        tmp = SSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，黑名单数目
        result1 = tmp.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 10) and (data_wireless['all_ssid'] in result2),"test many mac_blacklist,test fail!"
        print "test many mac_blacklist,test pass!"

    #删除所有的mac地址黑名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)
    def test_098_del_many_mac_blacklist(self):
        u"""删除所有的mac地址黑名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)"""
        log.debug("098")
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        tmp1 = SSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，黑名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp1.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result1 == 1 and ('Not connected' in result2),"test del all mac_blacklist,test fail!"
        print "test del all mac_blacklist,test pass!"

    #禁用mac filter，并判断本机无线能够连接成功(testlink_ID:364)
    def test_099_mac_blacklist_out(self):
        u"""禁用mac filter，并判断本机无线能够连接成功(testlink_ID:364)"""
        log.debug("099")
        #禁用ssid的无线过滤
        tmp = SSIDBusiness(self.driver)
        tmp.disable_macfilter(1)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"test mac out blacklist,test fail!"
        print "test mac out blacklist,test pass!"

    #刷新页面配置，显示是 disable 状态
    def test_100_mac_disable_display(self):
        u"""刷新页面配置，显示是 disable 状态"""
        log.debug("100")
        tmp = SSIDBusiness(self.driver)
        #点击ssid菜单
        tmp.SSID_menu()
        #获取第一个ssid的MAC过滤状态
        result = tmp.get_first_macfilter()
        assert result == (u"禁止" or "Disable"),"test mac filter display in disable status,test fail!"
        print "test mac filter display in disable status,test pass!"


    #Blacklist 多zone环境应用功能验证1(testlink_ID:365_1)
    def test_101_check_blacklist_many_SSID1(self):
        u"""Blacklist 多zone环境应用功能验证1(testlink_ID:365_1)"""
        log.debug("101")
        tmp = SSIDBusiness(self.driver)
        #新建一个ssid
        tmp.new_ssid(data_wireless['all_ssid']+"2",data_wireless['short_wpa'])
        #有多个ssid时，设置第2个ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist(2)
        #将所有ssid加入master ap
        tmp1 = APSBusiness(self.driver)
        tmp1.add_master_to_all_NG()
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "check blacklist validity in many SSID1,test fail!"
        print "check blacklist validity in many SSID1,test pass!"

    #Blacklist 多zone环境应用功能验证2(testlink_ID:365_2)
    def test_102_check_blacklist_many_SSID2(self):
        u"""Blacklist 多zone环境应用功能验证2(testlink_ID:365_2)"""
        log.debug("102")
        tmp = SSIDBusiness(self.driver)
        #有多个ssid时，设置第1个ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist_backup(1)
        #有多个ssid时,禁用第2个的无线过滤
        tmp.disable_macfilter(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ((data_wireless['all_ssid']+"2") in result2),\
            "check blacklist validity in many SSID2,test fail!"
        print "check blacklist validity in many SSID2,test pass!"

    #Blacklist 多zone环境应用功能验证3(testlink_ID:365_3)
    def test_103_check_blacklist_many_SSID3(self):
        u"""Blacklist 多zone环境应用功能验证3(testlink_ID:365_3)"""
        log.debug("103")
        tmp = SSIDBusiness(self.driver)
        #有多个ssid时，设置第2个ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist_backup(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ('Not connected' in result2),\
            "check blacklist validity in many SSID3,test fail!"
        print "check blacklist validity in many SSID3,test pass!"

    #Whitelist 多zone环境应用功能验证1(testlink_ID:366_1)
    def test_104_check_Whitelist_many_SSID1(self):
        u"""Whitelist 多zone环境应用功能验证1(testlink_ID:366_1)"""
        log.debug("104")
        tmp1 = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp1.randomMAC()
        tmp1.edit_accesslist_onemac(random_mac)
        tmp = SSIDBusiness(self.driver)
        #有多个ssid时,禁用第1个的无线过滤
        tmp.disable_macfilter(1)
        #有多个ssid时，设置第2个ssid的无线过滤的白名单
        tmp.wifi_n_whitelist(2)
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "check whitelist validity in many SSID1,test fail!"
        print "check whitelist validity in many SSID1,test pass!"

    #Whitelist 多zone环境应用功能验证2(testlink_ID:366_2)
    def test_105_check_Whitelist_many_SSID2(self):
        u"""Whitelist 多zone环境应用功能验证2(testlink_ID:366_2)"""
        log.debug("105")
        tmp = SSIDBusiness(self.driver)
        #有多个ssid时，设置第1个ssid的无线过滤的白名单
        tmp.wifi_n_whitelist_backup(1)
        #有多个ssid时,禁用第2个的无线过滤
        tmp.disable_macfilter(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ((data_wireless['all_ssid']+"2") in result2),\
            "check whitelist validity in many SSID2,test fail!"
        print "check whitelist validity in many SSID2,test pass!"

    #Whitelist 多zone环境应用功能验证3(testlink_ID:366_3)
    def test_106_check_Whitelist_many_SSID3(self):
        u"""Whitelist 多zone环境应用功能验证3(testlink_ID:366_3)"""
        log.debug("106")
        tmp = SSIDBusiness(self.driver)
        #有多个ssid时，设置第2个ssid的无线过滤的白名单
        tmp.wifi_n_whitelist_backup(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ('Not connected' in result2),\
            "check whitelist validity in many SSID3,test fail!"
        print "check whitelist validity in many SSID3,test pass!"

    #Whitelist 多zone环境应用功能验证4(testlink_ID:366_4)
    def test_107_check_Whitelist_many_SSID4(self):
        u"""Whitelist 多zone环境应用功能验证4(testlink_ID:366_4)"""
        log.debug("107")
        tmp = ClientAccessBusiness(self.driver)
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ((data_wireless['all_ssid']+"2") in result2),\
            "check whitelist validity in many SSID4,test fail!"
        print "check whitelist validity in many SSID4,test pass!"

    #Blacklist和whitelist在多zone环境里冲突时的功能验证1(testlink_ID:367_1)
    def test_108_check_mix_many_SSID1(self):
        u"""Blacklist和whitelist在多zone环境里冲突时的功能验证1(testlink_ID:367_1)"""
        log.debug("108")
        tmp = SSIDBusiness(self.driver)
        #有多个ssid时，设置第1个ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist_backup(1)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ((data_wireless['all_ssid']+"2") in result2),\
            "check whitelist and blacklist validity in many SSID1,test fail!"
        print "check whitelist and blacklist validity in many SSID1,test pass!"

     #Blacklist和whitelist在多zone环境里冲突时的功能验证2(testlink_ID:367_2)
    def test_109_check_mix_many_SSID2(self):
        u"""Blacklist和whitelist在多zone环境里冲突时的功能验证2(testlink_ID:367_2)"""
        log.debug("109")
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_onemac(random_mac)
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['all_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and ('Not connected' in result2),\
            "check whitelist and blacklist validity in many SSID2,test fail!"
        print "check whitelist and blacklist validity in many SSID2,test pass!"

    #终端的MAC地址在同时配置在 blacklistlist 和whitelist 名单里(testlink_ID:368)
    def test_110_check_mix_sametime_SSID(self):
        u"""Blacklist和whitelist在多zone环境里冲突时的功能验证2"""
        log.debug("110")
        tmp = SSIDBusiness(self.driver)
        #删除第二个ssid
        tmp.del_n_ssid(2)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #禁用第1个的无线过滤
        tmp.disable_macfilter(1)
        assert data_wireless['all_ssid'] in result,\
            "client mac in blacklist and whitelist in the sametime,test fail!"
        print "client mac in blacklist and whitelist in the sametime,test pass!"



    #WEP 64bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:371_1)
    def test_111_wep64_1_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:371_1)"""
        log.debug("111")
        tmp1 = ClientAccessBusiness(self.driver)
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #设置默认SSID的无线过滤的黑名单
        tmp.wifi_blacklist_backup1()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WEP64bit,test fail!"
        print "test one mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:371_2)
    def test_112_wep64_many_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:371_2)"""
        log.debug("112")
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WEP64bit,test fail!"
        print "test many mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:371_3)
    def test_113_wep64_1_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:371_3)"""
        log.debug("113")
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

    #WEP 64bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:371_4)
    def test_114_wep64_many_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:371_4)"""
        log.debug("114")
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

    #WEP 64bit 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:372_1)
    def test_115_wep64_1_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:372_1)"""
        log.debug("115")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的白名单
        tmp.wifi_whitelist_backup1()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WEP64bit,test fail!"
        print "test one mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:372_2)
    def test_116_wep64_many_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:372_2)"""
        log.debug("116")
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

    #WEP 64bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:372_3)
    def test_117_wep64_1_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:372_3)"""
        log.debug("117")
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

    #WEP 64bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:372_4)
    def test_118_wep64_many_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:372_4)"""
        log.debug("118")
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


    #WEP 128bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:373_1)
    def test_119_wep128_1_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:373_1)"""
        log.debug("119")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #设置默认SSID的无线过滤的黑名单
        tmp.wifi_blacklist_backup1()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WEP128bit,test fail!"
        print "test one mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:373_2)
    def test_120_wep128_many_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:373_2)"""
        log.debug("120")
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

    #WEP 128bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:373_3)
    def test_121_wep128_1_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:373_3)"""
        log.debug("121")
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

    #WEP 128bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:373_4)
    def test_122_wep128_many_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:373_4)"""
        log.debug("122")
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

    #WEP 128bit 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:374_1)
    def test_123_wep128_1_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:374_1)"""
        log.debug("123")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的白名单
        tmp.wifi_whitelist_backup1()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WEP128bit,test fail!"
        print "test one mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:374_2)
    def test_124_wep128_many_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:374_2)"""
        log.debug("124")
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

    #WEP 128bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:374_3)
    def test_125_wep128_1_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:374_3)"""
        log.debug("125")
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

    #WEP 128bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:374_4)
    def test_126_wep128_many_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:374_4)"""
        log.debug("126")
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


    #WPA 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:375_1)
    def test_127_WPA_1_blacklist(self):
        u"""WPA 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:375_1)"""
        log.debug("127")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #设置默认SSID的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:375_2)
    def test_128_WPA_many_blacklist(self):
        u"""WPA 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:375_2)"""
        log.debug("128")
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


    #WPA 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:375_3)
    def test_129_WPA_1_blacklist(self):
        u"""WPA 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:375_3)"""
        log.debug("129")
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

    #WPA 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:375_4)
    def test_130_WPA_many_blacklist(self):
        u"""WPA 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:375_4)"""
        log.debug("130")
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

    #WPA 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:376_1)
    def test_131_WPA_1_whitelist(self):
        u"""WPA 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:376_1)"""
        log.debug("131")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WPA,test fail!"
        print "test one mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:376_2)
    def test_132_WPA_many_whitelist(self):
        u"""WPA 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:376_2)"""
        log.debug("132")
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

    #WPA 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:376_3)
    def test_133_WPA_1_whitelist(self):
        u"""WPA 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:376_3)"""
        log.debug("133")
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

    #WPA 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:376_4)
    def test_134_WPA_many_whitelist(self):
        u"""WPA 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:376_4)"""
        log.debug("134")
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

    #WPA2 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:377_1)
    def test_135_WPA2_1_blacklist(self):
        u"""WPA2 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:377_1)"""
        log.debug("135")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        ##设置默认SSID无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #设置默认SSID的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WPA2,test fail!"
        print "test one mac in blacklist with WPA2,test pass!"

    #WPA2 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:377_2)
    def test_136_WPA2_many_blacklist(self):
        u"""WPA2 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:377_2)"""
        log.debug("136")
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


    #WPA2 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:377_3)
    def test_137_WPA2_1_blacklist(self):
        u"""WPA2 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:377_3)"""
        log.debug("137")
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

    #WPA2 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:377_4)
    def test_138_WPA2_many_blacklist(self):
        u"""WPA2 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:377_4)"""
        log.debug("138")
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

    #WPA2 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:378_1)
    def test_139_WPA2_1_whitelist(self):
        u"""WPA2 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:378_1)"""
        log.debug("139")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with WPA2,test fail!"
        print "test one mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:378_2)
    def test_140_WPA2_many_whitelist(self):
        u"""WPA2 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:378_2)"""
        log.debug("140")
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

    #WPA2 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:378_3)
    def test_141_WPA2_1_whitelist(self):
        u"""WPA2 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:378_3)"""
        log.debug("141")
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

    #WPA2 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:378_4)
    def test_142_WPA2_many_whitelist(self):
        u"""WPA2 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:378_4)"""
        log.debug("142")
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


    #open 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:379_1)
    def test_143_open_1_blacklist(self):
        u"""open 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:379_1)"""
        log.debug("143")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为不加密
        tmp.wifi_None_encryption()
        #设置默认SSID的无线过滤的黑名单
        tmp.wifi_blacklist_backup2()
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with open,test fail!"
        print "test one mac in blacklist with open,test pass!"

    #open 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:379_2)
    def test_144_open_many_blacklist(self):
        u"""open 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:379_2)"""
        log.debug("144")
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


    #open 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:379_3)
    def test_145_open_1_blacklist(self):
        u"""open 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:379_3)"""
        log.debug("145")
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

    #open 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:379_4)
    def test_146_open_many_blacklist(self):
        u"""open 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:379_4)"""
        log.debug("146")
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

    #open 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:379_5)
    def test_147_open_1_whitelist(self):
        u"""open 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:379_5)"""
        log.debug("147")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID的无线过滤的白名单
        tmp.wifi_whitelist_backup2()
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert data_wireless['all_ssid'] in result,"test one mac in whitelist with open,test fail!"
        print "test one mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:379_6)
    def test_148_open_many_whitelist(self):
        u"""open 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:379_6)"""
        log.debug("148")
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

    #open 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:379_7)
    def test_149_open_1_whitelist(self):
        u"""open 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:379_7)"""
        log.debug("149")
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

    #open 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:379_8)
    def test_150_open_many_whitelist(self):
        u"""open 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:379_8)"""
        log.debug("150")
        tmp2 = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp2.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp2.connect_NONE_AP_backup(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #禁用mac地址过滤
        tmp = SSIDBusiness(self.driver)
        tmp.disable_macfilter1(1)
        assert 'Not connected' in result,"test many mac in whitelist with open,test fail!"
        print "test many mac in whitelist with open,test pass!"


    #Gateway MAC Address为空的配置验证(testlink_ID:381)
    def test_151_check_wifi_n_isolation_gateway_mac_blank(self):
        u"""Gateway MAC Address为空的配置验证(testlink_ID:381)"""
        log.debug("151")
        tmp = SSIDBusiness(self.driver)
        #配置第n个ssid的客户端隔离的网关mac为空的测试
        result1,result2 = tmp.check_wifi_n_isolation_gateway_mac_err_backup(1," ")
        assert (result1 and result2) == True,"check gateway mac is blank,test fail!"
        print "check gateway mac is blank,test pass!"

    #单环境下client isolation功能验证radio--这里只验证后台规则生效(testlink_ID:382_1)
    def test_152_check_isolation_radio(self):
        u"""单环境下client isolation功能验证radio--这里只验证后台规则生效(testlink_ID:382_1)"""
        log.debug("152")
        tmp = SSIDBusiness(self.driver)
        #配置第1个ssid的客户端隔离的无线模式
        tmp. wifi_n_isolation(1,"radio")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result1) and ("radio" in result2),\
            "check isolation radio,test fail!"
        print "check isolation radio,test pass!"

    #单环境下client isolation功能验证internet(testlink_ID:382_2)
    def test_153_check_isolation_internet(self):
        u"""单环境下client isolation功能验证internet(testlink_ID:382_2)"""
        log.debug("153")
        tmp = SSIDBusiness(self.driver)
        #配置第1个ssid的客户端隔离的互联网模式
        tmp. wifi_n_isolation_backup(1,"internet")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        result3,result4 = tmp.check_isolation(data_wireless['all_ssid'])
        assert ("1" in result1) and ("internet" in result2) and \
               (result3 != 0) and (result4 == 0), \
            "check isolation internet,test fail!"
        print "check isolation internet,test pass!"

    #单环境下client isolation功能验证gatewaymac(testlink_ID:382_3)
    def test_154_check_isolation_gatewaymac(self):
        u"""单环境下client isolation功能验证gatewaymac(testlink_ID:382_3)"""
        log.debug("154")
        tmp = SSIDBusiness(self.driver)
        #配置第1个ssid的客户端隔离的网关mac模式
        #获取7000的mac地址
        route_mac = tmp.get_router_mac(data_basic['7000_ip'],data_basic['sshUser'],data_login['all'])
        print route_mac
        tmp. wifi_n_isolation_gateway_mac_backup(1,route_mac)
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.gateway_mac")
        result4,result5 = tmp.check_isolation(data_wireless['all_ssid'])
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #配置第1个ssid的客户端隔离的无线模式
        tmp. wifi_n_isolation_backup(1,"radio")
        assert ("1" in result1) and ("gateway_mac" in result2) and (route_mac in result3) and \
            (result4 == 0) and (result5 == 0), \
            "check isolation gateway mac,test fail!"
        print "check isolation gateway mac,test pass!"

    #重启查看client isolation是否依然生效(testlink_ID:383)
    def test_155_check_reboot_isolation(self):
        u"""重启查看client isolation是否依然生效(testlink_ID:383)"""
        log.debug("155")
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result1) and ("radio" in result2),\
            "check isolation radio after rebooting,test fail!"
        print "check isolation radio after rebooting,test pass!"

    #多功能混合验证 client isolation + encrypted  (open mode)(testlink_ID:384)
    def test_156_check_open_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (open mode)(testlink_ID:384)"""
        log.debug("156")
        tmp = SSIDBusiness(self.driver)
        #无线连接这个的AP
        result1 = tmp.connect_NONE_AP(data_wireless['all_ssid'],\
                        data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check open encryption and isolation radio,test fail!"
        print "check open encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WEP 64bit  mode)(testlink_ID:385)
    def test_157_check_wep64_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WEP 64bit  mode)(testlink_ID:385)"""
        log.debug("157")
        tmp = SSIDBusiness(self.driver)
        #设置wep64加密
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个的AP
        result1 = tmp.connect_WEP_AP(data_wireless['all_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wep64bit encryption and isolation radio,test fail!"
        print "check wep64bit encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WEP 128bit  mode)(testlink_ID:386)
    def test_158_check_wep128_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WEP 128bit  mode)(testlink_ID:386)"""
        log.debug("158")
        tmp = SSIDBusiness(self.driver)
        #设置wep128加密
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个的AP
        result1 = tmp.connect_WEP_AP(data_wireless['all_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wep128bit encryption and isolation radio,test fail!"
        print "check wep128bit encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES mode)(testlink_ID:387)
    def test_159_check_wpa2_mix_AES_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES mode)(testlink_ID:387)"""
        log.debug("159")
        tmp = SSIDBusiness(self.driver)
        ##设置ssid无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2 mix-AES encryption and isolation radio,test fail!"
        print "check wpa2 mix-AES encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES/TKIP mode)(testlink_ID:388)
    def test_160_check_wpa2_mix_AESTKIP_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES/TKIP mode)(testlink_ID:388)"""
        log.debug("160")
        tmp = SSIDBusiness(self.driver)
        ##设置ssid无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2 mix-AES/TKIP encryption and isolation radio,test fail!"
        print "check wpa2 mix-AES/TKIP encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA2  AES mode)(testlink_ID:389)
    def test_161_check_wpa2_AES_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA2  AES mode)(testlink_ID:389)"""
        log.debug("161")
        tmp = SSIDBusiness(self.driver)
        #首先取消客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        ##设置ssid无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #再选择客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2-AES encryption and isolation radio,test fail!"
        print "check wpa2-AES encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA2  AES/TKIP mode)(testlink_ID:390)
    def test_162_check_wpa2_AESTKIP_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA2  AES/TKIP mode)(testlink_ID:390)"""
        log.debug("162")
        tmp = SSIDBusiness(self.driver)
        ##设置ssid无线为wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2-AES/TKIP encryption and isolation radio,test fail!"
        print "check wpa2-AES/TKIP encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + hide SSID(testlink_ID:391)
    def test_163_check_hideSSID_isolation(self):
        u"""多功能混合验证 client isolation + hide SSID(testlink_ID:391)"""
        log.debug("163")
        tmp = SSIDBusiness(self.driver)
        #设置第一个ssid是否隐藏
        tmp.set_hide_ssid()
        result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        #取消第一个ssid是否隐藏
        tmp.set_hide_ssid()
        assert (result1 == False) and ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check hide SSID and isolation radio,test fail!"
        print "check hide SSID and isolation radio,test pass!"

    #多功能混合验证 client isolation + mac filter(testlink_ID:392)
    def test_164_check_macfilter_isolation(self):
        u"""多功能混合验证 client isolation + mac filter(testlink_ID:392)"""
        log.debug("164")
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp1.del_accesslist_manymac()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)

        tmp = SSIDBusiness(self.driver)
        tmp.wifi_whitelist_backup()
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['all_ssid'] in result1) and ("1" in result2) \
                and ("radio" in result3),\
                "check mac filter and isolation radio,test fail!"
        print "check mac filter and isolation radio,test pass!"

    #hide SSID、WPA2、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:403)
    def test_165_WPA2_all_mixed_whitelist(self):
        u"""hide SSID、WPA2、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:403)"""
        log.debug("165")
        tmp = SSIDBusiness(self.driver)
        #设置第一个ssid是否隐藏
        tmp.set_hide_ssid()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WPA2 in all mixed whitelist,test fail!"
        print "check WPA2 in all mixed whitelist,test pass!"

    #hide SSID、OPEN、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:399)
    def test_166_open_all_mixed_whitelist(self):
        u"""hide SSID、OPEN、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:399)"""
        log.debug("166")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为不加密
        tmp.wifi_None_encryption()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_NONE_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check OPEN in all mixed whitelist,test fail!"
        print "check OPEN in all mixed whitelist,test pass!"

    #hide SSID、WEP64、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:400)
    def test_167_WEP64_all_mixed_whitelist(self):
        u"""hide SSID、WEP64、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:400)"""
        log.debug("167")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为WEP64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WEP64 in all mixed whitelist,test fail!"
        print "check WEP64 in all mixed whitelist,test pass!"

    #hide SSID、WEP128、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:401)
    def test_168_WEP128_all_mixed_whitelist(self):
        u"""hide SSID、WEP128、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:401)"""
        log.debug("168")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为WEP128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WEP128 in all mixed whitelist,test fail!"
        print "check WEP128 in all mixed whitelist,test pass!"

    #hide SSID、WPA、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:402)
    def test_169_WPA_all_mixed_whitelist(self):
        u"""hide SSID、WPA、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:402)"""
        log.debug("169")
        tmp = SSIDBusiness(self.driver)
        ##设置ssid无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['all_ssid'] in result4),\
                "check WPA in all mixed whitelist,test fail!"
        print "check WPA in all mixed whitelist,test pass!"

    #hide SSID、WPA、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:397)
    def test_170_WPA_all_mixed_blacklist(self):
        u"""hide SSID、WPA、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:397)"""
        log.debug("170")
        tmp = SSIDBusiness(self.driver)
        tmp.wifi_blacklist_backup()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check WPA in all mixed blacklist,test fail!"
        print "check WPA in all mixed blacklist,test pass!"

    #hide SSID、open、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:394)
    def test_171_open_all_mixed_blacklist(self):
        u"""hide SSID、open、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:394)"""
        log.debug("171")
        tmp = SSIDBusiness(self.driver)
        #设置默认SSID无线为不加密
        tmp.wifi_None_encryption()
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_NONE_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check open in all mixed blacklist,test fail!"
        print "check open in all mixed blacklist,test pass!"

    #hide SSID、wep64、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:395)
    def test_172_wep64_all_mixed_blacklist(self):
        u"""hide SSID、wep64、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:395)"""
        log.debug("172")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为WEP64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wep64 in all mixed blacklist,test fail!"
        print "check wep64 in all mixed blacklist,test pass!"

    #hide SSID、wep128、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:396)
    def test_173_wep128_all_mixed_blacklist(self):
        u"""hide SSID、wep128、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:396)"""
        log.debug("173")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为WEP128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wep128 in all mixed blacklist,test fail!"
        print "check wep128 in all mixed blacklist,test pass!"

    #hide SSID、wpa2、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:398)
    def test_174_wpa2_all_mixed_blacklist(self):
        u"""hide SSID、wpa2、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:398)"""
        log.debug("174")
        tmp = SSIDBusiness(self.driver)
        #设置ssid无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(2,0,data_wireless['short_wpa'])
        #result1 = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        #禁用第1个的无线过滤
        tmp.disable_macfilter(1)
        #取消第一个ssid是否隐藏
        tmp.set_hide_ssid()
        #取消第n个ssid的客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wpa2 in all mixed blacklist,test fail!"
        print "check wpa2 in all mixed blacklist,test pass!"


    #enableRSSI 配置验证并检查(testlink_ID:414_1)
    def test_175_check_enable_rssi(self):
        u"""enableRSSI 配置验证并检查(testlink_ID:414_1)"""
        log.debug("175")
        tmp = SSIDBusiness(self.driver)
        #enableRSSI 配置验证并检查
        result1,result2 = tmp.check_enable_rssi()
        assert result1==result2=="-94","check enable RSSI,test fail!"
        print "check enable RSSI,test pass!"

    #disableRSSI 配置验证并检查(testlink_ID:414_2)
    def test_176_check_disable_rssi(self):
        u"""disableRSSI 配置验证并检查(testlink_ID:414_2)"""
        log.debug("176")
        tmp = SSIDBusiness(self.driver)
        #disableRSSI 配置验证并检查
        result1,result2 = tmp.check_disable_rssi()
        assert (result1=="-94") and (result2 == "disableicon"),"check disable RSSI,test fail!"
        print "check disable RSSI,test pass!"

    #enable rssi,Minimum RSSI (dBm)为空格的配置验证(testlink_ID:415_1)
    def test_177_check_min_rssi_blank(self):
        u"""enable rssi,Minimum RSSI (dBm)为空格的配置验证(testlink_ID:415_1)"""
        log.debug("177")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(" ")
        assert result1 and result2,"enable rssi when min rssi is blank,test fail!"
        print "enable rssi when min rssi is blank,test pass!"

    #disable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:415_2)
    def test_178_check_min_rssi_empty(self):
        u"""disable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:415_2)"""
        log.debug("178")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_disable_min_rssi_error("")
        assert (result1==False) and (result2==False),"disable rssi when min rssi is empty,test fail!"
        print "disable rssi when min rssi is empty,test pass!"

    #在Minimum RSSI (dBm)处输入大于-1的整数(testlink_ID:416_1)
    def test_179_check_min_rssi_more_than_negative1(self):
        u"""在Minimum RSSI (dBm)处输入大于-1的整数(testlink_ID:416_1)"""
        log.debug("179")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("0")
        assert result1 and result2,"when min rssi more than nagative 1,test fail!"
        print "when min rssi more than nagative 1,test pass!"

    #在Minimum RSSI (dBm)处输入小于-94的整数(testlink_ID:416_2)
    def test_180_check_min_rssi_less_than_negative94(self):
        u"""在Minimum RSSI (dBm)处输入小于-94的整数(testlink_ID:416_2)"""
        log.debug("180")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("-95")
        assert result1 and result2,"when min rssi less than nagative 95,test fail!"
        print "when min rssi less than nagative 95,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_3)
    def test_181_check_min_rssi_chinese(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如中文(testlink_ID:416_3)"""
        log.debug("181")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['CN_ssid'])
        assert result1 and result2,"when min rssi is chinese,test fail!"
        print "when min rssi is chinese,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_4)
    def test_182_check_min_rssi_ascii(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如ASCII码(testlink_ID:416_4)"""
        log.debug("182")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['ascii_ssid'])
        assert result1 and result2,"when min rssi is ascii,test fail!"
        print "when min rssi is ascii,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_5)
    def test_183_check_min_rssi_decimals(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如小数(testlink_ID:416_5)"""
        log.debug("183")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("-50.5")
        assert result1 and result2,"when min rssi is decimals,test fail!"
        print "when min rssi is decimals,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_6)
    def test_184_check_min_rssi_special(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如特殊字符(testlink_ID:416_6)"""
        log.debug("184")
        tmp = SSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['special_ssid'])
        assert result1 and result2,"when min rssi is special,test fail!"
        print "when min rssi is special,test pass!"

    #在Minimum RSSI (dBm)处输入-1(testlink_ID:417_1)
    def test_185_check_min_rssi_negative1(self):
        u"""在Minimum RSSI (dBm)处输入-1(testlink_ID:417_1)"""
        log.debug("185")
        tmp = SSIDBusiness(self.driver)
        #enableRSSI
        tmp.check_enable_rssi()
        #设置最小RSSI值，并检查是否正确
        result = tmp.check_min_rssi("-1")
        assert result == "-1","when min rssi is -1,test fail!"
        print "when min rssi is -1,test pass!"

    #RSSI功能验证-范围验证-1(testlink_ID:417_2)
    def test_186_check_min_rssi_negative1_validity(self):
        u"""RSSI功能验证-范围验证-1(testlink_ID:417_2)"""
        log.debug("186")
        tmp = SSIDBusiness(self.driver)
        tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在2分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        assert "Not connected.\n" in result,"check min rssi is -1 validity,test fail!"
        print "check min rssi is -1 validity,test pass!"

    #在Minimum RSSI (dBm)处输入-94(testlink_ID:417_3)
    def test_187_check_min_rssi_negative94(self):
        u"""在Minimum RSSI (dBm)处输入-1(testlink_ID:417_3)"""
        log.debug("187")
        tmp = SSIDBusiness(self.driver)
        result = tmp.check_min_rssi("-94")
        assert result == "-94","when min rssi is -94,test fail!"
        print "when min rssi is -94,test pass!"

    #RSSI功能验证-范围验证-94(testlink_ID:417_4)
    def test_188_check_min_rssi_negative94_validity(self):
        u"""RSSI功能验证-范围验证-94(testlink_ID:417_4)"""
        log.debug("188")
        tmp = SSIDBusiness(self.driver)
        tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在2分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        assert "Not connected.\n" not in result,"check min rssi is -94 validity,test fail!"
        print "check min rssi is -94 validity,test pass!"

    #在Minimum RSSI (dBm)处输入-10(testlink_ID:418_1)
    def test_189_check_min_rssi_negative10(self):
        u"""在Minimum RSSI (dBm)处输入-10(testlink_ID:418_1)"""
        log.debug("189")
        tmp = SSIDBusiness(self.driver)
        result = tmp.check_min_rssi("-10")
        assert result == "-10","when min rssi is -10,test fail!"
        print "when min rssi is -10,test pass!"

    #RSSI功能验证-范围验证-10(testlink_ID:418_2)
    def test_190_check_min_rssi_negative10_validity(self):
        u"""RSSI功能验证-范围验证-10(testlink_ID:418_2)"""
        log.debug("190")
        tmp = SSIDBusiness(self.driver)
        tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在2分钟内每隔5秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        #disableRSSI 配置验证并检查
        tmp.check_disable_rssi()
        assert "Not connected.\n" in result,"check min rssi is -10 validity,test fail!"
        print "check min rssi is -10 validity,test pass!"


    #SSID的创建数量限制(testlink_ID:425)
    def test_191_max_addSSID1(self):
        u"""additional SSID的创建数量限制(testlink_ID:425)"""
        log.debug("191")
        tmp = SSIDBusiness(self.driver)
        #增加到最大的额外ssid
        result1,result2 = tmp.add_SSID_max_16(data_basic['DUT_ip'],data_basic['sshUser'],\
                       data_login['all'],data_wireless['all_ssid'],\
                       data_wireless['short_wpa'])
        assert (result1==False) and ("='ssid15'" in result2),\
            "check max ssid number,test fail!"
        print "check max ssid number,test pass!"

    #删除所有的SSID(testlink_ID:427_2)
    def test_192_del_max_SSID(self):
        u"""删除所有的SSID(testlink_ID:427_2)"""
        log.debug("192")
        tmp = SSIDBusiness(self.driver)
        #删除所有SSID
        tmp.del_all_NG()
        #检测页面上是否有第一个ssid
        result = tmp.check_first_exist()
        print "result = %s"%result
        assert result,"delete max SSID number,test fail!"
        print "delete max SSID number,test pass!"

    #删除ssid后没有其他无线接口(testlink_ID:427_3)
    def test_193_del_all_ssid(self):
        u"""删除ssid后没有其他无线接口(testlink_ID:427_3)"""
        log.debug("193")
        tmp = SSIDBusiness(self.driver)
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig ath2")
        self.assertIn("No such device", result)
        print "ap hasn't other wifi interface after del new SSID,test pass!"

    ################以下是客户端数量限制的用例##################
#作者:蒋甜
#时间:2018年3月8日
    #在页面上把AP恢复出厂设置
    def test_194_set_factory_reset(self):
        u"""在页面上把AP恢复出厂设置"""
        log.debug("194")
        #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
        # Lg = LoginBusiness(self.driver)
        # Lg.login_again()
        tmp = APSBusiness(self.driver)
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #验证client limit框数量输入特殊字符的情况,并验证有没有错误提示(testlink_ID:1311)
    def test_195_check_ascii_client_limit(self):
        u"""验证client limit框输入特殊字符的错误提示(testlink_ID:1311)"""
        log.debug("195")
        tmp = SSIDBusiness(self.driver)
        #检查输入不合法的字符，查看页面的提示情况
        result = tmp.set_client_limit_error(1,data_wireless['limit_ascii'])
        self.assertTrue(result)

     #验证client limit框数量输入下限值0的情况(testlink_ID:1312)
    def test_196_check_min_client_limit(self):
        u"""验证client limit框输入下限值0(testlink_ID:1312)"""
        log.debug("196")
        tmp = SSIDBusiness(self.driver)
        #页面client limit输入0，保存并且应用
        result = tmp.set_wireless_client_limit(1,data_wireless['limit_min'])
        #对比ssh后台和页面上设置的值是否相等
        result1 = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['limit_min'])
        self.assertFalse(result)
        self.assertTrue(result1)

    #验证client limit框数量输入上限值127的情况(testlink_ID:1313)
    def test_197_check_max_client_limit(self):
        u"""验证client limit框输入上限值127(testlink_ID:1313)"""
        log.debug("197")
        tmp = SSIDBusiness(self.driver)
        #页面client limit输入127，保存并且应用
        result = tmp.set_wireless_client_limit(1,data_wireless['limit_max'])
        #对比ssh后台和页面上设置的值是否相等
        result1 = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['limit_max'])
        self.assertFalse(result)
        self.assertTrue(result1)

    #验证client limit输入范围，填入小于下限值(testlink_ID:1314)
    def test_198_lessmin_client_limit(self):
        u"""验证client limit框输入小于下限值(testlink_ID:1314)"""
        log.debug("198")
        tmp = SSIDBusiness(self.driver)
        #页面client limit输入不合法数字，查看错误提示
        result = tmp.set_client_limit_error(1,data_wireless['limit_less_min'])
        self.assertTrue(result)

    #验证client limit输入范围，填入大于上限值(testlink_ID:1315)
    def test_199_moremax_client_limit(self):
        u"""验证client limit框输入大于上限值(testlink_ID:1315)"""
        log.debug("199")
        tmp = SSIDBusiness(self.driver)
        #页面client limit输入不合法数字，查看错误提示
        result = tmp.set_client_limit_error(1,data_wireless['limit_more_max'])
        self.assertTrue(result)

    #验证client limit输入范围合法性，填入字母(testlink_ID:1316)
    def test_200_letter_client_limit(self):
        u"""验证client limit输入范围合法性，填入字母(testlink_ID:1316)"""
        log.debug("200")
        tmp = SSIDBusiness(self.driver)
        #页面client limit输入字母，查看错误提示
        result = tmp.set_client_limit_error(1,data_wireless['limit_letter'])
        self.assertTrue(result)

    #只有一个master的情况下验证limit(testlink_ID:1320)
    def test_201_master_client_limit(self):
        u"""只有一个master的情况下验证limit(testlink_ID:1320)"""
        log.debug("201")
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的名称和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        #修改第一个ssid的client limit数量
        tmp.set_wireless_client_limit(1,data_wireless['client_limit'])
        #验证ap后台是否client limit的配置修改成功
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,master can not allow client connect ssid")

    #边界值验证，当limit client数量设置为0(testlink_ID:1323)
    def test_202_client_limit_0(self):
        u"""边界值验证，当limit client数量设置为0(testlink_ID:1323)"""
        log.debug("202")
        tmp = SSIDBusiness(self.driver)
        #页面client limit输入0，保存并且应用
        tmp.set_wireless_client_limit(1,data_wireless['limit_min'])
        #对比ssh后台和页面上设置的值是否相等
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['limit_min'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 0,wpa client can connect ssid")

    #验证portal client是否被统计在limit client数量里(testlink_ID:1324)
    def test_203_portalclient_limit(self):
        u"""验证portal client是否被统计在limit client数量里(testlink_ID:1324)"""
        log.debug("203")
        #开启ssid0的强制门户认证
        tmp = SSIDBusiness(self.driver)
        tmp1 = CPBusiness(self.driver)
        #修改第一个ssid的client limit数量,并点击勾选门户认证
        tmp.check_portal_clientlimit(1,data_wireless['client_limit'])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        portal_title,redirect_title,again_title,expiration_title = tmp1.\
            check_No_auth_portal(data_wireless['all_ssid'],
            data_wireless['short_wpa'],data_basic['wlan_pc'],
            data_basic['lan_pc'],1,"wpa")
        self.assertTrue(result)
        self.assertEqual(portal_title, "gatewayname Entry")
        self.assertIn(u"腾讯", redirect_title)
        print "portal client can access wifi when ssid set limit client, test pass!"

    #验证radius client要被统计在limit client数量里(testlink_ID:1325)
    def test_204_radius_client_limit(self):
        u"""验证radius client要被统计在limit client数量里(testlink_ID:1325)"""
        log.debug("204")
        #取消界面的勾选portal(上一条用例中勾选，此条用例需去除)
        tmp = SSIDBusiness(self.driver)
        #修改第一个ssid的client limit数量
        tmp.wifi_8021x_portal(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 =tmp.connect_8021x_AP(data_wireless['all_ssid'],data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,802.1x client can connect ssid")
        print "radius client can access wifi when ssid set limit client, test pass!"

    #open加密模式，验证limit client(testlink_ID:1327)
    def test_205_open_client_limit(self):
        u"""open加密模式，验证limit client(testlink_ID:1327)"""
        log.debug("205")
        tmp = SSIDBusiness(self.driver)
        tmp.wifi_None_encryption()
        result =tmp.connect_NONE_AP(data_wireless['all_ssid'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result,msg="limit client 3,open client can connect ssid")
        print "open client can access wifi when ssid set limit client, test pass!"

    #wep64位加密模式,验证limit client(testlink_ID:1328_01 wep64bit)
    def test_206_wep64_client_limit(self):
        u"""验证wep client(wep64bit)要被统计在limit client数量里(testlink_ID:1328_01)"""
        log.debug("206")
        tmp = SSIDBusiness(self.driver)
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        result =tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result,msg="limit client 3,wep client can connect ssid")
        print "wep client can access wifi when ssid set limit client, test pass!"

        #wep128位加密模式,验证limit client(testlink_ID:1328_02 wep128bit)
    def test_207_wep128_client_limit(self):
        u"""验证wep client(wep64bit)要被统计在limit client数量里(testlink_ID:1328_02)"""
        log.debug("207")
        tmp = SSIDBusiness(self.driver)
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        result =tmp.connect_WEP_AP(data_wireless['all_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result,msg="limit client 3,wep client can connect ssid")
        print "wep client can access wifi when ssid set limit client, test pass!"

    #wpa2加密模式,验证limit client(testlink_ID:1329)
    def test_208_wpa_client_limit(self):
        u"""验证wpa client要被统计在limit client数量里(testlink_ID:1329)"""
        log.debug("208")
        tmp = SSIDBusiness(self.driver)
        tmp.wifi_wpa_encryption(2,0,data_wireless["short_wpa"])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 =tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,client can connect ssid")
        print "wpa client can access wifi when ssid set limit client, test pass!"

    #ssid固定2.4G时,验证limit client(testlink_ID:1330)
    def test_209_2G_client_limit(self):
        u"""ssid固定2.4G时,验证limit client(testlink_ID:1330)"""
        log.debug("209")
        tmp = SSIDBusiness(self.driver)
        tmp.wifi_wpa_encryption(3,0,data_wireless["short_wpa"])
        tmp.change_AP_Freq("2.4GHz")
        #检查2.4G的wireless client限制情况
        result = tmp.check_ath_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0,data_wireless['client_limit'])
        #检查5G的wireless client限制情况
        result1 = tmp.check_ath_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result,msg='2.4G client limit fail')
        self.assertFalse(result1,msg='5G climit limit success')
        self.assertIn(data_wireless['all_ssid'],result2,msg="limit client 3,client can connect ssid")
        print "2.4G client can access wifi when ssid set limit client, test pass!"

    #ssid固定5G时,验证limit client(testlink_ID:1331)
    def test_210_5G_client_limit(self):
        u"""ssid固定5G时,验证limit client(testlink_ID:1331)"""
        log.debug("210")
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("5GHz")
        #检查2.4G的wireless client限制情况
        result = tmp.check_ath_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0,data_wireless['client_limit'])
        #检查5G的wireless client限制情况
        result1 = tmp.check_ath_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result,msg='5G client limit fail')
        self.assertFalse(result1,msg='2.4G climit limit success')
        self.assertIn(data_wireless['all_ssid'],result2,msg="limit client 3,client can connect ssid")
        print "2.4G client can access wifi when ssid set limit client, test pass!"

    #ssid设置双频时,验证limit client(testlink_ID:1332,1334)
    def test_211_dual_client_limit(self):
        u"""ssid设置双频时,验证limit client(testlink_ID:1332,1334)"""
        log.debug("211")
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("Dual-Band")
        #检查2.4G的wireless client限制情况
        result = tmp.check_ath_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0,data_wireless['client_limit'])
        #检查5G的wireless client限制情况
        result1 = tmp.check_ath_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result,msg='2.4G client limit fail')
        self.assertTrue(result1,msg='5G climit limit fail')
        self.assertIn(data_wireless['all_ssid'],result2,msg="limit client 3,client can connect ssid")
        print "dual-band client can access wifi when ssid set limit client, test pass!"

    #隐藏ssid时,验证limit client(testlink_ID:1336)
    def test_212_hide_ssid_client_limit(self):
        u"""隐藏ssid时,验证limit client(testlink_ID:1336)"""
        log.debug("212")
        tmp = SSIDBusiness(self.driver)
        #隐藏第一个ssid
        tmp.set_hide_ssid()
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 = tmp.connect_WPA_hiddenssid_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,client can connect ssid")
        #取消隐藏ssid
        tmp.set_hide_ssid()
        print "hide ssid, client can access wifi when ssid set limit client, test pass!"

    #limit whitelist,验证limit client(testlink_ID:1339)
    def test_213_whitelist_ssid_client_limit(self):
        u"""limit whitelist,验证limit client(testlink_ID:1339)"""
        log.debug("213")
        tmp = SSIDBusiness(self.driver)
        #添加一个access list,输入一个mac地址,并在ssid中选择这个access list
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp1 = ClientAccessBusiness(self.driver)
        tmp1.add_accesslist_onemac(mac)
        #勾选白名单
        tmp.wifi_whitelist()
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,client can connect ssid")
        print "set whitelist, client can access wifi when ssid set limit client, test pass!"

    #offline client,验证limit client(testlink_ID:1341)
    def test_214_offline_client_limit(self):
        u"""offline client,验证limit client(testlink_ID:1341)"""
        log.debug("214")
        tmp = SSIDBusiness(self.driver)
        #禁用上一个用例中的勾选白名单
        tmp.disable_macfilter(1)
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        tmp.disconnect_ap()
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,client can connect ssid")
        print "connect then offline, client can access wifi when ssid set limit client, test pass!"

        #client反复online,offline,验证client不会被统计多次(testlink_ID:1342)
    def test_215_online_offline_client_limit(self):
        u"""client反复online,offline,验证client不会被统计多次(testlink_ID:1342)"""
        log.debug("215")
        tmp = SSIDBusiness(self.driver)
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        i = 1
        #客户端连接断开wifi3次
        while(i<4):
            tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
            #tmp.disconnect_ap()
            i+=1
        #客户端第四次连接wifi
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #tmp.disconnect_ap()
        #客户端第五次连接wifi
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,wep client can connect ssid")
        self.assertIn(data_wireless['all_ssid'],result2,msg="limit client 3,wep client can connect ssid")
        print "connect then offline, client can access wifi when ssid set limit client, test pass!"

    #client在长时间offline后,而limit未满额,再次成功接入(testlink_ID:1343)
    def test_216_longtime_offline_client_limit(self):
        u"""client在长时间offline后,而limit未满额,再次成功接入(testlink_ID:1343)"""
        log.debug("216")
        tmp = SSIDBusiness(self.driver)
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        tmp.disconnect_ap()
        #客户端断开五分钟后重连
        time.sleep(300)
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,client can connect ssid")
        print "long time offline, client can access wifi when ssid set limit client, test pass!"

    #client ip发生变化，该client不会被再次统计(testlink_ID:1345)
    def test_217_client_ip_limit(self):
        u"""client ip发生变化，该client不会被再次统计(testlink_ID:1345)"""
        log.debug("217")
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("5GHz")
        tmp.set_wireless_client_limit(1,data_wireless['client_limit_test'])
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit_test'])
        #禁用有线网卡
        tmp.networkcard_disable()
        #给无线网卡设置固定ip
        tmp.set_client_ip(data_basic['client_ip'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
         #取消给无线网卡固定的ip
        tmp.remove_client_ip()
        #启用有线网卡
        tmp.networkcard_enable()
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="limit client 3,client can connect ssid")
        print "set client ip, client can access wifi when ssid set limit client, test pass!"

    #多次修改client limit配置,确认配置是否能生效(testlink_ID:1346)
    def test_218_edit_client_limit(self):
        u"""多次修改client limit配置,确认配置是否能生效(testlink_ID:1346)"""
        log.debug("218")
        tmp = SSIDBusiness(self.driver)
        #修改上一条用例中ap频率为双频
        tmp.change_AP_Freq("Dual-Band")
        tmp.set_wireless_client_limit(1,data_wireless['client_limit'])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        tmp.set_wireless_client_limit(1,data_wireless['client_limit_test'])
        result1 = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit_test'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertIn(data_wireless['all_ssid'],result2,msg="edit limit client,client can connect ssid")
        print "edit client limit success, client can access wifi when ssid set limit client, test pass!"

    #配对一个slave ap,验证ssid0中master和slave的wireless client是否成功(testlink_ID:1349)
    def test_219_master_slave_client_limit(self):
        u"""配对一个slave ap,验证ssid0中master和slave的wireless client是否成功(testlink_ID:1349)"""
        log.debug("219")
        tmp = SSIDBusiness(self.driver)
        tmp1 = APSBusiness(self.driver)
        #搜索并配对一个slave ap
        tmp1.search_pair_special_AP(data_AP['slave:mac1'])
        #设置ssid的客户端限制数量为3
        tmp.set_wireless_client_limit(1,data_wireless['client_limit'])
        #检查master ap后台的客户端限制数量是否为3
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        #检查slave ap后台的客户端数量限制是否为3
        result1 = tmp.check_client_limit(data_basic['slave_ip1'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertIn(data_wireless['all_ssid'],result2,msg="limit client 3,client can connect ssid")

    #在ssid0的设备管理中,移除master ap,仅仅验证只有slave ap时，配置是否生效(testlink_ID:1321)
    def test_220_only_slave_client_limit(self):
        u"""在ssid0的设备管理中,移除master ap,仅仅验证只有slave ap时，配置是否生效(testlink_ID:1321)"""
        log.debug("220")
        tmp = SSIDBusiness(self.driver)
        tmp.del_all_ap()
        tmp.add_special_ap(1,data_AP['slave:mac1'])
        tmp.set_wireless_client_limit(1,data_wireless['client_limit_test'])
        result = tmp.check_client_limit(data_basic['slave_ip1'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit_test'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #验证进入master ap后台输入iwconfig
        result2 = tmp.ssh_iwconfig(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="slave ap limit success,client can connect ssid")
        #验证master ap的iwconfig中无ssid0的名称
        self.assertNotIn(data_wireless['all_ssid'],result2,msg=u'master ap 从ssid0移除失败')

    #在ssid0的设备管理中,移除slave ap,仅仅验证只有master ap时，配置是否生效(testlink_ID:1320)
    def test_221_only_master_client_limit(self):
        u"""在ssid0的设备管理中,移除slave ap,仅仅验证只有master ap时，配置是否生效(testlink_ID:1320)"""
        log.debug("221")
        tmp = SSIDBusiness(self.driver)
        tmp.del_all_ap()
        tmp.add_special_ap(1,data_AP['master:mac'])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit_test'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #验证进入slave ap后台输入iwconfig
        result2 = tmp.ssh_iwconfig(data_basic['slave_ip1'],data_login["all"],data_basic['sshUser'])
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result1,msg="slave ap limit success,client can connect ssid")
        #验证slave ap的iwconfig中无ssid0的名称
        self.assertNotIn(data_wireless['all_ssid'],result2,msg=u'slave ap 从ssid0移除失败')

    #新建一个ssid1,将slave加入ssid1,将ssid1设置与ssid0不同的值，确认配置同步，相当于额外ssid(testlink_ID:1337，1318)
    def test_222_add_ssid1_client_limit(self):
        u"""在ssid1加入slave,客户端在ssid0和ssid1中切换(testlink_ID:1337)"""
        log.debug("222")
        tmp = SSIDBusiness(self.driver)
        tmp.new_ssid(data_wireless['digital_letter_ssid'],data_wireless["short_wpa"])
        tmp.add_special_ap(2,data_AP['slave:mac1'])
        tmp.set_wireless_client_limit(2,data_wireless['client_limit'])
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['client_limit_test'])
        result1 = tmp.check_client_limit(data_basic['slave_ip1'],data_login["all"],data_basic['sshUser'],2,data_wireless['client_limit'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        result3 = tmp.connect_WPA_AP(data_wireless['digital_letter_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #验证ssid0中master ap配置同步，并且可以连接该wifi
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result2,msg="master ap limit success,client can connect ssid")
        #验证ssid1中slave ap配置同步，并且可以连接该wifi
        self.assertTrue(result1)
        self.assertIn(data_wireless['digital_letter_ssid'],result3,msg="slave ap limit success,client can connect ssid")

    #将master和slave都加入ssid1,检查master和slave的配置并且让客户端连接到ssid1
    def test_223_ssid1_client_limit(self):
        u"""在ssid1加入slave,客户端在ssid0和ssid1中切换(testlink_ID:1337)"""
        log.debug("223")
        tmp = SSIDBusiness(self.driver)
        tmp.add_all_ap()
        result = tmp.check_client_limit(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,data_wireless['client_limit'])
        result1 = tmp.check_client_limit(data_basic['slave_ip1'],data_login["all"],data_basic['sshUser'],2,data_wireless['client_limit'])
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        result3 = tmp.connect_WPA_AP(data_wireless['digital_letter_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #验证ssid1中master ap配置同步，并且可以连接该wifi
        self.assertTrue(result)
        self.assertIn(data_wireless['all_ssid'],result2,msg="master ap limit success,client can connect ssid")
        #验证ssid1中slave ap配置同步，并且可以连接该wifi
        self.assertTrue(result1)
        self.assertIn(data_wireless['digital_letter_ssid'],result3,msg="slave ap limit success,client can connect ssid")

    ################以下是band设置的用例##################
#作者:蒋甜
#时间:2018年3月22日
    #在页面上把AP恢复出厂设置
    def test_224_set_factory_reset(self):
        u"""在页面上把AP恢复出厂设置"""
        log.debug("224")
        #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
        # Lg = LoginBusiness(self.driver)
        # Lg.login_again()
        tmp = APSBusiness(self.driver)
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #开启mesh后配置5个相同vlan下的dual ssid
    def test_225_mesh_5_ssid(self):
        u"""开启mesh后配置5个相同vlan下的dual ssid(testlink_ID:852)"""
        log.debug("225")
        tmp = SSIDBusiness(self.driver)
        #修改默认ssid的帐号和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        tmp.new_n_ssid(2,5,data_wireless['all_ssid'],data_wireless['short_wpa'])
        result = tmp.check_have_n_ssid(5)
        self.assertTrue(result)

    #开启mesh后配置6个相同vlan下的dual ssid
    def test_226_mesh_6_ssid(self):
        u"""开启mesh后配置6个相同vlan下的dual ssid(testlink_ID:853)--bug107982"""
        log.debug("226")
        tmp = SSIDBusiness(self.driver)
        result = tmp.check_new_ssid_error()
        tmp.del_all_NG()
        self.assertTrue(result)

    #设置默认ssid的频段为2.4G
    def test_227_set_ssid_band_2G(self):
        u"""设置ssid的band为2.4G(testlink_ID:826)"""
        log.debug("227")
        #切换ssid的2G频段
        tmp = SSIDBusiness(self.driver)
        #先关闭mesh功能
        tmp1 = MeshBusiness(self.driver)
        tmp1.close_mesh()
        tmp.change_AP_Freq("2.4GHz")
        #ssh检查band是否设置成功
        result = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,2)
        result1 = tmp.ssh_iwconfig_ath_Fre(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0)
        result2 = tmp.ssh_iwconfig_ath(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1)
        self.assertTrue(result)
        self.assertEqual(result1,2)
        self.assertNotIn(data_wireless['all_ssid'],result2)

    #设置默认ssid的频段为2.4G后,扫描ssid
    def test_228_scan_ssid_band_2G(self):
        u"""设置ssid的band为2.4G,扫描该ssid(testlink_ID:827)"""
        log.debug("228")
        tmp = SSIDBusiness(self.driver)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0,data_wireless['all_ssid'])
        self.assertTrue(result)

    #设置默认ssid的频段为2.4G后，连接ssid
    def test_229_connect_ssid_band_2G(self):
        u"""设置ssid的band为2.4G,连接该ssid(testlink_ID:828)"""
        log.debug("229")
        tmp = SSIDBusiness(self.driver)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result)

    #设置默认ssid的频段为5G
    def test_230_set_ssid_band_5G(self):
        u"""设置ssid的band为5G(testlink_ID:829)"""
        log.debug("230")
        #切换ssid的5G频段
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("5GHz")
        #ssh检查band是否设置成功
        result = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,5)
        result1 = tmp.ssh_iwconfig_ath_Fre(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0)
        result2 = tmp.ssh_iwconfig_ath(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1)
        self.assertTrue(result)
        self.assertEqual(5,result1)
        self.assertNotIn(data_wireless['all_ssid'],result2)

    #设置默认ssid的频段为5G后,扫描ssid
    def test_231_scan_ssid_band_5G(self):
        u"""设置ssid的band为5G,扫描该ssid(testlink_ID:830)"""
        log.debug("231")
        tmp = SSIDBusiness(self.driver)
        result = tmp.ssid_scan_result(data_wireless['all_ssid'],data_basic['wlan_pc'])
        self.assertTrue(result)

    #设置默认ssid的频段为5G后，连接ssid
    def test_232_connect_ssid_band_5G(self):
        u"""设置ssid的band为5G,连接该ssid(testlink_ID:831)"""
        log.debug("232")
        tmp = SSIDBusiness(self.driver)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result)

    #设置默认ssid的频段为双频
    def test_233_set_ssid_band_dual(self):
        u"""设置ssid的band为双频(testlink_ID:832)"""
        log.debug("233")
        #切换ssid的双频段
        tmp = SSIDBusiness(self.driver)
        tmp.change_AP_Freq("Dual-Band")
        #ssh检查band是否设置成功,分别判断2.4G和5G的频段是否在配置中
        result = tmp.ssh_iwconfig_ath(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0)
        result1 = tmp.ssh_iwconfig_ath(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1)
        self.assertIn(data_wireless['all_ssid'],result)
        self.assertIn(data_wireless['all_ssid'],result1)

    #扫描开启vlan的双频ssid
    def test_234_scan_vlan_ssid_band_dual(self):
        u"""扫描开启vlan的双频ssid(testlink_ID:833)"""
        log.debug("234")
        #新建一个带vlan的ssid
        tmp = SSIDBusiness(self.driver)
        tmp.new_vlan_ssid(data_wireless['all_ssid']+"2",data_wireless['short_wpa'],2)
        tmp.n_add_all_ap(2)
        tmp1 = NGBusiness(self.driver)
        #在7000中新建一个ssid,设置vlan为2,开启DHCP
        tmp1.mixed_7000_new_NG()
        #在iwconfig中判断接口
        result = tmp.ssh_iwconfig_ath(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2)
        result1 = tmp.ssh_iwconfig_ath(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3)
        print result
        print result1
        self.assertIn(data_wireless['all_ssid']+"2",result)
        self.assertIn(data_wireless['all_ssid']+"2",result1)

    #连接开启vlan的双频ssid
    def test_235_connect_vlan_ssid_band_dual(self):
        u"""连接开启vlan的双频ssid(testlink_ID:834)"""
        log.debug("235")
        tmp = SSIDBusiness(self.driver)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid']+"2",result)

    #多个ssid配置2.4G
    def test_236_set_many_ssid_band_2G(self):
        u"""多个ssid配置2.4G(testlink_ID:835)"""
        log.debug("236")
        tmp = SSIDBusiness(self.driver)
        tmp.new_ssid(data_wireless['all_ssid']+"3",data_wireless['short_wpa'])
        tmp.n_add_all_ap(3)
        tmp.change_n_ssid_Freq(1,3,"2.4GHz")
        result = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,2)
        result1 = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3,2)
        self.assertTrue(result)
        self.assertTrue(result1)

     #多个ssid配置5G
    def test_237_set_many_ssid_band_5G(self):
        u"""多个ssid配置5G(testlink_ID:836)"""
        log.debug("237")
        tmp = SSIDBusiness(self.driver)
        tmp.change_n_ssid_Freq(1,3,"5GHz")
        result = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,5)
        result1 = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3,5)
        self.assertTrue(result)
        self.assertTrue(result1)

    #多个ssid配置双频
    def test_238_set_many_ssid_band_dual(self):
        u"""多个ssid配置双频(testlink_ID:837)"""
        log.debug("238")
        tmp = SSIDBusiness(self.driver)
        tmp.change_n_ssid_Freq(1,3,"Dual-Band")
        result1 = tmp.ssh_iwconfig_ath_Fre(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3)
        result2 = tmp.ssh_iwconfig_ath_Fre(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],5)
        self.assertEqual(5,result1)
        self.assertEqual(5,result2)

      #配置相同vlan下的多个ssid
    def test_239_set_many_same_vlan_ssid(self):
        u"""配置相同vlan下的多个ssid(testlink_ID:838)"""
        log.debug("239")
        tmp = SSIDBusiness(self.driver)
        #配置第一个ssid个第三个ssid的为2
        tmp.enable_vlan_ssid(1,2)
        tmp.enable_vlan_ssid(3,2)
        tmp.change_n_AP_Freq(1,"2.4GHz")
        tmp.change_n_AP_Freq(2,"5GHz")
        result = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,2)
        result1 = tmp.check_ssid_band(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,5)
        result2 = tmp.ssh_iwconfig_ath_Fre(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3)
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertEqual(5,result2)

    #扫描配置相同vlan下的多个ssid
    def test_240_scan_many_same_vlan_ssid(self):
        u"""扫描配置相同vlan下的多个ssid(testlink_ID:839)"""
        log.debug("240")
        tmp = SSIDBusiness(self.driver)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        #判断第3和第4个ath口是不时发射频率分别为2.4G和5G，且SSID的名称为第三个ssid的名称
        result1 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,data_wireless['all_ssid']+"3")
        result2 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3,data_wireless['all_ssid']+"3")
        self.assertEqual(5,result)
        self.assertEqual(2,result1)
        self.assertEqual(5,result2)

    #将默认的ssid的频段从2.4G修改成5G,并扫描此SSID
    def test_241_scan_2G_tran_5G(self):
        u"""扫描2.4G修改成5G后的ssid(testlink_ID:840)"""
        log.debug("241")
        tmp = SSIDBusiness(self.driver)
        tmp.change_n_AP_Freq(1,"5GHz")
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0,data_wireless['all_ssid'])
        self.assertEqual(5,result)

    #将默认的ssid的频段从2.4G修改成5G
    def test_242_connect_2G_tran_5G(self):
        u"""连接2.4G修改成5G后的ssid(testlink_ID:841)"""
        log.debug("242")
        tmp = SSIDBusiness(self.driver)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid'],result)

    #将第二个ssid的频段从5G修改成2.4G
    def test_243_scan_5G_tran_2G(self):
        u"""扫描5G修改成2.4G后的ssid(testlink_ID:842)"""
        log.debug("243")
        tmp = SSIDBusiness(self.driver)
        tmp.change_n_AP_Freq(2,"2.4GHz")
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        self.assertEqual(2,result)

     #将第二个ssid的频段从5G修改成2.4G
    def test_244_connect_5G_tran_2G(self):
        u"""连接5G修改成2.4G后的ssid(testlink_ID:843)"""
        log.debug("244")
        tmp = SSIDBusiness(self.driver)
        result = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertIn(data_wireless['all_ssid']+"2",result)

    #关闭ssid的wifi扫描
    def test_245_close_ssid_scan(self):
        u"""关闭ssid的wifi扫描(testlink_ID:844)"""
        log.debug("245")
        tmp = SSIDBusiness(self.driver)
        tmp.en_dis_nssid(2)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        self.assertFalse(result)

    #关闭再开启ssid的wifi扫描
    def test_246_open_ssid_scan(self):
        u"""关闭再开启ssid的wifi扫描(testlink_ID:845)"""
        log.debug("246")
        tmp = SSIDBusiness(self.driver)
        tmp.en_dis_nssid(2)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        self.assertEqual(2,result)

    #自动信道下扫描2.4GSSID
    def test_247_auto_channel_ssid_scan_2G(self):
        u"""自动信道下扫描2.4G(testlink_ID:846)"""
        log.debug("247")
        tmp = SSIDBusiness(self.driver)
        #关闭第一个到第三个ssid的vlan
        tmp.disable_vlan_ssid(1)
        tmp.disable_vlan_ssid(2)
        tmp.disable_vlan_ssid(3)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertEqual(2,result)
        self.assertIn(data_wireless['all_ssid']+"2",result1)

    # 固定信道下扫描2.4GSSID(将信道固定为3)
    def test_248_set_channel_ssid_scan_2G(self):
        u"""固定信道下扫描2.4GSSID(testlink_ID:847_01)"""
        log.debug("248")
        tmp1 = APSBusiness(self.driver)
        #设置master的信道,并用无线网卡连接
        result = tmp1.check_2g4_channel("3",data_wireless['all_ssid']+"2",data_wireless['short_wpa'],data_basic['wlan_pc'])
        # self.assertEqual(2422,result)

    #固定信道下扫描2.4GSSID(将信道固定为8)
    def test_249_set_channel_ssid_scan_2G(self):
        u"""固定信道下扫描2.4GSSID(testlink_ID:847_02)"""
        log.debug("249")
        tmp1 = APSBusiness(self.driver)
        #设置master的信道,并用无线网卡连接
        result = tmp1.check_2g4_channel("8",data_wireless['all_ssid']+"2",data_wireless['short_wpa'],data_basic['wlan_pc'])
        # self.assertEqual(2447,result)

    #自动信道下扫描5G
    def test_250_auto_channel_ssid_scan5G(self):
        u"""自动信道下扫描5G(testlink_ID:848)"""
        log.debug("250")
        tmp = SSIDBusiness(self.driver)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],0,data_wireless['all_ssid'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        self.assertEqual(5,result)
        self.assertIn(data_wireless['all_ssid'],result1)

    #固定信道下扫描5GSSID(将信道固定为44)
    def test_251_set_channel_ssid_scan_5G(self):
        u"""固定信道下扫描5GSSID(testlink_ID:849_01)"""
        log.debug("251")
        tmp1 = APSBusiness(self.driver)
        #设置master的信道,并用无线网卡连接
        result = tmp1.check_5g_channel("44",data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertEqual(5220,result)

    #固定信道下扫描5GSSID(将信道固定为161)
    def test_252_set_channel_ssid_scan_5G(self):
        u"""固定信道下扫描5GSSID(testlink_ID:849_02)"""
        log.debug("252")
        tmp1 = APSBusiness(self.driver)
        #设置master的信道,并用无线网卡连接
        result = tmp1.check_5g_channel("161",data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.assertEqual(5805,result)

    #ap作为master扫描SSID(testlink_ID:850)
    def test_253_scan_master_ssid(self):
        u"""ap作为master扫描SSID(testlink_ID:850)"""
        log.debug("253")
        tmp = SSIDBusiness(self.driver)
        tmp1 = APSBusiness(self.driver)
        #设置master的信道
        tmp1.set_master_ap_2g4_channel("0")
        tmp1.set_master_ap_5g_channel("0")
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        #判断第3和第4个ath口是不时发射频率分别为2.4G和5G，且SSID的名称为第三个ssid的名称
        result1 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,data_wireless['all_ssid']+"3")
        result2 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3,data_wireless['all_ssid']+"3")
        self.assertEqual(2,result)
        self.assertEqual(2,result1)
        self.assertEqual(5,result2)

    #master接入slave后，扫描slave发出的SSID
    def test_254_scan_slave_ssid(self):
        u"""master接入slave后，扫描slave发出的SSID(testlink_ID:851)"""
        log.debug("254")
        tmp = SSIDBusiness(self.driver)
        tmp1 = APSBusiness(self.driver)
        #配对slave ap
        tmp1.check_search_pair_AP(data_basic['DUT_ip'],\
                data_basic['sshUser'],data_login['all'],data_AP["slave:mac1"],
                data_AP["slave:mac2"])
         #将新配对的slave ap加入到ssid中
        tmp.n_add_all_ap(1)
        tmp.n_add_all_ap(2)
        tmp.n_add_all_ap(3)
        time.sleep(120)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['slave_ip1'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        #判断第3和第4个ath口是不时发射频率分别为2.4G和5G，且SSID的名称为第三个ssid的名称
        result1 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['slave_ip2'],data_login["all"],data_basic['sshUser'],2,data_wireless['all_ssid']+"3")
        result2 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['slave_ip2'],data_login["all"],data_basic['sshUser'],3,data_wireless['all_ssid']+"3")
        #解除配对
        tmp1.unpair_last_slave_ap(2)
        # tmp.del_all_NG()
        self.assertEqual(2,result)
        self.assertEqual(2,result1)
        self.assertEqual(5,result2)

    #断电重启,检查band配置是否发生改变
    def test_255_reboot_band(self):
        u"""断电重启,检查band配置是否发生改变(testlink_ID:854)"""
        log.debug("255")
        tmp = SSIDBusiness(self.driver)
        tmp1 = LoginBusiness(self.driver)
        tmp.reboot_router(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        time.sleep(300)
        result = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],1,data_wireless['all_ssid']+"2")
        #判断第3和第4个ath口是不时发射频率分别为2.4G和5G，且SSID的名称为第三个ssid的名称
        result1 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],2,data_wireless['all_ssid']+"3")
        result2 = tmp.ssh_iwconfig_ath_Fre_ssid(data_basic['DUT_ip'],data_login["all"],data_basic['sshUser'],3,data_wireless['all_ssid']+"3")
        tmp1.refresh_login_ap()
        tmp.del_all_NG()
        #删除7000上的group1
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_del_NG()
        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        # rsyslog服务器完成工作
        tmp.finish_rsyslog("SSID")
        self.assertEqual(2,result)
        self.assertEqual(2,result1)
        self.assertEqual(5,result2)


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
