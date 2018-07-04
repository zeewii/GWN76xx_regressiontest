#coding=utf-8
#作者：曾祥卫
#时间：2017.06.13
#描述：GWN76xx系统设置-调试-Ping/路由跟踪的控制层

from publicControl.public_control import PublicControl
from selenium.webdriver.support.select import Select

class PingControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击调试
    def Debug_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"调试","Debug")





    ###########################################################
    #以下是调试主页面中的操作
    ###########################################################
    #点击抓包菜单
    def Capture_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___capture")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Capture_menu' element! The reason is %s"%e)

    #点击Core文件菜单
    def Core_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___corefiles")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Core_menu' element! The reason is %s"%e)

    #点击Ping/路由跟踪 菜单
    def Ping_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___ping")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Ping_menu' element! The reason is %s"%e)

    #点击系统日志菜单
    def Syslog_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___systemlog")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Syslog_menu' element! The reason is %s"%e)


    ###########################################################
    #以下是Ping/路由跟踪 页面中的操作
    ###########################################################
    #输入目标值
    def set_ping_target(self,value):
        try:
            element = self.driver.find_element_by_id("ping_target")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_ping_target' element! The reason is %s"%e)

    #选择工具
    def set_ping_tool(self,text):
        try:
            element = self.driver.find_element_by_id("ping_tool")
            Select(element).select_by_visible_text(text)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_ping_tool' element! The reason is %s"%e)

    #点击开始
    def click_ping_run(self):
        try:
            element = self.driver.find_element_by_id("ping_run")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_ping_run' element! The reason is %s"%e)

    #获取输出的结果
    def get_ping_output(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("ping_output")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_ping_output' element! The reason is %s"%e)



