#coding=utf-8
#作者：曾祥卫
#时间：2017.03.29
#描述：GWN76xx网络组-额外ssid的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from data import data

data_ng = data.data_networkgroup()

class AddSSIDControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    #点击网络组-额外ssid
    def SSID_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"额外SSID","Additional SSID")


    #点击添加
    def add_button(self):
        try:
            element = self.driver.find_element_by_id("newssid")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'add_button' element! The reason is %s"%e)

    #只有一个额外ssid时，点击删除
    def del_add_ssid(self):
        try:
            element = self.driver.find_element_by_id("del_ssid0")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_add_ssid' element! The reason is %s"%e)

    #检测页面上是否有第一个额外ssid,有则返回True，没有则返回False
    def check_first_exist(self):
        try:
            self.driver.find_element_by_id("del_ssid0")
            return True
        except:
            return False

    #依次点击所有组的删除按钮
    def del_all_button(self):
        try:
            elements = self.driver.find_elements_by_class_name("delbutton")
            for element in elements:
                try:
                    if (u"删除" or "Delete") == element.get_attribute("title"):
                        element.click()
                        PublicControl.notice_ok(self)
                except:
                    print "webpage has not found 'title' or 'notice_ok' attribute"
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_all_button' element! The reason is %s"%e)


    #获取第一个额外ssid的开启状态
    def get_first_status(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[2]/div")
            icon = element.get_attribute("class")
            print icon
            return icon
        except Exception as e:
            raise Exception("webpage has not found 'get_first_status' element! The reason is %s"%e)

    #点击编辑第一个额外ssid
    def click_first_edit(self):
        try:
            element = self.driver.find_element_by_id("edit_ssid0")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_first_edit' element! The reason is %s"%e)

    #获取第一个额外ssid的名字
    def get_first_ssid_name(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[1]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_first_ssid_name' element! The reason is %s"%e)

    #获取第一个额外ssid的隐藏状态
    def get_first_hide(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[4]/div")
            icon = element.get_attribute("class")
            print icon
            return icon
        except Exception as e:
            raise Exception("webpage has not found 'get_first_status' element! The reason is %s"%e)

    #获取第一个额外ssid的MAC过滤状态
    def get_first_macfilter(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[6]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_first_macfilter' element! The reason is %s"%e)

    #获取第一个额外ssid的客户端隔离状态
    def get_first_isolation(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[7]/div")
            icon = element.get_attribute("class")
            print icon
            return icon
        except Exception as e:
            raise Exception("webpage has not found 'get_first_isolation' element! The reason is %s"%e)

    #获取第一个额外ssid的rssi状态
    def get_first_rssi(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[8]/div")
            icon = element.get_attribute("class")
            print icon
            return icon
        except Exception as e:
            raise Exception("webpage has not found 'get_first_rssi' element! The reason is %s"%e)

    #获取第一个额外rssi的值
    def get_first_rssi_value(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[8]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_first_rssi_value' element! The reason is %s"%e)



    ###########################################################
    #以下是添加窗口中的操作
    ###########################################################
    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id1
    def wifi_pagedown1(self):
        self.driver.find_element_by_id(data_ng["addssid_wifi_pagedown_id1"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id2
    def wifi_pagedown2(self):
        self.driver.find_element_by_id(data_ng["addssid_wifi_pagedown_id2"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id3
    def wifi_pagedown3(self):
        self.driver.find_element_by_id(data_ng["addssid_wifi_pagedown_id3"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #设置开启额外ssid
    def set_enable_disable(self):
        try:
            element = self.driver.find_element_by_id("enable")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_enable_disable' element! The reason is %s"%e)

    #设置ssid
    def set_ssid(self,ssid):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("ssid")
            element.clear()
            element.send_keys(ssid)
        except Exception as e:
            raise Exception("webpage has not found 'set_ssid' element! The reason is %s"%e)


    #设置wpa的密码
    def set_wpa_key(self,key):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("wpa_key")
            element.clear()
            element.send_keys(key)
        except Exception as e:
            raise Exception("webpage has not found 'set_wpa_key' element! The reason is %s"%e)

    #点击隐藏SSID
    def hide_ssid(self):
        try:
            element = self.driver.find_element_by_id("ssid_hidden")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'hide_ssid' element! The reason is %s"%e)


    #添加窗口中，wifi,选择wifi的安全模式
    def wifi_None(self):
        try:
            a = self.driver.find_element_by_id("encryption")
            a.send_keys("o")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_None' element! The reason is %s"%e)

    #添加窗口中，wifi,选择哪个加密方式
    def wifi_n_encryption(self,n):
        try:
            a = self.driver.find_element_by_id("encryption")
            for i in range(n):
                a.send_keys("w")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_n_encryption' element! The reason is %s"%e)


    #添加窗口中，wifi，输入wep密码
    def wifi_wep_key(self,NG_key):
        try:
            element = self.driver.find_element_by_id("wep_key")
            element.clear()
            element.send_keys(NG_key)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_wep_key' element! The reason is %s"%e)

    #添加窗口中，wifi，输入wpa密码
    def wifi_wpa_key(self,NG_key):
        try:
            element = self.driver.find_element_by_id("wpa_key")
            element.clear()
            element.send_keys(NG_key)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_wpa_key' element! The reason is %s"%e)

    #添加窗口中，wifi,选择WPA密钥模式
    def wifi_wpa_mode(self,mode):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("wpa_key_mode")
            if mode == "PSK":
                a.send_keys("p")
            else:
                a.send_keys("8")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_wpa_mode' element! The reason is %s"%e)

    #添加窗口中，wifi,选择WPA类型
    def wifi_wpa_type(self,m):
        try:
            a = self.driver.find_element_by_id("wpa_encryption")
            for i in range(m):
                a.send_keys("a")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_wpa_type' element! The reason is %s"%e)

    #设置radius服务器地址
    def set_radius_server(self,addr):
        try:
            a = self.driver.find_element_by_id("radius_server")
            a.clear()
            a.send_keys(addr)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_server' element! The reason is %s"%e)

    #设置radius服务器密钥
    def set_radius_secret(self,key):
        try:
            a = self.driver.find_element_by_id("radius_secret")
            a.clear()
            a.send_keys(key)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_radius_secret' element! The reason is %s"%e)


    #添加窗口中，wifi,选择使用mac地址过滤
    def set_mac_filter(self,mode):
        try:
            a = self.driver.find_element_by_id("mac_filtering")
            if mode == 'Disable':
                Select(a).select_by_value("0")
            elif mode == 'Whitelist':
                Select(a).select_by_value("1")
            elif mode == 'Blacklist':
                Select(a).select_by_value("2")
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_mac_filter' element! The reason is %s"%e)

    #添加窗口中，wifi,输入白名单
    def set_mac_whitelist(self,mac):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("mac_whitelist")
            a.clear()
            a.send_keys(mac)
        except Exception as e:
            raise Exception("webpage has not found 'set_mac_whitelist' element! The reason is %s"%e)

    #添加窗口中，选择第一个黑名单列表
    def set_onemac_blacklist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-black']/label/input")
            a.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_onemac_blacklist' element! The reason is %s"%e)

    #添加窗口中，选择第一个白名单列表
    def set_onemac_whitelist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-white']/label/input")
            a.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_onemac_whitelist' element! The reason is %s"%e)



    #添加窗口，wifi，添加mac白名单地址输入框,并输入随机mac地址
    def set_white_addmac(self):
        try:
            elements1 = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//input")
            elements1[-1].send_keys(Keys.TAB)
            elements = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//button")
            elements[-1].click()
            #elements[-1].send_keys(Keys.TAB)
            #elements1 = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//input")
            elements2 = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//input")
            elements2[-1].clear()
            #取随机mac地址
            random_mac = PublicControl.randomMAC(self)
            elements2[-1].send_keys(random_mac)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_white_addmac' element! The reason is %s"%e)

    #添加窗口，wifi，删除所有mac白名单地址输入框
    def del_white_addmac(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//button")
            for element in elements[:-1]:
                element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_white_addmac' element! The reason is %s"%e)

    #添加窗口，wifi，添加mac黑名单地址输入框,并输入随机mac地址
    def set_black_addmac(self):
        try:
            elements1 = self.driver.find_elements_by_xpath(".//*[@id='blacklistcontent']//input")
            elements1[-1].send_keys(Keys.TAB)
            elements = self.driver.find_elements_by_xpath(".//*[@id='blacklistcontent']//button")
            elements[-1].click()
            elements2 = self.driver.find_elements_by_xpath(".//*[@id='blacklistcontent']//input")
            elements2[-1].clear()
            #取随机mac地址
            random_mac = PublicControl.randomMAC(self)
            elements2[-1].send_keys(random_mac)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_black_addmac' element! The reason is %s"%e)

    #添加窗口，wifi，删除所有mac黑名单地址输入框
    def del_black_addmac(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='blacklistcontent']//button")
            for element in elements[:-1]:
                element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_black_addmac' element! The reason is %s"%e)


    #有多个额外ssid时，选择特定的一个，点击编辑
    #输入：n:第几个网络组
    def edit_n_button(self,n):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'edit_n_button' element! The reason is %s"%e)

    #有多个额外ssid时，删除特定的一个
    #输入：n:第几个网络组
    def del_n_button(self,n):
        try:
            elements = self.driver.find_elements_by_class_name("delbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_n_button' element! The reason is %s"%e)

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

    #添加窗口中，点击保存
    def save(self):
        try:
            element = self.driver.find_element_by_id("m_save")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'save' element! The reason is %s"%e)

    #添加窗口中，点击关闭
    def close(self):
        try:
            element = self.driver.find_element_by_id("closeedit")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'save' element! The reason is %s"%e)


    #点击客户端隔离
    def click_isolation(self):
        try:
            element = self.driver.find_element_by_id("isolation")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_isolation' element! The reason is %s"%e)

    #选择客户端隔离模式
    def isolation_mode(self,value):
        try:
            element = self.driver.find_element_by_id("isolation_mode")
            Select(element).select_by_value(value)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'isolation_mode' element! The reason is %s"%e)

    #输入网关mac地址----客户端隔离模式
    def gateway_mac(self,mac):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("gateway_mac")
            element.clear()
            element.send_keys(mac)
        except Exception as e:
            raise Exception("webpage has not found 'gateway_mac' element! The reason is %s"%e)

    #点击开启RSSI
    def click_rssi(self):
        try:
            AddSSIDControl.wifi_pagedown1(self)
            element = self.driver.find_element_by_id("rssi_enable")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_rssi' element! The reason is %s"%e)

    #获取最小RSSI值
    def get_min_rssi(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("rssi")
            result = element.get_attribute('value')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_min_rssi' element! The reason is %s"%e)

    #设置最小RSSI值
    def set_min_rssi(self,value):
        try:
            element = self.driver.find_element_by_id("rssi")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_min_rssi' element! The reason is %s"%e)

    #获取默认网络组的组名
    def get_1_network_group_membership(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='zone']/option[1]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_1_network_group_membership' element! The reason is %s"%e)

    #获取是否有第2个，第3个网络组的组名
    def get_2_3_network_group_membership(self):
        try:
            element1 = self.driver.find_element_by_xpath(".//*[@id='zone']/option[2]")
            element2 = self.driver.find_element_by_xpath(".//*[@id='zone']/option[3]")
            result1 = element1.text
            result2 = element2.text
            print result1,result2
            return result1,result2
        except:
            print "webpage has not found network group2 and group3!"
            return False,False

    #有多个网络组时，选择第几个网络组
    def choose_zone(self,n):
        try:
            for i in range(n):
                element = self.driver.find_element_by_id("zone")
                element.send_keys(Keys.DOWN)
                element.send_keys(Keys.TAB)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'choose_zone' element! The reason is %s"%e)

    #点击开启强制门户
    def click_portal(self):
        try:
            element = self.driver.find_element_by_id("portal_enable")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_portal' element! The reason is %s"%e)

     #选择对应的强制门户策略
    def set_portal_policy(self,n):
        try:
            a = self.driver.find_element_by_id('portal_policy')
            for i in range(n):
                a.send_keys(Keys.DOWN)
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_portal_policy' element! The reason is %s"%e)
