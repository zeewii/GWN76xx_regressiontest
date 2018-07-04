#coding=utf-8
#作者：曾祥卫
#时间：2017.05.23
#描述：GWN76xx设置向导的业务层

import time
from data import data
from navbar_control import NavbarControl
from overview.overview_business import OVBusiness
from access_points.aps_business import APSBusiness
from login.login_business import LoginBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness

data_basic = data.data_basic()

class NavbarBusiness(NavbarControl):

    def __init__(self,driver):
        #继承SWControl类的属性和方法
        NavbarControl.__init__(self,driver)


    #######################################################################
    #############################以下是搜索框的方法###########################
    #######################################################################
    #登录后主界面，确认有搜索按钮,点击搜索按钮，确定弹出搜索框
    def check_search(self):
        #检查页面中是否有搜索按钮
        result1 = NavbarControl.check_search_buttton(self)
        #点击页面上的放大镜打开搜索框
        NavbarControl.search_menu(self)
        #检查页面中是否有搜索框
        result2 = NavbarControl.check_search_input(self)
        print result1,result2
        return result1,result2

    #在搜索框中输入为空，无搜索结果展示
    def check_blankvalue_search(self):
        tmp = NavbarControl(self.driver)
        #点击页面上的放大镜打开搜索框
        tmp.search_menu()
        #在弹出的搜索框中输入空值,并在键盘中按enter
        tmp.set_search("")
        result = tmp.check_search_result()
        return result

    #输入信息，获取搜索结果
    def search_result(self,text):
        tmp = NavbarControl(self.driver)
        #点击页面上的放大镜打开搜索框
        tmp.search_menu()
        #在弹出的搜索框中输入信息,并在键盘中按enter
        tmp.set_search(text)
        #获取搜索的结果
        return tmp.get_search_result()

    #输入信息，获取搜索结果,并通过页面元素id来判断是否跳转到特定页面
    def click_result(self,text,id_element):
        try:
            tmp = NavbarControl(self.driver)
            #点击页面上的放大镜打开搜索框
            tmp.search_menu()
            #在弹出的搜索框中输入信息,并在键盘中按enter
            tmp.set_search(text)
            #点击搜索结果
            tmp.click_search_result(text)
            self.driver.find_element_by_id(id_element)
            return True
        except:
            return False

    #打开输入框，点击其他菜单，确认输入框消失
    def check_mouse(self):
        tmp = NavbarControl(self.driver)
        #点击页面上的放大镜打开搜索框
        tmp.search_menu()
        #点击概览菜单
        tmp1 = OVBusiness(self.driver)
        tmp1.OV_menu()
        #检查页面中是否有搜索框
        result  = tmp.check_search_input()
        return result



    #######################################################################
    #############################以下是刷新时间的方法###########################
    #######################################################################
    #选择刷新时间，切换到其他界面，和登出后在登录，检查刷新时间
    def check_change_refresh_time(self,time,username,pwd):
        tmp = NavbarControl(self.driver)
        #点击页面上的刷新时间间隔
        tmp.refresh_menu()
        #选择页面上的刷新时间间隔
        tmp.refresh_choose(time)
        #获取刷新时间
        result1 = tmp.get_refresh_time()
        #点击接入点菜单
        tmp1 = APSBusiness(self.driver)
        tmp1.APS_menu()
        #获取刷新时间
        result2 = tmp.get_refresh_time()
        #点击页面上的退出按钮
        tmp.logout()
        tmp2 = LoginBusiness(self.driver)
        #登录GWN7610的web界面
        tmp2.login(username,pwd)
        #获取刷新时间
        result3 = tmp.get_refresh_time()
        if (time in result1) and (time in result2) and (time in result3):
            return True
        else:
            return False

    #选择刷新时间-15s，记录master ap的设备运行时间，来确认刷新时间的正确性
    def check_15s_validity(self):
        #点击接入点菜单
        tmp1 = APSBusiness(self.driver)
        tmp1.APS_menu()
        #选择页面上的刷新时间间隔
        tmp = NavbarControl(self.driver)
        tmp.refresh_menu()
        tmp.refresh_choose("15s")
        #获取主界面的运行时间
        result1 = tmp1.get_uptime1()
        m = result1.split("m")
        a = int(m[-1].strip("s"))
        #如果现在运行时间大于45秒,则多等待15秒后再进行测试
        if a >= 45:
            time.sleep(15)
            #获取主界面的运行时间
            result1_2 = tmp1.get_uptime1()
            #等待设定的时间后
            time.sleep(15)
            result2 = tmp1.get_uptime1()
            x = result1_2.split("m")
            c = int(x[-1].strip("s"))
            n = result2.split("m")
            b = int(n[-1].strip("s"))
            result = b-c
            print c,b,result
            return result
        #等待设定的时间后
        time.sleep(15)
        result2 = tmp1.get_uptime1()
        n = result2.split("m")
        b = int(n[-1].strip("s"))
        result = b-a
        print a,b,result
        return result

    #选择刷新时间，记录master ap的设备运行时间，来确认刷新时间的正确性---该函数只合适分钟
    def check_min_validity(self,T):
        #点击接入点菜单
        tmp1 = APSBusiness(self.driver)
        tmp1.APS_menu()
        #选择页面上的刷新时间间隔
        tmp = NavbarControl(self.driver)
        tmp.refresh_menu()
        tmp.refresh_choose(T)
        #获取主界面的运行时间
        result1 = tmp1.get_uptime1()
        n = result1.split("m")
        m = n[0].split("h")
        a = int(m[-1])
        #如果现在运行时间大于55分钟,则多等待5分钟后再进行测试
        if a >= 55:
            time.sleep(300)
            #获取主界面的运行时间
            result1_2 = tmp1.get_uptime1()
            #等待设定的时间后
            t = int(T.strip("min"))*60
            time.sleep(t)
            result2 = tmp1.get_uptime1()
            c = result1_2.split("m")
            d = c[0].split("h")
            e = int(d[-1])
            f = result2.split("m")
            g = f[0].split("h")
            h = int(g[-1])
            result = h-e
            print e,h,result
            return result
        #等待设定的时间后
        t = int(T.strip("min"))*60
        time.sleep(t)
        result2 = tmp1.get_uptime1()
        x = result2.split("m")
        y = x[0].split("h")
        b = int(y[-1])
        result = b-a
        print a,b,result
        return result

    #选择刷新时间，记录master ap的设备运行时间，来确认刷新时间的正确性---该函数只合适Never
    def check_never_validity(self):
        #点击接入点菜单
        tmp1 = APSBusiness(self.driver)
        tmp1.APS_menu()
        #选择页面上的刷新时间间隔
        tmp = NavbarControl(self.driver)
        tmp.refresh_menu()
        tmp.refresh_choose(u"永不")
        #获取主界面的运行时间
        result1 = tmp1.get_uptime1()
        #等待2分钟
        time.sleep(120)
        result2 = tmp1.get_uptime1()
        return result1,result2

    #连续切换刷新时间，确认显示正确
    def check_many_change_refresh_time(self):
        result = []
        for i in range(5):
            for T in ["15s","1min","2min","5min",u"永不"]:
                #选择页面上的刷新时间间隔
                tmp = NavbarControl(self.driver)
                tmp.refresh_menu()
                tmp.refresh_choose(T)
                #获取刷新时间
                result1 = tmp.get_refresh_time()
                if result1 == T:
                    result.append(True)
                else:
                    result.append(False)
        print result
        return result

    #切换刷新时间，然后重启路由后，确认依然有效
    def check_reboot_refresh_time(self,web,username,pwd):
        #选择页面上的刷新时间间隔为5min
        tmp = NavbarControl(self.driver)
        tmp.refresh_menu()
        tmp.refresh_choose("5min")
        #重启路由
        tmp1 = UpgradeBusiness(self.driver)
        tmp1.web_reboot(data_basic['DUT_ip'])
        #重新登录ap，获取刷新时间
        self.driver.get(web)
        self.driver.implicitly_wait(10)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        Lg.login(username,pwd)
        #获取刷新时间
        result = tmp.get_refresh_time()
        if result == "5min":
            return True
        else:
            return False

    # #打开配置弹窗，点击刷新按钮无效
    # def check_config_window_refresh_button(self):
    #     #进入接入点，打开master ap的配置弹窗
    #     tmp = APSBusiness(self.driver)
    #     tmp.APS_menu()
    #     tmp.click_edit(1)
    #     #点击刷新按钮
    #     tmp1 = NavbarBusiness(self.driver)
    #     tmp1.refresh_menu()
    #     #刷新时间下拉框是否显示
    #     result = tmp1.display_refresh_time()
    #     time.sleep(10)
    #     return result


    #######################################################################
    #############################以下是web语言的用例##########################
    #######################################################################
    #选择语言，检查页面语言是否生效
    def check_language_validity(self,lang):
        tmp = NavbarControl(self.driver)
        #点击页面上的语言按钮
        tmp.language_menu()
        #选择页面上的语言
        tmp.language_choose(lang)
        #找到导航栏固件的元素定位
        result = self.driver.find_element_by_id("versioninfo").text
        print result
        return result

    #检查登录页面的默认语言（本机是简体中文）
    def check_login_defualt_language(self):
        tmp = NavbarControl(self.driver)
        #点击页面上的退出按钮
        tmp.logout()
        tmp1 = LoginBusiness(self.driver)
        #获取所选择的语言
        result = tmp1.login_get_language()
        return result

    #切换登录页面的语言
    def check_login_change_language(self,lang):
        tmp = NavbarControl(self.driver)
        #点击页面上的退出按钮
        tmp.logout()
        tmp1 = LoginBusiness(self.driver)
        #点击页面上的语言按钮
        tmp1.login_language_menu()
        tmp1.login_language_choose(lang)
        #获取所选择的语言
        result = tmp1.login_get_language()
        return result

    #连续切换语言，确认其正确性
    def check_many_change_language(self):
        result = []
        dict = {"English":"Firmware",u"简体中文":u"固件"}
        for i in range(5):
            for j in dict.keys():
                #选择页面上的语言
                result1 = NavbarBusiness.check_language_validity(self,j)
                if dict.get(j) in result1:
                    result.append(True)
                else:
                    result.append(False)
        print result
        return result

    #切换语言，确认刷新时间语言正确
    def check_language_refresh(self,lang,Refresh_interval):
        tmp = NavbarControl(self.driver)
        #点击页面上的语言按钮
        tmp.language_menu()
        #选择页面上的语言
        tmp.language_choose(lang)
        #点击刷新时间按钮
        self.driver.find_element_by_xpath(".//*[@title='%s']/div/div"%Refresh_interval).click()
        #获取刷新时间的语言
        result = self.driver.find_element_by_xpath(".//*[@title='%s']/ul/li[5]/a"%Refresh_interval).text
        print result
        return result

    #切换语言，确认搜索功能语言正确
    def check_language_search(self,lang,text):
        tmp = NavbarControl(self.driver)
        #点击页面上的语言按钮
        tmp.language_menu()
        #选择页面上的语言
        tmp.language_choose(lang)
        #输入信息，获取搜索结果
        result = NavbarBusiness.search_result(self,text)
        return result
