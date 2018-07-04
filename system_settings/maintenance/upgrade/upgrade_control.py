#coding=utf-8
#作者：曾祥卫
#时间：2017.03.16
#描述：GWN76xx系统设置-升级的控制层

from data import data
from publicControl.public_control import PublicControl
import time
from selenium.webdriver.support.ui import Select

class UpgradeControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击系统设置
    def System_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"系统设置","System Settings")
        #PublicControl.menu_css(self,".zone-zone.menuselected>a")


    ###########################################################
    #以下是系统设置主页面中的操作
    ###########################################################
    #点击基本菜单
    def Basic_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream_general")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Basic_menu' element! The reason is %s"%e)

    #点击升级菜单
    def Upgrade_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream_provision")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Upgrade_menu' element! The reason is %s"%e)

    #点击访问菜单
    def Access_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___password")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Access_menu' element! The reason is %s"%e)

    #点击外部系统日志菜单
    def External_Syslog_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___debug")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'External_Syslog_menu' element! The reason is %s"%e)


    #点击内部系统日志菜单
    def Internal_Syslog_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream_debug")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Internal_Syslog_menu' element! The reason is %s"%e)


    #点击保存
    def save(self):
        try:
            element = self.driver.find_element_by_css_selector("div.btn-group > button.btn.btn-primary")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'save_button' element! The reason is %s"%e)

    #点击重置
    def reset(self):
        try:
            element = self.driver.find_element_by_css_selector("div.btn-group > button.btn.btn-cancel")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'reset_button' element! The reason is %s"%e)


    ###########################################################
    #以下是升级页面中的操作
    ###########################################################
    #切换升级方式
    def set_firmware_protocal(self,mode):
        try:
            a = Select(self.driver.find_element_by_id("firmware_protocal"))
            #选择TFTP
            if mode == 'TFTP':
                a.select_by_visible_text("TFTP")
            #选择HTTP
            elif mode == 'HTTP':
                a.select_by_visible_text("HTTP")
            #选择HTTPS
            elif mode == 'HTTPS':
                a.select_by_visible_text("HTTPS")
            else:
                print "Firmware Protocal please input TFTP,HTTP,HTTPS"
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'firmware_protocal' element! The reason is %s"%e)


    #设置固件服务器，输入的地址为本机的ip地址
    #输入:eth为PC有线网卡的接口名
    def set_FM_server(self,addr):
        try:
            element = self.driver.find_element_by_id("firmware_server")
            element.clear()
            element.send_keys(addr)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'FM_server' element! The reason is %s"%e)

    #点击启动时检查
    def set_on_boot(self):
        try:
            element = self.driver.find_element_by_id("field_grandstream_provision_provision_on_boot")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_on_boot' element! The reason is %s"%e)


    #点击升级
    def upgrade_button(self):
        try:
            element = self.driver.find_element_by_id("field_grandstream_provision_provision_upgrade")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'upgrade_button' element! The reason is %s"%e)


    #点击重启
    def reboot(self):
        try:
            element = self.driver.find_element_by_id("field_grandstream_provision_provision_reboot")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'reboot' element! The reason is %s"%e)

    #获取重启按钮的名称
    def get_reboot(self):
        try:
            element = self.driver.find_element_by_id("field_grandstream_provision_provision_reboot")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_reboot' element! The reason is %s"%e)

    #点击恢复出厂
    def factory_reset(self):
        try:
            element = self.driver.find_element_by_id("field_grandstream_provision_provision_factreset")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'factory_reset' element! The reason is %s"%e)

    #获取重置按钮的名称
    def get_reset(self):
        try:
            element = self.driver.find_element_by_id("field_grandstream_provision_provision_factreset")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_reset' element! The reason is %s"%e)

    ###########################################################
    #以下是系统日志页面中的操作
    ###########################################################
    #输入系统日志服务器地址
    def set_syslog_uri(self,uri):
        try:
            element = self.driver.find_element_by_id("syslog_uri")
            element.clear()
            element.send_keys(uri)
        except Exception as e:
            raise Exception("webpage has not found 'set_syslog_uri' element! The reason is %s"%e)
