#coding=utf-8
#作者：曾祥卫
#时间：2017.04.24
#描述：用例层代码，调用clients_business

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
from data.logfile import Log

reload(sys)
sys.setdefaultencoding('utf-8')
log = Log("Clients")
data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_AP = data.data_AP()
data_ng = data.data_networkgroup()
data_client = data.data_Client()


class TestClients(unittest.TestCase):
    u"""测试客户端的用例集(runtime:1h)"""
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
        #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
        log.debug("001")
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
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'], data_basic['wlan_pc'])
        #禁用启用有线网卡，以便无线网卡能够在ap的client页面显示在线
        tmp.wlan_disable(data_basic['lan_pc'])
        tmp.wlan_enable(data_basic['lan_pc'])
        time.sleep(60)
        tmp.dhcp_release_wlan(data_basic["wlan_pc"])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #无线网卡连接上ap后，查看客户端信息(testlink_ID:485)
    def test_002_connect_clients_info(self):
        u"""无线网卡连接上ap后，查看客户端信息(testlink_ID:485)"""
        log.debug("002")
        tmp = ClientsBusiness(self.driver)
        Lg = LoginBusiness(self.driver)
        #使用无线网卡能够连接上ssid,并正常使用
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        Lg.refresh_login_ap()
        #获取客户端的mac地址
        result1 = tmp.check_client(data_basic['wlan_pc'])
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result2 = tmp.get_online_status(wlan_mac)
        print result1,result2
        assert result1 and ((u"在线" or 'Online') in result2),"test after connecting ap,clients info,test fail!"
        print "test after connecting ap,clients info,test pass!"

    #连接方式(无线)信息核对(testlink_ID:488)
    def test_003_check_connected_info(self):
        u"""连接方式(无线)信息核对(testlink_ID:488)"""
        log.debug("003")
        tmp = ClientsBusiness(self.driver)
        #点击客户端菜单
        tmp.clients_menu()
        #获取第一个客户端的类型
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.get_cient_type(wlan_mac)
        assert result == (u"无线" or "Wireless"),"Check wireless connected type info,test fail!"
        print "Check wireless connected type info,test pass!"

    #IP地址信息核对(testlink_ID:489)--bug78714
    def test_004_check_ip(self):
        u"""IP地址信息核对(testlink_ID:489)--bug78714"""
        log.debug("004")
        tmp = ClientsBusiness(self.driver)
        #点击客户端菜单
        tmp.clients_menu()
        #获取第一个客户端的IP地址
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.get_client_IP(wlan_mac)
        print "client ip on Client page is "+result
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        assert result != "","Check IP address on client page,test fail!"
        print "Check IP address on client page,test pass!"

    #连接时间信息核对--15s更新一次(testlink_ID:490)
    def test_005_check_connected_time(self):
        u"""连接时间信息核对--15s更新一次(testlink_ID:490)"""
        log.debug("005")
        tmp = ClientsBusiness(self.driver)
        #点击客户端菜单
        tmp.clients_menu()
        self.driver.refresh()
        #获取第一个客户端的连接时间
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result1 = tmp.get_client_time(wlan_mac)
        time.sleep(16)
        result2 = tmp.get_client_time(wlan_mac)
        assert result1 != result2,"Check updated time on client page,test fail!"
        print "Check updated time on client page,test pass!"

    #客户端离线后再上线，其连接时间重新开始更新(testlink_ID:491)
    def test_006_check_disconnect_connect_uptime(self):
        u"""客户端离线后再上线，其连接时间重新开始更新(testlink_ID:491)"""
        log.debug("006")
        tmp = ClientsBusiness(self.driver)
        result = tmp.disconnect_connect_uptime(data_basic['wlan_pc'])
        print result
        assert result,"restart connected time after disconnect and then connect client,test fail!"
        print "restart connected time after disconnect and then connect client,test pass!"

    #AP的mac地址信息核对(testlink_ID:492)
    def test_007_check_AP_mac(self):
        u"""AP的mac地址信息核对(testlink_ID:492)"""
        log.debug("007")
        tmp = ClientsBusiness(self.driver)
        #点击客户端菜单
        tmp.clients_menu()
        #获取客户端所连接的AP名称或mac
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.get_AP_name(wlan_mac)
        MasterAP = data_AP['master:mac'].upper()
        print result,MasterAP
        assert result == MasterAP,"Check AP mac,test fail!"
        print "Check AP mac,test pass!"

    #ssid0+无线+客户端显示(testlink_ID:494)
    def test_008_check_ssid0(self):
        u"""ssid0+无线+客户端显示(testlink_ID:494)"""
        log.debug("008")
        tmp = ClientsBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        client_mac,ssid_name,connecttype,conap = tmp.check_ssid(wlan_mac)
        print client_mac,ssid_name,connecttype,conap
        #得到无线客户端的mac
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        Mac = mac.upper()
        #得到master ap的mac
        MasterAP = data_AP['master:mac'].upper()
        assert (client_mac == Mac) and (ssid_name == data_wireless['all_ssid']) and \
            (connecttype == (u"无线" or "Wireless")) and (conap == MasterAP),\
            "Check ssid0+wireless+client display,test fail!"
        print "Check ssid0+wireless+client display,test pass!"

    #新建立的ssid1+有线或无线+用户客户端显示(testlink_ID:496)
    def test_009_check_ssid1(self):
        u"""新建立的ssid1+有线或无线+用户客户端显示(testlink_ID:496)"""
        log.debug("009")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        #新建一个SSID
        tmp = SSIDBusiness(self.driver)
        tmp.new_ssid(NG2_ssid,data_wireless["short_wpa"])
        #将master ap加入所有的ssids
        tmp1 = APSBusiness(self.driver)
        tmp1.add_master_to_all_NG()
        #使用无线网卡能够连接上NG2的ssid,并正常使用
        tmp1.connect_WPA_AP(NG2_ssid,data_wireless['short_wpa'],data_basic['wlan_pc'])
        tmp2 = ClientsBusiness(self.driver)
        #得到无线客户端的mac
        mac = tmp2.get_wlan_mac(data_basic['wlan_pc'])
        client_mac,ssid_name,connecttype,conap = tmp2.check_ssid(mac)
        print client_mac,ssid_name,connecttype,conap
        Mac = mac.upper()
        #得到master ap的mac
        MasterAP = data_AP['master:mac'].upper()
        assert (client_mac == Mac) and (ssid_name == NG2_ssid) and \
            (connecttype == (u"无线" or "Wireless")) and (conap == MasterAP),\
            "Check newssid+wireless+client display,test fail!"
        print "Check newssid+wireless+client display,test pass!"

    #ssid的客户端信息过滤1--选择ssid0没有客户端(testlink_ID:497_1)
    def test_010_check_ssid_filter1(self):
        u"""ssid的客户端信息过滤1--选择ssid0没有客户端(testlink_ID:497_1)--bug"""
        log.debug("010")
        tmp = ClientsBusiness(self.driver)
        result = tmp.check_ssid_filter(data_wireless['all_ssid'],data_basic['wlan_pc'])
        assert result == False,"Check client through ssid filter1,test fail!"
        print "Check client through ssid filter1,test pass!"

    #ssid的客户端信息过滤2--选择ssid1有客户端(testlink_ID:497_2)
    def test_011_check_ssid_filter2(self):
        u"""ssid的客户端信息过滤--选择ssid1有客户端(testlink_ID:497_2)--bug"""
        log.debug("011")
        tmp = ClientsBusiness(self.driver)
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        result = tmp.check_ssid_filter(NG2_ssid,data_basic['wlan_pc'])
        assert result,"Check client through ssid filter2,test fail!"
        print "Check client through ssid filter2,test pass!"

    #无线网卡断开ap后，查看客户端信息(testlink_ID:501)
    def test_012_disconnect_clients_info(self):
        u"""无线网卡断开ap后，查看客户端信息(testlink_ID:501)"""
        log.debug("012")
        tmp = ClientsBusiness(self.driver)
        #无线网卡断开已连接的AP
        tmp.wlan_disable(data_basic['wlan_pc'])
        #获取客户端的mac地址
        result1 = tmp.check_client(data_basic['wlan_pc'])
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result2 = tmp.get_offline_status(wlan_mac)
        print result1,result2
        #删除SSID1
        tmp1 = SSIDBusiness(self.driver)
        tmp1.del_all_NG()
        #使用无线网卡能够连接上ssid,并正常使用
        tmp.wlan_enable(data_basic['wlan_pc'])
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result1 and ((u"离线" or 'Offline') in result2),"test after disconnecting ap,test fail!"
        print "test after disconnecting ap,test pass!"

    #设置用户名为全数字(testlink_ID:512)
    def test_013_set_client_digital(self):
        u"""设置用户名为全数字(testlink_ID:512)"""
        log.debug("013")
        tmp = ClientsBusiness(self.driver)
        #客户端名称设置为不合法时
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result1,result2 = tmp.check_set_client_name(wlan_mac,data_client['digital_name'])
        assert result1 and result2,"set client name is digital,test fail!"
        print "set client name is digital,test pass!"

    #设置用户名为全字母(testlink_ID:513)
    def test_014_set_client_letter(self):
        u"""设置用户名为全字母(testlink_ID:513)"""
        log.debug("014")
        tmp = ClientsBusiness(self.driver)
        #只有一个客户端时，修改客户端名称
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.change_client_name(wlan_mac,data_client['letter_name'])
        #重启ap
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        tmp1.connect_WPA_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #获取第一个客户端的名称
        result = tmp.check_client_name(wlan_mac)
        assert result == data_client['letter_name'],"set client name is letter,test fail!"
        print "set client name is letter,test pass!"

    #设置用户名为---(testlink_ID:514)
    def test_015_set_client_err_name1(self):
        u"""设置用户名为---(testlink_ID:514)"""
        log.debug("015")
        tmp = ClientsBusiness(self.driver)
        #客户端名称设置为不合法时
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result1,result2 = tmp.check_set_client_name(wlan_mac,data_client['err_name1'])
        assert result1 and result2,"set client name is ---,test fail!"
        print "set client name is ---,test pass!"

    #设置用户名为___(testlink_ID:515)
    def test_016_set_client_err_name2(self):
        u"""设置用户名为___(testlink_ID:515)"""
        log.debug("016")
        tmp = ClientsBusiness(self.driver)
        #客户端名称设置为不合法时
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result1,result2 = tmp.check_set_client_name(wlan_mac,data_client['err_name2'])
        assert result1 and result2,"set client name is ___,test fail!"
        print "set client name is ___,test pass!"

    #设置用户名为全字母+数字(testlink_ID:512+513)
    def test_017_set_client_letter_digital(self):
        u"""设置用户名为全字母+数字(testlink_ID:512+513)"""
        log.debug("017")
        tmp = ClientsBusiness(self.driver)
        #只有一个客户端时，修改客户端名称
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.change_client_name(wlan_mac,data_client['letter_digital_name'])
        #重启ap
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        tmp1.connect_WPA_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #获取第一个客户端的名称
        result = tmp.check_client_name(wlan_mac)
        assert result == data_client['letter_digital_name'],"set client name is letter+digital,test fail!"
        print "set client name is letter+digital,test pass!"

    #删除设置用户名称后，用户再次连接后主机名显示为用户本身名字(testlink_ID:516)
    def test_018_del_client_name(self):
        u"""删除设置用户名称后，用户再次连接后主机名显示为用户本身名字(testlink_ID:516)"""
        log.debug("018")
        tmp = ClientsBusiness(self.driver)
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #只有一个客户端时，修改客户端名称
        tmp.change_client_name(wlan_mac,"")
        #重启ap
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        tmp1.connect_DHCP_WPA_AP(data_wireless['all_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #获取第一个客户端的名称
        result = tmp.check_client_name(wlan_mac)
        #取测试平台的name
        PC_name = subprocess.check_output("hostname",shell=True).strip("\n")
        print result,PC_name
        # tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        assert (result == PC_name) or (result == ""),"del client name,test fail!"
        print "del client name,test pass!"


    #Block client时的确认框(testlink_ID:517)
    def test_019_check_confirm_box(self):
        u"""Block client时的确认框(testlink_ID:517)"""
        log.debug("019")
        tmp = ClientsBusiness(self.driver)
        #Block client时的确认框
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        result = tmp.check_confirm_box(wlan_mac)
        assert result == True,"check confirm box Blocking client,test fail!"
        print "check confirm box Blocking client,test pass!"

    #block客户端后，判断客户端不能够连接(testlink_ID:518)
    def test_020_block_client(self):
        u"""block客户端后，判断客户端不能够连接(testlink_ID:518)"""
        log.debug("020")
        tmp = ClientsBusiness(self.driver)
        #使用无线网卡能够连接上ssid,并正常使用
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #只有一个客户端，阻塞该客户端
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.block_client(wlan_mac)
        #测试机上判断无线客户端是否依然是连接上的
        result = tmp.get_client_cmd_result("iw dev %s link"%data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"after blocking client,it can't connect AP,test fail!"
        print "after blocking client,it can't connect AP,test pass!"

    #Block wireless client后MAC地址会出现在Global Blacklist MAC(testlink_ID:519)
    def test_021_check_block_client(self):
        u"""Block wireless client后MAC地址会出现在Global Blacklist MAC(testlink_ID:519)"""
        log.debug("021")
        tmp = ClientAccessBusiness(self.driver)
        #获取Global Blacklist的mac地址
        result = tmp.get_Global_Blacklist_mac()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        assert mac.upper() in result,"After block wifi,check client mac in Global Blacklist MAC,test fail!"
        print "After block wifi,check client mac in Global Blacklist MAC,test pass!"

    #被blocked的wireless终端重连WLAN(testlink_ID:520)
    def test_022_connect_AP_again(self):
        u"""被blocked的wireless终端重连WLAN(testlink_ID:520)"""
        log.debug("022")
        tmp = ClientsBusiness(self.driver)
        #使用无线网卡能够连接上ssid,并正常使用
        result = tmp.connect_WPA_AP_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert 'Not connected' in result,"after blocking client,client connect ap again,test fail!"
        print "after blocking client,client connect ap again,test pass!"

    #在Global Blacklist MAC列表里删除已被block的终端MAC，判断客户端能够连接ap成功(testlink_ID:522)
    def test_023_unblock_client(self):
        u"""在Global Blacklist MAC列表里删除已被block的终端MAC，判断客户端能够连接ap成功(testlink_ID:522)"""
        log.debug("023")
        tmp = ClientAccessBusiness(self.driver)
        #删除Global Blacklist里面的所有的mac
        tmp.del_Global_Blacklist_mac()
        #使用无线网卡能够连接上ssid,并正常使用
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['all_ssid'] in result,"after unblocking client,it can connect AP,test fail!"
        print "after unblocking client,it can connect AP,test pass!"

    #被block的终端重连WLAN后再被block(testlink_ID:523)
    def test_024_unblock_block(self):
        u"""被block的终端重连WLAN后再被block(testlink_ID:523)"""
        log.debug("024")
        tmp = ClientsBusiness(self.driver)
        #只有一个客户端，阻塞该客户端
        wlan_mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.block_client(wlan_mac)
        #测试机上判断无线客户端是否依然是连接上的
        result = tmp.get_client_cmd_result("iw dev %s link"%data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"block client again,test fail!"
        print "block client again,test pass!"

    #被block的终端重连WLAN后再被block后Global Blacklist MAC列表验证(testlink_ID:524)
    def test_025_check_block_client_again(self):
        u"""被block的终端重连WLAN后再被block后Global Blacklist MAC列表验证(testlink_ID:524)"""
        log.debug("025")
        tmp = ClientAccessBusiness(self.driver)
        #获取Global Blacklist的mac地址
        result = tmp.get_Global_Blacklist_mac()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #删除Global Blacklist里面的所有的mac
        tmp.del_Global_Blacklist_mac()
        #使用无线网卡能够连接上ssid,并正常使用
        tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert mac.upper() in result,"After block wifi again,check client mac in Global Blacklist MAC,test fail!"
        print "After block wifi again,check client mac in Global Blacklist MAC,test pass!"

    #unblock客户端，然后在ap页面上执行重启,确认无线能够连接上ap
    def test_026_web_reboot(self):
        u"""unblock客户端，然后在ap页面上执行重启,确认无线能够连接上ap"""
        log.debug("026")
        tmp = UpgradeBusiness(self.driver)
        #在ap页面上执行重启
        tmp.web_reboot(data_basic['DUT_ip'])
        #使用无线网卡能够连接上ssid,并正常使用
        result = tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        #描述：使无线网卡释放IP地址
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("Clients")
        assert data_wireless['all_ssid'] in result,"test web reboot,test fail!"
        print "test web reboot,test pass!"


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
