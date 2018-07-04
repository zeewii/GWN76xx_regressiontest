#coding=utf-8
#作者：曾祥卫
#时间：2017.05.26
#描述：maintenance的用例集

import unittest,time
from selenium import webdriver
from system_settings.maintenance.access.access_business import AccessBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from system_settings.maintenance.basic.basic_business import BasicBusiness
from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from setupwizard.setupwizard_business import SWBusiness
from login.login_business import LoginBusiness
from data import data
from access_points.aps_business import APSBusiness
from navbar.navbar_business import NavbarBusiness
from connect.ssh import SSH
from data.logfile import Log

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
log = Log("Maintenance")

class TestMaintenance(unittest.TestCase):
    u"""测试维护的用例集(runtime:4h)"""
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

    ####################################################################
    ##################以下是升降级页面的测试用例#############################
    ####################################################################
    #设置上级GWN7000的配置，测试option 66 tftp降级(testlink_ID:1110_1)
    def test_002_option66_tftp_downgrade(self):
        u"""测试option 66 tftp降级(testlink_ID:1110_1)"""
        log.debug("002")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("66,%s"%data_basic['tftp_old_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['old_version'])
        assert result,"test option66 tftp downgrade,fail!"
        print "test option66 tftp downgrade,pass!"

    #设置上级GWN7000的配置，测试option 66tftp升级(testlink_ID:1110_2)
    def test_003_option66_tftp_upgrade(self):
        u"""测试option 66 tftp升级(testlink_ID:1110_2)"""
        log.debug("003")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("66,%s"%data_basic['tftp_new_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['version'])
        assert result,"test option66 tftp upgrade,fail!"
        print "test option66 tftp upgrade,pass!"

    #设置上级GWN7000的配置，测试option 66 http降级(testlink_ID:1110_1)
    def test_004_option66_http_downgrade(self):
        u"""设置上级GWN7000的配置，测试option 66 http降级(testlink_ID:1110_1)"""
        log.debug("004")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("66,http://%s"%data_basic['http_old_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['old_version'])
        assert result,"test option66 http downgrade,fail!"
        print "test option66 http downgrade,pass!"

    #设置上级GWN7000的配置，测试option 66http升级(testlink_ID:1110_2)
    def test_005_option66_http_upgrade(self):
        u"""测试option 66 http升级(testlink_ID:1110_2)"""
        log.debug("005")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("66,http://%s"%data_basic['http_new_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['version'])
        assert result,"test option66 http upgrade,fail!"
        print "test option66 http upgrade,pass!"

    #设置上级GWN7000的配置，测试option 66 https降级(testlink_ID:1110_1)
    def test_006_option66_https_downgrade(self):
        u"""设置上级GWN7000的配置，测试option 66 https降级(testlink_ID:1110_1)"""
        log.debug("006")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("66,https://%s"%data_basic['https_old_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['old_version'])
        assert result,"test option66 https downgrade,fail!"
        print "test option66 https downgrade,pass!"

    #设置上级GWN7000的配置，测试option 66https升级(testlink_ID:1110_2)
    def test_007_option66_https_upgrade(self):
        u"""测试option 66 https升级(testlink_ID:1110_2)"""
        log.debug("007")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("66,https://%s"%data_basic['https_new_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['version'])
        assert result,"test option66 https upgrade,fail!"
        print "test option66 https upgrade,pass!"

    #设置上级GWN7000的配置，测试option 43 tftp降级(testlink_ID:1114_1)
    def test_008_option43_tftp_downgrade(self):
        u"""测试option 43 tftp降级(testlink_ID:1114_1)"""
        log.debug("008")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("43,B.%s"%data_basic['tftp_old_addr'])
        #重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['old_version'])
        assert result,"test option43 tftp downgrade,fail!"
        print "test option43 tftp downgrade,pass!"

    #设置上级GWN7000的配置，测试option 43tftp升级(testlink_ID:1110_2)
    def test_009_option43_tftp_upgrade(self):
        u"""测试option 43 tftp升级(testlink_ID:1110_2)"""
        log.debug("009")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("43,B.%s"%data_basic['tftp_new_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['version'])
        assert result,"test option43 tftp upgrade,fail!"
        print "test option43 tftp upgrade,pass!"

    #设置上级GWN7000的配置，测试option 43 http降级(testlink_ID:1110_1)
    def test_010_option43_http_downgrade(self):
        u"""设置上级GWN7000的配置，测试option 43 http降级(testlink_ID:1110_1)"""
        log.debug("010")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("43,B.http://%s"%data_basic['http_old_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['old_version'])
        assert result,"test option43 http downgrade,fail!"
        print "test option43 http downgrade,pass!"

    #设置上级GWN7000的配置，测试option 43http升级(testlink_ID:1110_2)
    def test_011_option43_http_upgrade(self):
        u"""测试option 43 http升级(testlink_ID:1110_2)"""
        log.debug("011")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("43,B.http://%s"%data_basic['http_new_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['version'])
        assert result,"test option43 http upgrade,fail!"
        print "test option43 http upgrade,pass!"

    #设置上级GWN7000的配置，测试option 43 https降级(testlink_ID:1110_1)
    def test_012_option43_https_downgrade(self):
        u"""设置上级GWN7000的配置，测试option 43 https降级(testlink_ID:1110_1)"""
        log.debug("012")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("43,B.https://%s"%data_basic['https_old_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['old_version'])
        assert result,"test option43 https downgrade,fail!"
        print "test option43 https downgrade,pass!"

    #设置上级GWN7000的配置，测试option 43https升级(testlink_ID:1110_2)
    def test_013_option43_https_upgrade(self):
        u"""测试option 66 https升级(testlink_ID:1110_2)"""
        log.debug("013")
        #打开web登录7000,并进入网络组，修改网络组的dhcp选项
        tmp = NGBusiness(self.driver)
        tmp.mixed_7000_dhcp_option("43,B.https://%s"%data_basic['https_new_addr'])
        ##重启76xx并取出版本号来判断
        result = tmp.reboot_get_version(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'],data_basic['version'])

        #先把7000上值改为空
        tmp.mixed_7000_dhcp_option_blank()
        #然后重启7610
        tmp.reboot_router(data_basic['DUT_ip'],data_basic['sshUser'],\
                        data_login['all'])
        #检查ap重启完成
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.confirm_AP_reboot_finish(data_basic['DUT_ip'])
        assert result,"test option43 https upgrade,fail!"
        print "test option43 https upgrade,pass!"


    #测试http降级(testlink_ID:794_1)
    def test_014_http_downgrade(self):
        u"""测试http降级(testlink_ID:794_1)"""
        log.debug("014")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行http降级固件
        result = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['old_version'],data_basic['http_old_addr'],"HTTP")
        assert result,"test http downgrade,fail!"
        print "test http downgrade,pass!"

    #测试http升级(testlink_ID:794_2)
    def test_015_http_upgrade(self):
        u"""测试http升级(testlink_ID:794_2)"""
        log.debug("015")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行http升级固件
        result = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['version'],data_basic['http_new_addr'],"HTTP")
        assert result,"test http upgrade,fail!"
        print "test http upgrade,pass!"

    #测试https降级(testlink_ID:795_1)
    def test_016_https_downgrade(self):
        u"""测试https降级(testlink_ID:795_1)"""
        log.debug("016")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行https降级固件
        result = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['old_version'],data_basic['https_old_addr'],"HTTPS")
        assert result,"test https downgrade,fail!"
        print "test https downgrade,pass!"

    #测试https升级(testlink_ID:795_2)
    def test_017_https_upgrade(self):
        u"""测试https升级(testlink_ID:795_2)"""
        log.debug("017")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行https升级固件
        result = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['version'],data_basic['https_new_addr'],"HTTPS")
        assert result,"test https upgrade,fail!"
        print "test http upgrade,pass!"

    #测试tftp降级(testlink_ID:796_1)
    def test_018_tftp_downgrade(self):
        u"""测试tftp降级(testlink_ID:796_1)"""
        log.debug("018")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行tftp降级固件
        result = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['old_version'],data_basic['tftp_old_addr'],"TFTP")
        assert result,"test tftp downgrade,fail!"
        print "test tftp downgrade,pass!"

    #测试tftp升级(testlink_ID:796_2)
    def test_019_tftp_upgrade(self):
        u"""测试tftp升级(testlink_ID:796_2)"""
        log.debug("019")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行tftp升级固件
        result = tmp.upgrade_web(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['version'],data_basic['tftp_new_addr'],"TFTP")
        assert result,"test tftp upgrade,fail!"
        print "test tftp upgrade,pass!"

    #测试slave ap的升级(testlink_ID:798)
    def test_020_slave_ap_upgrade(self):
        u"""测试slave ap的升级(testlink_ID:798)"""
        log.debug("020")
        tmp = APSBusiness(self.driver)
        #没有配对的slave ap，先设置固件升级方式，然后搜索AP并配对然后升级slave ap的固件
        result = tmp.upgrade_slave_ap(data_basic['slave_ip1'],data_basic['slave_ip2'],data_basic['sshUser'],\
                    data_login['all'],data_basic['version'],data_basic['http_new_addr'],
                    "HTTP",data_AP['slave:mac1'],data_AP['slave:mac2'])
        #解除配对
        time.sleep(120)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        tmp.unpair_last_slave_ap(2)
        assert result,"test slave ap upgrade,fail!"
        print "test slave ap upgrade,pass!"

    #测试去掉upgrade on boot时，是否会降级(testlink_ID:809_1)
    def test_021_boot_downgrade(self):
        u"""测试cancel downgrade on boot(testlink_ID:809_1)"""
        log.debug("021")
        tmp = UpgradeBusiness(self.driver)
        result = tmp.upgrade_boot(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['version'],data_basic['http_old_addr'])
        assert result,"after cancelling downgrade on boot can't downgrade,fail!"
        print "after cancelling downgrade on boot can't downgrade,pass!"

    #测试勾上upgrade on boot时，是否会降级(testlink_ID:809_2)
    def test_022_boot_downgrade(self):
        u"""测试勾上 downgrade on boot(testlink_ID:809_2)"""
        log.debug("022")
        tmp = UpgradeBusiness(self.driver)
        result = tmp.upgrade_boot(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['old_version'],data_basic['http_old_addr'])
        assert result,"after clicking downgrade on boot can downgrade,fail!"
        print "after clicking downgrade on boot can downgrade,pass!"

    #测试去掉upgrade on boot时，是否会升级(testlink_ID:809_3)
    def test_023_boot_upgrade(self):
        u"""测试cancel upgrade on boot(testlink_ID:809_3)"""
        log.debug("023")
        tmp = UpgradeBusiness(self.driver)
        result = tmp.upgrade_boot(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['old_version'],data_basic['http_new_addr'])
        assert result,"after cancelling upgrade on boot can't upgrade,fail!"
        print "after cancelling upgrade on boot can't upgrade,pass!"

    #测试勾上upgrade on boot时，是否会升级(testlink_ID:809_4)
    def test_024_boot_upgrade(self):
        u"""测试勾上 upgrade on boot(testlink_ID:809_4)"""
        log.debug("024")
        tmp = UpgradeBusiness(self.driver)
        result = tmp.upgrade_boot(data_basic['DUT_ip'],data_basic['sshUser'],\
                data_login['all'],data_basic['version'],data_basic['http_new_addr'])
        assert result,"after clicking upgrade on boot can upgrade,fail!"
        print "after clicking upgrade on boot can upgrade,pass!"


    #################################################################
    #########以下是Reboot&Set Factory用例##############################
    #################################################################
    #webUI检查(testlink_ID:762)
    def test_025_check_reboot_reset_button(self):
        u"""webUI检查(testlink_ID:762)"""
        log.debug("025")
        tmp = UpgradeBusiness(self.driver)
        result1,result2 = tmp.check_reboot_reset_button()
        assert result1 == (u"重启" or "Reboot") and \
               result2 == (u"重置" or "Reset"),\
            "check reboot and reset button,test fail!"
        print "check reboot and reset button,test pass!"

    #重启确认(testlink_ID:764)
    def test_026_check_reboot_confirm(self):
        u"""重启确认(testlink_ID:764)"""
        log.debug("026")
        tmp = UpgradeBusiness(self.driver)
        result = tmp.check_reboot_confirm()
        assert result,"check confirm tip after clicking reboot,test fail!"
        print "check confirm tip after clicking reboot,test fail!"

    #点击重启后取消(testlink_ID:765)
    def test_027_check_cancel_reboot_confirm(self):
        u"""点击重启后取消(testlink_ID:765)"""
        log.debug("027")
        tmp = UpgradeBusiness(self.driver)
        result1,result2 = tmp.check_cancel_reboot_confirm(data_basic["DUT_ip"])
        assert (result1 == False) and (result2 == 0),"cancel reboot,test fail!"
        print "cancel reboot,test pass!"

    #点击重启并确认(testlink_ID:766)
    def test_028_check_ok_reboot_confirm(self):
        u"""点击重启后取消(testlink_ID:766)"""
        log.debug("028")
        #只有默认时，搜索-配对-加入网络组
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add_default(data_AP['slave:mac2'])
        tmp = UpgradeBusiness(self.driver)
        result1,result2 = tmp.check_ok_reboot_confirm(data_basic["DUT_ip"])
        assert (result1 != 0) and (result2 == 0),"confirm reboot,test fail!"
        print "confirm reboot,test pass!"

    #重启后配置检查(testlink_ID:767)
    def test_029_check_config(self):
        u"""重启后配置检查(testlink_ID:767)"""
        log.debug("029")
        tmp = SSH(data_basic["DUT_ip"],data_login["all"])
        result = tmp.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.ssid")
        assert data_wireless['all_ssid'] in result,"check config after rebooting,test fail!"
        print "check config after rebooting,test pass!"

    #Master上重启对其他设备的影响(testlink_ID:768)
    def test_030_check_slave_ap(self):
        u"""Master上重启对其他设备的影响(testlink_ID:768)"""
        log.debug("030")
        #判断是否还有slave ap的mac
        tmp= SSH(data_basic["DUT_ip"],data_login["all"])
        result = tmp.ssh_cmd(data_basic['sshUser'],"ubus call controller.discovery get_paired_devices")
        #mac地址去冒号
        tmp1 = UpgradeBusiness(self.driver)
        sm = data_AP["slave:mac2"].lower()
        m = tmp1.mac_drop(sm)
        assert m in result,"check effect after rebooting master ap,test fail!"
        print "check effect after rebooting master ap,test pass!"

    #恢复出厂确认(testlink_ID:769)
    def test_031_check_reset_confirm(self):
        u"""恢复出厂确认(testlink_ID:769)"""
        log.debug("031")
        tmp = UpgradeBusiness(self.driver)
        result = tmp.check_reset_confirm()
        assert result,"check confirm tip after clicking reset,test fail!"
        print "check confirm tip after clicking reset,test fail!"

    #点击重置后取消(testlink_ID:770)
    def test_032_check_cancel_reboot_confirm(self):
        u"""点击重置后取消(testlink_ID:770)"""
        log.debug("032")
        tmp = UpgradeBusiness(self.driver)
        result1,result2 = tmp.check_cancel_reset_confirm(data_basic["DUT_ip"])
        assert (result1 == False) and (result2 == 0),"cancel reset,test fail!"
        print "cancel reset,test pass!"

    #点击重置并确认(testlink_ID:771)
    def test_033_check_ok_reset_confirm(self):
        u"""点击重置并确认(testlink_ID:771)"""
        log.debug("033")
        #只有默认时，搜索-配对-加入网络组
        tmp = UpgradeBusiness(self.driver)
        result1,result2 = tmp.check_ok_reset_confirm(data_basic["DUT_ip"])
        tmp1 = SSH(data_basic["DUT_ip"],data_basic["super_defalut_pwd"])
        result3 = tmp1.ssh_cmd(data_basic['sshUser'],"uci show grandstream.general.admin_password")
        assert (result1 != 0) and (result2 == 0) and ("='admin'" in result3),"confirm reset,test fail!"
        print "confirm reset,test pass!"

    #恢复出厂后的系统配置情况(testlink_ID:772)
    def test_034_check_config(self):
        u"""恢复出厂后的系统配置情况(testlink_ID:772)"""
        log.debug("034")
        tmp = SSH(data_basic["DUT_ip"],data_basic["super_defalut_pwd"])
        result = tmp.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.ssid")
        assert data_wireless['all_ssid'] not in result,"check config after resetting,test fail!"
        print "check config after resetting,test pass!"

    #Master AP恢复出厂后状态检查(testlink_ID:773)
    def test_035_check_status(self):
        u"""Master AP恢复出厂后状态检查(testlink_ID:773)"""
        log.debug("035")
        element = self.driver.find_element_by_id('login_as_master')
        result = element.text
        print result
        assert result == "Login as master",\
            "check master ap status after resetting,test fail!"
        print "check master ap status after resetting,test pass!"

    #Master AP恢复出厂对Slave AP的影响(testlink_ID:774)
    def test_036_check_slave_ap(self):
        u"""Master AP恢复出厂对Slave AP的影响(testlink_ID:774)"""
        log.debug("036")
        #判断是否还有slave ap的mac
        tmp= SSH(data_basic["DUT_ip"],data_basic["super_defalut_pwd"])
        result = tmp.ssh_cmd(data_basic['sshUser'],"ubus call controller.discovery get_paired_devices")
        #mac地址去冒号
        tmp1 = UpgradeBusiness(self.driver)
        sm = data_AP["slave:mac2"].lower()
        m = tmp1.mac_drop(sm)
        assert m not in result,"check effect after rebooting master ap,test fail!"
        print "check effect after rebooting master ap,test pass!"

    #检查恢复出厂对版本的影响(testlink_ID:775)
    def test_037_check_version(self):
        u"""检查恢复出厂对版本的影响(testlink_ID:775)"""
        log.debug("037")
        tmp= SSH(data_basic["DUT_ip"],data_basic["super_defalut_pwd"])
        result = tmp.ssh_cmd(data_basic['sshUser'],"cat /tmp/gs_version")
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #使用新密码登录GWN7610的web界面
        tmp1 = LoginBusiness(self.driver)
        #调用实例的登录GWN76xx的web界面
        tmp1.login(data_basic['superUser'],data_basic["super_defalut_pwd"])
        #第一次登录页面需要设置管理员和用户密码
        tmp1.set_super_user_pwd(data_login["all"],data_login["all"],\
                              data_login["all"],data_login["all"])
        #关掉下次显示，并关闭设置向导
        tmp2 = SWBusiness(self.driver)
        tmp2.hidenexttime()
        tmp2.close_wizard()
        assert data_basic['version'] in result,"check version after resetting,test fail!"
        print "check version after resetting,test pass!"




    ###########################################################
    ############以下是Admin&User的测试用例########################
    ###########################################################
    #在页面上把AP恢复出厂设置
    def test_038_factory_reset(self):
        u"""在页面上把AP恢复出厂设置"""
        log.debug("038")
        tmp = APSBusiness(self.driver)
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #确认密码默认隐藏密钥(testlink_ID:870_1)
    def test_039_check_pwd_default_disappear(self):
        u"""确认密码默认隐藏密钥(testlink_ID:870_1)"""
        log.debug("039")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_pwd_default_disappear()
        assert result == ["password","password","password","password","password"],\
            "test default password is disappear,test fail!"
        print "test default password is disappear,test pass!"

    #点击显示后，确认密码能够显示(testlink_ID:870_2)
    def test_040_check_pwd_display(self):
        u"""确认密码默认隐藏密钥(testlink_ID:870_2)"""
        log.debug("040")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_pwd_display()
        assert result == ["text","text","text","text","text"],\
            "display password,test fail!"
        print "display password,test pass!"

    #修改所有密码时，当前密码错误时，弹出提示(testlink_ID:871)
    def test_041_check_pass0_err(self):
        u"""修改密码时，当前密码错误时，弹出提示(testlink_ID:871)"""
        log.debug("041")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_pass0_err(data_login['letter_pwd'],data_login['digital_pwd'])
        assert result,"when changing pwd,current pwd err,test fail!"
        print "when changing pwd,current pwd err,test pass!"

    #修改密码后，登录路由后台，验证是否修改成功
    def test_042_check_change_pwd(self):
        u"""修改密码后，登录路由后台，验证是否修改成功"""
        log.debug("042")
        tmp = AccessBusiness(self.driver)
        result1,result2 = tmp.check_change_pwd(data_login['all'],\
            data_login['digital_pwd'],data_login['letter_pwd'],\
                    data_basic['DUT_ip'],data_basic['sshUser'])
        #测试完后修改为常用密码
        tmp.change_pwd(data_login['digital_pwd'],data_login['all'],data_login['all'])
        tmp.apply()
        assert (data_login['digital_pwd'] in result1) and (data_login['letter_pwd'] in result2),\
            "after changing pwd,check pwd validity,test fail!"
        print "after changing pwd,check pwd validity,test pass!"

    #修改密码后，确认密码是隐藏密钥(testlink_ID:877)
    def test_043_check_pwd_disappear_again(self):
        u"""修改密码后，确认密码是隐藏密钥(testlink_ID:877)"""
        log.debug("043")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_pwd_disappear_again(data_login['all'],\
            data_login['digital_pwd'],data_login['letter_pwd'])
        #测试完后修改为常用密码
        tmp.change_pwd(data_login['digital_pwd'],data_login['all'],data_login['all'])
        tmp.apply()
        assert result == ["password","password","password","password","password"],\
            "test password is disappear again,test fail!"
        print "test password is disappear again,test pass!"

    #修改admin密码时，当前密码错误时，弹出提示(testlink_ID:882)
    def test_044_check_admin_pass0_err(self):
        u"""修改admin密码时，当前密码错误时，弹出提示(testlink_ID:882)"""
        log.debug("044")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_admin_pass0_err(data_login['letter_pwd'],data_login['digital_pwd'])
        assert result,"when changing admin pwd,current pwd err,test fail!"
        print "when changing admin pwd,current pwd err,test pass!"

    #修改admin密码后，登录路由后台，验证是否修改成功
    def test_045_check_change_admin_pwd(self):
        u"""修改admin密码后，登录路由后台，验证是否修改成功"""
        log.debug("045")
        tmp = AccessBusiness(self.driver)
        result1= tmp.check_change_admin_pwd(data_login['all'],\
            data_login['digital_pwd'],\
                    data_basic['DUT_ip'],data_basic['sshUser'])
        #测试完后修改为常用密码
        tmp.change_pwd(data_login['digital_pwd'],data_login['all'],data_login['all'])
        tmp.apply()
        assert (data_login['digital_pwd'] in result1) ,\
            "after changing admin pwd,check pwd validity,test fail!"
        print "after changing admin pwd,check pwd validity,test pass!"

    #修改admin密码后，确认密码是隐藏密钥(testlink_ID:877)
    def test_046_check_admin_pwd_disappear_again(self):
        u"""修改admin密码后，确认密码是隐藏密钥(testlink_ID:877)"""
        log.debug("046")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_admin_pwd_disappear_again(data_login['all'],\
            data_login['letter_pwd'])
        #测试完后修改为常用密码
        tmp.change_pwd(data_login['letter_pwd'],data_login['all'],data_login['all'])
        tmp.apply()
        assert result == ["password","password","password","password","password"],\
            "test admin password is disappear again,test fail!"
        print "test admin password is disappear again,test pass!"

    #修改user密码后，登录路由后台，验证是否修改成功
    def test_047_check_change_user_pwd(self):
        u"""修改user密码后，登录路由后台，验证是否修改成功"""
        log.debug("047")
        tmp = AccessBusiness(self.driver)
        result1= tmp.check_change_user_pwd(data_login['all'],\
            data_login['digital_pwd'],\
                    data_basic['DUT_ip'],data_basic['sshUser'])
        assert (data_login['digital_pwd'] in result1) ,\
            "after changing user pwd,check pwd validity,test fail!"
        print "after changing user pwd,check pwd validity,test pass!"

    #修改user密码后，确认密码是隐藏密钥(testlink_ID:877)
    def test_048_check_user_pwd_disappear_again(self):
        u"""修改user密码后，确认密码是隐藏密钥(testlink_ID:877)"""
        log.debug("048")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_user_pwd_disappear_again(data_login['letter_pwd'])
        assert result == ["password","password","password","password","password"],\
            "test user password is disappear again,test fail!"
        print "test user password is disappear again,test pass!"

    #修改admin密码，修改后仍然旧密码登录，确定不能登录成功(testlink_ID:879)
    def test_049_check_old_pwd_login(self):
        u"""修改admin密码，修改后仍然旧密码登录，确定不能登录成功(testlink_ID:879)"""
        log.debug("049")
        tmp = AccessBusiness(self.driver)
        result = tmp.use_pwd_login(data_login['all'],data_login['digital_pwd'],\
                        data_basic['superUser'],data_login['all'])
        assert result == False,"use old pwd login AP,test fail!"
        print "use old pwd login AP,test pass!"

    #使用修改后的密码登录，确认登录成功(testlink_ID:880)
    def test_050_check_new_pwd_login(self):
        u"""使用修改后的密码登录，确认登录成功(testlink_ID:880)"""
        log.debug("050")
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #使用新密码登录GWN7610的web界面
        tmp = LoginBusiness(self.driver)
        tmp.login(data_basic['superUser'],data_login['digital_pwd'])
        #判断是否登录成功
        result = tmp.login_test()
        #测试完后修改为常用密码
        tmp1 = AccessBusiness(self.driver)
        tmp1.change_pwd(data_login['digital_pwd'],data_login['all'],data_login['all'])
        tmp1.apply()
        assert result,"use new pwd login AP,test fail!"
        print "use new pwd login AP,test pass!"

    #修改admin密码时输入两次不一致的新密码(testlink_ID:883)
    def test_051_check_admin_pwd_different(self):
        u"""修改admin密码时输入两次不一致的新密码(testlink_ID:883)"""
        log.debug("051")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_admin_pwd_different(data_login['all'],data_login['digital_pwd'],\
                        data_login['letter_pwd'])
        assert result == (u"密码必须一致" or "Passwords must match"),\
            "when changing admin pwd,input twice pwd different,test fail!"
        print "when changing admin pwd,input twice pwd different,test pass!"

    #修改user密码时输入两次不一致的新密码(testlink_ID:891)
    def test_052_check_user_pwd_different(self):
        u"""修改user密码时输入两次不一致的新密码(testlink_ID:891)"""
        log.debug("052")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_user_pwd_different(data_login['digital_pwd'],\
                        data_login['letter_pwd'])
        assert result == (u"密码必须一致" or "Passwords must match"),\
            "when changing user pwd,input twice pwd different,test fail!"
        print "when changing user pwd,input twice pwd different,test pass!"

    #修改admin密码时只输入一次新密码(testlink_ID:884)
    def test_053_check_admin_pwd_once(self):
        u"""修改admin密码时只输入一次新密码(testlink_ID:884)"""
        log.debug("053")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_admin_pwd_once(data_login['all'],data_login['digital_pwd'],\
                            data_basic['DUT_ip'],data_basic['sshUser'])
        assert data_login['all'] in result,"input admin pwd only once,test fail!"
        print "input admin pwd only once,test pass!"

    #修改user密码时只输入一次新密码(testlink_ID:893)
    def test_054_check_user_pwd_once(self):
        u"""修改user密码时只输入一次新密码(testlink_ID:893)"""
        log.debug("054")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_user_pwd_once(data_login['digital_pwd'],data_login['all'],\
                            data_basic['DUT_ip'],data_basic['sshUser'])
        assert data_login['all'] in result,"input user pwd only once,test fail!"
        print "input user pwd only once,test pass!"

    #admin密码的大小写验证(testlink_ID:885)
    def test_055_check_admin_pwd_upper_lower(self):
        u"""admin密码的大小写验证(testlink_ID:885)"""
        log.debug("055")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_admin_pwd_different(data_login['all'],\
                    data_login['letter_pwd'],data_login['letter_pwd'].upper())
        assert result == (u"密码必须一致" or "Passwords must match"),\
            "ipunt admin pwd is lower and upper,test fail!"
        print "ipunt admin pwd is lower and upper,test pass!"

    #user密码的大小写验证(testlink_ID:892)
    def test_056_check_user_pwd_different(self):
        u"""user密码的大小写验证(testlink_ID:892)"""
        log.debug("056")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_user_pwd_different(data_login['letter_pwd'],\
                        data_login['letter_pwd'].upper())
        assert result == (u"密码必须一致" or "Passwords must match"),\
            "ipunt user pwd is lower and upper,test fail!"
        print "ipunt user pwd is lower and upper,test pass!"

    #修改admin密码时，输入和当前密码一样的新密码(testlink_ID:886)
    def test_057_check_same_admin_pwd(self):
        u"""修改admin密码时，输入和当前密码一样的新密码(testlink_ID:886)"""
        log.debug("057")
        #修改admin密码时，输入和当前密码一样的新密码
        tmp = AccessBusiness(self.driver)
        tmp.change_admin_pwd(data_login['all'],data_login['all'],data_login['all'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.general.admin_password")
        assert (data_login['all'] in result),"input same admin pwd,test fail!"
        print "input same admin pwd,test pass!"

    #登录web时先输入密码后输入用户名(testlink_ID:887)
    def test_058_check_exchange_admin_pwd(self):
        u"""登录web时先输入密码后输入用户名(testlink_ID:887)"""
        log.debug("058")
        tmp = AccessBusiness(self.driver)
        result = tmp.check_exchange_admin_pwd(data_basic['superUser'],data_login['all'])
        assert result,"exchange admin and pwd,test fail!"
        print "exchange admin and pwd,test pass!"

    #修改admin密码时，不输入当前密码，直接输入两次新密码(testlink_ID:888)
    def test_059_change_admin_no_current_pwd(self):
        u"""修改admin密码时，不输入当前密码，直接输入两次新密码(testlink_ID:888)"""
        log.debug("059")
        tmp = AccessBusiness(self.driver)
        result = tmp.change_admin_no_current_pwd(data_login['digital_pwd'])
        assert result,"change admin pwd but not input current pwd,test fail!"
        print "change admin pwd but not input current pwd,test pass!"

    #修改admin密码时，不输入当前密码，直接输入1次新密码(testlink_ID:889)
    def test_060_change_once_admin_no_current_pwd(self):
        u"""修改admin密码时，不输入当前密码，直接输入1次新密码(testlink_ID:889)"""
        log.debug("060")
        tmp = AccessBusiness(self.driver)
        result = tmp.change_once_admin_no_current_pwd(data_login['digital_pwd'])
        assert result == False,"change admin pwd but only input once pwd,test fail!"
        print "change admin pwd but only input once pwd,test pass!"

    #正确修改user密码后，用旧密码登录，确定不能登录成功(testlink_ID:894)
    def test_061_check_old_user_pwd_login(self):
        u"""正确修改密码后，用旧密码登录，确定不能登录成功(testlink_ID:894)"""
        log.debug("061")
        tmp = AccessBusiness(self.driver)
        result = tmp.use_user_pwd_login(data_login['digital_pwd'],\
                                data_basic['user'],data_login['all'])
        print result
        assert result == False,"use old user pwd login AP,test fail!"
        print "use old user pwd login AP,test pass!"

    #正确修改user密码后，用修改后的新密码登录，确认登录成功(testlink_ID:895)
    def test_062_check_new_user_pwd_login(self):
        u"""正确修改user密码后，用修改后的新密码登录，确认登录成功(testlink_ID:895)"""
        log.debug("062")
        #点击页面上的退出按钮
        tmp = NavbarBusiness(self.driver)
        tmp.logout()
        #使用新密码登录GWN7610的web界面
        tmp1 = LoginBusiness(self.driver)
        tmp1.login(data_basic['user'],data_login['digital_pwd'])
        #判断是否登录成功
        result = tmp1.login_test()
        print result
        assert result,"use new pwd login AP,test fail!"
        print "use new pwd login AP,test pass!"

    #user账号的权限验证(testlink_ID:896)
    def test_063_check_user_range(self):
        u"""user账号的权限验证(testlink_ID:896)"""
        log.debug("063")
        tmp = AccessBusiness(self.driver)
        result1 = tmp.check_user_range(data_basic['user'],data_login['digital_pwd'])
        #判断是否登录成功
        tmp1 = LoginBusiness(self.driver)
        result2 = tmp1.login_test()
        print result1,result2
        assert (result1 == False) and result2,"test user range,test fail!"
        print "test user range,test pass!"

    #用admin账号的密码登录user(testlink_ID:897)
    def test_064_adminpwd_to_user(self):
        u"""用admin账号的密码登录user(testlink_ID:897)"""
        log.debug("064")
        #点击页面上的退出按钮
        tmp1 = NavbarBusiness(self.driver)
        tmp1.logout()
        tmp = LoginBusiness(self.driver)
        tmp.login(data_basic['user'],data_login['all'])
        #判断是否登录成功
        result = tmp.login_test()
        print result
        assert result == False,"use admin's pwd login user,test fail!"
        print "use admin's pwd login user,test pass!"

    #用user账号的密码登录admin(testlink_ID:898)
    def test_065_userpwd_to_admin(self):
        u"""用user账号的密码登录admin(testlink_ID:898)"""
        log.debug("065")
        #点击页面上的退出按钮
        tmp1 = NavbarBusiness(self.driver)
        tmp1.logout()
        tmp = LoginBusiness(self.driver)
        tmp.login(data_basic['superUser'],data_login['digital_pwd'])
        #判断是否登录成功
        result = tmp.login_test()
        print result
        assert result == False,"use user's pwd login admin,test fail!"
        print "use user's pwd login admin,test pass!"

    #修改user密码，再用不完整的新密码登录web(testlink_ID:899)
    def test_066_user_incomplete(self):
        u"""修改user密码，再用不完整的新密码登录web(testlink_ID:899)"""
        log.debug("066")
        #点击页面上的退出按钮
        tmp1 = NavbarBusiness(self.driver)
        tmp1.logout()
        tmp = LoginBusiness(self.driver)
        tmp.login(data_basic['user'],data_login['digital_pwd'].strip("123"))
        #判断是否登录成功
        result = tmp.login_test()
        print result

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("Maintenance")

        assert result == False,"use incomplete pwd login,test fail!"
        print "use incomplete pwd login,test pass!"



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
