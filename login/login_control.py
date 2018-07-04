#coding=utf-8
#作者：曾祥卫
#时间：2017.03.10
#描述：GWN7610登录的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
import time
from data import data

class LoginControl(PublicControl):

    def __init__(self,driver,username=None,pwd=None):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)
        #自己LoginControl类的属性
        self.username = username
        self.pwd = pwd

    #输入用户名
    def set_username(self):
        try:
            WebDriverWait(self.driver,120).until(lambda x:self.driver.find_element_by_id("username"))
        except:
            data_basic = data.data_basic()
            PublicControl.wlan_enable(self,data_basic['lan_pc'])
            PublicControl.dhcp_release_wlan(self,data_basic['wlan_pc'])
            time.sleep(60)
            #self.driver.close()
            self.driver.refresh()
            self.driver.implicitly_wait(20)
        finally:
            username_element = self.driver.find_element_by_id("username")
            WebDriverWait(self.driver,120).until(lambda x:username_element)
            username_element.clear()
            username_element.send_keys(self.username)

    #获取用户名
    def get_username(self):
        try:
            username = self.driver.find_element_by_id("username").text
            return username
        except Exception as e:
            raise Exception("Login page get 'username' element is error! The reason is %s"%e)

    #输入密码
    def set_pwd(self):
        try:
            pwd_element = self.driver.find_element_by_id("password")
            pwd_element.clear()
            pwd_element.send_keys(self.pwd)
            self.driver.implicitly_wait(10)
        except:
            pwd_element = self.driver.find_element_by_css_selector(".password")
            pwd_element.send_keys(self.pwd)
            self.driver.implicitly_wait(10)

    #获取密码
    def get_pwd(self):
        try:
            pwd = self.driver.find_element_by_id("password").text
            return pwd
        except:
            pwd = self.driver.find_element_by_css_selector(".password").text
            return pwd

    #点击登录
    def submit(self):
        try:
            submit_element = self.driver.find_element_by_id("loginbtn")
            submit_element.click()
            self.driver.implicitly_wait(20)
            time.sleep(5)
        except Exception as e:
            raise Exception("Login page has not found 'submit' element! The reason is %s"%e)





    #点击登录页面的语言按钮
    #点击页面上的语言按钮
    def login_language_menu(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='lang_div']/div/div/div")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'login_language_menu' element! The reason is %s"%e)

    #选择页面上的语言
    def login_language_choose(self,lang):
        try:
            if lang == "English":
                n = 1
            elif lang == u"简体中文":
                n = 2
            element = self.driver.find_element_by_xpath(".//*[@id='lang_div']/div/ul/li[%d]/a"%n)
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'login_language_choose' element! The reason is %s"%e)

    #检查页面中是否有语言按钮
    #输出：True：有搜索按钮;False：无搜索按钮
    def check_login_language_buttton(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='lang_div']/div/div/div")
            return True
        except:
            return False

    #获取所选择的语言
    def login_get_language(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='lang_div']/div/div/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'login_get_language' element! The reason is %s"%e)

    #语言下拉框是否显示
    #输出：有则返回True，没有则返回False
    def login_display_language(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='lang_div']/div/ul/li[2]/a")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'login_display_language' element! The reason is %s"%e)






    ######################################################
    #第一次登录页面需要设置管理员和用户密码
    ######################################################
    #输入管理员密码
    def set_super_pwd1(self,super_pwd1):
        try:
            pwd_element = self.driver.find_element_by_id("change_new_pass")
            pwd_element.clear()
            pwd_element.send_keys(super_pwd1)
        except Exception as e:
            raise Exception("Login page set 'super_pwd1' element is error! The reason is %s"%e)

    #确定输入管理员密码
    def set_super_pwd2(self,super_pwd2):
        try:
            pwd_element = self.driver.find_element_by_id("change_new_pass_confirm")
            pwd_element.clear()
            pwd_element.send_keys(super_pwd2)
        except Exception as e:
            raise Exception("Login page set 'super_pwd2' element is error! The reason is %s"%e)

    #输入用户密码
    def set_user_pwd1(self,user_pwd1):
        try:
            pwd_element = self.driver.find_element_by_id("change_new_user_pass")
            pwd_element.clear()
            pwd_element.send_keys(user_pwd1)
        except Exception as e:
            raise Exception("Login page set 'user_pwd1' element is error! The reason is %s"%e)

    #确定用户密码
    def set_user_pwd2(self,user_pwd2):
        try:
            pwd_element = self.driver.find_element_by_id("change_new_user_pass_confirm")
            pwd_element.clear()
            pwd_element.send_keys(user_pwd2)
        except Exception as e:
            raise Exception("Login page set 'user_pwd2' element is error! The reason is %s"%e)

    #点击保存
    def save(self):
        try:
            submit_element = self.driver.find_element_by_id("change_pass_btn")
            submit_element.click()
            self.driver.implicitly_wait(20)
            time.sleep(30)
            #以下检查设备服务状态的窗口是否显示，显示就循环等待5s继续检查，不显示就跳出,持续10分钟
            service_status_element = self.driver.find_element_by_id("service_status_span")
            WebDriverWait(self.driver,720,5).until_not(lambda x:service_status_element.is_displayed())
            time.sleep(10)
        except Exception as e:
            raise Exception("Login page has not found 'save' element! The reason is %s"%e)

