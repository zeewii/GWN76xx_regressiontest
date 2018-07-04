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

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
data_Client = data.data_Client()
log = Log("Failover")
class TestFailover(unittest.TestCase):
    u"""测试Failover的用例集(runtime:4h)"""
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


    ###################------以下是failover的用例------########################
    #检查failover按钮的有效性-检查failover按钮的名称
    def test_002_check_failover_button_1(self):
        u"""检查failover按钮的有效性-检查failover按钮的名称(testlink_ID:2347-1)"""
        log.debug("002")
        tmp = APSBusiness(self.driver)
        #检查failover按钮的名称
        result = tmp.check_failover_button_name()
        self.assertEqual((u"故障切换" or "Failover"), result), "check failover button-1,fail!"
        print "check failover button-1,pass!"

    #检查failover按钮的有效性-按钮是否可以点击
    def test_003_check_failover_button_2(self):
        u"""检查failover按钮的有效性--按钮是否可以点击(testlink_ID:2347-2)"""
        log.debug("003")
        tmp = APSBusiness(self.driver)
        result = tmp.check_failover_button()
        self.assertTrue(result), "check failover button-2,fail!"
        print "check failover button-2,pass!"

    #没有匹配ap时，检查failover ap的mac list
    def test_004_no_pair_check_failover_AP_num(self):
        u"""没有匹配ap时，检查failover ap的mac list(testlink_ID:2348)"""
        log.debug("004")
        tmp = APSBusiness(self.driver)
        #检查所有可选择的failover ap的个数--1个
        result = tmp.check_failover_AP_num(1)
        self.assertTrue(result), "when no paired ap,check mac list of failover ap, fail!"
        print "when no paired ap,check mac list of failover ap ,pass!"

    #有一个匹配的ap时，检查failover ap的mac list
    def test_005_one_pair_check_failover_AP_num(self):
        u"""有一个匹配的ap时，检查failover ap的mac list(testlink_ID:2349)"""
        log.debug("005")
        tmp = APSBusiness(self.driver)
        #多个slave ap时，搜索并配对特定的ap
        tmp.search_pair_special_AP(data_AP['slave:mac2'])
        #检查所有可选择的failover ap的个数--2个
        result1 = tmp.check_failover_AP_num(2)
        #确认slave ap的mac是否在failover ap的mac list上
        result2 = tmp.check_slave_ap_in_failover_AP(data_AP['slave:mac2'])
        self.assertTrue(result1)
        self.assertTrue(result2), "when one paired ap,check mac list of failover ap, fail!"
        print "when one paired ap,check mac list of failover ap, pass!"

    #有一个匹配的不在线的ap时，检查failover ap的mac list
    def test_006_one_pair_offline_check_failover_AP_num(self):
        u"""有一个匹配的不在线的ap时，检查failover ap的mac list(testlink_ID:2350)"""
        log.debug("006")
        tmp = APSBusiness(self.driver)
        #重启the last slave ap--backup
        tmp.reboot_slave_ap1_backup()
        #检查所有可选择的failover ap的个数--2个
        result1 = tmp.check_failover_AP_num(2)
        #确认slave ap的mac是否在failover ap的mac list上
        result2 = tmp.check_slave_ap_in_failover_AP(data_AP['slave:mac2'])
        time.sleep(180)
        self.assertTrue(result1)
        self.assertTrue(result2), "when one paired ap is offline,check mac list of failover ap, fail!"
        print "when one paired ap is offline,check mac list of failover ap, pass!"

    #能够搜到一个ap时，检查failover ap的mac list
    def test_007_discover_ap_check_failover_AP_num(self):
        u"""能够搜到一个ap时，检查failover ap的mac list(testlink_ID:2351)"""
        log.debug("007")
        tmp = APSBusiness(self.driver)
        #搜索AP并判断，是否正确--backup
        result1 = tmp.search_AP_backup(data_AP['slave:mac1'])
        #检查所有可选择的failover ap的个数--2个
        result2 = tmp.check_failover_AP_num(2)
        #确认slave ap的mac是否在failover ap的mac list上
        result3 = tmp.check_slave_ap_in_failover_AP(data_AP['slave:mac1'])
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertFalse(result3),"when one paired ap is offline,check mac list of failover ap, fail!"
        print "when one paired ap is offline,check mac list of failover ap, pass!"

    #有多个匹配的ap时，检查failover ap的mac list
    def test_008_multiple_pair_check_failover_AP_num(self):
        u"""有多个匹配的ap时，检查failover ap的mac list(testlink_ID:2352)"""
        log.debug("008")
        tmp = APSBusiness(self.driver)
        #多个slave ap时，搜索并配对特定的ap
        tmp.search_pair_special_AP(data_AP['slave:mac1'])
        time.sleep(60)
        #检查所有可选择的failover ap的个数--2个
        result1 = tmp.check_failover_AP_num(3)
        #确认slave ap的mac是否在failover ap的mac list上
        result2 = tmp.check_slave_ap_in_failover_AP(data_AP['slave:mac2'])
        result3 = tmp.check_slave_ap_in_failover_AP(data_AP['slave:mac1'])
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3), "when multiple paired ap,check mac list of failover ap, fail!"
        print "when multiple paired ap,check mac list of failover ap, pass!"

    #配置一个特定的slave ap作为failover ap
    def test_009_setup_to_failover_ap(self):
        u"""配置一个特定的slave ap作为failover ap(testlink_ID:2353)"""
        log.debug("009")
        tmp = APSBusiness(self.driver)
        #设置slave ap为failover ap
        tmp.change_slave_to_failover(data_AP['slave:mac2'])
        #检查slave ap是否变为failover ap
        result = tmp.check_change_to_failover_AP(data_AP['slave:mac2'],
                    data_basic['DUT_ip'], data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "setup a slave ap to failover ap, test fail!"
        print "setup a slave ap to failover ap, test pass!"

    #指定failover ap后，确认failover ap的配置立即生效
    def test_010_check_failover_configuration_immediately(self):
        u"""指定failover ap后，确认failover ap的配置立即生效(testlink_ID:2359)"""
        log.debug("010")
        #slave ap  变为failover 模式
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        #检查slave ap是否变为failover ap
        tmp = APSBusiness(self.driver)
        result2 = tmp.check_change_to_failover_AP(data_AP['slave:mac2'],
                    data_basic['DUT_ip'], data_basic['sshUser'], data_login['all'])
        self.assertIn("slave", result1)
        self.assertTrue(result2), "Designate a failover ap check configuration take effect immediately,test fail!"
        print "Designate a failover ap check configuration take effect immediately,test pass!"

    #改变failover ap从一个slave ap到另一个slave ap
    def test_011_change_failover_ap(self):
        u"""改变failover ap从一个slave ap到另一个slave ap(testlink_ID:2354)"""
        log.debug("011")
        tmp = APSBusiness(self.driver)
        #设置slave ap为failover ap
        tmp.change_slave_to_failover(data_AP['slave:mac1'])
        #检查slave ap是否变为failover ap
        result = tmp.check_change_to_failover_AP(data_AP['slave:mac1'],
                    data_basic['DUT_ip'], data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "change failover from a slave ap to another, test fail!"
        print "change failover from a slave ap to another, test pass!"

    #再次改变failover ap从一个slave ap到另一个slave ap
    def test_012_change_failover_ap_again(self):
        u"""再次改变failover ap从一个slave ap到另一个slave ap(testlink_ID:2355)"""
        log.debug("012")
        tmp = APSBusiness(self.driver)
        #设置slave ap为failover ap
        tmp.change_slave_to_failover(data_AP['slave:mac2'])
        #检查slave ap是否变为failover ap
        result = tmp.check_change_to_failover_AP(data_AP['slave:mac2'],
                    data_basic['DUT_ip'], data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "change failover from a slave ap to another again, test fail!"
        print "setup a slave ap to failover ap again, test pass!"

    #重复切换failover ap为不同的slave ap 3次
    def test_013_check_repeatedly_switch_to_failover_AP(self):
        u"""重复切换failover ap为不同的slave ap 3次(testlink_ID:2421)"""
        log.debug("013")
        tmp = APSBusiness(self.driver)
        result = tmp.check_repeatedly_switch_to_failover_AP(data_AP['slave:mac1'],
            data_AP['slave:mac2'], data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        self.assertNotIn(False, result),"repeatedly switch different slave to failover,test fail!"
        print "repeatedly switch different slave to failover,test pass!"

    #unpair the designated failover ap, 检查failover ap的mac list
    def test_014_unpair_ap_check_failover_AP(self):
        u"""unpair the designated failover ap, 检查failover ap的mac list(testlink_ID:2356)"""
        log.debug("014")
        tmp = APSBusiness(self.driver)
        #解除特定slave AP的配对
        tmp.unpair_special_slave_AP(data_AP['slave:mac2'])
        #检查所有可选择的failover ap的个数--2个
        result1 = tmp.check_failover_AP_num(2)
        #确认slave ap的mac是否在failover ap的mac list上
        result2 = tmp.check_slave_ap_in_failover_AP(data_AP['slave:mac2'])
        self.assertTrue(result1)
        self.assertFalse(result2), "when unpaired ap, check mac list of failover ap, fail!"
        print "when unpaired ap, check mac list of failover ap, pass!"

    #确认failover ap和master ap有相同的配置
    def test_015_check_failover_ap_configuation(self):
        u"""确认failover ap和master ap有相同的配置(testlink_ID:2360)"""
        log.debug("015")
        tmp = APSBusiness(self.driver)
        #多个slave ap时，搜索并配对特定的ap
        tmp.search_pair_special_AP(data_AP['slave:mac2'])
        time.sleep(60)
        #设置slave ap为failover ap
        tmp.change_slave_to_failover(data_AP['slave:mac2'])
        #确认failover ap和master ap有相同的配置
        result = tmp.check_check_failover_ap_configuation(
            data_basic['DUT_ip'],data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "check failover ap configuation is same master ap, test fail!"
        print "check failover ap configuation is same master ap, test pass!"

    #master ap做一些改变，确认failover ap和master ap有相同的配置
    def test_016_check_failover_ap_configuation_after_change_master(self):
        u"""master ap做一些改变，确认failover ap和master ap有相同的配置(testlink_ID:2361)"""
        log.debug("016")
        #修改默认网络组的ssid和密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        tmp = APSBusiness(self.driver)
        #确认failover ap和master ap有相同的配置
        result = tmp.check_check_failover_ap_configuation(
            data_basic['DUT_ip'],data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "check failover ap configuation is same master ap after changing master ap, test fail!"
        print "check failover ap configuation is same master ap after changing master ap, test pass!"

    #指定一个离线的slave ap作为failover ap，检查failover ap的配置是否同步
    def test_017_check_offline_failover_ap(self):
        u"""指定一个离线的slave ap作为failover ap，检查failover ap的配置是否同步(testlink_ID:2362)"""
        log.debug("017")
        tmp = APSBusiness(self.driver)
        #解除特定slave AP2的配对
        tmp.unpair_special_slave_AP(data_AP['slave:mac2'])
        #重启the last slave ap--backup
        tmp.reboot_slave_ap1_backup()
        #设置slave ap1为failover ap
        time.sleep(80)
        tmp.change_slave_to_failover(data_AP['slave:mac1'])
        time.sleep(180)
        #确认failover ap和master ap有相同的配置
        result = tmp.check_check_failover_ap_configuation(
            data_basic['DUT_ip'],data_basic['slave_ip1'],
            data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "check failover ap configuation when it's offline, test fail!"
        print "check failover ap configuation when it's offline, test pass!"

    #reboot ap,检查failover ap的配置是否同步
    def test_018_check_failover_ap_configuation_after_ap(self):
        u"""reboot ap,检查failover ap的配置是否同步(testlink_ID:2363)"""
        log.debug("018")
        tmp = APSBusiness(self.driver)
        #重启the last slave ap
        tmp.reboot_slave_ap1()
        #确认failover ap和master ap有相同的配置
        result = tmp.check_check_failover_ap_configuation(
            data_basic['DUT_ip'],data_basic['slave_ip1'],
            data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "check failover ap configuation after reboot, test fail!"
        print "check failover ap configuation after reboot, test pass!"

    #准备好master ap的配置及流量，设置好failover ap
    def test_019_config_master_ap_setup_failover_ap(self):
        u"""准备好master ap的配置及流量，设置好failover ap"""
        log.debug("019")
        tmp = APSBusiness(self.driver)
        #解除特定slave AP1的配对
        tmp.unpair_special_slave_AP(data_AP['slave:mac1'])
        #web页面退出登录
        tmp2 = NavbarBusiness(self.driver)
        tmp2.logout()
        #AP 下载/上传流量---master ap
        tmp1 = OVBusiness(self.driver)
        tmp1.set_AP_download_unload(data_wireless['all_ssid'],
            data_wireless["short_wpa"], data_basic['wlan_pc'], data_basic['lan_pc'])
        #重新登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'], data_login['all'])
        #多个slave ap时，搜索并配对特定的ap
        tmp.search_pair_special_AP(data_AP['slave:mac2'])
        #设置slave ap为failover ap
        tmp.change_slave_to_failover(data_AP['slave:mac2'])
        #检查slave ap是否变为failover ap
        result = tmp.check_change_to_failover_AP(data_AP['slave:mac2'],
                    data_basic['DUT_ip'], data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "master ap and set failover ap ready, test fail!"
        print "master ap and set failover ap ready, test pass!"

    #Verify cannot access Failover AP's webUI after master ap lost 14 port within 10mins
    #master ap controller发生故障10分钟内，确认不能访问failover ap的web页面
    def test_020_cannot_access_failover_webUI_in_10mins(self):
        u"""master ap controller发生故障10分钟内，确认不能访问failover ap的web页面(testlink_ID:2375)"""
        log.debug("020")
        tmp = APSBusiness(self.driver)
        #master ap关闭controller
        tmp.close_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #等待3分钟
        time.sleep(180)
        #判断failover ap的页面是否能够访问
        result1 = tmp.check_access_failover_webUI(data_basic['slave_web2'])
        #再等待3分钟
        time.sleep(180)
        #判断failover ap的页面是否能够访问
        result2 = tmp.check_access_failover_webUI(data_basic['slave_web2'])
        self.assertTrue(result1)
        self.assertTrue(result2), "after close master ap controller within 10mins,check failover ap webUI cannot access, test fail!"
        print "after close master ap controller within 10mins,check failover ap webUI cannot access, test pass!"

    #master ap controller发生故障10分钟后，确认能访问failover ap的web页面
    def test_021_cannot_access_failover_webUI_in_10mins(self):
        u"""master ap controller发生故障10分钟后，确认能访问failover ap的web页面(testlink_ID:2376)"""
        log.debug("021")
        tmp = APSBusiness(self.driver)
        #等待10分钟--上一用例已等待6分钟，所以这里只等待4分钟
        time.sleep(240)
        #判断failover ap的页面是否能够访问
        result1 = tmp.check_access_failover_webUI(data_basic['slave_web2'])
        #判断登录页面是否有用户名的元素
        Lg = LoginBusiness(self.driver)
        result2 = Lg.web_login_test()
        self.assertFalse(result1)
        self.assertTrue(result2), "after close master ap controller over 10mins,check failover ap webUI can access, test fail!"
        print "after close master ap controller over 10mins,check failover ap webUI can access, test pass!"

    #failover ap上，确认流量是否能够同步master ap
    def test_022_failover_check_flow(self):
        u"""failover ap上，确认流量是否能够同步master ap(testlink_ID:2365)--bug83451"""
        log.debug("022")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        tmp1 = OVBusiness(self.driver)
        #获取第一个ap下载流量
        result1, result2 = tmp1.get_AP_download()
        assert ("MB" in result1) or ("GB" in result1)
        self.assertLess(0, result2), "failover ap,check the sync of failover ap's DB,test fail!"
        print "failover ap,check the sync of failover ap's DB,test pass!"

    #failover ap上，不能点击任何配置按钮
    def test_023_failover_click_button(self):
        u"""failover ap上，不能点击任何配置按钮(testlink_ID:2407)"""
        log.debug("023")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #判断：failover登录后，ap页面上升级，添加的网络组，配置的按钮都不能点击
        result = tmp.check_failover_AP_cannot_click_button()
        self.assertEqual(["true","true","true"], result), "failover ap,cannot click any config button,test fail!"
        print "failover ap,cannot click any config button,test pass!"

    #failover ap上，检查切换master按钮-检查failover按钮的名称
    def test_024_check_switch_to_master_button_1(self):
        u"""failover ap上，检查切换master按钮-检查failover按钮的名称(testlink_ID:2358-1)"""
        log.debug("024")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #检查failover按钮的名称
        result = tmp.check_failover_button_name()
        self.assertEqual((u"切换为Master" or "Switch to Master"), result), "check switch to master button-1,fail!"
        print "check switch to master button-1,pass!"

    #failover ap上，检查切换master按钮-点击是否弹出确认框
    def test_025_check_switch_to_master_button_2(self):
        u"""failover ap上，检查切换master按钮-点击是否弹出确认框(testlink_ID:2358-2)"""
        log.debug("025")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #确认点击切换为master，是否弹出确认提示框
        result = tmp.check_click_switch_to_master()
        self.assertTrue(result), "check switch to master button-2,fail!"
        print "check switch to master button-2,pass!"

    #failover ap上，检查切换master按钮-弹出确认框点击取消
    def test_026_check_switch_to_master_button_3(self):
        u"""failover ap上，检查切换master按钮-弹出确认框点击取消(testlink_ID:2358-3)"""
        log.debug("026")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #点击切换为master后取消
        result1,result2 = tmp.check_cancel_switch_to_master(data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'])
        self.assertFalse(result1)
        self.assertTrue(result2), "check switch to master button-3,fail!"
        print "check switch to master button-3,pass!"

    #failover ap上，检查切换master按钮-弹出确认框点击确认
    def test_027_check_switch_to_master_button_4(self):
        u"""failover ap上，检查切换master按钮-弹出确认框点击确认(testlink_ID:2358-4)"""
        log.debug("027")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #点击切换为master后确认
        result = tmp.check_ok_switch_to_master(data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "check switch to master button-4,fail!"
        print "check switch to master button-4,pass!"

    #failover ap 切换到master ap模式后，能够发现未匹配的ap
    def test_028_failover_master_can_discover_ap(self):
        u"""failover ap 切换到master ap模式后，能够发现未匹配的ap(testlink_ID:2377)"""
        log.debug("028")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #搜索AP并判断，是否正确--backup
        result1 = tmp.search_AP_backup(data_AP["slave:mac1"])
        time.sleep(60)
        #搜索AP并配对并判断是否配对成功
        result2 = tmp.check_search_pair_special_AP(data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'], data_AP["slave:mac1"])
        #该ap恢复出厂配置
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_factory_reset_backup(data_basic['slave_ip2'])
        self.assertTrue(result1)
        self.assertTrue(result2), "after failover change to master can discover and pair ap, test fail!"
        print "after failover change to master can discover pair ap, test pass!"

    #failover ap 切换到master ap模式后，能够正常接管ap
    def test_029_failover_master_can_takeover_ap(self):
        u"""failover ap 切换到master ap模式后，能够正常接管ap(testlink_ID:2379)"""
        log.debug("029")
        tmp = APSBusiness(self.driver)
        #开启master ap的controller
        tmp.open_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        time.sleep(60)
        #搜索并配对特定的ap
        tmp.search_pair_AP(data_AP["slave:mac1"],data_AP["slave:mac2"])
        #设置slave ap2为failover ap
        tmp.change_slave_to_failover(data_AP["slave:mac2"])
        #master ap关闭controller
        tmp.close_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #等待10分钟
        time.sleep(610)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #设置failover ap为master ap
        tmp.change_failover_to_master()
        #登录后台，判断slave ap是否接管成功
        result = tmp.check_slave_ap_pair(data_basic['slave_ip2'],
            data_basic['sshUser'], data_login['all'], data_AP["slave:mac1"])
        self.assertTrue(result), "after failover change to master can take over ap, test fail!"
        print "after failover change to master can take over ap, test pass!"

    #failover ap 切换到master ap模式后，AP数量不变
    def test_030_failover_master_ap_num(self):
        u"""failover ap 切换到master ap模式后，AP数量不变(testlink_ID:2393)"""
        log.debug("030")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #确定在线ap的数量
        #点击接入点
        tmp.APS_menu()
        result = tmp.online_AP_num()
        self.assertEqual(3, result), "after failover change to master check ap num, test fail!"
        print "after failover change to master check ap num, test pass!"

    #failover ap 切换到master ap模式后，能够修改ap的配置
    def test_031_failover_master_can_modify_ap_configuration(self):
        u"""failover ap 切换到master ap模式后，能够修改ap的配置(testlink_ID:2381)"""
        log.debug("031")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #修改slave ap 2.4G无线信道为11
        tmp.set_slave_ap_2g4_channel(data_AP["slave:mac1"],"11")
        #修改failover ap 2.4G无线信道为10
        tmp.set_slave_ap_2g4_channel(data_AP["slave:mac2"],"10")
        time.sleep(60)
        #登录后台检查模式
        result1 = tmp.check_2g4_channel_backup(data_basic['slave_ip1'],
            data_login['all'], data_basic['sshUser'])
        result2 = tmp.check_2g4_channel_backup(data_basic['slave_ip2'],
            data_login['all'], data_basic['sshUser'])
        # self.assertIn("11", result1)
        # self.assertIn("10", result2), "after failover change to master can modify ap configuration, test fail!"
        print "after failover change to master can modify ap configuration, test pass!"

    #failover ap 切换到master ap模式后，能够修改网络组的配置
    def test_032_failover_master_can_modify_NG_configuration(self):
        u"""failover ap 切换到master ap模式后，能够修改网络组的配置(testlink_ID:2382)"""
        log.debug("032")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #修改网络组的ssid
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_ng['NG2_ssid'], data_wireless['short_wpa'])
        tmp2 = SSH(data_basic['slave_ip2'],data_login["all"])
        result1 = tmp2.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.ssid")
        result2 = tmp.connect_DHCP_WPA_AP(data_ng['NG2_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        self.assertIn(data_ng['NG2_ssid'], result1)
        self.assertIn(data_ng['NG2_ssid'], result2), "after failover change to master can modify network configuration, test fail!"
        print "after failover change to master can modify network configuration, test pass!"

    #failover ap 切换到master ap模式后，能够修改client的配置
    def test_034_failover_master_can_modify_client_configuration(self):
        u"""failover ap 切换到master ap模式后，能够修改client的配置(testlink_ID:2384)"""
        log.debug("034")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #修改客户端名字
        tmp1 = ClientsBusiness(self.driver)
        mac = tmp1.get_wlan_mac(data_basic['wlan_pc'])
        tmp1.change_client_name(mac, data_Client['letter_digital_name'])
        #获取第一个客户端的名称
        time.sleep(60)
        result = tmp1.check_client_name(mac)
        tmp1.dhcp_release_wlan(data_basic['wlan_pc'])
        self.assertEqual(data_Client['letter_digital_name'], result), "after failover change to master can modify client configuration, test fail!"
        print "after failover change to master can modify client configuration, test pass!"

    #failover ap 切换到master ap模式后，能够修改系统设置的配置
    def test_035_failover_master_can_modify_system_configuration(self):
        u"""failover ap 切换到master ap模式后，能够修改系统设置的配置(testlink_ID:2385)"""
        log.debug("035")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #修改user密码后，登录路由后台，验证是否修改成功
        tmp1 = AccessBusiness(self.driver)
        result = tmp1.check_change_user_pwd(data_login['all'],
            data_login['digital_pwd'], data_basic['slave_ip2'],
            data_basic['sshUser'])
        #该ap恢复出厂配置
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_factory_reset_backup(data_basic['slave_ip2'])
        #开启master ap的controller
        tmp.open_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #7000新建一个网络组，vid设为2,开启dhcp server
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_new_NG()
        self.assertIn(data_login['digital_pwd'], result), "after failover change to master can modify systemsetting configuration, test fail!"
        print "after failover change to master can modify systemsetting configuration, test pass!"

    #指定failover ap后，确定failover ap的功能正常
    def test_036_check_slave_failover_function(self):
        u"""指定failover ap后，确定failover ap的功能正常(testlink_ID:2369)"""
        log.debug("036")
        #点击网络组，添加一个新的指定VID的网络组
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_vlan_ssid(data_ng['NG2_ssid'], data_wireless['short_wpa'], "2")
        tmp = APSBusiness(self.driver)
        #搜索并配对特定的ap
        tmp.search_pair_AP(data_AP["slave:mac1"],data_AP["slave:mac2"])
        #设置slave ap2为failover ap
        tmp.change_slave_to_failover(data_AP["slave:mac2"])
        #slave加入第2个网络组
        tmp.add_slave_to_NG(data_AP["slave:mac2"], 2)
        #无线网卡连接该ap
        result = tmp.connect_WPA_AP(data_ng['NG2_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        self.assertIn(data_ng['NG2_ssid'], result), "after designating failover ap,check failover ap function,test fail!"
        print "after designating failover ap,check failover ap function,test pass!"

    #failover ap模式下，检查ap流量能正确显示
    def test_037_failover_check_flow(self):
        u"""failover ap 切换到master ap模式后，检查ap流量能正确显示(testlink_ID:2409)"""
        log.debug("037")
        tmp = APSBusiness(self.driver)
        #master ap关闭controller
        tmp.close_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #等待10分钟
        time.sleep(610)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #AP 下载/上传流量---master ap
        tmp1 = OVBusiness(self.driver)
        tmp1.set_AP_download_unload(data_ng['NG2_ssid'],
            data_wireless["short_wpa"], data_basic['wlan_pc'], data_basic['lan_pc'])
        # 作为failover登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login("failover", data_login['all'])
        #获取第一个ap下载流量
        result1, result2 = tmp1.get_AP_download()
        assert ("MB" in result1) or ("GB" in result1)
        self.assertLess(0, result2), "after failover change to master check ap traffic,test fail!"
        print "after failover change to master check ap traffic,test pass!"


    #failover ap 切换到master ap模式后，客户端不会断开
    def test_038_failover_master_client_keep_connecting(self):
        u"""failover ap 切换到master ap模式后，客户端不会断开(testlink_ID:2391)"""
        log.debug("038")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #设置failover ap为master ap
        tmp.change_failover_to_master()
        result = tmp.get_client_cmd_result("iw dev %s link"%data_basic['wlan_pc'])
        self.assertIn(data_ng['NG2_ssid'], result), "after failover change to master client won't disconnect, test fail!"
        print "after failover change to master client won't disconnect, test pass!"


    #failover ap 切换到master ap模式后，客户端数目不会改变
    def test_039_failover_master_check_client_num(self):
        u"""failover ap 切换到master ap模式后，客户端数目不会改变(testlink_ID:2394)"""
        log.debug("039")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        tmp1 = ClientsBusiness(self.driver)
        #点击客户端菜单
        tmp1.clients_menu()
        #获取客户端的数量
        result = tmp1.get_clients_num()
        self.assertEqual(1, result), "after failover change to master check client number, test fail!"
        print "after failover change to master check client number, test pass!"

    #failover ap 切换到master ap模式后，确认failover ap流量能正确更新到新的master ap上
    def test_040_failover_master_check_ap_flow(self):
        u"""failover ap 切换到master ap模式后，确认failover ap流量能正确更新到新的master ap上(testlink_ID:2395)"""
        log.debug("040")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        tmp1 = OVBusiness(self.driver)
        #获取第一个ap下载流量
        result1, result2 = tmp1.get_AP_download()
        assert ("MB" in result1) or ("GB" in result1)
        self.assertLess(0, result2), "after failover change to master check ap traffic,test fail!"
        print "after failover change to master check ap traffic,test pass!"

    #failover ap 切换到master ap模式后，确认failover ap已经切换成master ap模式
    def test_041_failover_master_check_change_success(self):
        u"""failover ap 切换到master ap模式后，确认failover ap已经切换成master ap模式(testlink_ID:2408)"""
        log.debug("041")
        #slave ap  变为failover 模式
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        result2 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.failover")
        self.assertIn("master", result1)
        self.assertIn("Entry not found", result2), "after failover change to master check change success,test fail!"
        print "when old master change success,test pass!"

    #failover ap 切换到master ap模式后，确认client 的流量有效
    def test_042_failover_master_check_client_flow(self):
        u"""failover ap 切换到master ap模式后，确认ap 的流量有效(testlink_ID:2396)"""
        log.debug("042")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #client下载流量统计的准确性
        tmp1 = OVBusiness(self.driver)
        result1, result2 = tmp1.check_client_download()
        assert ("MB" in result1) or ("GB" in result1)
        self.assertLess(0, result2), "after failover change to master check client traffic,test fail!"
        print "after failover change to master check client traffic,test pass!"

    #failover ap 切换到master ap模式后，指定slave ap1为新的failover ap
    def test_043_failover_master_designate_slave_to_failover(self):
        u"""failover ap 切换到master ap模式后，指定slave ap1为新的failover ap(testlink_ID:2418)"""
        log.debug("043")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #设置slave ap为failover ap
        tmp.change_slave_to_failover(data_AP['slave:mac1'])
        #检查slave ap是否变为failover ap
        result = tmp.check_change_to_failover_AP(data_AP['slave:mac1'],
                    data_basic['slave_ip2'], data_basic['sshUser'], data_login['all'])
        self.assertTrue(result), "after failover switch to master,designate another slave ot failover, test fail!"
        print "after failover switch to master,designate another slave ot failover, test pass!"


    #failover ap 切换到master ap模式后，当老的master ap回来，确认老master和现在master功能正常
    def test_044_failover_master_check_client_flow(self):
        u"""failover ap 切换到master ap模式后，当老的master ap回来，确认老master和现在master功能正常(testlink_ID:2403)"""
        log.debug("044")
        tmp = APSBusiness(self.driver)
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #现在的master ap解除slave ap1的配对
        tmp.unpair_special_slave_AP_backup(data_AP["slave:mac1"])
        #开启master ap的controller
        tmp.open_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        time.sleep(60)
        #无线网卡连接现在的master ap
        result1 = tmp.connect_WPA_AP(data_ng['NG2_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        #无线网卡连接老的master ap
        result2 = tmp.connect_WPA_AP(data_wireless['all_ssid'], data_wireless['short_wpa'],
            data_basic['wlan_pc'])
        #该ap恢复出厂配置
        tmp2 = UpgradeBusiness(self.driver)
        tmp2.web_factory_reset_backup(data_basic['slave_ip2'])

        #删除7000新建的网络组
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_del_NG()

        self.assertIn(data_ng['NG2_ssid'], result1)
        self.assertIn(data_wireless['all_ssid'], result2), "after failover change to master check client traffic,test fail!"
        print "after failover change to master check client traffic,test pass!"



    #failover ap 能正常切换到failover mode
    def test_045_slave_switch_failover_mode(self):
        u"""failover ap 能正常切换到failover mode(testlink_ID:2371,2374)"""
        log.debug("045")
        tmp = APSBusiness(self.driver)
        #搜索并配对特定的ap
        tmp.search_pair_AP(data_AP["slave:mac1"],data_AP["slave:mac2"])
        #设置slave ap2为failover ap
        tmp.change_slave_to_failover(data_AP["slave:mac2"])
        #master ap关闭controller
        tmp.close_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #等待10分钟
        time.sleep(610)
        #slave ap  变为failover 模式
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        result2 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.failover")
        self.assertIn("master", result1)
        self.assertIn("1", result2), "failover ap can switch to failover mode, test fail!"
        print "failover ap can switch to failover mode, test pass!"

    #当老的master ap回来后，failover ap将变回slave ap模式
    def test_046_failover_ruturn_slave(self):
        u"""当老的master ap回来后，failover ap将变回slave ap模式(testlink_ID:2397)"""
        log.debug("046")
        tmp = APSBusiness(self.driver)
        #开启master ap的controller
        tmp.open_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        time.sleep(60)
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        self.assertIn("slave", result), "when old master come back,failover return slave ap mode,test fail!"
        print "when old master come back,failover return slave ap mode,test pass!"

    #在10分钟后，master ap回来后，确认master 和failover ap正常
    def test_047_master_camebake_over_10mins(self):
        u"""在10分钟后，master ap回来后，确认master 和failover ap正常(testlink_ID:2373)"""
        log.debug("047")
        #检查master ap
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        self.assertIn("master", result), "Master ap came back over 10 mins,test fail!"
        print "Master ap came back over 10 mins,test pass!"

    #当老的master ap回来后，failover ap被master ap接管
    def test_048_failover_be_takenover(self):
        u"""当老的master ap回来后，failover ap被master ap接管(testlink_ID:2399)"""
        log.debug("048")
        tmp = APSBusiness(self.driver)
        #登录后台，判断slave ap是否配对成功
        result = tmp.check_slave_ap_pair(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'], data_AP["slave:mac2"])
        self.assertTrue(result), "when old master come back,failover be taken over,test fail!"
        print "when old master come back,failover be taken over,test pass!"

    #当老的master ap回来后，老的slave ap能够被接管
    def test_049_old_slave_be_takenover(self):
        u"""当老的master ap回来后，老的slave ap能够被接管(testlink_ID:2400)"""
        log.debug("049")
        tmp = APSBusiness(self.driver)
        #登录后台，判断slave ap是否配对成功
        result = tmp.check_slave_ap_pair(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'], data_AP["slave:mac1"])
        self.assertTrue(result), "when old master come back,old slave ap be taken over,test fail!"
        print "when old master come back,old slave ap be taken over,test pass!"

    #当老的master ap回来后，failover ap的webUI不能访问
    def test_050_failover_webUI_cannot_access(self):
        u"""当老的master ap回来后，failover ap的webUI不能访问(testlink_ID:2401)"""
        log.debug("050")
        tmp = APSBusiness(self.driver)
        #判断failover ap的页面是否能够访问
        result = tmp.check_access_failover_webUI(data_basic['slave_web2'])
        self.assertTrue(result), "when old master come back,failover webUI cannot access,test fail!"
        print "when old master come back,failover webUI cannot access,test pass!"

    #在10分钟内，master ap回来后，确认master 和failover ap正常
    def test_051_master_camebake_within_10mins(self):
        u"""在10分钟内，master ap回来后，确认master 和failover ap正常(testlink_ID:2372)"""
        log.debug("051")
        tmp = APSBusiness(self.driver)
        #master ap关闭controller
        tmp.close_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #等待3分钟
        time.sleep(180)
        #开启master ap的controller
        tmp.open_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        time.sleep(60)
        #检查master ap
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        #检查failover ap
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        self.assertIn("master", result1)
        self.assertIn("slave", result2), "Master ap came back with in 10 mins,test fail!"
        print "Master ap came back with in 10 mins,test pass!"

    #当master ap回来后，确认能够修改配置
    def test_052_master_cameback_can_update_configuration(self):
        u"""当master ap回来后，确认能够修改配置(testlink_ID:2406)"""
        log.debug("052")
        tmp1 = SSIDBusiness(self.driver)
        #删除所有的网络组
        tmp1.del_all_NG()
        #修改group0的ssid
        ssid = data_wireless['all_ssid']+"-9"
        tmp1.change_wifi_ssid_key(ssid,data_wireless['short_wpa'])
        #检查ssid是否修改成功
        result1 = tmp1.check_NG_ssid(data_basic["DUT_ip"],
            data_basic["sshUser"], data_login['all'])
        result2 = tmp1.check_NG_ssid(data_basic["slave_ip1"],
            data_basic["sshUser"], data_login['all'])
        result3 = tmp1.check_NG_ssid(data_basic["slave_ip2"],
            data_basic["sshUser"], data_login['all'])
        time.sleep(60)
        #解除slave1,slave2的配对
        tmp = APSBusiness(self.driver)
        tmp.unpair_last_slave_ap(2)
        self.assertIn(ssid, result1)
        self.assertIn(ssid, result2)
        self.assertIn(ssid, result3), "when master ap came back,check can update configuration,test fail!"
        print "when master ap came back,check can update configuration,test pass!"

    #当master ap回来后，确认能够发现ap
    def test_053_master_camebake_can_discover(self):
        u"""当master ap回来后，确认能够发现ap(testlink_ID:2404)"""
        log.debug("053")
        tmp = APSBusiness(self.driver)
        result = tmp.search_AP(data_AP["slave:mac1"],data_AP["slave:mac2"])
        self.assertTrue(result),"when master ap came back,check can discover ap,test fail!"
        print "when master ap came back,check can discover ap,test pass!"

    #当master ap回来后，确认能够配对ap
    def test_054_master_camebake_can_pair(self):
        u"""当master ap回来后，确认能够配对ap(testlink_ID:2405)"""
        log.debug("054")
        tmp = APSBusiness(self.driver)
        result = tmp.check_search_pair_AP(data_basic['DUT_ip'],\
                data_basic['sshUser'],data_login['all'],data_AP["slave:mac1"],
                data_AP["slave:mac2"])
        self.assertTrue(result),"when master ap came back,check can pair ap,test fail!"
        print "when master ap came back,check can pair ap,test pass!"

    #指定failover ap，并断开master ap后，10分钟内，重启failover ap
    def test_055_reboot_failover_switching(self):
        u"""指定failover ap，并断开master ap后，10分钟内，重启failover ap(testlink_ID:2413)"""
        log.debug("055")
        tmp = APSBusiness(self.driver)
        #设置slave ap2为failover ap
        tmp.change_slave_to_failover(data_AP["slave:mac2"])
        #master ap关闭controller
        tmp.close_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        #等待1分钟
        time.sleep(60)
        #重启failover ap
        tmp.reboot_router(data_basic['slave_ip2'],data_basic['sshUser'],
            data_login['all'])
        #等待3分钟
        time.sleep(180)
        #failover ap依然是slave ap模式
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        #等待10分钟
        time.sleep(610)
        #slave ap  变为failover 模式
        ssh = SSH(data_basic['slave_ip2'], data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        result2 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.failover")
        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'], "failover", data_login['all'])
        #设置failover ap为master ap
        tmp.change_failover_to_master()
        result3 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.role")
        result4 = ssh.ssh_cmd(data_basic['sshUser'], "uci show controller.main.failover")

        #登录failover ap的web界面
        tmp.login_failover_ap(data_basic['slave_web2'],
            data_basic['superUser'], data_login['all'])
        #该ap恢复出厂配置
        tmp2 = UpgradeBusiness(self.driver)
        tmp2.web_factory_reset_backup(data_basic['slave_ip2'])
        #开启master ap的controller
        tmp.open_master_controller(data_basic['DUT_ip'],
            data_basic['sshUser'], data_login['all'])
        time.sleep(60)
        self.assertIn("master", result1)
        self.assertIn("1", result2)
        self.assertIn("master", result3)
        self.assertIn("Entry not found", result4)
        self.assertIn("slave", result), "reboot failover ap, test fail!"
        print "reboot failover ap, test pass!"

    ####################################################################
    ##################以下是fallback IP的测试用例##################
    ####################################################################
    #disable/enable dhcp server when GWN76xx is in unpaired status,fallback IP works fine
    def test_056_check_fallback_IP_function(self):
        u"""disable/enable dhcp server when GWN76xx is in unpaired status,fallback IP works fine(testlink_ID:2335,2343)"""
        log.debug("056")
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

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("Failover")

        self.assertTrue(result1)
        self.assertTrue(result2), "dis/enable dhcp server,check fallback ip,test fail!"
        print "dis/enable dhcp server,check fallback ip,test pass!"


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
