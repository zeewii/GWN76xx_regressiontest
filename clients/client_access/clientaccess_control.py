#coding=utf-8
#作者：曾祥卫
#时间：2017.03.29
#描述：GWN76xx客户端的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
import time

class ClientAccessControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    #点击客户端访问菜单
    def clientaccess_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"客户端访问","Client Access")
        #time.sleep(5)

    #点击添加按钮
    def add_button(self):
        try:
            element = self.driver.find_element_by_id("newbmRules")
            element.click()
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'add_button' element! The reason is %s"%e)

    #编辑Global Blacklist
    def edit_Global_Blacklist_button(self):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[0].click()
            self.driver.implicitly_wait(60)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'edit_Global_Blacklist_button' element! The reason is %s"%e)


    #只有一个新增访问列表时，点击编辑
    def edit_button(self):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[-1].click()
            self.driver.implicitly_wait(60)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'edit_button' element! The reason is %s"%e)

    #有多个新增访问列表时，选择特定的访问列表，点击编辑
    #输入：n:第几个访问列表
    def edit_access_n_button(self,n):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'edit_access_n_button' element! The reason is %s"%e)

    #只添加了一个新增访问列表时，点击删除这个访问列表的删除按钮
    def del_first_button(self):
        try:
            element = self.driver.find_element_by_id("del_cacl0")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'del_first_button' element! The reason is %s"%e)


    #获取Global Blacklist的删除的显示状态
    #输出：True：灰色（无法点击）,False:不是灰色（可以点击）
    def get_global_del_button_status(self):
        try:
            element = self.driver.find_element_by_id("del_global")
            self.driver.implicitly_wait(20)
            result = element.get_attribute("disabled")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_global_del_button_status' element! The reason is %s"%e)

    #点击Global Blacklist的删除按钮
    def set_global_del_button(self):
        try:
            element = self.driver.find_element_by_id("del_global")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_global_del_button' element! The reason is %s"%e)

    #获取Global Blacklist的mac地址
    def get_Global_Blacklist(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='blockMacRules_table']/div[2]/div[2]/div")
            result = element.get_attribute("title")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_Global_Blacklist' element! The reason is %s"%e)

    #获取access list1的mac地址
    def get_Access_List1(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='blockMacRules_table']/div[3]/div[2]/div")
            result = element.get_attribute("title")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_Access_List1' element! The reason is %s"%e)

    #获取页面上所有的标题
    def g_all_title(self):
        try:
            result = []
            elements = self.driver.find_elements_by_class_name("titlediv")
            for element in elements:
                result.append(element.get_attribute("title"))
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_all_title' element! The reason is %s"%e)

    #获取access list对应的mac地址
    def get_Access_List_n(self,name):
        try:
            i = 2
            while i<20:
                xpath = ".//*[@id='blockMacRules_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                title = element.get_attribute("title")
                print title
                if name in title:
                    element1 = self.driver.find_element_by_xpath(".//*[@id='blockMacRules_table']/div[%s]/div[2]/div"%i)
                    result = element1.get_attribute("title")
                    print result
                    return result
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'get_Access_List_n' element! The reason is %s"%e)

    #编辑对应的access list
    def edit_access_list_n(self,name):
        try:
            i = 2
            while i<20:
                xpath = ".//*[@id='blockMacRules_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                title = element.get_attribute("title")
                print title
                if name in title:
                    element1 = self.driver.find_element_by_xpath(".//*[@id='blockMacRules_table']/div[%s]/div[3]/div/button[1]"%i)
                    element1.click()
                    self.driver.implicitly_wait(20)
                    break
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'edit_access_list_n' element! The reason is %s"%e)

    #删除对应的access list
    def del_access_list_n(self,name):
        try:
            i = 2
            while i<20:
                xpath = ".//*[@id='blockMacRules_table']/div[%s]/div[1]/div"%i
                element = self.driver.find_element_by_xpath(xpath)
                title = element.get_attribute("title")
                print title
                if name in title:
                    element1 = self.driver.find_element_by_xpath(".//*[@id='blockMacRules_table']/div[%s]/div[3]/div/button[2]"%i)
                    element1.click()
                    self.driver.implicitly_wait(20)
                    break
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'del_access_list_n' element! The reason is %s"%e)




    ###########################################################
    #以下是添加窗口中的操作
    ###########################################################
    #在添加窗口输入一个mac地址
    def set_mac(self,mac):
        try:
            element = self.driver.find_element_by_id("mac")
            element.clear()
            element.send_keys(mac)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_mac' element! The reason is %s"%e)

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

    #点击保存
    def save(self):
        try:
            element = self.driver.find_element_by_id("m_save")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'save' element! The reason is %s"%e)

    #在添加窗口点击+号
    def set_add_mac(self):
        try:
            element = self.driver.find_element_by_css_selector(".btn.btn-success.macbtn.addmac")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_add_mac' element! The reason is %s"%e)

    #添加窗口，点击+号，输入一个mac地址
    def set_add_addmac(self):
        try:
            element = self.driver.find_element_by_css_selector(".btn.btn-success.macbtn.addmac")
            element.click()
            self.driver.implicitly_wait(20)
            elements = self.driver.find_elements_by_css_selector(".form-control.luci2-field-validate.macinput.tableinput")
            elements[-1].clear()
            #取随机mac地址
            random_mac = PublicControl.randomMAC(self)
            elements[-1].send_keys(random_mac)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_add_addmac' element! The reason is %s"%e)

    #添加窗口，一直点击-号，删除所有的mac，只保留第一个mac地址
    def del_all_addmac(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".btn.macbtn.btn-danger.delmac")
            for element in elements[1:]:
                element.click()
                self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_all_addmac' element! The reason is %s"%e)

    #添加窗口，一直点击-号，删除所有的mac，不保留第一个mac地址
    def del_all_addmac_backup(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".btn.macbtn.btn-danger.delmac")
            for element in elements:
                element.click()
                self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_all_addmac_backup' element! The reason is %s"%e)


    #获取Global Blacklist的名称的显示状态
    #输出：True：灰色（无法点击）,False:不是灰色（可以点击）
    def get_global_name_status(self):
        try:
            element = self.driver.find_element_by_id("name")
            self.driver.implicitly_wait(20)
            result = element.get_attribute("disabled")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_global_name_status' element! The reason is %s"%e)


    #在添加窗口点击关闭
    def close_edit(self):
        try:
            element = self.driver.find_element_by_id("closeedit")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'close_edit' element! The reason is %s"%e)

    #修改list的名称
    def set_list_name(self,name):
        try:
            element = self.driver.find_element_by_id("name")
            element.clear()
            element.send_keys(name)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_list_name' element! The reason is %s"%e)
