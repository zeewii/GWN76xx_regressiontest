#coding=utf-8
#作者：曾祥卫
#时间：2017.03.29
#描述：GWN76xx客户端访问的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
import time

class ClientsControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    #点击客户端菜单
    def clients_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"客户端","Clients")
        #time.sleep(5)

    #获取客户端的类型
    def get_cient_type(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[5]"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_cient_type' element! The reason is %s"%e)

    #获取客户端的名字
    def get_client_name(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[2]/div"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_client_name' element! The reason is %s"%e)

    #获取客户端的IP地址
    def get_client_IP(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[6]"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_client_IP' element! The reason is %s"%e)

    #获取客户端的连接时间
    def get_client_time(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[8]/div/div[2]"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_client_time' element! The reason is %s"%e)


    #获取客户端的在线状态
    def get_online_status(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[8]/div/div[1]/span"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_online_status' element! The reason is %s"%e)

    #获取客户端的离线状态
    def get_offline_status(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[8]/div/span"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_offline_status' element! The reason is %s"%e)

    #点击编辑按钮
    def set_edit(self,mac):
        try:
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                print(MAC)
                if MAC in element.text:
                    print "click edit mac:%s!"%mac
                    self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[17]/div/button[1]"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
            time.sleep(3)
        except:
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "click edit mac:%s!"%mac
                    self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[15]/div/button[1]"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
            time.sleep(3)


    #点击阻塞按钮
    def set_block(self,mac):
        try:
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "click block mac:%s!"%mac
                    self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[17]/div/button[2]"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
            time.sleep(3)
        except:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "click block mac:%s!"%mac
                    self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[15]/div/button[2]"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
            time.sleep(3)


    #点击禁止客户端按钮
    def click_banned_client(self):
        try:
            element = self.driver.find_element_by_id("banneddiv")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'click_banned_client' element! The reason is %s"%e)

    #获取客户端所连接的AP的mac
    def get_AP_name(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[12]/a"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_AP_name' element! The reason is %s"%e)


    #获取客户端所连接的AP名称
    def get_AP_name_no_mac(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='clients_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s!"%mac
                    element1 = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[10]/div/div[1]/a"%i)
                    result = element1.text
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_AP_name' element! The reason is %s"%e)


    #通过ssid过滤
    def ssid_filter(self,link):
        try:
            first = self.driver.find_element_by_xpath(".//*[@id='filterdiv']/div[1]/div/div")
            first.click()
            time.sleep(5)
            self.driver.find_element_by_link_text(link).click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'ssid_filter' element! The reason is %s"%e)

    #获取客户端的数量
    def get_clients_num(self):
        try:
            elements = self.driver.find_elements_by_class_name("blockbutton")
            result = len(elements)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_clients_num' element! The reason is %s"%e)



    #####################################################################
    #######以下是禁止客户端的操作############################################
    #####################################################################

    #获取被block的客户端的mac地址
    def get_block_client(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='banned_mac']/div[1]/input")
            result = element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_block_client' element! The reason is %s"%e)

    #设置block的客户端的mac地址
    def set_block_client(self,mac):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='banned_mac']/div[1]/input")
            element.clear()
            element.send_keys(mac)
        except Exception as e:
            raise Exception("webpage has not found 'set_block_client' element! The reason is %s"%e)


    #点击减号按钮
    def click_minus(self):
        try:
            element = self.driver.find_element_by_css_selector(".btn.btn-danger")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_minus' element! The reason is %s"%e)

    #点击加号按钮
    def click_plus(self):
        try:
            element = self.driver.find_element_by_css_selector(".btn.btn-success")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_plus' element! The reason is %s"%e)

    #点击保存
    def save(self):
        try:
            element = self.driver.find_element_by_id("ban_save")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'save' element! The reason is %s"%e)

    #添加mac地址输入框,并输入随机mac地址
    def set_addmac(self):
        try:
            element = self.driver.find_element_by_css_selector(".btn.btn-success")
            element.click()
            elements1 = self.driver.find_elements_by_xpath(".//*[@id='banned_mac']//input")
            elements1[-1].clear()
            #取随机mac地址
            random_mac = PublicControl.randomMAC(self)
            elements1[-1].send_keys(random_mac)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_addmac' element! The reason is %s"%e)

    #删除最后一个mac输入框
    def del_addmac(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".btn.btn-danger")
            elements[0].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_addmac' element! The reason is %s"%e)

    #关闭禁用客户端窗口
    def close_banned_client(self):
        try:
            element = self.driver.find_element_by_id("closebanedit")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'close_banned_client' element! The reason is %s"%e)




    #####################################################################
    #######以下是编辑--状态的操作############################################
    #####################################################################
    #获取客户端mac
    def get_edit_client_mac(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("mac")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_edit_client_mac' element! The reason is %s"%e)

    #获取SSID
    def get_edit_ssid(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("conssid")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_edit_ssid' element! The reason is %s"%e)

    #获取连接方式
    def get_edit_connecttype(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("connecttype")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_edit_connecttype' element! The reason is %s"%e)

    #获取已连接的AP的mac
    def get_edit_conap(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("conap")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_edit_conap' element! The reason is %s"%e)

    #获取已连接的AP的信道
    def get_edit_channel(self):
        try:
            element = self.driver.find_element_by_id("channel")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_edit_channel' element! The reason is %s"%e)

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



    #####################################################################
    #######以下是用户配置页面的操作##########################################
    #####################################################################
    #点击配置菜单
    def config_menu(self):
        try:
            element = self.driver.find_element_by_id("m_config")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'config_menu' element! The reason is %s"%e)

    #输入客户端名称
    #输入：客户端名称
    def set_client_name(self,name):
        try:
            element = self.driver.find_element_by_id("name")
            element.clear()
            element.send_keys(name)
        except Exception as e:
            raise Exception("webpage has not found 'set_client_name' element! The reason is %s"%e)

    #点击保存
    def client_save(self):
        try:
            element = self.driver.find_element_by_id("m_saveclient")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'client_save' element! The reason is %s"%e)
