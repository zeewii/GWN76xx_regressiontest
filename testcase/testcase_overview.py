#coding=utf-8
#作者：曾祥卫
#时间：2017.03.22
#描述：用例集，调用OVbusiness

import unittest,time
from selenium import webdriver
from login.login_business import LoginBusiness
from overview.overview_business import OVBusiness
from access_points.aps_business import APSBusiness
from setupwizard.setupwizard_business import SWBusiness
from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from clients.clients_business import ClientsBusiness
from data import data
from connect.ssh import SSH
from data.logfile import Log
data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_ap = data.data_AP()
log = Log("Overview")
class TestOverView(unittest.TestCase):
    u"""测试概览的用例集(runtime:1h40m)"""
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

    #在页面上把AP恢复出厂设置，并运行设置向导并配对slave ap，修改ssid，密码(testlink_ID:773)
    def test_001_factory_reset_setupwizard(self):
        u"""在页面上把AP恢复出厂设置，并运行设置向导并配对slave ap，修改ssid，密码(testlink_ID:773)"""
        log.debug("001")
        #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
        Lg = LoginBusiness(self.driver)
        Lg.login_again()
        tmp = APSBusiness(self.driver)
        #描述：启用无线网卡
        tmp.wlan_enable(data_basic['wlan_pc'])
        #rsyslog服务器准备
        tmp.ready_rsyslog()
        result1 = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        #运行设置向导并配对slave ap，修改ssid，密码
        time.sleep(60)
        tmp1 = SWBusiness(self.driver)
        result2 = tmp1.complete_backup(data_wireless['all_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'],
                                data_ap["slave:mac2"])

        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],data_wireless['short_wpa'], data_basic['wlan_pc'])
        #禁用启用有线网卡，以便无线网卡能够在ap的client页面显示在线
        tmp.wlan_disable(data_basic['lan_pc'])
        tmp.wlan_enable(data_basic['lan_pc'])
        time.sleep(60)
        tmp.dhcp_release_wlan(data_basic["wlan_pc"])

        print result1,result2
        assert result1 and result2,"reset the AP defalut config and run setupwizard in webpage,fail!"
        print "reset the AP defalut config and run setupwizard in webpage,pass!"

    #AP状态窗（实时更新）(testlink_ID:1135)
    def test_002_AP_status(self):
        u"""AP状态窗（实时更新）(testlink_ID:1135)"""
        log.debug("002")
        tmp = OVBusiness(self.driver)
        #获取全部AP数
        result1 = tmp.get_aptotal()
        #检查AP的页面
        result2 =\
            tmp.check_ap()
        #解除最后两个slave AP的配对
        tmp1 = APSBusiness(self.driver)
        tmp1.unpair_last_slave_ap(1)
        assert (result1 == "3") and (result2 == ['1','2']),"check AP status,test fail!"
        print "check AP status,test pass!"

    #已发现AP数量统计-已发现，但未配对(testlink_ID:1136)
    def test_003_AP_num_unpair(self):
        u"""已发现AP数量统计-已发现，但未配对(testlink_ID:1136)"""
        log.debug("003")
        tmp = OVBusiness(self.driver)
        #获取全部AP数
        result1 = tmp.get_aptotal()
        #检查AP的页面
        result2 = tmp.check_ap()
        assert (result1 == "3") and (result2 == ['2','1']),"check AP number on unpair slave ap,test fail!"
        print "check AP number on unpair slave ap,test pass!"

    #已发现AP数量统计-发现后，配对AP，AP数量不统计在发现AP中(testlink_ID:1137)
    def test_004_AP_num_pair(self):
        u"""已发现AP数量统计-发现后，配对AP，AP数量不统计在发现AP中(testlink_ID:1137)"""
        log.debug("004")
        #只有默认时，搜索-配对-加入网络组
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add_default(data_ap["slave:mac2"])
        #返回概览页面
        tmp = OVBusiness(self.driver)
        tmp.OV_menu()
        #获取已发现的AP数
        time.sleep(30)
        result = tmp.get_apdiscovered()
        assert result == "1","check AP number on pair slave ap,test fail!"
        print "check AP number on pair slave ap,test pass!"

    #在线AP数量统计-在线AP 数量正确(testlink_ID:1139)
    def test_005_AP_num_online(self):
        u"""已发现的AP离线后，发现统计数目将更新(testlink_ID:1139)"""
        log.debug("005")
        tmp = OVBusiness(self.driver)
        #获取在线的AP数
        result = tmp.get_aponline()
        assert result == "2","check AP online number,test fail!"
        print "check AP online number,test pass!"

    #AP总量统计正确(testlink_ID:1143)
    def test_006_AP_total(self):
        u"""AP总量统计正确(testlink_ID:1143)"""
        log.debug("006")
        tmp = OVBusiness(self.driver)
        #获取在线的AP数
        result = tmp.get_aptotal()
        assert result == "3","check AP total number,test fail!"
        print "check AP total number,test pass!"

    #点击窗口右上角可以跳转到接入点页面(testlink_ID:1147)
    def test_007_goto_AP_webpage(self):
        u"""点击窗口右上角可以跳转到接入点页面(testlink_ID:1147)"""
        log.debug("007")
        tmp = OVBusiness(self.driver)
        result = tmp.goto_AP_webpage()
        assert result,"click goto button can't goto AP webpage,test fail!"
        print "click goto button can goto AP webpage,test pass!"

    #AP数量和状态必须与接入点页面的信息一致(testlink_ID:1148)
    def test_008_check_AP_webpage_online_num(self):
        u"""AP数量和状态必须与接入点页面的信息一致(testlink_ID:1148)"""
        log.debug("008")
        tmp1 = APSBusiness(self.driver)
        tmp1.APS_menu()
        result = tmp1.online_AP_num()
        #解除最后一个slave AP的配对
        tmp1.unpair_last_slave_ap(1)
        assert result == 2,"check AP number is different as AP webpage online,test fail!"
        print "check AP number is same as AP webpage online,test pass!"

    #客户端状态窗（实时更新）(testlink_ID:1150)
    def test_009_clients_status(self):
        u"""客户端状态窗（实时更新）(testlink_ID:1150)"""
        log.debug("009")
        #修改默认网络组的ssid和密码
        tmp = OVBusiness(self.driver)
        #使用无线连接该AP
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],\
                data_wireless["short_wpa"],data_basic['wlan_pc'])
        #等待2分钟
        time.sleep(120)
        #切换到overview菜单
        tmp.OV_menu()
        result = tmp.get_clientstotal()
        assert result == "1","check clients status,test fail!"
        print "check clients status,test pass!"

    #2.4G/5G 用户数量统计(testlink_ID:1151,1152)
    def test_010_clients_num(self):
        u"""2.4G/5G 用户数量统计(testlink_ID:1151,1152)"""
        log.debug("010")
        tmp = OVBusiness(self.driver)
        #获取2.4G客户端数
        result1 = tmp.get_2g4_client()
        #获取5G客户端数
        result2 = tmp.get_5g_client()
        #释放无线网卡的ip
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        #AP切换到2.4G
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_AP_Freq("2.4GHz")
        assert (result1 == "1") or (result2 == "1"),"check clients number,test fail!"
        print "check clients number,test pass!"

    #终端设备在2.4G上， 检查用户数量统计是否正确(testlink_ID:1153_1)
    def test_011_2g4_client_num(self):
        u"""终端设备在2.4G上， 检查用户数量统计是否正确(testlink_ID:1153_1)"""
        log.debug("011")
        tmp = OVBusiness(self.driver)
        #使用无线连接该AP
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless["short_wpa"],data_basic['wlan_pc'])
        #等待2分钟
        time.sleep(120)
        #获取2.4G客户端数
        result = tmp.get_2g4_client()
        #释放无线网卡的ip
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        #AP切换到5G
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_AP_Freq("5GHz")
        assert result == "1","check 2.4G client number,test fail!"
        print "check 2.4G client number,test pass!"

    #终端设备在5G上， 检查用户数量统计是否正确(testlink_ID:1153_2)
    def test_012_5g_client_num(self):
        u"""终端设备在5G上， 检查用户数量统计是否正确(testlink_ID:1153_2)"""
        log.debug("012")
        tmp = OVBusiness(self.driver)
        #使用无线连接该AP
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless["short_wpa"],data_basic['wlan_pc'])
        time.sleep(120)
        # 获取5G客户端数
        result = tmp.get_5g_client()
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        #释放无线网卡的ip
        tmp.disconnect_ap()
        #AP切换到双频
        #切换Dual-Band频段
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_AP_Freq("Dual-Band")
        #7000上新建一个网络组，vid设为2,开启dhcp server
        tmp2 = NGBusiness(self.driver)
        tmp2.mixed_7000_new_NG()
        assert result == "1","check 5G client number,test fail!"
        print "check 5G client number,test pass!"

    #终端设备关联在Slave AP上和不同的network group，检查用户数量统计是否正确(testlink_ID:1155,1156)
    def test_013_slave_AP_client_num(self):
        u"""终端设备关联在Slave AP上，检查用户数量统计是否正确(testlink_ID:1155,1156)"""
        log.debug("013")
        #新增一个ssid
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        Add = SSIDBusiness(self.driver)
        Add.new_vlan_ssid(NG2_ssid,data_wireless["short_wpa"],"2")
        #多个网络组时，搜索-配对-加入ssid
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add(2,data_ap["slave:mac2"])
        #使用无线连接slave AP
        tmp1.connect_DHCP_WPA_AP(NG2_ssid,\
                    data_wireless["short_wpa"],data_basic['wlan_pc'])
        #等待2分钟
        time.sleep(120)
        tmp = OVBusiness(self.driver)
        tmp.OV_menu()
        #获取2.4G客户端数
        result1 = tmp.get_2g4_client()
        #获取5G客户端数
        result2 = tmp.get_5g_client()
        #释放无线网卡的ip
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        assert (result1 == "1") or (result2 == "1"),\
            "check clients number when client connect slave AP,test fail!"
        print "check clients number when client connect slave AP,test pass!"

    #AP解除配对后，只要在客户端列表，依然统计在该AP上关联的终端设备(testlink_ID:1158)
    def test_014_unpair_client_num(self):
        u"""AP解除配对后，只要在客户端列表，依然统计在该AP上关联的终端设备(testlink_ID:1158)"""
        log.debug("014")
        #解除最后一个slave AP的配对
        tmp1 = APSBusiness(self.driver)
        tmp1.unpair_last_slave_ap(1)
        tmp = OVBusiness(self.driver)
        tmp.OV_menu()
        #获取2.4G客户端数
        result1 = tmp.get_2g4_client()
        #获取5G客户端数
        result2 = tmp.get_5g_client()
        #使用无线连接master AP
        tmp.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert (result1 == "1") or (result2 == "1"),\
            "check clients number when client connect slave AP,test fail!"
        print "check clients number when client connect slave AP,test pass!"

    #点击窗口右上角可以跳转客户端页面(testlink_ID:1159)
    def test_015_goto_Clients_webpage(self):
        u"""点击窗口右上角可以跳转客户端页面(testlink_ID:1159)"""
        log.debug("015")
        tmp = OVBusiness(self.driver)
        result = tmp.goto_Client_webpage()
        assert result,"click goto button can't goto Clients webpage,test fail!"
        print "click goto button can goto Clients webpage,test pass!"

    #Client数量和状态必须与客户端页面的信息一致(testlink_ID:1160)
    def test_016_check_Clients_webpage(self):
        u"""Client数量和状态必须与客户端页面的信息一致(testlink_ID:1160)"""
        log.debug("016")
        tmp = OVBusiness(self.driver)
        #获取2.4G客户端数
        result1 = tmp.get_2g4_client()
        #获取5G客户端数
        result2 = tmp.get_5g_client()
        result = (int(result1)+int(result2))
        tmp1 = ClientsBusiness(self.driver)
        tmp1.clients_menu()
        num = tmp1.get_clients_num()
        assert result == num,"check client number is different as Clients webpage,test fail!"
        print "check client number is same as Clients webpage,test pass!"

    #Client数量和状态必须与AP配置页面的client信息一致(testlink_ID:1161)
    def test_017_check_AP_webpage(self):
        u"""Client数量和状态必须与AP配置页面的client信息一致(testlink_ID:1161)"""
        log.debug("017")
        tmp = OVBusiness(self.driver)
        #获取2.4G客户端数
        result1 = tmp.get_2g4_client()
        #获取5G客户端数
        result2 = tmp.get_5g_client()
        result = (int(result1)+int(result2))
        #获取所有用户设备数
        tmp1 = APSBusiness(self.driver)
        num = tmp1.check_users_num()
        assert result == num,"check client number is different as AP webpage,test fail!"
        print "check client number is same as AP webpage,test pass!"

    #AP 下载流量统计的准确性---master ap(testlink_ID:1196_1)---有概率性bug
    def test_018_masterAP_download(self):
        u"""AP 下载流量统计的准确性---master ap(testlink_ID:1196_1)---有概率性bug"""
        log.debug("018")
        tmp = OVBusiness(self.driver)
        #AP 下载流量统计的准确性---master ap
        result1,result2 = tmp.check_masterAP_download_backup(data_wireless['all_ssid'],\
                data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'],
                data_ap['master:mac'])
        assert ("MB" in result1) or ("GB" in result1),"check master ap download fail!"
        print "check master ap download pass!"

    #AP 上传流量统计的准确性---master ap(testlink_ID:1195_1)---有概率性bug
    def test_019_masterAP_upload(self):
        u"""AP 上传流量统计的准确性---master ap(testlink_ID:1195_1)---有概率性bug"""
        log.debug("019")
        tmp = OVBusiness(self.driver)
        #AP 上传流量统计的准确性---master ap
        result1,result2 = tmp.check_masterAP_upload_backup(data_wireless['all_ssid'],\
                data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'],
                data_ap['master:mac'])
        #master AP切换到Dual-Band
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_AP_Freq("Dual-Band")

        assert ("MB" in result1) or ("GB" in result1),"check master ap upload fail!"
        print "check master ap upload pass!"

    #AP 下载流量统计的准确性---slave ap(testlink_ID:1196_2)---有概率性bug
    def test_020_slaveAP_download(self):
        u"""AP 下载流量统计的准确性---slave ap(testlink_ID:1196_2)---有概率性bug"""
        log.debug("020")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        #多个网络组时，搜索-配对-加入网络组
        tmp1 = APSBusiness(self.driver)
        tmp1.search_pair_add(2,data_ap["slave:mac2"])

        tmp = OVBusiness(self.driver)
        tmp.OV_menu()
        #AP 下载流量统计的准确性---有概率性bug
        result1,result2 = tmp.check_slaveAP_download_backup(NG2_ssid,\
                data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'],
                data_ap["slave:mac2"])
        assert ("MB" in result1) or ("GB" in result1),"check slave ap download fail!"
        print "check slave ap download pass!"

    #AP 上传流量统计的准确性---slave ap(testlink_ID:1195_2)---有概率性bug
    def test_021_slaveAP_upload(self):
        u"""AP 上传流量统计的准确性---slave ap(testlink_ID:1195_2)---有概率性bug"""
        log.debug("021")
        NG2_ssid = "%s-2"%data_ng["NG2_ssid"]
        tmp = OVBusiness(self.driver)
        #AP 上传流量统计的准确性---slave ap
        result1,result2 = tmp.check_slaveAP_upload_backup(NG2_ssid,\
                data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'],
                data_ap["slave:mac2"])
        #删除7000新建的网络组
        tmp1 = NGBusiness(self.driver)
        tmp1.mixed_7000_del_NG()

        assert ("MB" in result1) or ("GB" in result1),"check slave ap upload fail!"
        print "check slave ap upload pass!"

    #TOP AP状态窗（每5分钟更新）(testlink_ID:1178)---有概率性bug
    def test_022_TOP_AP(self):
        u"""TOP AP状态窗（每5分钟更新）(testlink_ID:1178)---有概率性bug"""
        log.debug("022")
        tmp2 = OVBusiness(self.driver)
        #已有添加一个slave ap到默认网络组后，检查TOP页面
        result = tmp2.step_001_check_top(data_ap['master:mac'],data_ap['slave:mac2'],\
            data_wireless['all_ssid'],data_basic['wlan_pc'])
        print result
        assert result,"Check TOP AP status,test fail!"
        print "Check TOP AP status,test pass!"

    #Slave AP可以显示在Top AP列表中(testlink_ID:1180)---有概率性bug
    def test_023_check_slave_AP(self):
        u"""Slave AP可以显示在Top AP列表中(testlink_ID:1180)---有概率性bug"""
        log.debug("023")
        tmp = OVBusiness(self.driver)
        result = tmp.get_top()
        assert (data_ap['slave:mac2'].upper() in result),"slave ap in TOP AP,test fail!"
        print "slave ap in TOP AP,test pass!"

    #Master AP可以显示在Top AP列表中(testlink_ID:1181)---有概率性bug
    def test_024_check_master_AP(self):
        u"""Master AP可以显示在Top AP列表中(testlink_ID:1181)---有概率性bug"""
        log.debug("024")
        tmp = OVBusiness(self.driver)
        result = tmp.get_top()
        assert (data_ap['master:mac'].upper() in result),"master ap in TOP AP,test fail!"
        print "master ap in TOP AP,test pass!"

    #AP 类型可以正确显示(testlink_ID:1191)---有概率性bug
    def test_025_check_AP_type(self):
        u"""AP 类型可以正确显示(testlink_ID:1191)---有概率性bug"""
        log.debug("025")
        tmp = OVBusiness(self.driver)
        #登录web页面获取DUT的hostname
        DUT_hostname = tmp.get_DUT_hostname()
        result = tmp.get_top()
        assert (DUT_hostname in result),"AP type in TOP AP,test fail!"
        print "AP type in TOP AP,test pass!"

    #点击TOP AP右上角的三个小点，页面将跳转到接入点页面(testlink_ID:1179)
    def test_026_goto_Clients_webpage(self):
        u"""点击TOP AP右上角的三个小点，页面将跳转到接入点页面(testlink_ID:1179)"""
        log.debug("026")
        tmp = OVBusiness(self.driver)
        result = tmp.goto_TOP_AP_webpage()
        assert result,"click goto button can't goto AP webpage,test fail!"
        print "click goto button can goto AP webpage,test pass!"

    #点击TOP SSID右上角的三个小点，页面将跳转到网络组页面(testlink_ID:1201)
    def test_027_goto_NG_webpage(self):
        u"""点击TOP SSID右上角的三个小点，页面将跳转到网络组页面(testlink_ID:1201)"""
        log.debug("027")
        tmp = OVBusiness(self.driver)
        result = tmp.goto_NG_webpage()
        assert result,"click goto button can't goto network  group webpage,test fail!"
        print "click goto button can goto network group webpage,test pass!"

    #ssid 上传流量统计的准确性(testlink_ID:1214)---有概率性bug
    def test_028_SSID_upload(self):
        u"""ssid 上传流量统计的准确性(testlink_ID:1214)---有概率性bug"""
        log.debug("028")
        #ssid 上传流量统计的准确性
        tmp = OVBusiness(self.driver)
        result1,result2 = tmp.check_ssid_upload()
        assert ("MB" in result1) or ("GB" in result1),"test ssid upload fail!"
        print "test ssid upload pass!"

    #ssid 下载流量统计的准确性(testlink_ID:1215)
    def test_029_SSID_download(self):
        u"""ssid 下载流量统计的准确性(testlink_ID:1215)"""
        log.debug("029")
        #ssid 下载流量统计的准确性
        tmp = OVBusiness(self.driver)
        result1,result2 = tmp.check_ssid_download()
        assert ("MB" in result1) or ("GB" in result1),"test ssid upload fail!"
        print "test ssid upload pass!"


    #点击TOP clients右上角的三个小点，页面将跳转到客户端页面(testlink_ID:1220)
    def test_030_goto_TOP_Clients_webpage(self):
        u"""点击TOP clients右上角的三个小点，页面将跳转到客户端页面(testlink_ID:1220)"""
        log.debug("030")
        tmp = OVBusiness(self.driver)
        result = tmp.goto_TOP_Clients_webpage()
        assert result,"click goto button can't goto Clients webpage,test fail!"
        print "click goto button can goto Clients webpage,test pass!"

    #client 上传流量统计的准确性(testlink_ID:1224)
    def test_031_client_upload(self):
        u"""client 上传流量统计的准确性(testlink_ID:1224)"""
        log.debug("031")
        #client 上传流量统计的准确性
        tmp = OVBusiness(self.driver)
        result1,result2 = tmp.check_client_upload()
        assert ("MB" in result1) or ("GB" in result1),"test client upload fail!"
        print "test client upload pass!"

    #client 下载流量统计的准确性(testlink_ID:1225)
    def test_032_client_download(self):
        u"""client 下载流量统计的准确性(testlink_ID:1225)"""
        log.debug("032")
        #client下载流量统计的准确性
        tmp = OVBusiness(self.driver)
        result1,result2 = tmp.check_client_download()

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("OverView")

        assert ("MB" in result1) or ("GB" in result1),"test client upload fail!"
        print "test client upload pass!"





    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
