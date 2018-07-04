#coding=utf-8
#作者：曾祥卫
#时间：2017.03.15
#描述：用例集，调用aps_business

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from access_points.aps_business import APSBusiness
from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from network_group.add_ssid.addssid_business import AddSSIDBusiness
from clients.clients_business import ClientsBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from system_settings.maintenance.access.access_business import AccessBusiness
from system_settings.maintenance.basic.basic_business import BasicBusiness
from overview.overview_business import OVBusiness
from data import data
from connect.ssh import SSH
from navbar.navbar_business import NavbarBusiness
from data.logfile import Log

log = Log("accesspoint")

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
data_Client = data.data_Client()


class TestAccessPoints(unittest.TestCase):
    u"""测试接入点的用例集(runtime:8h30m)"""
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

    #搜索AP并判断，是否正确
    def test_002_search_AP(self):
        u"""测试搜索AP并判断是否正确"""
        log.debug("002")
        search = APSBusiness(self.driver)
        result = search.search_AP(data_AP["slave:mac1"],data_AP["slave:mac2"])
        assert result,"search AP and check ok,test fail!"
        print "search AP and check ok,test pass!"

    #搜索AP并配对
    def test_003_search_pair_AP(self):
        u"""测试搜索AP并配对"""
        log.debug("003")
        search = APSBusiness(self.driver)
        result = search.check_search_pair_AP(data_basic['DUT_ip'],\
                data_basic['sshUser'],data_login['all'],data_AP["slave:mac1"],
                data_AP["slave:mac2"])
        #解除slave ap1的配对
        search.unpair_special_slave_AP(data_AP["slave:mac1"])
        assert result,"search AP and pair,test fail!"
        print "search AP and pair,test pass!"

    #添加slave ap到新建的ssid
    def test_004_slave_add_NG(self):
        u"""测试添加slave ap到新建的ssid"""
        log.debug("004")
        add = APSBusiness(self.driver)
        result = add.slave_add_NG(data_basic['DUT_ip'],\
            data_basic['sshUser'],data_login['all'],2,data_AP["slave:mac2"],\
            data_ng["NG2_ssid"],data_wireless["short_wpa"])
        assert result,"add slave AP to the new ssid,test fail!"
        print "add slave AP to the new ssid,test pass!"

    #使用无线网卡能够连接上新建的ssid,确定slave ap已经切换到新建的ssid,并正常使用
    def test_005_connect_slave_ap(self):
        u"""使用无线网卡能够连接上新建的ssid,确定slave ap已经切换到新建的ssid"""
        log.debug("005")
        tmp = APSBusiness(self.driver)
        result = tmp.connect_WPA_AP(data_ng["NG2_ssid"],\
                        data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert data_ng["NG2_ssid"] in result,"using wireless card to connect the new ssid,test fail!"
        print "using wireless card can connect the new ssid,test pass!"

    #使用无线网卡能够连接上group0的网络组，并正常使用
    def test_006_connect_master_ap(self):
        u"""使用无线网卡能够连接上group0的网络组，并正常使用"""
        log.debug("006")
        tmp = APSBusiness(self.driver)
        result = tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic["wlan_pc"])
        #禁用启用有线网卡，以便无线网卡能够在ap的client页面显示在线
        time.sleep(120)
        tmp.dhcp_release_wlan(data_basic["wlan_pc"])
        assert data_wireless['all_ssid'] in result,"using wireless card to connect the ssid of group0,test fail!"
        print "using wireless card to connect the ssid of group0,test pass!"


    #基本状态信息合法性和准确性检查(testlink_ID:237)
    def test_007_check_status(self):
        u"""基本状态信息合法性和准确性检查(testlink_ID:237)"""
        log.debug("007")
        tmp = APSBusiness(self.driver)
        result = tmp.step_002_check_status(data_basic['DUT_ip'],\
            data_basic['sshUser'],data_login['all'],
            data_AP["master:mac"],data_basic['DUT_ip'])
        assert result == [True,True,True],"check AP status,test fail!"
        print "check AP status,test pass!"

    #MAC信息检查(testlink_ID:241)
    def test_008_client_mac(self):
        u"""MAC信息检查(testlink_ID:241)"""
        log.debug("008")
        tmp = APSBusiness(self.driver)
        result = tmp.check_client_mac(data_AP["master:mac"],data_basic['wlan_pc'])
        print result
        assert result,"check client mac,test fail!"
        print "check client mac,test pass!"

    #Hostname 信息检查(testlink_ID:242)
    def test_009_client_name(self):
        u"""Hostname 信息检查(testlink_ID:242)"""
        log.debug("009")
        name = data_Client['letter_digital_name']
        tmp = APSBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.check_client_name(wlan_mac,name,data_AP["master:mac"])
        print result
        tmp.disconnect_ap()
        assert result,"check changing host name,test fail!"
        print "check changing host name,test pass!"

    # #Device Name 字符配置验证(testlink_ID:246)
    # def test_010_device_name(self):
    #     u"""Device Name 字符配置验证(testlink_ID:246)"""
    #     names = [data_AP['letter_device_name'],data_AP['digital_device_name'],data_AP['all_device_name']]
    #     tmp = APSBusiness(self.driver)
    #     result = tmp.check_device_names(1,names)
    #     print result
    #     assert result == [True,True,True],"check device name,test fail!"
    #     print "check device name,test pass!"
    #
    # #Slave Device Name验证(testlink_ID:247)
    # def test_011_slave_device_name(self):
    #     u"""Slave Device Name验证(testlink_ID:247)"""
    #     names = [data_AP['letter_device_name'],data_AP['digital_device_name'],data_AP['all_device_name']]
    #     tmp = APSBusiness(self.driver)
    #     result = tmp.check_device_names(2,names)
    #     print result
    #     assert result == [True,True,True],"check slave ap device name,test fail!"
    #     print "check slave ap device name,test pass!"
    #
    # #Device Name 在各个页面的生效情况(testlink_ID:248)
    # def test_012_check_all_device_name(self):
    #     u"""Device Name 在各个页面的生效情况(testlink_ID:248)"""
    #     tmp = APSBusiness(self.driver)
    #     result = tmp.check_all_device_name(data_wireless['all_ssid'],\
    #                     data_wireless["short_wpa"],data_basic["wlan_pc"],data_AP['all_device_name'])
    #     print result
    #     assert result == [True,True,True],"check device name in all webpages,test fail!"
    #     print "check device name in all webpages,test pass!"

    #勾选Fixed IP(testlink_ID:249_1)
    def test_013_check_choose_fixed_ip(self):
        u"""勾选Fixed IP(testlink_ID:249_1)"""
        log.debug("013")
        tmp = APSBusiness(self.driver)
        ip,result = tmp.check_choose_fixed_ip(data_AP["master:mac"])
        assert ip == data_basic["DUT_ip"] and result ==[True,True,True],"check choose fixed ip,test fail!"
        print "check choose fixed ip,test pass!"

    #取消勾选Fixed IP(testlink_ID:250_1)
    def test_014_check_cancel_fixed_ip(self):
        u"""取消勾选Fixed IP(testlink_ID:250_1)"""
        log.debug("014")
        tmp = APSBusiness(self.driver)
        ip,result = tmp.check_cancel_fixed_ip(data_AP["master:mac"])
        assert result ==[False,False,False],"check cancel fixed ip,test fail!"
        print "check cancel fixed ip,test pass!"

    #输入合法性检测(testlink_ID:251)
    def test_015_check_ip_legal(self):
        u"""输入合法性检测(testlink_ID:251)"""
        log.debug("015")
        tmp = APSBusiness(self.driver)
        result1,result2 = tmp.check_ip_legal(data_AP["master:mac"],data_AP['validity_fixed_ip'],\
                    data_AP['validity_fixed_netmask'],data_AP['validity_fixed_ip'])
        assert result1 and result2,"check cancel fixed ip validity,test fail!"
        print "check cancel fixed ip validity,test pass!"

    #配置完整性检测(testlink_ID:252)
    def test_016_check_ip_integrity(self):
        u"""配置完整性检测(testlink_ID:252)"""
        log.debug("016")
        tmp = APSBusiness(self.driver)
        result1,result2 = tmp.check_ip_legal(data_AP["master:mac"],data_AP['fixed_ip'],\
                    data_AP['fixed_netmask']," ")
        assert result1 and result2,"check cancel fixed ip integrity,test fail!"
        print "check cancel fixed ip integrity,test pass!"


    #指定固定ip后slave ap的ip是否正确(testlink_ID:249_2)
    def test_017_set_slave_fixed_ip(self):
        u"""指定固定ip后slave ap的ip是否正确(testlink_ID:249_2)"""
        log.debug("017")
        tmp = APSBusiness(self.driver)
        result = tmp.set_ap_fixed_ip(data_AP["slave:mac2"],data_AP['fixed_ip'],\
                    data_AP['fixed_netmask'],data_basic['7000_ip'])
        assert result,"test set slave ap fixed ip,test fail!"
        print "test set slave ap fixed ip,test pass!"

    #save and apply,CLI命令检查(testlink_ID:253)
    def test_018_check_ip_validity(self):
        u"""save and apply,CLI命令检查(testlink_ID:253)"""
        log.debug("018")
        tmp = APSBusiness(self.driver)
        result = tmp.check_AP_config(data_AP['fixed_ip'],data_basic['sshUser'],\
                                     data_login['all'])
        assert "option static '1'" in result,"test set ip validity,test fail!"
        print "test set ip validity,test pass!"

    #解除固定ip后的slave ap的ip是否恢复(testlink_ID:250_2)
    def test_019_cancel_slave_fixed_ip(self):
        u"""解除固定ip后的slave ap的ip是否恢复(testlink_ID:250_2)"""
        log.debug("019")
        tmp = APSBusiness(self.driver)
        result = tmp.cancel_ap_fixed_ip(data_AP["slave:mac2"],data_basic['slave_ip2'])
        assert result,"test cancel slave ap fixed ip,test fail!"
        print "test cancel slave ap fixed ip,test pass!"

    #取消勾选Fixed IP测试(testlink_ID:250_3)
    def test_020_cancel_ip_validity(self):
        u"""取消勾选Fixed IP测试(testlink_ID:250_3)"""
        log.debug("020")
        tmp = APSBusiness(self.driver)
        result = tmp.check_AP_config(data_basic['slave_ip2'],data_basic['sshUser'],\
                                     data_login['all'])
        assert "option static '0'" in result,"test set ip validity,test fail!"
        print "test set ip validity,test pass!"

    #解除最后一个slave AP的配对
    def test_021_unpair_last_ap(self):
        u"""测试解除最后一个slave AP的配对"""
        log.debug("021")
        unpair = APSBusiness(self.driver)
        result = unpair.step_001_unpair_last(data_basic['DUT_ip'],\
            data_basic['sshUser'],data_login['all'],data_AP["slave:mac2"])
        assert result,"unpair the last ap,test fail!"
        print "unpair the last ap,test pass!"

    #Dual-Band(testlink_ID:263)
    def test_022_check_Dual_Band(self):
        u"""Dual-Band(testlink_ID:263)"""
        log.debug("022")
        tmp = APSBusiness(self.driver)
        #使用无线网卡连接上AP后，取出该AP的频率值
        result1 = tmp.connected_AP_Freq(data_wireless['all_ssid'], \
                    data_wireless["short_wpa"],data_basic["wlan_pc"])
        #确认有两个无线接口
        tmp1 = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath0 | grep ESSID")
        result3 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath1 | grep ESSID")
        #切换2.4G频段
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_AP_Freq("2.4GHz")
        assert (result1 > 2400) and (data_wireless['all_ssid'] in result2) \
            and (data_wireless['all_ssid'] in result3),"test set AP Dual-Band,fail!"
        print "test set AP Dual-Band,pass!"

    #2.4G(testlink_ID:261)
    def test_023_check_2g4(self):
        u"""2.4G(testlink_ID:261)"""
        log.debug("023")
        tmp = APSBusiness(self.driver)
        #使用无线网卡连接上AP后，取出该AP的频率值
        result = tmp.connected_AP_Freq(data_wireless['all_ssid'], \
                    data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert (result > 2400) and (result < 2500),"test set AP 2.4G,fail!"
        print "test set AP 2.4G,pass!"

     #802.11b(testlink_ID:264)
    def test_024_check_2g4_b(self):
        u"""802.11b(testlink_ID:264)"""
        log.debug("024")
        tmp = APSBusiness(self.driver)
        #切换2.4b模式
        result = tmp.change_2g4_mode(data_basic['DUT_ip'],data_login['all'],\
                    1,data_basic['sshUser'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert ("11" in result) and (data_wireless['all_ssid'] in result1),"test set AP 802.11b,fail!"
        print "test set AP 802.11b,pass!"

    #802.11g(testlink_ID:265)
    def test_025_check_2g4_g(self):
        u"""802.11g(testlink_ID:265)"""
        log.debug("025")
        tmp = APSBusiness(self.driver)
        #切换2.4g模式
        result = tmp.change_2g4_mode(data_basic['DUT_ip'],data_login['all'],\
                    1,data_basic['sshUser'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert ("54" in result) and (data_wireless['all_ssid'] in result1),"test set AP 802.11g,fail!"
        print "test set AP 802.11g,pass!"

    #802.11n(testlink_ID:266)
    def test_026_check_2g4_n(self):
        u"""802.11n(testlink_ID:266)"""
        log.debug("026")
        tmp = APSBusiness(self.driver)
        #切换2.4n模式
        result = tmp.change_2g4_mode(data_basic['DUT_ip'],data_login['all'],\
                    1,data_basic['sshUser'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert ("173" in result) and (data_wireless['all_ssid'] in result1),"test set AP 802.11n,fail!"
        print "test set AP 802.11n,pass!"


    #5G(testlink_ID:262)
    def test_027_check_5g(self):
        u"""5G(testlink_ID:262)"""
        log.debug("027")
        tmp = APSBusiness(self.driver)
        #设置ap频段，然后使用无线网卡连接判断设置是否成功
        result = tmp.AP_Freq("5GHz",data_wireless['all_ssid'], \
                    data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result > 5100,"test set AP 5G,fail!"
        print "test set AP 5G,pass!"

    #802.11ac(testlink_ID:267)
    def test_028_check_5g_ac(self):
        u"""802.11ac(testlink_ID:267)"""
        log.debug("028")
        tmp = APSBusiness(self.driver)
        result = tmp.check_5g_mode(data_basic['DUT_ip'],data_login['all'],\
                    data_basic['sshUser'])
        result1 = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                        data_wireless["short_wpa"],data_basic["wlan_pc"])
        #切换2.4G频段
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_AP_Freq("2.4GHz")
        assert ("866.7" in result) and (data_wireless['all_ssid'] in result1),"test set AP 802.11ac,fail!"
        print "test set AP 802.11ac,pass!"


    #测试的2.4G无线信道：指定固定信道1时(testlink_ID:275)
    def test_029_2g4_fixed_channel1(self):
        u"""测试的2.4G无线信道：指定固定信道1时(testlink_ID:275)"""
        log.debug("029")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_2g4_channel("1",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2412,"test 2.4G fixed channel 1,test fail!"
        print "test 2.4G fixed channel 1,test pass!"

    #测试的2.4G无线信道：指定固定信道2时(testlink_ID:275)
    def test_030_2g4_fixed_channel2(self):
        u"""测试的2.4G无线信道：指定固定信道2时(testlink_ID:275)"""
        log.debug("030")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("2",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2417,"test 2.4G fixed channel 2,test fail!"
        print "test 2.4G fixed channel 2,test pass!"

    #测试的2.4G无线信道：指定固定信道3时(testlink_ID:275)
    def test_031_2g4_fixed_channel3(self):
        u"""测试的2.4G无线信道：指定固定信道3时(testlink_ID:275)"""
        log.debug("031")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("3",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2422,"test 2.4G fixed channel 3,test fail!"
        print "test 2.4G fixed channel 3,test pass!"

    #测试的2.4G无线信道：指定固定信道4时(testlink_ID:275)
    def test_032_2g4_fixed_channel4(self):
        u"""测试的2.4G无线信道：指定固定信道4时(testlink_ID:275)"""
        log.debug("032")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("4",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2427,"test 2.4G fixed channel 4,test fail!"
        print "test 2.4G fixed channel 4,test pass!"

    #测试的2.4G无线信道：指定固定信道5时(testlink_ID:275)
    def test_033_2g4_fixed_channel5(self):
        u"""测试的2.4G无线信道：指定固定信道5时(testlink_ID:275)"""
        log.debug("033")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("5",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2432,"test 2.4G fixed channel 5,test fail!"
        print "test 2.4G fixed channel 5,test pass!"

    #测试的2.4G无线信道：指定固定信道6时(testlink_ID:275)
    def test_034_2g4_fixed_channel6(self):
        u"""测试的2.4G无线信道：指定固定信道6时(testlink_ID:275)"""
        log.debug("034")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("6",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2437,"test 2.4G fixed channel 6,test fail!"
        print "test 2.4G fixed channel 6,test pass!"

    #测试的2.4G无线信道：指定固定信道7时(testlink_ID:275)
    def test_035_2g4_fixed_channel7(self):
        u"""测试的2.4G无线信道：指定固定信道7时(testlink_ID:275)"""
        log.debug("035")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("7",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2442,"test 2.4G fixed channel 7,test fail!"
        print "test 2.4G fixed channel 7,test pass!"

    #测试的2.4G无线信道：指定固定信道8时(testlink_ID:275)
    def test_036_2g4_fixed_channel8(self):
        u"""测试的2.4G无线信道：指定固定信道8时(testlink_ID:275)"""
        log.debug("036")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("8",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result== 2447,"test 2.4G fixed channel 8,test fail!"
        print "test 2.4G fixed channel 8,test pass!"

    #测试的2.4G无线信道：指定固定信道9时(testlink_ID:275)
    def test_037_2g4_fixed_channel9(self):
        u"""测试的2.4G无线信道：指定固定信道9时(testlink_ID:275)"""
        log.debug("037")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("9",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2452,"test 2.4G fixed channel 9,test fail!"
        print "test 2.4G fixed channel 9,test pass!"

    #测试的2.4G无线信道：指定固定信道10时(testlink_ID:275)
    def test_038_2g4_fixed_channel10(self):
        u"""测试的2.4G无线信道：指定固定信道10时(testlink_ID:275)"""
        log.debug("038")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("10",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2457,"test 2.4G fixed channel 10,test fail!"
        print "test 2.4G fixed channel 10,test pass!"

    #测试的2.4G无线信道：指定固定信道11时(testlink_ID:275)
    def test_039_2g4_fixed_channel11(self):
        u"""测试的2.4G无线信道：指定固定信道11时(testlink_ID:275)"""
        log.debug("039")
        #切换2.4G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp = APSBusiness(self.driver)
        result =tmp.check_2g4_channel("11",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 2462,"test 2.4G fixed channel 11,test fail!"
        print "test 2.4G fixed channel 11,test pass!"


    #测试的5G无线信道：指定固定信道36时(testlink_ID:276)
    def test_040_5g_fixed_channel36(self):
        u"""测试的5G无线信道：指定固定信道36时(testlink_ID:276)"""
        log.debug("040")
        #切换仅5G频段
        tmp1 = APSBusiness(self.driver)
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_AP_Freq("5GHz")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        result =tmp1.check_5g_channel("36",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5180,"test 2.4G fixed channel 36,test fail!"
        print "test 2.4G fixed channel 36,test pass!"

    #测试的5G无线信道：指定固定信道40时(testlink_ID:276)
    def test_041_5g_fixed_channel40(self):
        u"""测试的5G无线信道：指定固定信道40时(testlink_ID:276)"""
        log.debug("041")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("40",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5200,"test 2.4G fixed channel 40,test fail!"
        print "test 2.4G fixed channel 40,test pass!"

    #测试的5G无线信道：指定固定信道44时(testlink_ID:276)
    def test_042_5g_fixed_channel44(self):
        u"""测试的5G无线信道：指定固定信道44时(testlink_ID:276)"""
        log.debug("042")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("44",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5220,"test 2.4G fixed channel 44,test fail!"
        print "test 2.4G fixed channel 44,test pass!"

    #测试的5G无线信道：指定固定信道48时(testlink_ID:276)
    def test_043_5g_fixed_channel48(self):
        u"""测试的5G无线信道：指定固定信道48时(testlink_ID:276)"""
        log.debug("43")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("48",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5240,"test 2.4G fixed channel 48,test fail!"
        print "test 2.4G fixed channel 48,test pass!"

    #测试的5G无线信道：指定固定信道149时(testlink_ID:276)
    def test_044_5g_fixed_channel149(self):
        u"""测试的5G无线信道：指定固定信道149时(testlink_ID:276)"""
        log.debug("044")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("149",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5745,"test 2.4G fixed channel 149,test fail!"
        print "test 2.4G fixed channel 149,test pass!"

    #测试的5G无线信道：指定固定信道153时(testlink_ID:276)
    def test_045_5g_fixed_channel153(self):
        u"""测试的5G无线信道：指定固定信道153时(testlink_ID:276)"""
        log.debug("045")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("153",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5765,"test 2.4G fixed channel 153,test fail!"
        print "test 2.4G fixed channel 153,test pass!"

    #测试的5G无线信道：指定固定信道157时(testlink_ID:276)
    def test_046_5g_fixed_channel157(self):
        u"""测试的5G无线信道：指定固定信道157时(testlink_ID:276)"""
        log.debug("046")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("157",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        assert result == 5785,"test 2.4G fixed channel 157,test fail!"
        print "test 2.4G fixed channel 157,test pass!"

    #测试的5G无线信道：指定固定信道161时(testlink_ID:276)
    def test_047_5g_fixed_channel161(self):
        u"""测试的5G无线信道：指定固定信道161时(testlink_ID:276)"""
        log.debug("047")
        #切换5G无线信道，判断，无线网卡连接取出该AP的频率值
        tmp1 = APSBusiness(self.driver)
        result =tmp1.check_5g_channel("161",data_wireless['all_ssid'], data_wireless["short_wpa"],data_basic["wlan_pc"])
        #切换2.4G频段
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_AP_Freq("2.4GHz")
        assert result == 5805,"test 2.4G fixed channel 161,test fail!"
        print "test 2.4G fixed channel 157,test pass!"

    #2.4g切换到b模式后，判断shortGI是否是灰色(testlink_ID:280_1)
    def test_048_check_shortGI_b(self):
        u"""2.4g切换到b模式后，判断shortGI是否是灰色(testlink_ID:280_1)"""
        log.debug("048")
        #切换2.4G的模式为b
        tmp1 = APSBusiness(self.driver)
        #切换2.4b模式
        tmp1.change_2g4_mode(data_basic['DUT_ip'],data_login['all'],\
                    1,data_basic['sshUser'])
        result1,result2 = tmp1.check_2g4_shortgi()
        assert result1,"test 2.4G 11b shorGI is disable,test fail!"
        print "test 2.4G 11b shorGI is disable,test pass!"

    #2.4g切换到g模式后，判断shortGI是否是灰色(testlink_ID:280_2)
    def test_049_check_shortGI_g(self):
        u"""2.4g切换到g模式后，判断shortGI是否是灰色(testlink_ID:280_2)"""
        log.debug("049")
        #切换2.4G的模式为g
        tmp1 = APSBusiness(self.driver)
        tmp1.change_2g4_mode(data_basic['DUT_ip'],data_login['all'],\
                    1,data_basic['sshUser'])
        result1,result2 = tmp1.check_2g4_shortgi()
        assert result1,"test 2.4G 11g shorGI is disable,test fail!"
        print "test 2.4G 11g shorGI is disable,test pass!"

    #2.4g切换到11n模式后，判断shortGI是否是灰色(testlink_ID:280_3)
    def test_050_check_shortGI_n(self):
        u"""2.4g切换到n模式后，判断shortGI是否是灰色(testlink_ID:280_3)"""
        log.debug("050")
        #切换2.4G的模式为n
        tmp1 = APSBusiness(self.driver)
        tmp1.change_2g4_mode(data_basic['DUT_ip'],data_login['all'],\
                    1,data_basic['sshUser'])
        result1,result2 = tmp1.check_2g4_shortgi()
        #点击勾上2.4g的shortgi
        tmp1.cancel_2g4_shortgi()
        #切换Dual-Band频段
        tmp2 = SSIDBusiness(self.driver)
        tmp2.change_AP_Freq("Dual-Band")
        assert result1 == None,"test 2.4G 11n shorGI is enable,test fail!"
        print "test 2.4G 11n shorGI is enable,test pass!"

    #5g模式，判断shortGI是否是灰色(testlink_ID:280_4)
    def test_051_check_shortGI_ac(self):
        u"""5g模式，判断shortGI是否是灰色(testlink_ID:280_4)"""
        log.debug("051")
        #检查5g的shortGI是否被选中
        tmp1 = APSBusiness(self.driver)
        result = tmp1.check_5g_shortgi()
        assert result == "true","test 5G 11ac shorGI is enable,test fail!"
        print "test 5G 11ac shorGI is enable,test pass!"

    #取消2.4g的shortgi后，检查是否取消选中(testlink_ID:280_5)
    def test_052_check_shortGI_cancel(self):
        u"""取消2.4g的shortgi后，检查是否取消选中(testlink_ID:280_5)"""
        log.debug("052")
        tmp = APSBusiness(self.driver)
        #取消2.4g的shortgi
        tmp.cancel_2g4_shortgi()
        result1,result2 = tmp.check_2g4_shortgi()
        #重启master ap
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        assert result2  == None,"test cancel shortgi,test fail!"
        print "test cancel shortgi,test pass!"

    #取消2.4g的shortgi后，重启ap检查是否取消选中(testlink_ID:280_6)
    def test_053_check_reboot_shortGI_cancel(self):
        u"""取消2.4g的shortgi后，重启ap检查是否取消选中(testlink_ID:280_6)"""
        log.debug("053")
        tmp = APSBusiness(self.driver)
        result1,result2 = tmp.check_2g4_shortgi()
        #勾上2.4g的shortgi
        tmp.cancel_2g4_shortgi()
        assert result2  == None,"test cancel shortgi,test fail!"
        print "test cancel shortgi,test pass!"

    #取消5g的shortgi后，检查是否取消选中(testlink_ID:280_7)
    def test_054_check_shortGI_cancel(self):
        u"""取消5g的shortgi后，检查是否取消选中(testlink_ID:280_7)"""
        log.debug("054")
        tmp1 = APSBusiness(self.driver)
        #取消5g的shortgi
        tmp1.cancel_5g_shortgi()
        result = tmp1.check_5g_shortgi()
        #重启master ap
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        assert result  == None,"test cancel shortgi,test fail!"
        print "test cancel shortgi,test pass!"

    #取消5g的shortgi后，重启ap检查是否取消选中(testlink_ID:280_7)
    def test_055_check_shortGI_cancel(self):
        u"""取消5g的shortgi后，重启ap检查是否取消选中(testlink_ID:280_7)"""
        log.debug("055")
        tmp1 = APSBusiness(self.driver)
        result = tmp1.check_5g_shortgi()
        #再选择5g的shortgi
        tmp1.cancel_5g_shortgi()
        assert result  == None,"test cancel shortgi,test fail!"
        print "test cancel shortgi,test pass!"
    #
    # #802.11n enable Short GI ,检查1,2,3流(testlink_ID:282_1)
    # def test_056_2g4_active_stream_enable(self):
    #     u"""802.11n enable Short GI ,检查1,2,3流(testlink_ID:282_1)"""
    #     #依次选择2.4g的激活空间流后，登录路由后台取出比特流
    #     tmp = APSBusiness(self.driver)
    #     result = tmp.check_2g4_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     assert ("72" in result[0]) and ("144" in result[1]) and ("216" in result[2]),"test 11n active stream enable,test fail!"
    #     print "test 11n active stream enable,test pass!"
    #
    # #802.11n disable Short GI ,检查1,2,3流(testlink_ID:282_2)
    # def test_057_2g4_active_stream1_disable(self):
    #     u"""802.11n disable Short GI ,检查1,2,3流(testlink_ID:282_2)"""
    #     tmp = APSBusiness(self.driver)
    #     #取消2.4g的shortgi
    #     tmp.cancel_2g4_shortgi()
    #     #依次选择2.4g的激活空间流后，登录路由后台取出比特流
    #     result = tmp.check_2g4_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     #测试完成，勾上2.4g的shortgi
    #     tmp.cancel_2g4_shortgi()
    #     assert ("65" in result[0]) and ("130" in result[1]) and ("195" in result[2]),"test 11n active stream disable,test fail!"
    #     print "test 11n active stream disable,test pass!"
    #
    # #802.11ac-80M enable Short GI ,检查1,2,3流(testlink_ID:285_1)
    # def test_058_5g_80M_active_stream_enable(self):
    #     u"""802.11ac-80M enable Short GI ,检查1,2,3流(testlink_ID:285_1)"""
    #     #依次选择5g的激活空间流后，登录路由后台取出比特流
    #     tmp = APSBusiness(self.driver)
    #     result = tmp.check_5g_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     assert ("200" in result[0]) and ("400" in result[1]) and ("600" in result[2]),"test 11ac-80M active stream enable,test fail!"
    #     print "test 11ac-80M active stream enable,test pass!"
    #
    # #802.11ac-80M disable Short GI ,检查1,2,3流(testlink_ID:285_2)
    # def test_059_5g_80M_active_stream_disable(self):
    #     u"""802.11ac-80M disable Short GI ,检查1,2,3流(testlink_ID:285_2)"""
    #     #取消5g的shortgi
    #     tmp1 = APSBusiness(self.driver)
    #     tmp1.cancel_5g_shortgi()
    #     #依次选择5g的激活空间流后，登录路由后台取出比特流
    #     result = tmp1.check_5g_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     assert ("390" in result[0]) and ("780" in result[1]) and ("1.17" in result[2]),"test 11ac-80M active stream disable,test fail!"
    #     print "test 11ac-80M active stream disable,test pass!"
    #
    # #802.11ac-20MHz enable Short GI ,检查1,2,3流(testlink_ID:283_1)
    # def test_060_5g_20M_active_stream_enable(self):
    #     u"""802.11ac-20MHz enable Short GI ,检查1,2,3流(testlink_ID:283_1)"""
    #     #依次选择5g的激活空间流后，登录路由后台取出比特流
    #     tmp1 = APSBusiness(self.driver)
    #     ##切换5G模式的带宽
    #     tmp1.change_5g_width("20MHz")
    #     #勾上5g的shortgi
    #     tmp1.cancel_5g_shortgi()
    #     result = tmp1.check_5g_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     assert ("86.7" in result[0]) and ("173.3" in result[1]) and ("288.9" in result[2]),"test 11ac-20M active stream enable,test fail!"
    #     print "test 11ac-20M active stream enable,test pass!"
    #
    # #802.11ac-20MHz disable Short GI ,检查1,2,3流(testlink_ID:283_2)
    # def test_061_5g_20M_active_stream_disable(self):
    #     u"""802.11ac-20MHz disable Short GI ,检查1,2,3流(testlink_ID:283_2)"""
    #     #依次选择5g的激活空间流后，登录路由后台取出比特流
    #     tmp1 = APSBusiness(self.driver)
    #     #disable 5g的shortgi
    #     tmp1.cancel_5g_shortgi()
    #     result = tmp1.check_5g_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     assert ("78" in result[0]) and ("156" in result[1]) and ("260" in result[2]),"test 11ac-20M active stream disable,test fail!"
    #     print "test 11ac-20M active stream disable,test pass!"
    #
    # #802.11ac-40MHz enable Short GI ,检查1,2,3流(testlink_ID:284_1)
    # def test_062_5g_40M_active_stream_enable(self):
    #     u"""802.11ac-40MHz enable Short GI ,检查1,2,3流(testlink_ID:284_1)"""
    #     #依次选择5g的激活空间流后，登录路由后台取出比特流
    #     tmp1 = APSBusiness(self.driver)
    #     ##切换5G模式的带宽
    #     tmp1.change_5g_width("40MHz")
    #     #勾上5g的shortgi
    #     tmp1.cancel_5g_shortgi()
    #     result = tmp1.check_5g_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     assert ("200" in result[0]) and ("400" in result[1]) and ("600" in result[2]),"test 11ac-40M active stream enable,test fail!"
    #     print "test 11ac-40M active stream enable,test pass!"
    #
    # #802.11ac-40MHz disable Short GI ,检查1,2,3流(testlink_ID:284_2)
    # def test_063_5g_40M_active_stream_disable(self):
    #     u"""802.11ac-40MHz disable Short GI ,检查1,2,3流(testlink_ID:284_2)"""
    #     #依次选择5g的激活空间流后，登录路由后台取出比特流
    #     tmp1 = APSBusiness(self.driver)
    #     #disable 5g的shortgi
    #     tmp1.cancel_5g_shortgi()
    #     result = tmp1.check_5g_active_streams_7610(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     #测试完成，勾上5g的shortgi
    #     tmp1.cancel_5g_shortgi()
    #     ##切换5G模式的带宽-80M
    #     tmp1.change_5g_width("80MHz")
    #     assert ("180" in result[0]) and ("360" in result[1]) and ("540" in result[2]),"test 11ac-40M active stream disable,test fail!"
    #     print "test 11ac-40M active stream disable,test pass!"
    #
    #
    # #2.4g stream1,AP发射功率(testlink_ID:290)
    # def test_064_2g4_stream1_power(self):
    #     u"""2.4g stream1,AP发射功率(testlink_ID:290)"""
    #     powers = data_AP['7610_2g4_stream1_powers']
    #     print powers
    #     #选择2.4g的激活空间流1
    #     tmp = APSBusiness(self.driver)
    #     tmp.change_2g4_active_streams("1")
    #     result = tmp.check_2g4_power(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     self.assertEqual(result[0], powers[0])
    #     self.assertLessEqual(result[1],powers[1]+3)
    #     self.assertGreaterEqual(result[1],powers[1]-3)
    #     self.assertLessEqual(result[2],powers[2]+3)
    #     self.assertGreaterEqual(result[2],powers[2]-3)
    #     print "test 2.4g stream1 power,test pass!"
    #
    # #2.4g stream2,AP发射功率(testlink_ID:291)
    # def test_065_2g4_stream2_power(self):
    #     u"""2.4g stream2,AP发射功率(testlink_ID:291)"""
    #     powers = data_AP['7610_2g4_stream2_powers']
    #     print powers
    #     #选择2.4g的激活空间流2
    #     tmp = APSBusiness(self.driver)
    #     tmp.change_2g4_active_streams("2")
    #     result = tmp.check_2g4_power(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     self.assertEqual(result[0], powers[0])
    #     self.assertLessEqual(result[1],powers[1]+3)
    #     self.assertGreaterEqual(result[1],powers[1]-3)
    #     self.assertLessEqual(result[2],powers[2]+3)
    #     self.assertGreaterEqual(result[2],powers[2]-3),
    #     "test 2.4g stream2 power,test fail!"
    #     print "test 2.4g stream2 power,test pass!"
    #
    # #2.4g stream3,AP发射功率(testlink_ID:292)
    # def test_066_2g4_stream3_power(self):
    #     u"""2.4g stream3,AP发射功率(testlink_ID:292)"""
    #     powers = data_AP['7610_2g4_stream3_powers']
    #     print powers
    #     #选择2.4g的激活空间流3
    #     tmp = APSBusiness(self.driver)
    #     tmp.change_2g4_active_streams("3")
    #     result = tmp.check_2g4_power(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     self.assertEqual(result[0], powers[0])
    #     self.assertLessEqual(result[1],powers[1]+3)
    #     self.assertGreaterEqual(result[1],powers[1]-3)
    #     self.assertLessEqual(result[2],powers[2]+3)
    #     self.assertGreaterEqual(result[2],powers[2]-3),
    #     "test 2.4g stream3 power,test fail!"
    #     print "test 2.4g stream3 power,test pass!"
    #
    # #5g stream1,AP发射功率(testlink_ID:293)
    # def test_067_5g_stream1_power(self):
    #     u"""5g stream1,AP发射功率(testlink_ID:293)"""
    #     powers = data_AP['7610_5g_stream1_powers']
    #     print powers
    #     #选择5g的激活空间流1
    #     tmp1 = APSBusiness(self.driver)
    #     tmp1.change_5g_active_streams("1")
    #     result = tmp1.check_5g_power(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     self.assertEqual(result[0], powers[0])
    #     self.assertLessEqual(result[1],powers[1]+3)
    #     self.assertGreaterEqual(result[1],powers[1]-3)
    #     self.assertLessEqual(result[2],powers[2]+3)
    #     self.assertGreaterEqual(result[2],powers[2]-3),
    #     "test 5g stream1 power,test fail!"
    #     print "test 5g stream1 power,test pass!"
    #
    #
    # #5g stream2,AP发射功率(testlink_ID:294)
    # def test_068_5g_stream2_power(self):
    #     u"""5g stream2,AP发射功率(testlink_ID:294)"""
    #     powers = data_AP['7610_5g_stream2_powers']
    #     print powers
    #     #选择5g的激活空间流2
    #     tmp1 = APSBusiness(self.driver)
    #     tmp1.change_5g_active_streams("2")
    #     result = tmp1.check_5g_power(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     self.assertEqual(result[0], powers[0])
    #     self.assertLessEqual(result[1],powers[1]+3)
    #     self.assertGreaterEqual(result[1],powers[1]-3)
    #     self.assertLessEqual(result[2],powers[2]+3)
    #     self.assertGreaterEqual(result[2],powers[2]-3),
    #     "test 5g stream2 power,test fail!"
    #     print "test 5g stream2 power,test pass!"
    #
    # #5g stream3,AP发射功率(testlink_ID:295)
    # def test_069_5g_stream3_power(self):
    #     u"""5g stream3,AP发射功率(testlink_ID:295)"""
    #     powers = data_AP['7610_5g_stream3_powers']
    #     print powers
    #     #选择5g的激活空间流3
    #     tmp1 = APSBusiness(self.driver)
    #     tmp1.change_5g_active_streams("3")
    #     result = tmp1.check_5g_power(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
    #     self.assertEqual(result[0], powers[0])
    #     self.assertLessEqual(result[1],powers[1]+3)
    #     self.assertGreaterEqual(result[1],powers[1]-3)
    #     self.assertLessEqual(result[2],powers[2]+3)
    #     self.assertGreaterEqual(result[2],powers[2]-3),
    #     "test 5g stream2 power,test fail!"
    #     print "test 5g stream2 power,test pass!"


    #重启检查master ap的配置依然生效(testlink_ID:296_1)
    def test_070_reboot_master(self):
        u"""重启检查master ap的配置依然生效(testlink_ID:296_1)"""
        log.debug("070")
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig ath0 | grep ESSID")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig ath1 | grep ESSID")
        assert (data_wireless['all_ssid'] in result1) \
            and (data_wireless['all_ssid'] in result2), "after reboot master ap check config,test fail!"
        print "after reboot master ap check config,test pass!"

    #测试slave ap的重启(testlink_ID:296_2)
    def test_071_slave_ap_reboot(self):
        u"""测试slave ap的重启(testlink_ID:296_2)"""
        log.debug("071")
        tmp = APSBusiness(self.driver)
        #重启slave ap
        tmp.reboot_slave_ap(data_AP['slave:mac2'])
        result = tmp.get_ping(data_basic['slave_ip2'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig ath0 | grep ESSID")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"iwconfig ath1 | grep ESSID")

        #在页面上把AP恢复出厂设置
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(30)
        #接触slave ap2的配对
        tmp.unpair_special_slave_AP(data_AP['slave:mac2'])
        tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])

        assert (result == 0) and (data_wireless['all_ssid'] in result1) \
            and (data_wireless['all_ssid'] in result2),"test slave ap reboot,fail!"
        print "test slave ap reboot,pass!"

    ###################------以下是custom wireless power的用例------########################
    #tx-power可配置范围-2.4G
    def test_072_2g4_custom_power_range(self):
        u"""tx-power可配置范围-2.4G(testlink_ID:2219-1)"""
        log.debug("072")
        tmp1 = SSIDBusiness(self.driver)
        #修改默认的ssid
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        tmp = APSBusiness(self.driver)
        #取最大，最小和中间值进行测试
        powers = [data_AP['max_power'],data_AP['min_power'],data_AP['medium_power']]
        print powers
        #设置ap的2.4G的自定义功率值，并检查页面上是否配置成功
        result = tmp.check_ap_2g4_custom_power_webpage(data_AP["master:mac"],powers)
        self.assertNotIn(False,result), "check AP 2.4G custom power range, test fail! "
        print "check AP 2.4G custom power range, test pass! "

    #tx-power可配置范围-5G
    def test_073_5g_custom_power_range(self):
        u"""tx-power可配置范围-5G(testlink_ID:2219-2)"""
        log.debug("073")
        tmp = APSBusiness(self.driver)
        #取最大，最小和中间值进行测试
        powers = [data_AP['max_power'],data_AP['min_power'],data_AP['medium_power']]
        print powers
        #设置ap的5G的自定义功率值，并检查页面上是否配置成功
        result = tmp.check_ap_5g_custom_power_webpage(data_AP["master:mac"],
            powers)
        self.assertNotIn(False,result), "check AP 5G custom power range, test fail! "
        print "check AP 5G custom power range, test pass! "

    #验证设置ap的2.4G的自定义功率值小于最小值时，检查页面上是否会报错-2.4G
    def test_074_check_ap_2g4_custom_power_less_min(self):
        u"""验证设置ap的2.4G的自定义功率值小于最小值时，检查页面上是否会报错-2.4G(testlink_ID:2220-1)"""
        log.debug("074")
        tmp = APSBusiness(self.driver)
        powers = data_AP['less_min_powers']
        print powers
        result = tmp.check_ap_2g4_custom_powers_invalid(data_AP["master:mac"],
                powers)
        print result
        self.assertNotIn(False,result), "input AP 2.4G custom power less min power, test fail!"
        print "input AP 2.4G custom power less min power, test pass!"

     #验证设置ap的5G的自定义功率值小于最小值时，检查页面上是否会报错-5G
    def test_075_check_ap_5g_custom_power_less_min(self):
        u"""验证设置ap的5G的自定义功率值小于最小值时，检查页面上是否会报错-5G(testlink_ID:2220-2)"""
        log.debug("075")
        tmp = APSBusiness(self.driver)
        powers = data_AP['less_min_powers']
        print powers
        result = tmp.check_ap_5g_custom_powers_invalid(data_AP["master:mac"],
                powers)
        print result
        self.assertNotIn(False,result), "input AP 5G custom power less min power, test fail!"
        print "input AP 5G custom power less min power, test pass!"

    #验证设置ap的2.4G的自定义功率值大于最大值时，检查页面上是否会报错-2.4G
    def test_076_check_ap_2g4_custom_power_more_max(self):
        u"""验证设置ap的2.4G的自定义功率值大于最大值时，检查页面上是否会报错-2.4G(testlink_ID:2221-1)"""
        log.debug("076")
        tmp = APSBusiness(self.driver)
        powers = data_AP['more_max_powers']
        print powers
        result = tmp.check_ap_2g4_custom_powers_invalid(data_AP["master:mac"],
                powers)
        print result
        self.assertNotIn(False,result), "input AP 2.4G custom power more max power, test fail!"
        print "input AP 2.4G custom power more max power, test pass!"

    #验证设置ap的5G的自定义功率值大于最大值时，检查页面上是否会报错-5G
    def test_077_check_ap_5g_custom_power_more_max(self):
        u"""验证设置ap的5G的自定义功率值大于最大值时，检查页面上是否会报错-5G(testlink_ID:2221-2)"""
        log.debug("077")
        tmp = APSBusiness(self.driver)
        powers = data_AP['more_max_powers']
        print powers
        result = tmp.check_ap_5g_custom_powers_invalid(data_AP["master:mac"],
                powers)
        print result
        self.assertNotIn(False,result), "input AP 5G custom power more max power, test fail!"
        print "input AP 5G custom power more max power, test pass!"

    #验证设置ap的2.4G的自定义功率值为特殊字符，检查页面上是否会报错-2.4G
    def test_078_check_ap_2g4_custom_power_letter(self):
        u"""验证设置ap的2.4G的自定义功率值为特殊字符，检查页面上是否会报错-2.4G(testlink_ID:2222-1)"""
        log.debug("078")
        tmp = APSBusiness(self.driver)
        #验证设置ap的2.4G的自定义功率值非法时，检查页面上是否会报错
        result = tmp.check_ap_2g4_custom_power_invalid(data_AP["master:mac"],
            data_AP['letter_power'])
        self.assertTrue(result), "input 2.4G custom power is letter,test fail!"
        print "input 2.4G custom power is letter,test pass!"

    #验证设置ap的5G的自定义功率值为特殊字符，检查页面上是否会报错-5G
    def test_079_check_ap_5g_custom_power_letter(self):
        u"""验证设置ap的5G的自定义功率值为特殊字符，检查页面上是否会报错-5G(testlink_ID:2222-2)"""
        log.debug("079")
        tmp = APSBusiness(self.driver)
        #验证设置ap的5G的自定义功率值非法时，检查页面上是否会报错
        result = tmp.check_ap_5g_custom_power_invalid(data_AP["master:mac"],
            data_AP['letter_power'])
        self.assertTrue(result), "input 5G custom power is letter,test fail!"
        print "input 5G custom power is letter,test pass!"

    #2.4G，stream选择1,自定义功率分别配置1-31,后台查看是否都对应生效
    def test_080_check_2g4_stream1_custom_power(self):
        u"""2.4G，stream选择1,自定义功率分别配置1-31,后台查看是否都对应生效(testlink_ID:2229)--bug84723"""
        log.debug("080")
        tmp = APSBusiness(self.driver)
        #选择2.4g的激活空间流1
        tmp.change_2g4_active_streams("1")
        #自定义功率分别配置功率
        powers = data_AP['stream_powers']
        #验证ap的2.4G的自定义功率值
        result = tmp.check_ap_2g4_custom_power(data_AP["master:mac"],
            powers,data_basic['DUT_ip'],data_basic['sshUser'], data_login['all'])
        self.assertNotIn(False, result), "set 2.4G stream1,choose custom power from 1 to 31,test fail!"
        print "set 2.4G stream1,choose custom power from 1 to 31,test pass!"

    #2.4G，stream选择2,自定义功率分别配置1-31,后台查看是否都对应生效
    def test_081_check_2g4_stream2_custom_power(self):
        u"""2.4G，stream选择2,自定义功率分别配置1-31,后台查看是否都对应生效(testlink_ID:2230)--bug84723"""
        log.debug("081")
        tmp = APSBusiness(self.driver)
        #选择2.4g的激活空间流2
        tmp.change_2g4_active_streams("2")
        #自定义功率分别配置功率
        powers = data_AP['stream_powers']
        #验证ap的2.4G的自定义功率值
        result = tmp.check_ap_2g4_custom_power(data_AP["master:mac"],
            powers,data_basic['DUT_ip'],data_basic['sshUser'], data_login['all'])
        self.assertNotIn(False, result), "set 2.4G stream2,choose custom power from 1 to 31,test fail!"
        print "set 2.4G stream2,choose custom power from 1 to 31,test pass!"

    #5G，stream选择1,自定义功率分别配置1-31,后台查看是否都对应生效
    def test_083_check_5g_stream1_custom_power(self):
        u"""5G，stream选择1,自定义功率分别配置1-31,后台查看是否都对应生效(testlink_ID:2232)--bug84723"""
        log.debug("083")
        tmp = APSBusiness(self.driver)
        #选择5g的激活空间流1
        tmp.change_5g_active_streams("1")
        #自定义功率分别配置功率
        powers = data_AP['stream_powers']
        #验证ap的5G的自定义功率值
        result = tmp.check_ap_5g_custom_power(data_AP["master:mac"],
            powers,data_basic['DUT_ip'],data_basic['sshUser'], data_login['all'])
        self.assertNotIn(False, result), "set 5G stream1,choose custom power from 1 to 31,test fail!"
        print "set 5G stream1,choose custom power from 1 to 31,test pass!"

    #5G，stream选择2,自定义功率分别配置1-31,后台查看是否都对应生效
    def test_084_check_5g_stream2_custom_power(self):
        u"""5G，stream选择2,自定义功率分别配置1-31,后台查看是否都对应生效(testlink_ID:2233)--bug84723"""
        log.debug("084")
        tmp = APSBusiness(self.driver)
        #选择5g的激活空间流2
        tmp.change_5g_active_streams("2")
        #自定义功率分别配置功率
        powers = data_AP['stream_powers']
        #验证ap的5G的自定义功率值
        result = tmp.check_ap_5g_custom_power(data_AP["master:mac"],
            powers,data_basic['DUT_ip'],data_basic['sshUser'], data_login['all'])
        self.assertNotIn(False, result), "set 5G stream2,choose custom power from 1 to 31,test fail!"
        print "set 5G stream2,choose custom power from 1 to 31,test pass!"

    #设置国家代码为CHINA，2.4GHZ custom power允许配置的范围(1-20)
    def test_086_check_china_2g4_custom_power_range(self):
        u"""设置国家代码为CHINA，2.4GHZ custom power允许配置的范围(1-20)(testlink_ID:2237)--bug84660"""
        log.debug("086")
        tmp1 = BasicBusiness(self.driver)
        #设置国家
        tmp1.set_country("156")
        tmp = APSBusiness(self.driver)
        #验证设置ap的2.4G的自定义功率值为21时
        result = tmp.check_ap_2g4_custom_power_invalid_backup(data_AP["master:mac"],"21")
        # self.assertTrue(result), "set country to CHINA,check 2.4G custom power,test fail!"
        print "set country to CHINA,check 2.4G custom power,test pass!"

    #设置国家代码为CHINA，5GHZ custom power允许配置的范围(1-31)
    def test_087_check_china_5g_custom_power_range(self):
        u"""设置国家代码为CHINA，5GHZ custom power允许配置的范围(1-31)(testlink_ID:2238)"""
        log.debug("087")
        tmp = APSBusiness(self.driver)
        #验证设置ap的5G的自定义功率值为31时
        result = tmp.check_ap_5g_custom_power_invalid_backup(data_AP["master:mac"],"31")
        self.assertFalse(result), "set country to CHINA,check 5G custom power,test fail!"
        print "set country to CHINA,check 5G custom power,test pass!"

    #设置国家代码为EGYPT，2.4GHZ custom power允许配置的范围(1-20)
    def test_088_check_EGYPT_2g4_custom_power_range(self):
        u"""设置国家代码为EGYPT，2.4GHZ custom power允许配置的范围(1-20)(testlink_ID:2239)--bug84660"""
        log.debug("088")
        tmp1 = BasicBusiness(self.driver)
        #设置国家
        tmp1.set_country("818")
        tmp = APSBusiness(self.driver)
        #验证设置ap的2.4G的自定义功率值为21时
        result = tmp.check_ap_2g4_custom_power_invalid_backup(data_AP["master:mac"],"21")
        # self.assertTrue(result), "set country to EGYPT,check 2.4G custom power,test fail!"
        print "set country to EGYPT,check 2.4G custom power,test pass!"

    #设置国家代码为EGYPT，5GHZ custom power允许配置的范围(1-31)
    def test_089_check_EGYPT_5g_custom_power_range(self):
        u"""设置国家代码为EGYPT，5GHZ custom power允许配置的范围(1-31)(testlink_ID:2240)"""
        log.debug("089")
        tmp = APSBusiness(self.driver)
        #验证设置ap的5G的自定义功率值为31时
        result = tmp.check_ap_5g_custom_power_invalid_backup(data_AP["master:mac"],"31")
        self.assertFalse(result), "set country to EGYPT,check 5G custom power,test fail!"
        print "set country to EGYPT,check 5G custom power,test pass!"

    #设置国家代码为QATER，2.4GHZ custom power允许配置的范围(1-20)
    def test_090_check_QATER_2g4_custom_power_range(self):
        u"""设置国家代码为QATER，2.4GHZ custom power允许配置的范围(1-20)(testlink_ID:2241)--bug84660"""
        log.debug("090")
        tmp1 = BasicBusiness(self.driver)
        #设置国家
        tmp1.set_country("634")
        tmp = APSBusiness(self.driver)
        #验证设置ap的2.4G的自定义功率值为21时
        result = tmp.check_ap_2g4_custom_power_invalid_backup(data_AP["master:mac"],"21")
        # self.assertTrue(result), "set country to QATER,check 2.4G custom power,test fail!"
        print "set country to QATER,check 2.4G custom power,test pass!"

    #设置国家代码为QATER，5GHZ custom power允许配置的范围(1-20)
    def test_091_check_QATER_5g_custom_power_range(self):
        u"""设置国家代码为QATER，5GHZ custom power允许配置的范围(1-20)(testlink_ID:2242)--bug84660"""
        log.debug("091")
        tmp = APSBusiness(self.driver)
        #验证设置ap的5G的自定义功率值为21时
        result = tmp.check_ap_5g_custom_power_invalid_backup(data_AP["master:mac"],"21")
        # self.assertTrue(result), "set country to QATER,check 5G custom power,test fail!"
        print "set country to QATER,check 5G custom power,test pass!"

    #设置国家代码为JAPAN，2.4GHZ custom power允许配置的范围(1-23)
    def test_092_check_JAPAN_2g4_custom_power_range(self):
        u"""设置国家代码为JAPAN，2.4GHZ custom power允许配置的范围(1-23)(testlink_ID:2245)--bug84660"""
        log.debug("092")
        tmp1 = BasicBusiness(self.driver)
        #设置国家
        tmp1.set_country("392")
        tmp = APSBusiness(self.driver)
        #验证设置ap的2.4G的自定义功率值为24时
        result = tmp.check_ap_2g4_custom_power_invalid_backup(data_AP["master:mac"],"24")
        # self.assertTrue(result), "set country to JAPAN,check 2.4G custom power,test fail!"
        print "set country to JAPAN,check 2.4G custom power,test pass!"

    #设置国家代码为JAPAN，5GHZ custom power允许配置的范围(1-30)
    def test_093_check_JAPAN_5g_custom_power_range(self):
        u"""设置国家代码为JAPAN，5GHZ custom power允许配置的范围(1-30)(testlink_ID:2246)--bug84660"""
        log.debug("093")
        tmp = APSBusiness(self.driver)
        #验证设置ap的5G的自定义功率值为31时
        result = tmp.check_ap_5g_custom_power_invalid_backup(data_AP["master:mac"],"31")
        # self.assertTrue(result), "set country to JAPAN,check 5G custom power,test fail!"
        print "set country to JAPAN,check 5G custom power,test pass!"

    #设置国家代码为US，2.4GHZ custom power允许配置的范围(1-31)
    def test_094_check_US_2g4_custom_power_range(self):
        u"""设置国家代码为US，2.4GHZ custom power允许配置的范围(1-31)(testlink_ID:2243)"""
        log.debug("094")
        tmp1 = BasicBusiness(self.driver)
        #设置国家
        tmp1.set_country("840")
        tmp = APSBusiness(self.driver)
        #验证设置ap的2.4G的自定义功率值为31时
        result = tmp.check_ap_2g4_custom_power_invalid_backup(data_AP["master:mac"],"31")
        self.assertFalse(result), "set country to US,check 2.4G custom power,test fail!"
        print "set country to US,check 2.4G custom power,test pass!"

    #设置国家代码为US，5GHZ custom power允许配置的范围(1-31)
    def test_095_check_US_5g_custom_power_range(self):
        u"""设置国家代码为US，5GHZ custom power允许配置的范围(1-31)(testlink_ID:2244)"""
        log.debug("095")
        tmp = APSBusiness(self.driver)
        #验证设置ap的5G的自定义功率值为31时
        result = tmp.check_ap_5g_custom_power_invalid_backup(data_AP["master:mac"],"31")
        self.assertFalse(result), "set country to US,check 5G custom power,test fail!"
        print "set country to US,check 5G custom power,test pass!"

    #slave 2.4G custom power
    def test_096_check_slave_2g4_custom_power(self):
        u"""slave 2.4G custom power(testlink_ID:2253)"""
        log.debug("096")
        tmp = APSBusiness(self.driver)
        #多个slave ap时，搜索并配对slave2
        tmp.search_pair_special_AP(data_AP['slave:mac2'])
        #验证2.4G的发射功率是否正确
        result = tmp.check_ap_2g4_custom_power(data_AP['slave:mac2'],
            ["16"], data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "check 2.4G custom power, test fail!"
        print "check 2.4G custom power, test pass!"

    #slave 5G custom power
    def test_097_check_slave_5g_custom_power(self):
        u"""slave 5G custom power(testlink_ID:2254)"""
        log.debug("097")
        tmp = APSBusiness(self.driver)
        #验证5G的发射功率是否正确
        result = tmp.check_ap_5g_custom_power(data_AP['slave:mac2'],
            ["16"], data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'])
        tmp.unpair_special_slave_AP(data_AP['slave:mac2'])
        self.assertTrue(result), "check 5G custom power, test fail!"
        print "check 5G custom power, test pass!"

    #custom power 设置一个较小的值，如2,确认客户端是否能够连接
    def test_098_check_little_custom_power(self):
        u"""custom power 设置一个较小的值，如2,确认客户端是否能够连接(testlink_ID:2255)"""
        log.debug("098")
        tmp = APSBusiness(self.driver)
        #设置2.4G和5G的custom power都为2dBm
        tmp.set_ap_2g4_custom_power(data_AP['master:mac'],"2")
        tmp.set_ap_5g_custom_power(data_AP['master:mac'],"2")
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic["wlan_pc"])
        self.assertIn(data_wireless['all_ssid'], result), "set custom power is litter value, test fail!"
        print "set custom power is litter value,test pass!"

    #custom power 设置一个较大的值，如31,确认客户端是否能够连接
    def test_099_check_big_custom_power(self):
        u"""custom power 设置一个较大的值，如31,确认客户端是否能够连接(testlink_ID:2256)"""
        log.debug("099")
        tmp = APSBusiness(self.driver)
        #设置2.4G和5G的custom power都为31dBm
        tmp.set_ap_2g4_custom_power(data_AP['master:mac'],"31")
        tmp.set_ap_5g_custom_power(data_AP['master:mac'],"31")
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],
            data_wireless["short_wpa"],data_basic["wlan_pc"])
        self.assertIn(data_wireless['all_ssid'], result), "set custom power is big value, test fail!"
        print "set custom power is big value,test pass!"

    #恢复出厂设置，custom power也能恢复出厂配置
    def test_100_set_factory_custom_power(self):
        u"""恢复出厂设置，custom power也能恢复出厂配置(testlink_ID:2259)"""
        log.debug("100")
        tmp = APSBusiness(self.driver)
        #在页面上把AP恢复出厂设置
        tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        time.sleep(60)
        result1 = tmp.check_2g4_custom_power(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'],"31")
        result2 = tmp.check_5g_custom_power(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'],"31")

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("AccessPoints")

        self.assertFalse(result1)
        self.assertFalse(result2), "set ap factory,check custom power, test fail!"
        print "set ap factory,check custom power, test pass!"

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
