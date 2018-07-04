#coding=utf-8
#作者：曾祥卫
#时间：2017.12.06
#描述：GWN76xx客户端的时间策略控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
import time

class TimePolicyControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击时间策略菜单
    def timepolicy_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"时间策略","Time Policy")

    #点击添加按钮
    def add_button(self):
        try:
            element = self.driver.find_element_by_id("newobj")
            element.click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'add_button' element! The reason is %s"%e)

    #点击编辑按钮
    def edit_button(self, n):
        try:
            elements = self.driver.find_elements_by_css_selector(".editbutton")
            elements[n].click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'edit_button' element! The reason is %s"%e)

    #点击删除按钮
    def del_button(self, n):
        try:
            elements = self.driver.find_elements_by_css_selector(".delbutton")
            elements[n].click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'del_button' element! The reason is %s"%e)

    #依次点击所有组的删除按钮
    def del_all_button(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".delbutton")
            for element in elements:
                element.click()
                PublicControl.notice_ok(self)
                self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'del_all_button' element! The reason is %s"%e)

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



    #################以下新建策略的页面上###########################
    #设置名称
    def set_name(self, n, name):
        try:
            element = self.driver.find_element_by_id("field_grandstream_tc%s_tc%s_name"%(n, n))
            element.clear()
            element.send_keys(name)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_name' element! The reason is %s"%e)

    #点击开启
    def click_enable_disable(self, n):
        try:
            element = self.driver.find_element_by_id("field_grandstream_tc%s_tc%s_enabled"%(n, n))
            element.click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'click_enable_disable' element! The reason is %s"%e)

    # #检查开启是否个勾选
    # def check_enable_disable(self, n):
    #     try:
    #         element = self.driver.find_element_by_id("field_grandstream_tc%s_tc%s_enabled"%(n, n))
    #         result = element.is_selected()
    #         print result
    #         return result
    #     except Exception as e:
    #         raise Exception("webpage has not found 'check_enable_disable' element! The reason is %s"%e)

    #设置客户端连接限制时间
    def set_connection_time(self, n, value):
        try:
            element = self.driver.find_element_by_id("field_grandstream_tc%s_tc%s_connection_time"%(n, n))
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_connection_time' element! The reason is %s"%e)

    #设置客户端连接限制时间的单位
    #unit:m, h, d
    def set_connection_time_unit(self,unit):
        try:
            elements = self.driver.find_elements_by_css_selector('.form-control.unit-select')
            Select(elements[0]).select_by_value(unit)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_connection_time_unit' element! The reason is %s"%e)

    #设置客户端重连超时类型
    #unit:daily, weekly, hourly, timed
    def set_reconnect_type(self, n, unit):
        try:
            element = self.driver.find_element_by_id('field_grandstream_tc%s_tc%s_reconnect_type'%(n, n))
            Select(element).select_by_value(unit)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_reconnect_type' element! The reason is %s"%e)

    #设置每天的第几小时重连
    def set_reset_hour(self, n, value):
        try:
            element = self.driver.find_element_by_id("field_grandstream_tc%s_tc%s_reset_hour"%(n, n))
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_reset_hour' element! The reason is %s"%e)

    #设置每周的第几天
    #text:星期日， 星期一......星期六
    def set_reset_day(self, n, text):
        try:
            element = self.driver.find_element_by_id('field_grandstream_tc%s_tc%s_reset_day'%(n, n))
            Select(element).select_by_visible_text(text)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_reset_day' element! The reason is %s"%e)

    #设置客户端重连超时
    def set_connection_timeout(self, n, value):
        try:
            element = self.driver.find_element_by_id("field_grandstream_tc%s_tc%s_connection_timeout"%(n, n))
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_connection_timeout' element! The reason is %s"%e)

    #设置客户端重连超时的单位
    #unit:m, h, d
    def set_connection_timeout_unit(self,unit):
        try:
            elements = self.driver.find_elements_by_css_selector('.form-control.unit-select')
            Select(elements[1]).select_by_value(unit)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_connection_timeout_unit' element! The reason is %s"%e)

    #点击保存
    def click_save(self):
        try:
            element = self.driver.find_element_by_id("m_save")
            element.click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'click_save' element! The reason is %s"%e)



    #判断页面上提示信息是否正确
    def check_error(self,text):
        try:
            self.driver.implicitly_wait(10)
            error_infos = self.driver.find_elements_by_css_selector(".luci2-field-error.label.label-danger")
            print len(error_infos)
            for error_info in error_infos:
                if error_info.is_displayed() == True:
                    return True
            return False
        except:
            return False

    #判断页面上有新建的时间策略
    def check_have_timepolicy(self):
        try:
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_css_selector('.editbutton')
            return True
        except:
            return False

    #判断页面上是否有Enable图标
    def check_enbale_timepolicy(self):
        try:
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_css_selector('.enableicon')
            return True
        except:
            return False