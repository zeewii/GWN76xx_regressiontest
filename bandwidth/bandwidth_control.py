#coding=utf-8
#作者：蒋甜
#时间：2018.03.29
#描述：GWN76xx带宽规则的控制层

from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import subprocess
from data import data
from selenium.webdriver.support.ui import WebDriverWait

d = data.data_basic()

import time

class BandwidthControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    ########################################################
    ###############带宽规则界面################################
    ########################################################

    #点击页面上带宽规则
    def Bw_menu(self):
        PublicControl.menu_css(self,u"带宽规则",'Bandwidth Rules')

    #点击带宽页面中的添加带宽规则
    def add_Bandwidth_Rule_Bt(self):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("newbwRules")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'add_Bandwidth_Rule' element! The reason is %s"%e)

     #勾选/去勾选带宽规则
    def enable_dis_Bandwidth(self):
        try:
            element = self.driver.find_element_by_id("enabled")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'enable_dis_Bandwidth' element! The reason is %s"%e)

    #选择所有ssid
    def check_all_ssid(self):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("chkall")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'check_all_ssid' element! The reason is %s"%e)

    #16个ssid时，添加带宽规则时翻页
    def pagedown_16ssid(self):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_id']/label[14]/input")
            element.send_keys(Keys.TAB)
        except Exception as e:
            raise Exception("webpage has not found 'pagedown_16ssid' element! The reason is %s"%e)


    #选择none ssid
    def check_none_ssid(self):
        try:
            element = self.driver.find_element_by_id("unchkall")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'check_none_ssid' element! The reason is %s"%e)

    #选择第n个ssid
    def select_n_ssid(self,n):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(3)
            xpath = ".//*[@id='ssid_id']/label[%s]/input"%n
            element = self.driver.find_element_by_xpath(xpath)
            element.click()
        except Exception as e:
            raise Exception("webpage has not found 'select_one_ssid' element! The reason is %s"%e)

    #选择约束范围,全部,MAC,IP地址
    def select_Range_Constraint(self,type):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(5)
            a = self.driver.find_element_by_id("type")
            if type == 'All':
                a.send_keys("a")
                a.send_keys(Keys.TAB)
            elif type == 'MAC':
                a.send_keys("m")
                a.send_keys(Keys.TAB)
            elif type == 'IP Address':
                a.send_keys("i")
                a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'select_Range_Constraint' element! The reason is %s"%e)

    #选择约束范围 MAC后需输入MAC地址
    def Mac_Address(self,mac):
        try:
            element = self.driver.find_element_by_id("bwRulesMac")
            element.send_keys(mac)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'Mac_Address'element! The reason is %s"%e)

    #选择约束范围 IP后需输入IP地址
    def IP_Address(self,ip):
        try:
            time.sleep(5)
            element = self.driver.find_element_by_id("bwRulesIp")
            element.send_keys(ip)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'IP_Address'element! The reason is %s"%e)

    #设置上传速率
    def set_Upstream_Rate(self,rate):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("urate")
            element.clear()
            element.send_keys(rate)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_Upstream_Rate'element! The reason is %s"%e)

    #清空上传速率的值
    def clear_Upstream_Rate(self):
        try:
            time.sleep(2)
            element = self.driver.find_element_by_id("urate")
            element.clear()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_Upstream_Rate'element! The reason is %s"%e)

    #设置下载速率
    def set_Downstream_Rate(self,rate):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("drate")
            element.clear()
            element.send_keys(rate)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_Downstream_Rate'element! The reason is %s"%e)

     #清空上传速率的值
    def clear_Downstream_Rate(self):
        try:
            element = self.driver.find_element_by_id("drate")
            element.clear()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_Downstream_Rate'element! The reason is %s"%e)

    #设置上传速率单位
    def set_Upstream_Rate_unit(self,unit):
        try:
            a = self.driver.find_element_by_css_selector(".form-control.unit-select.urate-unit")
            a.click()
            if "M" == unit:
                a.send_keys("M")
                a.send_keys(Keys.TAB)
            if "k" == unit:
                a.send_keys("k")
                a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_Upstream_Rate_unit'element! The reason is %s"%e)

    #设置下载速率单位
    def set_Downstream_Rate_unit(self,unit):
        try:
            time.sleep(3)
            a = self.driver.find_element_by_css_selector(".form-control.unit-select.drate-unit")
            if "M" == unit:
                a.send_keys("M")
                a.send_keys(Keys.TAB)
            if "k" == unit:
                a.send_keys("k")
                a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_Downstream_Rate_unit'element! The reason is %s"%e)

    #设置保存
    def save(self):
        try:
            element = self.driver.find_element_by_id("m_save")
            element.click()
            time.sleep(3)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'save'element! The reason is %s"%e)

    #检查带宽规则界面的编辑按钮
    def check_edit_button_backup(self,n):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            print n
            element = elements[n-1]
            time.sleep(3)
            self.driver.implicitly_wait(20)
            if element.is_enabled():
                return True
            else:
                return False
        except :
            return False

    #检查带宽规则界面的编辑按钮
    def check_edit_button(self,n):
        try:
            element = self.driver.find_elements_by_class_name("editbutton")[n-1]
            print element
            return True
        except :
            return False

    #点击带宽规则界面的编辑按钮
    def click_edit_button(self,n):
        try:
            time.sleep(5)
            elements = self.driver.find_elements_by_class_name("editbutton")
            element = elements[n-1]
            element.click()
            time.sleep(3)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_edit_button' element! The reason is %s"%e)

    #检查第n条规则开启/关闭带宽规则的状态
    def check_enable_bandwidth(self,n):
        try:
            n+=1
            xpath = ".//*[@id='bandwidthRules_table']/div[%s]/div[1]/div"%n
            elements = self.driver.find_element_by_xpath(xpath)
            a = elements.get_attribute("class")
            return a
        except Exception as e:
            raise Exception("webpage has not found 'check_enable_bandwidth' element! The reason is %s"%e)

    #检查ssid是否被勾选
    def ssid_checkd(self):
        try:
            result = []
            elements = self.driver.find_elements_by_xpath(".//*[@id='ssid_id']//input")
            for element in elements:
                a = element.get_attribute("checked")
                print a
                if a:
                    result.append(True)
                else:
                    result.append(False)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'ssid_checkd' element! The reason is %s"%e)

    #添加带宽规则时，ssid名称列表显示
    def check_ssid_name(self,ssid):
        n =2
        while(n<10):
            xpath=".//*[@id='bandwidthRules_table']/div[%s]/div[2]/div"%n
            print xpath
            time.sleep(10)
            try:
                element =self.driver.find_element_by_xpath(xpath)
                a = element.get_attribute("title")
                if a == ssid:
                    return True
                n+=1
            except:
                return False

    #删除界面所有的带宽规则
    def del_bandwidth_rule_button(self):
        try:
            time.sleep(3)
            elements = self.driver.find_elements_by_class_name("delbutton")
            for element in elements:
                try:
                    if element.is_enabled():
                        element.click()
                        PublicControl.notice_ok(self)
                except:
                    print "webpage has not found 'title' or 'notice_ok' attribute"
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_bandwidth_rule_button' element! The reason is %s"%e)

    #查看某规则对应的范围
    def check_range(self,n):
        xpath = ".//*[@id='bandwidthRules_table']/div[%s]/div[3]/div"%(n+1)
        print xpath
        time.sleep(10)
        try:
            element =self.driver.find_element_by_xpath(xpath)
            a = element.get_attribute("title")
            print a
            if a == "All"or a == u"全部":
                result = "All"
                return result
            if a =="MAC":
                result = "MAC"
                return result
            if a =="IP Address":
                result = "IP"
                return result
        except:
            return False

    #查看某规则对应的MAC/IP设置
    def check_mac_ip(self,mac,n):
        xpath = ".//*[@id='bandwidthRules_table']/div[%s]/div[4]/div"%(n+1)
        print xpath
        time.sleep(10)
        try:
            element = self.driver.find_element_by_xpath(xpath)
            a = element.get_attribute("title")
            print a
            if mac == a:
                return True
        except:
            return False

    #查看上游速率
    def check_upstream_rule(self,n,upstream):
        time.sleep(5)
        xpath = ".//*[@id='bandwidthRules_table']/div[%s]/div[5]/div"%(n+1)
        print xpath
        time.sleep(10)
        try:
            element = self.driver.find_element_by_xpath(xpath)
            a = element.get_attribute("title")
            b= a.split('M')
            print b[0]
            print a
            if upstream == b[0]:
                return True
        except:
            return False


    #判断输入框下方是否有错误提示,有则返回True，没有则返回False
    def check_error(self):
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

    #关闭
    def bandwidth_cancel(self):
        time.sleep(2)
        element = self.driver.find_element_by_id("m_cancel")
        element.click()

    #根据ssid找特定的带宽规则
    def del_special_bandwidth_rule(self,n):
        self.driver.implicitly_wait(10)
        time.sleep(3)
        id = "del_rule%s"%(n-1)
        time.sleep(3)
        element = self.driver.find_element_by_id(id)
        element.click()

    #删除带宽规则确认按钮
    def del_bandwidth_rule_ok_button(self):
        time.sleep(3)
        try:
            element = self.driver.find_element_by_xpath("html/body/div[11]/div/div/div[3]/button[1]")
            element.click()
        except Exception as e:
            raise Exception("webpage has not found 'del_bandwidth_rule' element! The reason is %s"%e)

