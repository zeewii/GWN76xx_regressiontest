#coding=utf-8
#作者：曾祥卫
#时间：2017.07.27
#描述：GWN76xx强制门户认证的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

class CPControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击页面上强制网络门户
    def CP_menu(self):
        PublicControl.menu_css(self,u"强制网络门户",'Captive Portal')

    #点击强制网络门户页面上的策略菜单
    def nds_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream_nds")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'nds_menu' element! The reason is %s"%e)

    #点击强制网络门户页面上的文件菜单
    def file_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___file")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'file_menu' element! The reason is %s"%e)

    #点击强制网络门户页面上的客户端菜单
    def client_menu(self):
        try:
            element = self.driver.find_element_by_id("sectiontab_grandstream___client")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'client_menu' element! The reason is %s"%e)



    #################################################
    #以下是策略的页面操作
    #################################################
    #点击编辑按钮
    #输入：n,点击第几个列表进行编辑
    def click_edit_button(self,n):
        try:
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_edit_button' element! The reason is %s"%e)

    #点击添加按钮
    def click_add(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("newcaptiveportal")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_add' element! The reason is %s"%e)

    #点击删除按钮
    def del_button(self,n):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("del_portal_policy_%s"%(n-1))
            element.click()
        except Exception as e:
            raise Exception("webpage has not found 'del_all_button' element! The reason is %s"%e)


    #################################################
    #以下是编辑或添加的页面操作
    #################################################
    #输入list名称
    def set_policy_name(self,name):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("policyName")
            element.clear()
            element.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_policy_name' element! The reason is %s"%e)

    #输入有效期
    #输入：n,第几个列表进行编辑或添加
    def set_expiration(self,n,t):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("field_grandstream_portal_policy_%s_portal_policy_%s_expiration"%((n-1),(n-1)))
            element.clear()
            element.send_keys(t)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_Expiration' element! The reason is %s"%e)

    #选择认证方式
    #输入：type:0-免认证，1-Radius服务，10-社交登录认证，12-凭据，13-简单密码认证
    def set_auth_type(self,mode):
        try:
            element = self.driver.find_element_by_id("auth_type")
            Select(element).select_by_value(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_auth_type' element! The reason is %s"%e)

    #选择认证方式--radius改回免认证
    def set_radius_to_No_auth(self):
        try:
            element = self.driver.find_element_by_id("auth_type")
            element.send_keys(Keys.UP)
            element.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_to_No_auth' element! The reason is %s"%e)


    #输入radius服务器地址
    #输入：n,第几个列表进行编辑或添加
    def set_radius_server_address(self,n,addr):
        try:
            element = self.driver.find_element_by_id("field_grandstream_portal_policy_%s_portal_policy_%s_radius_server"%((n-1),(n-1)))
            element.clear()
            element.send_keys(addr)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_server_address' element! The reason is %s"%e)

    #输入radius服务器的端口
    def set_radius_server_port(self,port):
        try:
            element = self.driver.find_element_by_id("radius_port")
            element.clear()
            element.send_keys(port)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_server_port' element! The reason is %s"%e)

    #输入radius服务器密钥
    #输入：n,第几个列表进行编辑或添加
    def set_radius_server_secret(self,n,key):
        try:
            element = self.driver.find_element_by_id("field_grandstream_portal_policy_%s_portal_policy_%s_radius_secret"%((n-1),(n-1)))
            element.clear()
            element.send_keys(key)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_server_secret' element! The reason is %s"%e)

    #选择radius认证方式
    #输入：mode：PAP，CHAP，MS-CHAP
    def set_radius_auth_method(self,mode):
        try:
            element = self.driver.find_element_by_id("radius_method")
            Select(element).select_by_visible_text(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_auth_method' element! The reason is %s"%e)

    #点击使用默认门户页面
    def click_default_page(self):
        try:
            element = self.driver.find_element_by_id("enable_default_page")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_default_page' element! The reason is %s"%e)

    #选择门户页面定制
    #输入：page:/password_auth.html,/portal_default.html,
    # /portal_pass.html,/social_auth.html,/twitter.html,
    # /twitter_website.html,/vouchers_auth.html,/wechat.html
    def set_portal_page(self,page):
        try:
            element = self.driver.find_element_by_id("portal_page_path")
            Select(element).select_by_visible_text(page)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_portal_page' element! The reason is %s"%e)

    #编辑或添加的页面点击保存
    def click_add_save(self):
        try:
            element = self.driver.find_element_by_id("m_savefolder")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'click_add_save' element! The reason is %s"%e)

    #获取页面所有标题
    def get_titlediv(self):
        try:
            result = []
            elements = self.driver.find_elements_by_css_selector(".titlediv")
            self.driver.implicitly_wait(20)
            for element in elements:
                result.append(element.text)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_titlediv' element! The reason is %s"%e)

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

    #################################################
    #以下是客户端的页面操作
    #################################################
    #获取客户端的数量--最多检查5个
    def get_clients_number(self):
        number = 0
        for i in range(2,7):
            try:
                self.driver.find_element_by_xpath(".//*[@id='clientslist']/fieldset/div/div[%s]/div[1]/div"%i)
                number = number + 1
            except:
                number = number + 0
        print number
        return number

    #获取客户端的mac地址
    #输入：n，第几个客户端
    def get_client_mac(self,n):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[2]/div"%(n+1))
            MAC = element.text
            mac = MAC.lower()
            print mac
            return mac
        except Exception as e:
            raise Exception("webpage has not found 'get_client_mac' element! The reason is %s"%e)

    #获取客户端的ip地址
    #输入：n，第几个客户端
    def get_client_ip(self,n):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[3]/div"%(n+1))
            ip = element.text
            print ip
            return ip
        except Exception as e:
            raise Exception("webpage has not found 'get_client_ip' element! The reason is %s"%e)

    #获取客户端的认证状态
    #输入：n，第几个客户端
    def get_client_auth_status(self,n):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='clients_table']/div[%s]/div[8]/div"%(n+1))
            status = element.text
            print status
            return status
        except Exception as e:
            raise Exception("webpage has not found 'get_client_auth_status' element! The reason is %s"%e)









    #################################################
    #以下是免认证的portal的页面操作
    #################################################
    #点击同意协议
    def click_agree(self):
        try:
            element = self.driver.find_element_by_id("agree")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_agree' element! The reason is %s"%e)

    #点击connect to WiFi按钮
    def click_connect_WiFi(self):
        try:
            element = self.driver.find_element_by_id("twitter-submit")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'click_connect_WiFi' element! The reason is %s"%e)

    #################################################
    #以下是radius认证的portal的页面操作
    #################################################
    #输入用户名
    def set_radius_name(self,radius_name):
        try:
            element = self.driver.find_element_by_id("twitter-username")
            element.clear()
            element.send_keys(radius_name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_name' element! The reason is %s"%e)

    #输入密码
    def set_radius_password(self,radius_password):
        try:
            element = self.driver.find_element_by_id("twitter-password")
            element.clear()
            element.send_keys(radius_password)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_password' element! The reason is %s"%e)

