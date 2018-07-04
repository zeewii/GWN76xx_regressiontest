#coding=utf-8
#作者：曾祥卫
#时间：2017.05.23
#描述：GWN76xx设置向导的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from publicControl.public_control import PublicControl
import time

class NavbarControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击页面上的问号开启设置向导
    def SW_menu(self):
        try:
            element = self.driver.find_element_by_id("helpbtn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'setupwizard' element! The reason is %s"%e)

    #点击页面上的放大镜打开搜索框
    def search_menu(self):
        try:
            element = self.driver.find_element_by_id("searchbtn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'search_menu' element! The reason is %s"%e)

    #点击页面上的刷新时间间隔
    def refresh_menu(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@title='刷新间隔']/div/div")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'refresh_menu' element! The reason is %s"%e)

    #选择页面上的刷新时间间隔
    def refresh_choose(self,time):
        try:
            if time == "15s":
                n = 1
            elif time == "1min":
                n = 2
            elif time == "2min":
                n = 3
            elif time == "5min":
                n = 4
            elif time == u"永不" or time == "Never":
                n = 5
            element = self.driver.find_element_by_xpath(".//*[@title='刷新间隔']/ul/li[%d]/a"%n)
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'refresh_choose' element! The reason is %s"%e)


    #点击页面上的语言按钮
    def language_menu(self):
        try:
            element = self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div[8]/div/div")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'language_menu' element! The reason is %s"%e)

    #选择页面上的语言
    def language_choose(self,lang):
        try:
            if lang == "English":
                n = 1
            elif lang == u"简体中文":
                n = 2
            element = self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div[8]/ul/li[%d]/a"%n)
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'language_choose' element! The reason is %s"%e)


    #点击页面上的退出按钮
    def logout(self):
        try:
            element = self.driver.find_element_by_id("logoutbtn")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'logout' element! The reason is %s"%e)


    #######################################################################
    #############################以下是搜索框的方法###########################
    #######################################################################

    #检查页面中是否有搜索按钮
    #输出：True：有搜索按钮;False：无搜索按钮
    def check_search_buttton(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_id("searchbtn")
            return True
        except:
            return False

    #检查页面中是否有搜索框
    #输出：有则返回True，没有则返回False
    def check_search_input(self):
        try:
            element = self.driver.find_element_by_id("searchinput")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_search_input' element! The reason is %s"%e)


    #在弹出的搜索框中输入内容,并在键盘中按enter
    def set_search(self,text):
        try:
            element = self.driver.find_element_by_id("searchinput")
            element.clear()
            element.send_keys(text)
            element.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_search' element! The reason is %s"%e)

    #获取搜索结果信息
    def get_search_result_info(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("searchresult")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_search' element! The reason is %s"%e)


    #检查页面中搜索框下是否有搜索结果
    #输出：有则返回True，没有则返回False
    def check_search_result(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("searchresult")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_search_result' element! The reason is %s"%e)

    #获取搜索的结果
    def get_search_result(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_xpath(".//*[@class='resultBox']//div")
            for element in elements:
                print element.text
                result.append(element.text)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_search_result' element! The reason is %s"%e)

    #只有一个搜索结果时，点击搜索结果
    def click_search_result(self,text):
        try:
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_xpath(".//*[@class='resultBox']//div")
            for element in elements:
                if text in element.text:
                    element.click()
                    self.driver.implicitly_wait(10)
                    time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'click_search_result' element! The reason is %s"%e)


    #######################################################################
    #############################以下是刷新时间的方法###########################
    #######################################################################
    #检查页面中是否有搜索按钮
    #输出：True：有搜索按钮;False：无搜索按钮
    def check_refresh_buttton(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@title='刷新间隔']")
            return True
        except:
            return False

    #获取刷新时间
    def get_refresh_time(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@title='刷新间隔']/div/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_refresh_time' element! The reason is %s"%e)

    #刷新时间下拉框是否显示
    #输出：有则返回True，没有则返回False
    def display_refresh_time(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@title='刷新间隔']/ul/li[2]/a")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'display_refresh_time' element! The reason is %s"%e)


    #######################################################################
    #############################以下是web语言的用例##########################
    #######################################################################
    #检查页面中是否有语言按钮
    #输出：True：有搜索按钮;False：无搜索按钮
    def check_language_buttton(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div[8]/div/div")
            return True
        except:
            return False

    #获取所选择的语言
    def get_language(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div[8]/div/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_language' element! The reason is %s"%e)

    #语言下拉框是否显示
    #输出：有则返回True，没有则返回False
    def display_language(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div[8]/ul/li[2]/a")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'display_language' element! The reason is %s"%e)
