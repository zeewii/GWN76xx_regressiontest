#coding=utf-8
#作者：曾祥卫
#时间：2017.12.06
#描述：用例层代码，调用timepolicy_business

import unittest
import time,subprocess
from selenium import webdriver
import sys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from clients.timepolicy.timepolicy_business import TimePolicyBusiness
from clients.banned_clients.bannedclients_business import BannedClientsBusiness
from login.login_business import LoginBusiness
from clients.clients_business import ClientsBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from access_points.aps_business import APSBusiness
#from network_group.networkgroup_business import NGBusiness
from ssid.ssid_business import SSIDBusiness
from network_group.add_ssid.addssid_business import AddSSIDBusiness
from data import data
from connect.ssh import SSH
from data.logfile import Log
reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_AP = data.data_AP()
data_ng = data.data_networkgroup()
data_client = data.data_Client()
log = Log("Clienttimepolicy")

class TestClientTimePolicy(unittest.TestCase):
    u"""测试客户端时间策略的用例集(runtime:2h)"""
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

    #name为空(testlink_ID:3171)
    def test_002_check_name_null(self):
        u"""name为空(testlink_ID:3171)"""
        log.debug("002")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, "", "1", "1", u"该字段不能为空", "h")
        self.assertTrue(result), "check name is null, test fail!"
        print "check name is null, test pass!"

    #name字符长度超过32
    def test_003_check_name_over_max_length(self):
        u"""name字符长度超过32(testlink_ID:3172)"""
        log.debug("003")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, data_wireless['long_ssid']+"a",
            "1", "1", u"最多只能有32个字符", "h")
        self.assertTrue(result), "check name is null, test fail!"
        print "check name is null, test pass!"

    #name字符长度等于1
    def test_004_check_name_length_1(self):
        u"""name字符长度等于1(testlink_ID:3173)"""
        log.debug("004")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, "a", "1", "1", "h")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check name's length is 1, test fail!"
        print "check name's length is 1, test pass!"

    #name字符长度等于32
    def test_005_check_name_length_32(self):
        u"""name字符长度等于1(testlink_ID:3174)"""
        log.debug("005")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, data_wireless['long_ssid'], "1", "1", "h")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check name's length is 32, test fail!"
        print "check name's length is 32, test pass!"

    #name为特殊字符或汉字
    def test_006_check_name_chinese(self):
        u"""name为特殊字符或汉字(testlink_ID:3175)"""
        log.debug("006")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "1", "h")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check name is Chinese, test fail!"
        print "check name is Chinese, test pass!"

    #添加两条相同name的策略
    def test_007_check_same_name_policy(self):
        u"""添加两条相同name的策略(testlink_ID:3176)"""
        log.debug("007")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, "a", "1", "1", "h")
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(1, "a", "2", "2", u"此时间策略已经存在", "h")
        self.driver.refresh()
        self.driver.implicitly_wait(60)
        time.sleep(10)
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check two same name time policys, test fail!"
        print "check two same name time policys, test pass!"

    #Enable勾选
    def test_008_check_enable_timepolicy(self):
        u"""Enable勾选(testlink_ID:3177)"""
        log.debug("008")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "1", "h")
        #判断页面上是否有Enable图标
        result = tmp.check_enbale_timepolicy()
        self.assertTrue(result), "check enable time policy, test fail!"
        print "check enable time policy, test pass!"

    #Enable不勾选
    def test_009_check_disable_timepolicy(self):
        u"""Enable不勾选(testlink_ID:3178)"""
        log.debug("009")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，点击Enable
        tmp.enable_disable_timepolicy(0)
        #判断页面上是否有Enable图标
        result = tmp.check_enbale_timepolicy()
        tmp.del_all_timepolicy()
        self.assertFalse(result), "check disable time policy, test fail!"
        print "check disable time policy, test pass!"

    #Connection Time选择m，不填入数字
    def test_010_check_connection_time_m_null(self):
        u"""Connection Time选择m，不填入数字(testlink_ID:3179)"""
        log.debug("010")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1",
            "", "1", u"该字段不能为空", "m")
        self.assertTrue(result), "check connection time is null, test fail!"
        print "check connection time is null, test pass!"

    #Connection Time选择m，填入数字100000000
    def test_011_check_connection_time_m_100000000(self):
        u"""Connection Time选择m，填入数字100000000(testlink_ID:3180)"""
        log.debug("011")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1",
            "100000000", "1", u"必须是一个整数并小于或等于99999999", "m")
        self.assertTrue(result), "check connection time less 100000000, test fail!"
        print "check connection time less 100000000, test pass!"

    #Connection Time选择m，填入数字1-99999999之间的数字-1
    def test_012_check_connection_time_m_0(self):
        u"""Connection Time选择m，填入数字1-99999999之间的数字-1(testlink_ID:3181-1)"""
        log.debug("012")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "1", "m")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check connection time is 1, test fail!"
        print "check connection time is 1, test pass!"

    #Connection Time选择m，填入数字1-99999999之间的数字-2
    def test_013_check_connection_time_m_99999999(self):
        u"""Connection Time选择m，填入数字1-99999999之间的数字-2(testlink_ID:3181-2)"""
        log.debug("013")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "99999999", "1", "m")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check connection time is 99999999, test fail!"
        print "check connection time is 99999999, test pass!"

    #Connection Time选择m，填入非数字字符
    def test_014_check_connection_time_m_invalid(self):
        u"""Connection Time选择m，填入非数字字符(testlink_ID:3182)"""
        log.debug("014")
        tmp = TimePolicyBusiness(self.driver)
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1", "abc", "1",
            u"必须是一个整数并大于或等于0", "m")
        self.assertTrue(result), "check connection time is invalid, test fail!"
        print "check connection time is invalid, test pass!"

    #Connection Time选择h，不填入数字
    def test_015_check_connection_time_h_null(self):
        u"""Connection Time选择m，不填入数字(testlink_ID:3183)"""
        log.debug("015")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1",
            "", "1", u"该字段不能为空", "h")
        self.assertTrue(result), "check connection time is null, test fail!"
        print "check connection time is null, test pass!"

    #Connection Time选择h，填入数字100000000
    def test_016_check_connection_time_h_100000000(self):
        u"""Connection Time选择m，填入数字100000000(testlink_ID:3184)"""
        log.debug("016")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1",
            "100000000", "1", u"必须是一个整数并小于或等于99999999", "h")
        self.assertTrue(result), "check connection time less 100000000, test fail!"
        print "check connection time less 100000000, test pass!"

    #Connection Time选择h，填入数字1-99999999之间的数字-1
    def test_017_check_connection_time_h_0(self):
        u"""Connection Time选择m，填入数字1-99999999之间的数字-1(testlink_ID:3185-1)"""
        log.debug("017")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "1", "h")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check connection time is 1, test fail!"
        print "check connection time is 1, test pass!"

    #Connection Time选择h，填入数字1-99999999之间的数字-2
    def test_018_check_connection_time_h_99999999(self):
        u"""Connection Time选择m，填入数字1-99999999之间的数字-2(testlink_ID:3185-2)"""
        log.debug("018")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "99999999", "1", "h")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check connection time is 99999999, test fail!"
        print "check connection time is 99999999, test pass!"

    #Connection Time选择h，填入非数字字符
    def test_019_check_connection_time_h_invalid(self):
        u"""Connection Time选择m，填入非数字字符(testlink_ID:3186)"""
        log.debug("019")
        tmp = TimePolicyBusiness(self.driver)
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1", "abc", "1",
            u"必须是一个整数并大于或等于0", "h")
        self.assertTrue(result), "check connection time is invalid, test fail!"
        print "check connection time is invalid, test pass!"

    #Connection Time选择d，不填入数字
    def test_020_check_connection_time_d_null(self):
        u"""Connection Time选择m，不填入数字(testlink_ID:3187)"""
        log.debug("020")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1",
            "", "1", u"该字段不能为空", "d")
        self.assertTrue(result), "check connection time is null, test fail!"
        print "check connection time is null, test pass!"

    #Connection Time选择d，填入数字100000000
    def test_021_check_connection_time_d_100000000(self):
        u"""Connection Time选择m，填入数字100000000(testlink_ID:3188)"""
        log.debug("021")
        tmp = TimePolicyBusiness(self.driver)
        #输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1",
            "100000000", "1", u"必须是一个整数并小于或等于99999999", "d")
        self.assertTrue(result), "check connection time less 100000000, test fail!"
        print "check connection time less 100000000, test pass!"

    #Connection Time选择d，填入数字1-99999999之间的数字-1
    def test_022_check_connection_time_d_0(self):
        u"""Connection Time选择m，填入数字1-99999999之间的数字-1(testlink_ID:3189-1)"""
        log.debug("022")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "1", "d")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check connection time is 1, test fail!"
        print "check connection time is 1, test pass!"

    #Connection Time选择d，填入数字1-99999999之间的数字-2
    def test_023_check_connection_time_d_99999999(self):
        u"""Connection Time选择m，填入数字1-99999999之间的数字-2(testlink_ID:3189-2)"""
        log.debug("023")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "99999999", "1", "d")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        tmp.del_all_timepolicy()
        self.assertTrue(result), "check connection time is 99999999, test fail!"
        print "check connection time is 99999999, test pass!"

    #Connection Time选择d，填入非数字字符
    def test_024_check_connection_time_d_invalid(self):
        u"""Connection Time选择m，填入非数字字符(testlink_ID:3190)"""
        log.debug("024")
        tmp = TimePolicyBusiness(self.driver)
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1", "abc", "1",
            u"必须是一个整数并大于或等于0", "d")
        self.assertTrue(result), "check connection time is invalid, test fail!"
        print "check connection time is invalid, test pass!"

    #Timeout Type选择Reset Hourly
    def test_025_check_timeout_hourly(self):
        u"""Timeout Type选择Reset Hourly(testlink_ID:3191)"""
        log.debug("025")
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "1", "h")
        #编辑一个时间策略，修改客户端重连超时类型为每小时
        tmp.change_timeout_hourly(0)
        result = tmp.get_titlediv()
        tmp.del_all_timepolicy()
        self.assertIn(u"每小时", result), "check timeout is hourly, test fail!"
        print "check timeout is hourly, test pass!"

    #Timeout Type选择Daily,不填入数字
    def test_026_check_timeout_daily_null(self):
        u"""Timeout Type选择Daily,不填入数字(testlink_ID:3192)"""
        log.debug("026")
        tmp = TimePolicyBusiness(self.driver)
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1", "1", "",
            u"该字段不能为空", "h")
        self.assertTrue(result), "check timeout is hourly and input null, test fail!"
        print "check timeout is hourly and input null, test pass!"

    #Timeout Type选择Daily,填入大于或等于24的数字
    def test_027_check_timeout_daily_24(self):
        u"""Timeout Type选择Daily,不填入数字(testlink_ID:3193)"""
        log.debug("027")
        tmp = TimePolicyBusiness(self.driver)
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        result = tmp.check_new_timepolicy_tip(0, u"时间策略1", "1", "24",
            u"必须是一个0到23的整数", "h")
        self.assertTrue(result), "check timeout is hourly and input 24, test fail!"
        print "check timeout is hourly and input 24, test pass!"

    #Timeout Type选择Daily,填入0-23的数字
    def test_028_check_timeout_daily_0_23(self):
        u"""Timeout Type选择Daily,填入0-23的数字(testlink_ID:3194)"""
        log.debug("028")
        tmp = TimePolicyBusiness(self.driver)
        #新建时间策略，输入相应的数据，检查页面上是否有提示
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "1", "23", "h")
        #判断页面上有新建的时间策略
        result = tmp.check_have_timepolicy()
        self.assertTrue(result), "check timeout is hourly and input 0-23, test fail!"
        print "check timeout is hourly and input 0-23, test pass!"

    #Timeout Type选择Reset Weekly
    def test_029_check_timeout_weekly(self):
        u"""Timeout Type选择Reset Weekly(testlink_ID:3195)"""
        log.debug("029")
        tmp = TimePolicyBusiness(self.driver)
        #修改客户端重连超时类型为每周后，检查页面上是否显示对应的礼拜
        result = tmp.check_timeout_weekly(0, "20")
        self.assertNotIn(False, result), "check timeout is weekly, test fail!"
        print "check timeout is weekly, test pass!"

    #Hour of the Day合法字符
    def test_030_check_timeout_weekly_reset_hour(self):
        u"""Hour of the Day合法字符(testlink_ID:3196)"""
        log.debug("030")
        tmp = TimePolicyBusiness(self.driver)
        #修改客户端重连超时类型为每周后，并每天的第几小时，能够保存
        result = tmp.check_timeout_weekly_reset_hour(0)
        self.assertNotIn(False, result), "when timeout is weekly check reset hour, test fail!"
        print "when timeout is weekly check reset hour, test pass!"

    #Hour of the Day不合法字符
    def test_031_check_timeout_weekly_reset_hour_invalid(self):
        u"""Hour of the Day不合法字符(testlink_ID:3197)"""
        log.debug("031")
        tmp = TimePolicyBusiness(self.driver)
        #Hour of the Day不合法字符
        t_outs = ["-1", "26", "abc"]
        result = tmp.check_timeout_weekly_reset_hour_invalid(0, t_outs)
        self.assertNotIn(False, result), "when timeout is weekly check reset hour, test fail!"
        print "when timeout is weekly check reset hour, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择m，填入数字1-99999999之间的数字-1
    def test_032_check_timeout_timed_m_0(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择m，填入数字1-99999999之间的数字-1(testlink_ID:3198-1)"""
        log.debug("032")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，修改客户端重连超时类型为根据时间
        tmp.change_timeout_timed(0, "1", "m")
        #获取页面所有标题
        result = tmp.get_titlediv()
        self.assertIn("1m", result), "check timeout type is timed,the timout time is 1, test fail!"
        print "check timeout type is timed,the timout time is 1, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择m，填入数字1-99999999之间的数字-2
    def test_033_check_timeout_timed_m_99999999(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择m，填入数字1-99999999之间的数字-2(testlink_ID:3198-2)"""
        log.debug("033")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，修改客户端重连超时类型为根据时间
        tmp.change_timeout_timed(0, "99999999", "m")
        #获取页面所有标题
        result = tmp.get_titlediv()
        self.assertIn("99999999m", result), "check timeout type is timed,the timout time is 99999999, test fail!"
        print "check timeout type is timed,the timout time is 99999999, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择h，填入数字1-99999999之间的数字-3
    def test_034_check_timeout_timed_h_0(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择h，填入数字1-99999999之间的数字-3(testlink_ID:3198-3)"""
        log.debug("034")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，修改客户端重连超时类型为根据时间
        tmp.change_timeout_timed(0, "1", "h")
        #获取页面所有标题
        result = tmp.get_titlediv()
        self.assertIn("1h", result), "check timeout type is timed,the timout time is 1, test fail!"
        print "check timeout type is timed,the timout time is 1, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择h，填入数字1-99999999之间的数字-4
    def test_035_check_timeout_timed_h_99999999(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择h，填入数字1-99999999之间的数字-2(testlink_ID:3198-4)"""
        log.debug("035")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，修改客户端重连超时类型为根据时间
        tmp.change_timeout_timed(0, "99999999", "h")
        #获取页面所有标题
        result = tmp.get_titlediv()
        self.assertIn("99999999h", result), "check timeout type is timed,the timout time is 99999999, test fail!"
        print "check timeout type is timed,the timout time is 99999999, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择d，填入数字1-99999999之间的数字-5
    def test_036_check_timeout_timed_d_0(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择d，填入数字1-99999999之间的数字-5(testlink_ID:3198-5)"""
        log.debug("036")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，修改客户端重连超时类型为根据时间
        tmp.change_timeout_timed(0, "1", "d")
        #获取页面所有标题
        result = tmp.get_titlediv()
        self.assertIn("1d", result), "check timeout type is timed,the timout time is 1, test fail!"
        print "check timeout type is timed,the timout time is 1, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择d，填入数字1-99999999之间的数字-6
    def test_037_check_timeout_timed_d_99999999(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择d，填入数字1-99999999之间的数字-6(testlink_ID:3198-6)"""
        log.debug("037")
        tmp = TimePolicyBusiness(self.driver)
        #编辑一个时间策略，修改客户端重连超时类型为根据时间
        tmp.change_timeout_timed(0, "99999999", "d")
        #获取页面所有标题
        result = tmp.get_titlediv()
        self.assertIn("99999999d", result), "check timeout type is timed,the timout time is 99999999, test fail!"
        print "check timeout type is timed,the timout time is 99999999, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择m，填入数字100000000
    def test_038_check_connection_time_m_100000000(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择m，填入数字100000000(testlink_ID:3199-1)"""
        log.debug("038")
        tmp = TimePolicyBusiness(self.driver)
        #检查客户端重连超时为非法字符时的情况
        result = tmp.check_edit_timeout_timed_tip(0,
            "100000000", "m", u"必须是一个整数并小于或等于99999999")
        self.assertTrue(result), "check timeout type is timed,the timout time is 100000000, test fail!"
        print "check timeout type is timed,the timout time is 100000000, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择m，填入非数字字符
    def test_039_check_connection_time_m_letter(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择m，填入非数字字符(testlink_ID:3199-2)"""
        log.debug("039")
        tmp = TimePolicyBusiness(self.driver)
        #检查客户端重连超时为非法字符时的情况
        result = tmp.check_edit_timeout_timed_tip(0,
            "abc", "m", u"必须是一个整数并大于或等于0")
        self.assertTrue(result), "check timeout type is timed,the timout time is letter, test fail!"
        print "check timeout type is timed,the timout time is letter, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择h，填入数字100000000
    def test_040_check_connection_time_h_100000000(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择h，填入数字100000000(testlink_ID:3199-3)"""
        log.debug("040")
        tmp = TimePolicyBusiness(self.driver)
        #检查客户端重连超时为非法字符时的情况
        result = tmp.check_edit_timeout_timed_tip(0,
            "100000000", "h", u"必须是一个整数并小于或等于99999999")
        self.assertTrue(result), "check timeout type is timed,the timout time is 100000000, test fail!"
        print "check timeout type is timed,the timout time is 100000000, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择h，填入非数字字符
    def test_041_check_connection_time_h_letter(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择h，填入非数字字符(testlink_ID:3199-4)"""
        log.debug("041")
        tmp = TimePolicyBusiness(self.driver)
        #检查客户端重连超时为非法字符时的情况
        result = tmp.check_edit_timeout_timed_tip(0,
            "abc", "h", u"必须是一个整数并大于或等于0")
        self.assertTrue(result), "check timeout type is timed,the timout time is letter, test fail!"
        print "check timeout type is timed,the timout time is letter, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择d，填入数字100000000
    def test_042_check_connection_time_d_100000000(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择d，填入数字100000000(testlink_ID:3199-5)"""
        log.debug("042")
        tmp = TimePolicyBusiness(self.driver)
        #检查客户端重连超时为非法字符时的情况
        result = tmp.check_edit_timeout_timed_tip(0,
            "100000000", "d", u"必须是一个整数并小于或等于99999999")
        self.assertTrue(result), "check timeout type is timed,the timout time is 100000000, test fail!"
        print "check timeout type is timed,the timout time is 100000000, test pass!"

    #客户端重连超时类型选择timed，客户端重连超时单位选择d，填入非数字字符
    def test_043_check_connection_time_d_letter(self):
        u"""客户端重连超时类型选择timed，客户端重连超时单位选择d，填入非数字字符(testlink_ID:3199-6)"""
        log.debug("043")
        tmp = TimePolicyBusiness(self.driver)
        #检查客户端重连超时为非法字符时的情况
        result = tmp.check_edit_timeout_timed_tip(0,
            "abc", "d", u"必须是一个整数并大于或等于1")
        self.assertTrue(result), "check timeout type is timed,the timout time is letter, test fail!"
        print "check timeout type is timed,the timout time is letter, test pass!"

    #检查页面信息
    def test_044_check_webUI(self):
        u"""检查页面信息(testlink_ID:3200)"""
        log.debug("044")
        #点击客户端菜单
        tmp1 = ClientsBusiness(self.driver)
        tmp1.clients_menu()
        #点击时间策略菜单
        tmp = TimePolicyBusiness(self.driver)
        tmp.timepolicy_menu()
        #获取页面所有标题
        result1 = tmp.get_titlediv()
        #判断页面上是否有Enable图标
        result2 = tmp.check_enbale_timepolicy()
        self.assertIn(u"时间策略1", result1)
        self.assertIn(u"根据时间", result1)
        self.assertIn("99999999d", result1)
        self.assertTrue(result2), "check time policy webUI, test fail!"
        print "check time policy webUI, test pass!"

    #修改配置之后检查页面信息
    def test_045_check_webUI_change_config(self):
        u"""修改配置之后检查页面信息(testlink_ID:3201)"""
        log.debug("045")
        tmp = TimePolicyBusiness(self.driver)
        #修改客户端重连超时类型为每小时
        tmp.change_timeout_hourly(0)
        #获取页面所有标题
        result1 = tmp.get_titlediv()
        #判断页面上是否有Enable图标
        result2 = tmp.check_enbale_timepolicy()
        #删除所有的时间策略
        tmp.del_all_timepolicy()
        self.assertIn(u"时间策略1", result1)
        self.assertIn(u"每小时", result1)
        self.assertTrue(result2), "check time policy webUI after change config, test fail!"
        print "check time policy webUI after change config, test pass!"

    #Connection Time单位选择m分钟，功能测试
    def test_046_check_connection_m_time_function(self):
        u"""Connection Time单位选择m分钟，功能测试(testlink_ID:3202)"""
        log.debug("046")
        tmp = TimePolicyBusiness(self.driver)
        #断开无线网卡的连接
        tmp.disconnect_ap()
        #先修改ap的系统时间为01:00:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date -s 01:00:00")
        #按照默认配置，新建一个时间策略
        tmp.new_timepolicy_default(0, u"时间策略1", "2", "23", "m")
        #进入网络组中选择客户端时间策略
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_client_time_policy_pagedown(1, u"时间策略1")
        #无线网卡连接
        tmp1.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        #等待3分钟
        time.sleep(240)
        #判断AP是否依然连接
        result1 = subprocess.check_output("iw dev %s link"%data_basic['wlan_pc'], shell=True)
        #释放无线网卡的ip
        tmp1.dhcp_release_wlan(data_basic['wlan_pc'])
        #获取禁止的客户端页面所有标题
        tmp2 = BannedClientsBusiness(self.driver)
        result2 = tmp2.get_bannedclients_title()
        wlan_mac = tmp2.get_wlan_mac(data_basic['wlan_pc']).upper()
        self.assertNotIn(data_wireless['all_ssid'], result1)
        self.assertIn(wlan_mac, result2),
        "check connection time function is min, test fail!"
        print "check connection time function is min, test pass!"

    #Connection Time单位选择h小时，功能测试
    def test_047_check_connection_time_h_function(self):
        u"""Connection Time单位选择h小时，功能测试(testlink_ID:3203)"""
        log.debug("047")
        tmp2 = BannedClientsBusiness(self.driver)
        #断开无线网卡的连接
        tmp2.disconnect_ap()
        #先解锁客户端
        tmp2.unblock_clients(1)
        #先修改ap的系统时间为01:00:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date -s 01:00:00")
        #按照默认配置，编辑一个时间策略-5小时
        tmp = TimePolicyBusiness(self.driver)
        tmp.edit_timepolicy_default(0, u"时间策略1", "5", "23", "h")
        #无线网卡连接
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        #再修改ap的系统时间为06:00:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date -s 06:00:00")
        #等待3分钟
        time.sleep(180)
        #判断AP是否依然连接
        result1 = subprocess.check_output("iw dev %s link"%data_basic['wlan_pc'], shell=True)
        #释放无线网卡的ip
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        #获取禁止的客户端页面所有标题
        tmp2 = BannedClientsBusiness(self.driver)
        result2 = tmp2.get_bannedclients_title()
        wlan_mac = tmp2.get_wlan_mac(data_basic['wlan_pc']).upper()
        self.assertNotIn(data_wireless['all_ssid'], result1)
        self.assertIn(wlan_mac, result2),
        "check connection time function is hour, test fail!"
        print "check connection time function is hour, test pass!"

    #Connection Time单位选择d天，功能测试
    def test_048_check_connection_time_d_function(self):
        u"""Connection Time单位选择d天，功能测试(testlink_ID:3204)"""
        log.debug("048")
        tmp2 = BannedClientsBusiness(self.driver)
        #断开无线网卡的连接
        tmp2.disconnect_ap()
        #先解锁客户端
        tmp2.unblock_clients(1)
        #先修改ap的系统时间为2018-08-08 01:00:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date 201808080100")
        #按照默认配置，编辑一个时间策略-1天
        tmp = TimePolicyBusiness(self.driver)
        tmp.edit_timepolicy_default(0, u"时间策略1", "1", "23", "d")
        #无线网卡连接
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        #再修改ap的系统时间为2018-08-09 01:00:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date 201808090100")
        #等待3分钟
        time.sleep(180)
        #判断AP是否依然连接
        result1 = subprocess.check_output("iw dev %s link"%data_basic['wlan_pc'], shell=True)
        #释放无线网卡的ip
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        #获取禁止的客户端页面所有标题
        result2 = tmp2.get_bannedclients_title()
        wlan_mac = tmp2.get_wlan_mac(data_basic['wlan_pc']).upper()
        self.assertNotIn(data_wireless['all_ssid'], result1)
        self.assertIn(wlan_mac, result2),
        "check connection time function is day, test fail!"
        print "check connection time function is day, test pass!"

    #Timeout type选择reset daily测试
    def test_049_check_timeout_reconnection_daily_function(self):
        u"""Timeout type选择reset daily测试(testlink_ID:3206)"""
        log.debug("049")
        tmp2 = BannedClientsBusiness(self.driver)
        wlan_mac = tmp2.get_wlan_mac(data_basic['wlan_pc']).upper()
        #再修改ap的系统时间为22:59:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date -s 22:59:00")
        #等待3分钟
        time.sleep(180)
        #无线网卡连接
        result3 = tmp2.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        tmp2.dhcp_release_wlan(data_basic['wlan_pc'])
        result4 = tmp2.get_bannedclients_title()
        self.assertIn(data_wireless['all_ssid'], result3)
        self.assertNotIn(wlan_mac, result4),
        "check reconnection timeout function is daily, test fail!"
        print "check reconnection timeout function is daily, test pass!"

    #Timeout type选择reset hourly测试
    def test_050_check_timeout_reconnection_hourly_function(self):
        u"""Timeout type选择reset hourly测试(testlink_ID:3205)"""
        log.debug("050")
        tmp2 = BannedClientsBusiness(self.driver)
        #断开网线网卡的连接
        tmp2.disconnect_ap()
        tmp = TimePolicyBusiness(self.driver)
        #按照默认配置，编辑一个时间策略-5分钟,每天23点超时
        tmp.edit_timepolicy_default(0, u"时间策略1", "5", "23", "m")
        #再编辑默认时间策略，修改客户端重连超时类型为每小时
        tmp.change_timeout_hourly(0)
        #无线网卡连接
        #先修改ap的系统时间为22:00:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date -s 22:00:00")
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        #等待6分钟
        time.sleep(360)
        #判断AP是否依然连接
        result1 = subprocess.check_output("iw dev %s link"%data_basic['wlan_pc'], shell=True)
        #释放无线网卡的ip
        tmp2.dhcp_release_wlan(data_basic['wlan_pc'])
        #获取禁止的客户端页面所有标题
        tmp2 = BannedClientsBusiness(self.driver)
        result2 = tmp2.get_bannedclients_title()
        wlan_mac = tmp2.get_wlan_mac(data_basic['wlan_pc']).upper()

        #再修改ap的系统时间为22:59:00
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date -s 22:59:00")
        #等待3分钟
        time.sleep(180)
        #无线网卡连接
        result3 = tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        tmp2.dhcp_release_wlan(data_basic['wlan_pc'])
        result4 = tmp2.get_bannedclients_title()
        # self.assertNotIn(data_wireless['all_ssid'], result1)
        # self.assertIn(wlan_mac, result2)
        self.assertIn(data_wireless['all_ssid'], result3)
        self.assertNotIn(wlan_mac, result4),
        "check reconnection timeout function is hourly, test fail!"
        print "check reconnection timeout function is hourly, test pass!"

    #Timeout type选择reset weekly测试
    def test_051_check_timeout_reconnection_weekly_function(self):
        u"""Timeout type选择reset weekly测试(testlink_ID:3207)"""
        log.debug("051")
        tmp2 = BannedClientsBusiness(self.driver)
        #等待4分钟--等待客户端再次被踢掉
        time.sleep(240)
        #先解锁客户端
        tmp2.unblock_clients(1)
        #断开无线网卡的连接
        tmp2.disconnect_ap()
        tmp = TimePolicyBusiness(self.driver)
        tmp.change_timeout_weekly(0, u"星期三", "23")
        #先修改ap的系统时间为2018-08-07 22:00:00(当天是星期二)
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date 201808072200")
        #无线网卡连接
        tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        #等待6分钟
        time.sleep(360)
        #判断AP是否依然连接
        result1 = subprocess.check_output("iw dev %s link"%data_basic['wlan_pc'], shell=True)
        #获取禁止的客户端页面所有标题
        tmp2.dhcp_release_wlan(data_basic['wlan_pc'])
        result2 = tmp2.get_bannedclients_title()
        wlan_mac = tmp2.get_wlan_mac(data_basic['wlan_pc']).upper()

        #再修改ap的系统时间为2018-08-08 22:59:00(当天是星期三)
        ssh = SSH(data_basic['DUT_ip'], data_login['all'])
        ssh.ssh_cmd(data_basic['sshUser'], "date 201808082259")
        #等待3分钟
        time.sleep(180)
        #无线网卡连接
        result3 = tmp.connect_DHCP_WPA_AP(data_wireless['all_ssid'],
            data_wireless['short_wpa'], data_basic['wlan_pc'])
        tmp2.dhcp_release_wlan(data_basic['wlan_pc'])
        result4 = tmp2.get_bannedclients_title()

        #测试完毕，禁用无线网卡，使pc够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.disconnect_ap()
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("ClientTimePolicy")
        # self.assertNotIn(data_wireless['all_ssid'], result1)
        # self.assertIn(wlan_mac, result2)
        self.assertIn(data_wireless['all_ssid'], result3)
        self.assertNotIn(wlan_mac, result4),
        "check reconnection timeout function is weekly, test fail!"
        print "check reconnection timeout function is weekly, test pass!"






    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()

