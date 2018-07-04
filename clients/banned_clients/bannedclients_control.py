#coding=utf-8
#作者：曾祥卫
#时间：2017.12.07
#描述：GWN76xx客户端的禁止的客户端

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
import time

class BannedClientsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击禁止的客户端
    def bannedclients_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"禁止的客户端","Banned Clients")

    #点击解锁按钮
    def unblock_button(self, n):
        try:
            elements = self.driver.find_elements_by_css_selector(".unblockbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'unblock_button' element! The reason is %s"%e)

    #获取页面所有标题
    def get_titlediv(self):
        try:
            result = []
            elements = self.driver.find_elements_by_css_selector(".titlediv")
            self.driver.implicitly_wait(20)
            for element in elements:
                result.append(element.text)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_titlediv' element! The reason is %s"%e)
