#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：GWN76xx网络组的控制层

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

class NGControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击网络组
    def NG_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"网络组","Network Group")
        #PublicControl.menu_css(self,".zone-zone.menuselected>a")


    #点击添加
    def add_button(self):
        try:
            element = self.driver.find_element_by_id("newzone")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'add_button' element! The reason is %s"%e)

    #只有一个默认网络组时，点击编辑
    def edit_button(self):
        try:
            element = self.driver.find_element_by_class_name("editbutton")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'edit_button' element! The reason is %s"%e)

    #获取默认网络组的删除的显示状态
    #输出：True：灰色（无法点击）,False:不是灰色（可以点击）
    def get_group0_del_button_status(self):
        try:
            element = self.driver.find_element_by_id("del_zone0")
            self.driver.implicitly_wait(20)
            result = element.get_attribute("disabled")
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_group0_del_button_status' element! The reason is %s"%e)

    #点击默认网络组的删除按钮
    def set_group0_del_button(self):
        try:
            element = self.driver.find_element_by_id("del_zone0")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_group0_del_button' element! The reason is %s"%e)


    #检查界面上是否有配置的对话框窗口
    #输出：有则返回True，没有则返回False
    def check_dialog(self):
        try:
            element = self.driver.find_element_by_css_selector(".dialogtitle")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'dialogtitle' element! The reason is %s"%e)



    #有多个网络组时，选择默认网络组group0时，点击编辑
    def edit_group0_button(self):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[-1].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'edit_group0_button' element! The reason is %s"%e)

    #有多个网络组时，选择特定的网络组，点击编辑
    #输入：n:第几个网络组
    def edit_groupn_button(self,n):
        try:
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'edit_groupn_button' element! The reason is %s"%e)

    #获取所有的网络组名和SSID名
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

    #获取所有enableicon的个数
    def get_enableicon(self):
        try:
            self.driver.implicitly_wait(20)
            elements = self.driver.find_elements_by_css_selector(".enableicon")
            result = len(elements)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_enableicon' element! The reason is %s"%e)

    #获取所有disableicon的个数
    def get_disableicon(self):
        try:
            self.driver.implicitly_wait(20)
            elements = self.driver.find_elements_by_css_selector(".disableicon")
            result = len(elements)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_disableicon' element! The reason is %s"%e)


    #只添加了一个网络组时，点击删除这个网络组的删除按钮
    def del_first_button(self):
        try:
            element = self.driver.find_element_by_id("del_zone1")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'del_first_button' element! The reason is %s"%e)


    #依次点击所有组的删除按钮
    def del_all_button(self):
        try:
            # #取删除键所有的元素
            # elements = self.driver.find_elements_by_class_name("delbutton")
            # i = 0
            # #当i小于所有元素的个数时进行循环
            # while(i<len(tmp)):
            #     #再次取当前页面的删除键的所有元素
            #     inputs = self.driver.find_elements_by_class_name("delbutton")
            #     #点击最后一个删除按钮
            #     inputs[-1].click()
            #     i +=1
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
            raise Exception("webpage has not found 'del_all_button' element! The reason is %s"%e)


    ###########################################################
    #以下是添加窗口中的操作
    ###########################################################

    #添加窗口中，点击基本
    def add_NG_basic(self):
        try:
            element = self.driver.find_element_by_id("m_basic")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_basic' element! The reason is %s"%e)

    #添加窗口中，点击wifi
    def add_NG_wifi(self):
        try:
            element = self.driver.find_element_by_id("m_wifi")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi' element! The reason is %s"%e)

    #添加窗口中，点击设备管理
    def add_NG_device(self):
        try:
            element = self.driver.find_element_by_id("m_deviceManage")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_device' element! The reason is %s"%e)

    #添加窗口中，点击保存
    def add_NG_save(self):
        try:
            element = self.driver.find_element_by_id("m_save")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_save' element! The reason is %s"%e)

    #添加窗口中，点击取消
    def add_NG_cancel(self):
        try:
            element = self.driver.find_element_by_id("m_cancel")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_cancel' element! The reason is %s"%e)

    #添加窗口中，点击关闭
    def add_NG_close(self):
        try:
            element = self.driver.find_element_by_id("closeedit")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_close' element! The reason is %s"%e)


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



    ###################################################
    #以下是添加窗口中，基本页面
    ###################################################
    #添加窗口中，基本，输入网络组名称
    def add_NG_basic_name(self,NG_name):
        try:
            element = self.driver.find_element_by_id("name")
            element.send_keys(NG_name)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_basic_name' element! The reason is %s"%e)

    #添加窗口中，基本，获取输入网络组名称
    def get_add_NG_basic_name(self):
        try:
            self.driver.implicitly_wait(5)
            element = self.driver.find_element_by_id("name")
            #print element.get_attribute("value")
            return element.get_attribute("value")
        except Exception as e:
            raise Exception("webpage has not found 'get_add_NG_basic_name' element! The reason is %s"%e)


    #添加窗口中，基本，勾选开启
    def add_NG_basic_enable(self):
        try:
            element = self.driver.find_element_by_id("enable")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_basic_enable' element! The reason is %s"%e)

    #添加窗口中，基本，流量转发选择wan0
    def add_NG_basic_wan0(self):
        try:
            element = self.driver.find_element_by_id("wan0")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_basic_enable' element! The reason is %s"%e)


    #添加窗口中，基本，获取VLAN的勾选情况
    #输出：True:被选中,None:没选中
    def get_NG_basic_VLAN(self):
        try:
            self.driver.implicitly_wait(5)
            element = self.driver.find_element_by_id("vlan")
            return element.get_attribute("checked")
        except Exception as e:
            raise Exception("webpage has not found 'get_NG_basic_VLAN' element! The reason is %s"%e)

    #添加窗口中，基本，点击VLAN的勾选
    def set_NG_basic_VLAN(self):
        try:
            element = self.driver.find_element_by_id("vlan")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_NG_basic_VLAN' element! The reason is %s"%e)

    #添加窗口中，基本，获取VLAN ID
    def get_NG_basic_VLANID(self):
        try:
            self.driver.implicitly_wait(5)
            element = self.driver.find_element_by_id("vlanid")
            #print element.get_attribute("value")
            return element.get_attribute("value")
        except Exception as e:
            raise Exception("webpage has not found 'get_NG_basic_VLANID' element! The reason is %s"%e)

    #添加窗口中，基本，输入VLAN ID
    def set_NG_basic_VLANID(self,VID):
        try:
            element = self.driver.find_element_by_id("vlanid")
            element.clear()
            element.send_keys(VID)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_NG_basic_VLANID' element! The reason is %s"%e)

    #添加窗口中，基本，输入dhcp网关
    def set_NG_basic_dhcp_gateway(self,gateway):
        try:
            self.driver.find_element_by_id("dhcpv4_lease_time").send_keys(Keys.PAGE_DOWN)
            element = self.driver.find_element_by_id("ipv4_route")
            element.clear()
            element.send_keys(gateway)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_NG_basic_dhcp_gateway' element! The reason is %s"%e)


    ###################################################
    #以下是添加窗口中，wifi页面
    ###################################################
    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id1
    def wifi_pagedown1(self):
        time.sleep(2)
        self.driver.find_element_by_id(data_ng["wifi_pagedown_id1"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id2
    def wifi_pagedown2(self):
        time.sleep(2)
        self.driver.find_element_by_id(data_ng["wifi_pagedown_id2"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-wifi页面-id2
    def wifi_pagedown3(self):
        time.sleep(2)
        self.driver.find_element_by_id(data_ng["wifi_pagedown_id3"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #添加窗口中，wifi，点击开启wifi
    def add_NG_wifi_enable(self):
        try:
            element = self.driver.find_element_by_id("wireless")
            element.click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_enable' element! The reason is %s"%e)

    #添加窗口中，wifi，输入ssid
    def add_NG_wifi_ssid(self,NG_ssid):
        try:
            element = self.driver.find_element_by_id("ssid")
            element.clear()
            element.send_keys(NG_ssid)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_ssid' element! The reason is %s"%e)

    #添加窗口中，wifi,选择wifi的安全模式
    def add_NG_wifi_None(self):
        try:
            a = self.driver.find_element_by_id("encryption")
            a.send_keys("o")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_None' element! The reason is %s"%e)

    #添加窗口中，wifi,选择哪个加密方式
    def add_NG_wifi_n_encryption(self,n):
        try:
            a = self.driver.find_element_by_id("encryption")
            for i in range(n):
                a.send_keys("w")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_n_encryption' element! The reason is %s"%e)

    #添加窗口中，wifi，输入wep密码
    def add_NG_wifi_wep_key(self,NG_key):
        try:
            element = self.driver.find_element_by_id("wep_key")
            element.clear()
            element.send_keys(NG_key)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_wep_key' element! The reason is %s"%e)

    #添加窗口中，wifi，输入wpa密码
    def add_NG_wifi_wpa_key(self,NG_key):
        try:
            element = self.driver.find_element_by_id("wpa_key")
            element.clear()
            element.send_keys(NG_key)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_wpa_key' element! The reason is %s"%e)

    #添加窗口中，wifi,选择WPA密钥模式
    def add_NG_wifi_wpa_mode(self,mode):
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
            raise Exception("webpage has not found 'add_NG_wifi_wpa_mode' element! The reason is %s"%e)

    #添加窗口中，wifi,选择WPA类型
    def add_NG_wifi_wpa_type(self,m):
        try:
            a = self.driver.find_element_by_id("wpa_encryption")
            for i in range(m):
                a.send_keys("a")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_wifi_wpa_type' element! The reason is %s"%e)

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



    #点击隐藏ssid
    def set_hidden_ssid(self):
        try:
            element = self.driver.find_element_by_id("ssid_hidden")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_hidden_ssid' element! The reason is %s"%e)

    #添加窗口中，wifi,选择使用mac地址过滤
    def set_mac_filter(self,mode):
        try:
            NGControl.wifi_pagedown3(self)
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

    #添加窗口中，选择第一个黑名单列表
    def set_onemac_blacklist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-black']/label/input")
            a.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_onemac_blacklist' element! The reason is %s"%e)

    #添加窗口中，选择第二个黑名单列表
    def set_twomac_blacklist(self):
        try:
            a = self.driver.find_element_by_xpath(".//*[@id='maclist-black']/label[2]/input")
            a.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_twomac_blacklist' element! The reason is %s"%e)


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


    #添加窗口，wifi，添加mac白名单地址输入框,并输入随机mac地址
    def set_white_addmac(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//button")
            elements[-1].click()
            elements[-1].send_keys(Keys.TAB)
            elements1 = self.driver.find_elements_by_xpath(".//*[@id='whitelistcontent']//input")
            elements1[-1].clear()
            #取随机mac地址
            random_mac = PublicControl.randomMAC(self)
            elements1[-1].send_keys(random_mac)
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
            elements = self.driver.find_elements_by_xpath(".//*[@id='blacklistcontent']//button")
            elements[-1].click()
            elements[-1].send_keys(Keys.TAB)
            elements1 = self.driver.find_elements_by_xpath(".//*[@id='blacklistcontent']//input")
            elements1[-1].clear()
            #取随机mac地址
            random_mac = PublicControl.randomMAC(self)
            elements1[-1].send_keys(random_mac)
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
            element = self.driver.find_element_by_id("rssi_enable")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_rssi' element! The reason is %s"%e)

    #获取RSSI是否被选中
    def get_rssi_status(self):
        try:
            element = self.driver.find_element_by_id("rssi_enable")
            result = element.get_attribute("checked")
            self.driver.implicitly_wait(20)
            print "The result of RSSI whether been checked is %s"%result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_rssi_status' element! The reason is %s"%e)

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
            self.driver.find_element_by_id("rssi_enable").send_keys(Keys.TAB)
            element = self.driver.find_element_by_id("rssi")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_min_rssi' element! The reason is %s"%e)

    #设置客户端时间策略
    def set_client_time_policy(self,text):
        try:
            element = self.driver.find_element_by_id('timed_client_policy')
            Select(element).select_by_visible_text(text)
            self.driver.implicitly_wait(60)
        except Exception as e:
            raise Exception("webpage has not found 'set_client_time_policy' element! The reason is %s"%e)

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








    #####################################################################
    #######以下是GWN7000的页面控制弹出的编辑窗口
    #####################################################################
    #设置dhcp选项的值
    def set_7000_dhcp_option(self,value):
        try:
            element = self.driver.find_element_by_id("dhcp_option")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_7000_dhcp_option' element! The reason is %s"%e)

    #点击开启ipv4
    def set_7000_ipv4(self):
        try:
            element = self.driver.find_element_by_id("ipv4")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'set_7000_ipv4' element! The reason is %s"%e)

    #点击开启ipv4 DHCP
    def set_7000_ipv4_dhcp(self):
        try:
            element = self.driver.find_element_by_id("ipv4_dhcp_enable")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'set_7000_ipv4_dhcp' element! The reason is %s"%e)

    #设置dhcp server的租期时间
    def set_7000_ipv4_dhcp_lease_time(self,value):
        try:
            element = self.driver.find_element_by_id("dhcpv4_lease_time")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_7000_ipv4_dhcp_lease_time' element! The reason is %s"%e)

    ##################以下是AP DHCP server的方法##################
    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-基本页面-id1
    def basic_pagedown1(self):
        time.sleep(2)
        self.driver.find_element_by_id(data_ng["basic_pagedown_id1"]).send_keys(Keys.PAGE_DOWN)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-基本页面-id2
    def basic_pagedown2(self):
        time.sleep(2)
        self.driver.find_element_by_id(data_ng["basic_pagedown_id2"]).send_keys(Keys.PAGE_DOWN)
        self.driver.implicitly_wait(10)

    #网络组页面中需要翻页操作时需要找到最底下的元素属性:网络组-编辑-基本页面-id3
    def basic_pagedown3(self):
        time.sleep(2)
        self.driver.find_element_by_id(data_ng["basic_pagedown_id3"]).send_keys(Keys.TAB)
        self.driver.implicitly_wait(10)

    #点击开启ipv4
    def s_ipv4(self):
        try:
            element = self.driver.find_element_by_id("ipv4")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_ipv4' element! The reason is %s"%e)

    #设置IPv4静态地址
    def s_ipv4_static(self,value):
        try:
            element = self.driver.find_element_by_id("ipv4_static")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 's_ipv4_static' element! The reason is %s"%e)


    #检查ipv4 DHCP server是否勾选
    #输出：选中：True;没选中:None
    def check_ipv4_dhcp(self):
        try:
            element = self.driver.find_element_by_id("ipv4_dhcp_enable")
            result = element.get_attribute('checked')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_7000_ipv4_dhcp' element! The reason is %s"%e)

    #设置dhcp网关
    def s_dhcp_gateway(self,value):
        try:
            element = self.driver.find_element_by_id("ipv4_route")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 's_dhcp_gateway' element! The reason is %s"%e)

    #获取dhcp网关
    def g_dhcp_gateway(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("ipv4_route")
            result = element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_dhcp_gateway' element! The reason is %s"%e)


    #DHCP开始地址
    def s_ipv4_dhcp_start(self,value):
        try:
            element = self.driver.find_element_by_id("ipv4_dhcp_start")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 's_ipv4_dhcp_start' element! The reason is %s"%e)

    #获取DHCP开始地址
    def g_ipv4_dhcp_start(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("ipv4_dhcp_start")
            result = element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_ipv4_dhcp_start' element! The reason is %s"%e)


    #DHCP结束地址
    def s_ipv4_dhcp_end(self,value):
        try:
            element = self.driver.find_element_by_id("ipv4_dhcp_end")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 's_ipv4_dhcp_end' element! The reason is %s"%e)

    #获取DHCP结束地址
    def g_ipv4_dhcp_end(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("ipv4_dhcp_end")
            result = element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_ipv4_dhcp_end' element! The reason is %s"%e)


    #设置首选dns
    def s_dhcp_dns1(self,value):
        try:
            element = self.driver.find_element_by_id("preferred_dns")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 's_dhcp_dns1' element! The reason is %s"%e)

    #设置次选dns
    def s_dhcp_dns2(self,value):
        try:
            element = self.driver.find_element_by_id("alternate_dns")
            element.clear()
            element.send_keys(value)
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 's_dhcp_dns2' element! The reason is %s"%e)

    #获取首选dns
    def g_dhcp_dns1(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("preferred_dns")
            result = element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_dhcp_dns1' element! The reason is %s"%e)

    #获取次选dns
    def g_dhcp_dns2(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("alternate_dns")
            result = element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_dhcp_dns2' element! The reason is %s"%e)

