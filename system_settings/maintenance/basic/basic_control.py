#coding=utf-8
#作者：曾祥卫
#时间：2017.05.26
#描述：GWN76xx系统设置-基本的控制层

from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
import time

class BasicControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    #选择设置不同的时区
    def set_time_zone(self,text):
        try:
            element = self.driver.find_element_by_id("field_grandstream_general_general_timezone")
            Select(element).select_by_visible_text(text)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_time_zone' element! The reason is %s"%e)

     #切换国家代码
    def set_country_code(self,country_code):
        try:
            element = self.driver.find_element_by_id("country_code")
            Select(element).select_by_value(country_code)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'country_code' element! The reason is %s"%e)

    #修改NTP 服务器
    def set_ntp_server(self,ntpser):
        try:
            elements = self.driver.find_elements_by_css_selector("div.input-group > input.form-control.luci2-field-validate")
            elements[-2].clear()
            elements[-2].send_keys(ntpser)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_ntp_server' element! The reason is %s"%e)


    #点击增加NTP 服务器
    def add_ntpser_button(self):
        try:
            element = self.driver.find_element_by_css_selector(".btn.btn-success")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'add_ntpser_button' element! The reason is %s"%e)


    #点击移除ntp服务器
    def remove_ntpser_button(self):
        try:
            elements = self.driver.find_elements_by_css_selector("span.input-group-btn > button.btn.btn-danger")
            for element in elements:
                element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'remove_ntpser_button' element! The reason is %s"%e)




