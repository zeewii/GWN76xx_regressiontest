#coding=utf-8
#作者：曾祥卫
#时间：2017.05.23
#描述：用例集，调用navbar_business

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ssid.ssid_business import SSIDBusiness
from login.login_business import LoginBusiness
from navbar.navbar_business import NavbarBusiness
from access_points.aps_business import APSBusiness
from data import data
from data.logfile import Log
data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_AP = data.data_AP()
data_navbar = data.data_navbar()
log = Log("Navbar")
class TestNavbar(unittest.TestCase):
    u"""测试导航的用例集(runtime:40m)"""
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
        #修改默认ssid和密码
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

    #######################################################################
    #############################以下是搜索的用例##########################
    #######################################################################

    #进入登录界面，确认没有搜索按钮(testlink_ID:1277)
    def test_002_check_search_login_web(self):
        u"""进入登录界面，确认没有搜索按钮(testlink_ID:1277)"""
        log.debug("002")
        tmp = NavbarBusiness(self.driver)
        #点击页面上的退出按钮
        tmp.logout()
        #检查页面中是否有搜索按钮
        result = tmp.check_search_buttton()
        assert result == False,"test no search button in login web,test fail!"
        print "test no search button in login web,test pass!"

    #登录后主界面，确认有搜索按钮,点击搜索按钮，确定弹出搜索框(testlink_ID:1278)
    def test_003_check_search_main_web(self):
        u"""登录后主界面，确认有搜索按钮,点击搜索按钮，确定弹出搜索框(testlink_ID:1278)"""
        log.debug("003")
        tmp = NavbarBusiness(self.driver)
        result1,result2 = tmp.check_search()
        assert result1 and result2,"test search button and input in main web,test fail!"
        print "test search button and input in main web,test pass!"

    #在搜索框中输入为空，无搜索结果展示(testlink_ID:1279)
    def test_004_check_search_blankvalue(self):
        u"""在搜索框中输入为空，无搜索结果展示(testlink_ID:1279)"""
        log.debug("004")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_blankvalue_search()
        assert result == False,"test input blank value in search input,test fail!"
        print "test input blank value in search input,test pass!"

    #输入不存在信息(testlink_ID:1280)
    def test_005_check_search_inexistence(self):
        u"""输入不存在信息(testlink_ID:1280)"""
        log.debug("005")
        tmp = NavbarBusiness(self.driver)
        #输入不存在信息，获取搜索结果
        result = tmp.search_result(data_navbar['inexistence_info'])
        assert (u"对不起, 没有匹配的结果" or "Sorry,no matching results") in result,"test input inexistence info,test fail!"
        print "test input inexistence info,test fail!"

    #输入存在的AP的mac地址(testlink_ID:1281_1)
    def test_006_check_search_AP(self):
        u"""输入存在的AP的mac地址(testlink_ID:1281_1)"""
        log.debug("006")
        tmp = NavbarBusiness(self.driver)
        #输入存在的master AP的mac地址
        mac1 = data_AP['master:mac']
        #mac地址去掉冒号
        mac = tmp.mac_drop(mac1)
        id_element = 'oper-addtozone-btn'
        result = tmp.click_result(mac,id_element)
        print result
        assert result,"test input master ap mac,test fail!"
        print "test input master ap mac,test pass!"

    #输入存在的客户端mac地址(testlink_ID:1281_2)---bug80460
    def test_007_check_search_client(self):
        u"""输入存在的客户端mac地址(testlink_ID:1281_2)---bug80460"""
        log.debug("007")
        tmp = NavbarBusiness(self.driver)
        #客户端连接上AP
        tmp.connect_WPA_AP(data_wireless['all_ssid'],data_wireless["short_wpa"],\
                           data_basic["wlan_pc"])
        time.sleep(60)
        #获取无线客户端的mac地址
        client_mac1 = tmp.get_wlan_mac(data_basic["wlan_pc"])
        #mac地址去掉冒号
        mac = tmp.mac_drop(client_mac1)
        id = 'mac_%s'%mac
        result = tmp.click_result(mac,id)
        print result
        assert result,"test input client mac,test fail!"
        print "test input client mac,test pass!"

    #输入存在的SSID(testlink_ID:1281_4)
    def test_008_check_search_SSID(self):
        u"""输入存在的SSID(testlink_ID:1281_4)"""
        log.debug("008")
        tmp = NavbarBusiness(self.driver)
        result = tmp.click_result(data_wireless['all_ssid'],"del_ssid0")
        print result
        assert result,"test input SSID,test fail!"
        print "test input SSID,test pass!"

    #多字符输入-最大32位(testlink_ID:1282)
    def test_009_check_search_max_letter(self):
        u"""多字符输入-最大32位(testlink_ID:1282)"""
        log.debug("009")
        tmp = NavbarBusiness(self.driver)
        #输入信息
        tmp.search_result(data_wireless['long_ssid']+"abc")
        #获取搜索框中输入内容
        result = tmp.get_search_result_info()
        assert ((data_wireless['long_ssid']+"abc") not in result) and (data_wireless['long_ssid'] in result),\
        "test max letter,test fail!"
        print "test max letter,test pass!"

    #输入规则(testlink_ID:1283)
    def test_010_check_upper_lower(self):
        u"""输入规则(testlink_ID:1283)"""
        log.debug("010")
        tmp = NavbarBusiness(self.driver)
        #输入存在的master AP的mac地址
        mac1 = data_AP['master:mac']
        #小写mac地址
        mac = mac1.lower()
        #大写mac地址
        MAC = mac1.upper()
        #mac地址去掉冒号
        mac_result = tmp.mac_drop(mac)
        #先输入小写的mac地址，并获取搜索结果
        result1 = tmp.search_result(mac)
        #关闭搜索框
        tmp.search_menu()
        #再输入大写的mac地址，并获取搜索结果
        result2 = tmp.search_result(MAC)
        assert (mac_result in result1) and (mac_result in result2),\
        "test upper and lower letter,test fail!"
        print "test upper and lower letter,test pass!"

    #模糊搜索--只输入存在的MAC地址的一个或多个字符(testlink_ID:1284_1)
    def test_011_check_search_vague(self):
        u"""模糊搜索--只输入存在的MAC地址的一个或多个字符(testlink_ID:1284_1)"""
        log.debug("011")
        tmp = NavbarBusiness(self.driver)
        #master AP的mac地址
        mac1 = data_AP['master:mac']
        #mac地址通过冒号分割成多个字符串
        mac = mac1.split(":")
        #mac地址去掉冒号
        mac_result = tmp.mac_drop(mac1)
        #输入mac地址最后两个字符串
        result = tmp.search_result(mac[-1])
        assert mac_result in result,"test vague search mac,test fail!"
        print "test vague search mac,test pass!"

    #模糊搜索--只输入存在的SSID名称的一个或多个字符(testlink_ID:1284_2)
    def test_012_check_search_vague(self):
        u"""模糊搜索--只输入存在的SSID名称的一个或多个字符(testlink_ID:1284_2)"""
        log.debug("012")
        tmp = NavbarBusiness(self.driver)
        #获取SSID
        SSID = data_wireless['all_ssid']
        #mac地址通过冒号分割成多个字符串
        vague_SSID = SSID.split("-")
        #输入SSID最前面的字符
        result = tmp.search_result(vague_SSID[0])
        assert SSID in result,"test vague search SSID,test fail!"
        print "test vague search SSID,test pass!"

    #多次点击Enter键(testlink_ID:1285)
    def test_013_check_search_many_Enter(self):
        u"""多次点击Enter键(testlink_ID:1285)"""
        log.debug("013")
        tmp = NavbarBusiness(self.driver)
        #点击页面上的放大镜打开搜索框
        tmp.search_menu()
        #在弹出的搜索框中输入信息,并在键盘中按enter
        tmp.set_search("group0")
        #点击10次Enter
        for i in range(10):
            element = self.driver.find_element_by_id("searchinput")
            element.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(10)
        result = tmp.get_search_result()
        print len(result)
        assert len(result) < 8,"test search click many Enter,test fail!"
        print "test search click many Enter,test pass!"

    #点击其他菜单,搜索框消失(testlink_ID:1286)
    def test_014_check_search_mouse(self):
        u"""点击其他菜单,搜索框消失(testlink_ID:1286)"""
        log.debug("014")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_mouse()
        assert result == False,"test search input disappear after click other menu,test fail! "
        print "test search input disappear after click other menu,test pass! "



    #######################################################################
    #############################以下是刷新时间的用例##########################
    #######################################################################

    #进入登录界面，确认没有刷新按钮(testlink_ID:1262)
    def test_015_check_refresh_login_web(self):
        u"""进入登录界面，确认没有刷新按钮(testlink_ID:1262)"""
        log.debug("015")
        tmp = NavbarBusiness(self.driver)
        #点击页面上的退出按钮
        tmp.logout()
        #检查页面中是否有搜索按钮
        result = tmp.check_refresh_buttton()
        print result
        assert result == False,"test no refresh button in login web,test fail!"
        print "test no refresh button in login web,test pass!"

    #登录后主界面，确认有刷新按钮(testlink_ID:1263)
    def test_016_check_refresh_main_web(self):
        u"""登录后主界面，确认有刷新按钮(testlink_ID:1263)"""
        log.debug("016")
        tmp = NavbarBusiness(self.driver)
        #检查页面中是否有搜索按钮
        result = tmp.check_refresh_buttton()
        print result
        assert result,"test have refresh button in main web,test fail!"
        print "test have refresh button in main web,test pass!"

    #获取默认刷新时间为15s(testlink_ID:1264)
    def test_017_check_refresh_default_time(self):
        u"""获取默认刷新时间为15s(testlink_ID:1264)"""
        log.debug("017")
        tmp = NavbarBusiness(self.driver)
        #获取刷新时间
        result = tmp.get_refresh_time()
        assert "15s" in result,"test default refresh time,test fail!"
        print "test default refresh time,test pass!"

    #刷新时间选择区显示检测-15s(testlink_ID:1265_1)
    def test_018_check_refresh_choose_15s(self):
        u"""刷新时间选择区显示检测-15s(testlink_ID:1265_1)"""
        log.debug("018")
        tmp = NavbarBusiness(self.driver)
        #选择刷新时间，切换到其他界面，和登出后在登录，检查刷新时间
        result = tmp.check_change_refresh_time("15s",\
                    data_basic['superUser'],data_login['all'])
        print result
        assert result,"test refresh time is 15s,test fail!"
        print "test refresh time is 15s,test fail!"

    #刷新时间选择区显示检测-1min(testlink_ID:1265_2)
    def test_019_check_refresh_choose_1min(self):
        u"""刷新时间选择区显示检测-1min(testlink_ID:1265_2)"""
        log.debug("019")
        tmp = NavbarBusiness(self.driver)
        #选择刷新时间，切换到其他界面，和登出后在登录，检查刷新时间
        result = tmp.check_change_refresh_time("1min",\
                    data_basic['superUser'],data_login['all'])
        print result
        assert result,"test refresh time is 1min,test fail!"
        print "test refresh time is 1min,test fail!"

    #刷新时间选择区显示检测-2min(testlink_ID:1265_3)
    def test_020_check_refresh_choose_2min(self):
        u"""刷新时间选择区显示检测-2min(testlink_ID:1265_3)"""
        log.debug("020")
        tmp = NavbarBusiness(self.driver)
        #选择刷新时间，切换到其他界面，和登出后在登录，检查刷新时间
        result = tmp.check_change_refresh_time("2min",\
                    data_basic['superUser'],data_login['all'])
        print result
        assert result,"test refresh time is 2min,test fail!"
        print "test refresh time is 2min,test fail!"

    #刷新时间选择区显示检测-5min(testlink_ID:1265_4)
    def test_021_check_refresh_choose_5min(self):
        u"""刷新时间选择区显示检测-5min(testlink_ID:1265_4)"""
        log.debug("021")
        tmp = NavbarBusiness(self.driver)
        #选择刷新时间，切换到其他界面，和登出后在登录，检查刷新时间
        result = tmp.check_change_refresh_time("5min",\
                    data_basic['superUser'],data_login['all'])
        print result
        assert result,"test refresh time is 5min,test fail!"
        print "test refresh time is 5min,test fail!"

    #刷新时间选择区显示检测-永不(testlink_ID:1265_5)
    def test_022_check_refresh_choose_Never(self):
        u"""刷新时间选择区显示检测-永不(testlink_ID:1265_5)"""
        log.debug("022")
        tmp = NavbarBusiness(self.driver)
        #选择刷新时间，切换到其他界面，和登出后在登录，检查刷新时间
        result = tmp.check_change_refresh_time(u"永不",\
                    data_basic['superUser'],data_login['all'])
        print result
        assert result,"test refresh time is Never,test fail!"
        print "test refresh time is Never,test fail!"

    #选择刷新时间-15s，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1266)
    def test_023_check_15s_validity(self):
        u"""选择刷新时间-15s，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1266)"""
        log.debug("023")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_15s_validity()
        self.assertLessEqual(result,17)
        self.assertGreaterEqual(result,13),"test refresh time validity is 15s,test fail!"
        print "test refresh time validity is 15s,test pass!"


    #选择刷新时间-1min，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1267)
    def test_024_check_1min_validity(self):
        u"""选择刷新时间-1min，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1267)"""
        log.debug("024")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_min_validity("1min")
        assert result == 1,"test refresh time validity is 1min,test fail!"
        print "test refresh time validity is 1min,test pass!"

    #选择刷新时间-2min，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1268)
    def test_025_check_2min_validity(self):
        u"""选择刷新时间-2min，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1268)"""
        log.debug("025")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_min_validity("2min")
        assert result == 2,"test refresh time validity is 2min,test fail!"
        print "test refresh time validity is 2min,test pass!"

    #选择刷新时间-5min，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1269)
    def test_026_check_5min_validity(self):
        u"""选择刷新时间-5min，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1269)"""
        log.debug("026")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_min_validity("5min")
        assert result == 5,"test refresh time validity is 5min,test fail!"
        print "test refresh time validity is 5min,test pass!"

    #选择刷新时间-Never，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1270)
    def test_027_check_never_validity(self):
        u"""选择刷新时间-never，记录master ap的设备运行时间，来确认刷新时间的正确性(testlink_ID:1270)"""
        log.debug("027")
        tmp = NavbarBusiness(self.driver)
        result1,result2 = tmp.check_never_validity()
        assert result1 == result2,"test refresh time validity is Never,test fail!"
        print "test refresh time validity is Never,test pass!"

    #连续切换刷新时间，确认显示正确(testlink_ID:1272)
    def test_028_check_many_change_refresh_time(self):
        u"""连续切换刷新时间，确认显示正确(testlink_ID:1272)"""
        log.debug("028")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_many_change_refresh_time()
        assert False not in result,"test change refresh time many times,test fail!"
        print "test change refresh time many times,test pass!"

    #切换刷新时间，然后重启路由后，确认依然有效(testlink_ID:1273)
    def test_029_check_reboot_refresh_time(self):
        u"""切换刷新时间，然后重启路由后，确认依然有效(testlink_ID:1273)"""
        log.debug("029")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_reboot_refresh_time(data_basic['DUT_web'],\
                  data_basic['superUser'],data_login['all'])
        print result
        assert result,"test refresh time after reboot ap,test fail!"
        print "test refresh time after reboot ap,test pass!"




    #######################################################################
    #############################以下是web语言的用例##########################
    #######################################################################
    #主界面，确认有语言按钮(testlink_ID:706)
    def test_030_check_language_main_web(self):
        u"""登录后主界面，确认有刷新按钮(testlink_ID:706)"""
        log.debug("030")
        tmp = NavbarBusiness(self.driver)
        #检查页面中是否有搜索按钮
        result = tmp.check_language_buttton()
        print result
        assert result,"test have language button in main web,test fail!"
        print "test have language button in main web,test pass!"

    #主界面，点击语言按钮后，确认有下拉框选项
    def test_031_check_language_display(self):
        u"""登录后主界面，确认有刷新按钮"""
        log.debug("031")
        tmp = NavbarBusiness(self.driver)
        #点击语言按钮
        tmp.language_menu()
        #语言下拉框是否显示
        result = tmp.display_language()
        assert result,"test language display,test fail!"
        print "test language display,test pass!"

    #选择英文，确认其是否展示有效(testlink_ID:707_1)
    def test_032_check_language_English(self):
        u"""选择英文，确认其是否展示有效(testlink_ID:707_1)"""
        log.debug("032")
        tmp = NavbarBusiness(self.driver)
        #选择语言，检查页面语言是否生效
        result1 = tmp.check_language_validity("English")
        #获取搜索AP的text
        tmp1 = APSBusiness(self.driver)
        result2 = tmp1.check_get_discover_AP()
        assert ("Firmware" in result1) and ("Discover AP" in result2),"test English language,test fail!"
        print "test English language,test pass!"

    #选择中文，确认其是否展示有效(testlink_ID:707_2)
    def test_033_check_language_Chinese(self):
        u"""选择英文，确认其是否展示有效(testlink_ID:707_2)"""
        log.debug("033")
        tmp = NavbarBusiness(self.driver)
        #选择语言，检查页面语言是否生效
        result = tmp.check_language_validity(u"简体中文")
        assert u"固件" in result,"test Chinese language,test fail!"
        print "test Chinese language,test pass!"

    #检查登录页面的默认语言（本机是简体中文）(testlink_ID:707_3)
    def test_034_check_login_defualt_language(self):
        u"""检查登录页面的默认语言（本机是简体中文）(testlink_ID:707_3)"""
        log.debug("034")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_login_defualt_language()
        assert u"简体中文" in result,"test default language in login web,test fail!"
        print "test default language in login web,test pass!"

    #切换登录页面的语言(testlink_ID:707_4)
    def test_035_check_login_change_language(self):
        u"""切换登录页面的语言(testlink_ID:707_4)"""
        log.debug("035")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_login_change_language("English")
        assert "English" in result,"test change language in login web,test fail!"
        print "test change language in login web,test pass!"

    #连续切换语言，确认其正确性(testlink_ID:710)
    def test_036_check_many_change_language(self):
        u"""连续切换语言，确认其正确性(testlink_ID:710)"""
        log.debug("036")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_many_change_language()
        assert False not in result,"test change language many times,test fail!"
        print "test change language many times,test pass!"

    #切换英文语言，确认刷新时间语言正确(testlink_ID:712_1)
    def test_037_check_English_refresh_time(self):
        u"""切换英文语言，确认刷新时间语言正确(testlink_ID:712_1)"""
        log.debug("037")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_language_refresh("English","Refresh interval")
        assert "Never" in result,"test refresh time in English language,test fail!"
        print "test refresh time in English language,test pass!"

    #切换中文语言，确认刷新时间语言正确(testlink_ID:712_2)
    def test_038_check_Chinese_refresh_time(self):
        u"""切换中文语言，确认刷新时间语言正确(testlink_ID:712_2)"""
        log.debug("038")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_language_refresh(u"简体中文",u"刷新间隔")
        assert u"永不" in result,"test refresh time in Chinese language,test fail!"
        print "test refresh time in Chinese language,test pass!"

    #切换英文语言，确认搜索功能语言正确(testlink_ID:713_1)
    def test_039_check_English_search(self):
        u"""切换英文语言，确认搜索功能语言正确(testlink_ID:713_1)"""
        log.debug("039")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_language_search("English",data_navbar['inexistence_info'])
        assert "Sorry, no matching results." in result,"test search in English language,test fail!"
        print "test search in English language,test pass!"

    #切换中文语言，确认搜索功能语言正确(testlink_ID:713_2)
    def test_040_check_Chinese_search(self):
        u"""切换中文语言，确认搜索功能语言正确(testlink_ID:713_2)"""
        log.debug("040")
        tmp = NavbarBusiness(self.driver)
        result = tmp.check_language_search(u"简体中文",data_navbar['inexistence_info'])

        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("Navbar")
        assert u"对不起, 没有匹配的结果" in result,"test search in Chinese language,test fail!"
        print "test search in Chinese language,test pass!"


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
