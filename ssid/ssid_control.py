#coding=utf-8
#作者：曾祥卫
#时间：2018.01.22
#描述：GWN76xxssid的控制层

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

class SSIDControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)


    #点击ssid
    def SSID_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"SSIDs","SSIDs")

    #点击添加
    def add_button(self):
        try:
            element = self.driver.find_element_by_id("newssid")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'add_button' element! The reason is %s"%e)

    #只有一个ssid时，点击删除
    def del_add_ssid(self):
        try:
            element = self.driver.find_element_by_id("del_ssid0")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_add_ssid' element! The reason is %s"%e)

    #检测页面上是否有第一个ssid,有则返回True，没有则返回False
    def check_first_exist(self):
        try:
            self.driver.find_element_by_id("del_ssid0")
            return True
        except:
            return False

    #依次点击所有ssid的删除按钮
    def del_all_button(self):
        try:
            time.sleep(3)
            elements = self.driver.find_elements_by_class_name("delbutton")
            for i in range(len(elements)-1):
                time.sleep(5)
                elements1 = self.driver.find_elements_by_class_name("delbutton")
                elements1[1].click()
                PublicControl.notice_ok(self)
            self.driver.implicitly_wait(20)
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_del_ssid_button_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'del_all_button' element! The reason is %s"%e)

#依次点击所有ssid的删除按钮
    def del_all_button_backup(self,n):
        for i in range (1,n):
            try:
                element = self.driver.find_element_by_id("del_ssid%s"%i)
                element.click()
                PublicControl.notice_ok(self)
            except:
                print "webpage has not found 'title' or 'notice_ok' attribute"
                self.driver.implicitly_wait(20)


    #获取第一个ssid的开启状态
    def get_first_status(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[2]/div")
            icon = element.get_attribute("class")
            print icon
            return icon
        except Exception as e:
            raise Exception("webpage has not found 'get_first_status' element! The reason is %s"%e)

    #点击编辑第一个ssid
    def click_first_edit(self):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_id("edit_ssid0")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_first_edit' element! The reason is %s"%e)

    #有多个ssid时，选择特定的一个，点击编辑
    #输入：n:第几个网络组
    def edit_n_button(self,n):
        try:
            time.sleep(3)
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'edit_n_button' element! The reason is %s"%e)

    #多个ssid,点击编辑第n个ssid
    def edit_n_Bt(self,n):
        try:
            n = n-1
            id ='edit_ssid%s'%str(n)
            print(id)
            time.sleep(3)
            elements = self.driver.find_element_by_id(id)
            elements.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'edit_n_button' element! The reason is %s"%e)

    #获取第一个ssid的名字
    def get_first_ssid_name(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[1]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_first_ssid_name' element! The reason is %s"%e)

    #获取第一个ssid的MAC过滤状态
    def get_first_macfilter(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[6]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_first_macfilter' element! The reason is %s"%e)

    #获取第一个ssid的强制网络门户状态
    def get_first_portal(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='ssid_table']/div[2]/div[7]/div")
            icon = element.get_attribute("class")
            print icon
            return icon
        except Exception as e:
            raise Exception("webpage has not found 'get_first_portal' element! The reason is %s"%e)

    #获取第一个ssid的rssi状态
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
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id1"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id2
    def wifi_pagedown2(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id2"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id3
    def wifi_pagedown3(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id3"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id4
    def wifi_pagedown4(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id4"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id5
    def wifi_pagedown5(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id5"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id6
    def wifi_pagedown6(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id6"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id7
    def wifi_pagedown7(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id7"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id7
    def wifi_pagedown8(self):
        self.driver.find_element_by_id(data_ng["ssid_wifi_pagedown_id8"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)


    #输入：num：需要翻页时用到的第几个id
    def wifi_pagedown(self,num):
        try:
            id = data_ng["ssid_wifi_pagedown_id%s"%num]
            self.driver.find_element_by_id(id).send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'wifi_pagedown' element! The reason is %s"%e)










    #添加窗口中，点击wifi
    def add_ssid_wifi(self):
        try:
            element = self.driver.find_element_by_id("m_wifi")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_ssid_wifi' element! The reason is %s"%e)

    #添加窗口中，点击设备管理
    def add_ssid_device(self):
        try:
            element = self.driver.find_element_by_id("m_deviceManage")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_ssid_device' element! The reason is %s"%e)


    #设置开启ssid
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

    #输入：mode，要设置的频段:2.4G,5G,Dual-Band
    def set_Frequency(self,mode):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("ssid_band")
            if mode == "2.4GHz":
                a.send_keys("2")
            elif mode == "5GHz":
                a.send_keys("5")
            elif mode == "Dual-Band":
                a.send_keys("d")
        except Exception as e:
            raise Exception("webpage has not found 'set_Frequency' element! The reason is %s"%e)


    #点击隐藏SSID
    def hide_ssid(self):
        try:
            element = self.driver.find_element_by_id("ssid_hidden")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'hide_ssid' element! The reason is %s"%e)

    #添加窗口中，wifi，点击VLAN的勾选
    def set_VLAN(self):
        try:
            element = self.driver.find_element_by_id("vlan")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_VLAN' element! The reason is %s"%e)

    #添加窗口中，基本，输入VLAN ID
    def set_VLANID(self,VID):
        try:
            element = self.driver.find_element_by_id("vlanid")
            element.clear()
            element.send_keys(VID)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_VLANID' element! The reason is %s"%e)


    #添加窗口中，wifi,选择wifi的open加密
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
            a.send_keys(Keys.ENTER)
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
            a.send_keys(Keys.ENTER)
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

    #添加窗口中，选择第二个白名单列表
    def set_twomac_whitelist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-white']/label[2]/input")
            a.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_twomac_whitelist' element! The reason is %s"%e)


    #添加窗口中，选择白名单,列表能显示
    def get_whitelist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-white']/label/input")
            result = a.get_attribute('type')
            print result
            if result == 'checkbox':
                return True
            else:
                return False
        except Exception as e:
            raise Exception("webpage has not found 'get_whitelist' element! The reason is %s"%e)


    #添加窗口中，wifi,获取白名单的值
    def get_mac_whitelist(self):
        try:
            self.driver.implicitly_wait(10)
            tmp = self.driver.find_element_by_id("mac_whitelist")
            result = tmp.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_mac_whitelist' element! The reason is %s"%e)


    #添加窗口中，选择第二个黑名单列表
    def set_twomac_blacklist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-black']/label[2]/input")
            a.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_twomac_blacklist' element! The reason is %s"%e)


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


    #添加窗口，wifi，mac白名单提示信息
    def get_white_mac_info(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='maclist-white']/span")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_white_mac_info' element! The reason is %s"%e)

    #添加窗口，wifi，mac黑名单提示信息
    def get_black_mac_info(self):
        try:
            element = self.driver.find_element_by_xpath(".//*[@id='maclist-black']/span")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_black_mac_info' element! The reason is %s"%e)

    #添加窗口中，选择黑名单,列表能显示
    def get_blacklist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-black']/label/input")
            result = a.get_attribute('type')
            print result
            if result == 'checkbox':
                return True
            else:
                return False
        except Exception as e:
            raise Exception("webpage has not found 'get_blacklist' element! The reason is %s"%e)



    #有多个ssid时，删除特定的一个
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
            time.sleep(3)
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
            time.sleep(3)
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


    #设置客户端时间策略
    def set_client_time_policy(self,text):
        try:
            element = self.driver.find_element_by_id('timed_client_policy')
            Select(element).select_by_visible_text(text)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_client_time_policy' element! The reason is %s"%e)

    ###################################################
    #以下是添加窗口中，设备管理页面
    ###################################################
    #添加窗口中，设备管理，可添加设备，只有一个设备时,只添加一个设备
    def add_Available_device_one(self):
        try:
            element = self.driver.find_element_by_css_selector("#avaaps>option")
            element.click()
            #点击向右的按钮
            self.driver.find_element_by_id("right").click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_Available_device_one' element! The reason is %s"%e)

    #添加窗口中，设备管理，可添加设备，添加所有设备
    def add_Available_device_all(self):
        try:
            elements = self.driver.find_elements_by_css_selector("#avaaps>option")
            for element in elements:
                element.click()
                #点击向右的按钮
                self.driver.find_element_by_id("right").click()
                self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_Available_device_all' element! The reason is %s"%e)

    #添加窗口中，设备管理，可添加设备，获取可添加的设备的名称
    def get_Available_Devices_name(self):
        try:
            result = []
            elements = self.driver.find_elements_by_css_selector("#avaaps>option")
            for element in elements:
                result.append(element.text)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_Available_device_name' element! The reason is %s"%e)

    #添加窗口中，设备管理，已添加设备，只有一个设备时,只删除一个设备
    def del_Member_device_one(self):
        try:
            element = self.driver.find_element_by_css_selector("#ap>option")
            element.click()
            #点击向左的按钮
            self.driver.find_element_by_id("left").click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'del_Member_device_one' element! The reason is %s"%e)

    #添加窗口中，设备管理，已添加设备，删除所有设备
    def del_Member_device_all(self):
        try:
            elements = self.driver.find_elements_by_css_selector("#ap>option")
            for element in elements:
                element.click()
                #点击向左的按钮
                self.driver.find_element_by_id("left").click()
                self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'del_Member_device_all' element! The reason is %s"%e)

    #添加窗口中，设备管理，已添加设备，获取已添加的设备的名称
    def get_Member_Devices_name(self):
        try:
            result = []
            elements = self.driver.find_elements_by_css_selector("#ap>option")
            for element in elements:
                result.append(element.text)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_Member_Devices_name' element! The reason is %s"%e)

    #################以下是客户端数量限制的元素##################
    ########################作者:蒋甜########################
    #####################2018年3月12日######################

    #ssid配置页面的无线客户端数量限制框
    def set_wifi_client_limit(self,number):
        try:
            element = self.driver.find_element_by_id("wifi_client_limit")
            element.clear()
            element.send_keys(number)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_wifi_client_limit' element! The reason is %s"%e)

    def wifi_client_limit_tips(self):
        try:
            time.sleep(3)
            element = self.driver.find_element_by_xpath(".//*[@id='wifidiv']/div[7]/div[2]/div")
            self.driver.implicitly_wait(20)
            if element.is_displayed() == True:
                return True
            else:
                return False
        except Exception as e:
            raise Exception("webpage has not found 'wifi_client_limit_tips' element! The reason is %s"%e)

    #ssid配置设备管理，有多个ap时，添加特定的设备
    def add_special_device(self,mac):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(5)
            MAC = mac.upper()
            print MAC
            i = 1
            while i<10:
                self.driver.implicitly_wait(10)
                print "-----------1.start choosing ap-----------"
                xpath = ".//*[@id='avaaps']/option[%s]"%i
                element = self.driver.find_element_by_xpath(xpath)
                WebDriverWait(self.driver,120).until(lambda x:element)
                time.sleep(3)
                print "-----------2.find ap mac-----------"
                print element.text
                print i
                if MAC in element.text:
                    element.click()
                    right = self.driver.find_element_by_id('right')
                    right.click()
                    return True
                else:
                    i+=1
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'add_special_ap_to_ssid' element! The reason is %s"%e)


    #检查界面上是否有第n个ssid
    #作者:蒋甜
    def check_have_n_ssid(self,n):
        try:
            n-=1
            self.driver.implicitly_wait(60)
            ssid = "edit_ssid%s"%n
            self.driver.find_element_by_id(ssid)
            return True
        except Exception as e:
            return False

    #检查界面上新建ssid时是否有关于mesh的错误提示
    def new_ssid_tips(self):
        time.sleep(3)
        element = self.driver.find_elements_by_css_selector(".modal-header.dialogtitle.modal-title")[1]
        self.driver.implicitly_wait(20)
        if element.is_displayed()== True:
            PublicControl.notice_ok(self)
            return True
        else:
            print "webpage has not found mesh ssid error tips"
            return False

     #检查界面上新建ssid时是否有关于mesh的错误提示
    def new_ssid_tips_mesh(self):
        time.sleep(3)
        element = self.driver.find_element_by_id("notice_mesh")
        self.driver.implicitly_wait(20)
        if element.is_displayed()== True:
            return True
        else:
            print "webpage has not found mesh ssid error tips"
            return False


    def ssid_cancel(self):
        time.sleep(2)
        element = self.driver.find_element_by_id("m_cancel")
        element.click()
