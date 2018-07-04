#coding=utf-8
#作者：曾祥卫
#时间：2017.03.14
#描述：GWN76xx设置向导的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
import time

class SWControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击页面上的问号开启设置向导
    def SW_menu(self):
        try:
            element = self.driver.find_element_by_id("helpbtn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'setupwizard' element! The reason is %s"%e)


    #点击下一步
    def nextstep(self):
        try:
            element = self.driver.find_element_by_id("nextstep")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'nextstep' element! The reason is %s"%e)

    ########################################################
    #以下是首页操作
    ########################################################
    #点击下次不再显示
    def hidenexttime(self):
        try:
            element = self.driver.find_element_by_id("hidenexttime")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'hidenexttime' element! The reason is %s"%e)

    #检查登录web界面，判断是否会显示向导页面
    #输出：有则返回True，没有则返回False
    def check_wizard(self):
        try:
            element = self.driver.find_element_by_id("wizarddivcontent")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_wizard' element! The reason is %s"%e)


    #下次不再显示是否被选中
    #输出：true：被选中，None：没被选中
    def get_hidenexttime(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("hidenexttime")
            result = element.get_attribute("checked")
            return result
        except Exception as e:
            raise Exception("webpage has not found 'hidenexttime' element! The reason is %s"%e)

    #获取提示信息
    def get_startcontent(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("startcontent1")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'startcontent' element! The reason is %s"%e)

    ########################################################
    #以下是APs页面操作
    ########################################################

    #点击上一步
    def prevstep(self):
        try:
            element = self.driver.find_element_by_id("prevstep")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'prevstep' element! The reason is %s"%e)

    #点击配对选中的设备
    def pair(self,mac):
        time.sleep(120)
        MAC = mac.upper()
        i = 2
        while i<6:
            try:
                print "i=%s"%i
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='wizardstepdiv']/fieldset/div/div[%s]/div[2]"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng setupwizard pair debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng setupwizard pair debug:2.can find this AP mac-----------"
                    print "choose mac:%s to pair"%element.text
                    element2 = self.driver.find_element_by_xpath(".//*[@id='wizardstepdiv']/fieldset/div/div[%s]/div[6]/div//button"%i)
                    pair_enable = element2.is_enabled()
                    print "-----------rick.zeng setupwizard pair debug:3.this AP pair button is %s-----------"%pair_enable
                    element2.click()
                    self.driver.implicitly_wait(10)
                    print "-----------rick.zeng setupwizard pair debug:4.click pair button successfully-----------"
                    break
                elif ap_mac_text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_setupwizard_pair_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng setupwizard pair debug:5.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                else:
                    print "-----------rick.zeng setupwizard pair debug:6.can't find this AP mac-----------"
            except Exception as e:
                current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                png = "error_setupwizard_pair_%s.png"%str(current_time)
                self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                raise Exception("webpage has not found 'setupwizard pair' element! The reason is %s"%e)
            i = i+1
        time.sleep(10)

    #只有一个slave时，解除配对的设备
    def unpair(self):
        try:

            elements = self.driver.find_elements_by_class_name("unpairbutton")
            for element in elements:
                if element.get_attribute("disabled") == None:
                    element.click()
                    self.driver.implicitly_wait(10)
                    time.sleep(10)
        except Exception as e:
            raise Exception("webpage has not found 'unpair' element! The reason is %s"%e)



    #获取APs页面的值
    def get_APs_text(self):
        try:
            result = []
            #elements = self.driver.find_elements_by_css_selector(".cell.clearfix.content.col-xs-2.col-sm-2.col-md-2.col-lg-2")
            elements = self.driver.find_elements_by_css_selector("div.luci2-grid.luci2-grid-hover > div > div")
            for element in elements:
                result.append(element.text)
            self.driver.implicitly_wait(10)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_APs_text' element! The reason is %s"%e)

    #获取APs页面的状态信息
    def get_APs_status(self):
        try:
            result = []
            #elements = self.driver.find_elements_by_css_selector(".cell.clearfix.content.col-xs-2.col-sm-2.col-md-2.col-lg-2")
            elements = self.driver.find_elements_by_css_selector("div.luci2-grid.luci2-grid-hover > div > div > span")
            for element in elements:
                result.append(element.text)
            self.driver.implicitly_wait(10)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_APs_status' element! The reason is %s"%e)


    #获取APs页面中没有配对的元素的disabled属性
    #输出：true：被选中，None：没被选中
    def get_APs_unpair(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_class_name("unpairbutton")
            for element in elements:
                result1 = element.get_attribute("disabled")
                result.append(result1)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'APs disabled value' element! The reason is %s"%e)



    ########################################################
    #以下是网络组页面操作
    ########################################################
    #获取wifi的状态
    #输出：true：被选中，None：没被选中
    def get_wifi_status(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("enableWifi")
            result = element.get_attribute("checked")
            return result
        except Exception as e:
            raise Exception("webpage has not found 'wifi status' element! The reason is %s"%e)

    #设置wifi的状态
    def set_wifi_status(self):
        try:
            element = self.driver.find_element_by_id("enableWifi")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'wifi status' element! The reason is %s"%e)


    #修改SSID
    def ssid(self,ssid):
        try:
            element = self.driver.find_element_by_id("field_grandstream_ssid0_ssid0_ssid")
            element.clear()
            element.send_keys(ssid)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'ssid' element! The reason is %s"%e)

    #获取SSID
    def get_ssid(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("field_grandstream_ssid0_ssid0_ssid")
            result = element.get_attribute('value')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'ssid' element! The reason is %s"%e)


    #修改wpa密码
    def wpa_key(self,key):
        try:
            element = self.driver.find_element_by_id("field_grandstream_ssid0_ssid0_wpa_key")
            element.clear()
            element.send_keys(key)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'wpa_key' element! The reason is %s"%e)

    #获取可添加设备的mac
    def get_available_devices(self):
        try:
            result = []
            self.driver.implicitly_wait(5)
            elements = self.driver.find_elements_by_css_selector("#wizardavaaps>option")
            for element in elements:
                result.append(element.text)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'available_devices' element! The reason is %s"%e)

    #获取已添加设备的mac
    def get_member_devices(self):
        try:
            result = []
            self.driver.implicitly_wait(5)
            elements = self.driver.find_elements_by_css_selector("#wizardap>option")
            for element in elements:
                result.append(element.text)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'member_devices' element! The reason is %s"%e)


    #获取已添加设备的mac

    #设备管理，只有一个设备时,只添加一个设备
    def add_NG(self):
        try:
            element = self.driver.find_element_by_css_selector("#wizardavaaps>option")
            element.click()
            #点击向右的按钮
            self.driver.find_element_by_id("wizardright").click()
            self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG' element! The reason is %s"%e)

    #设备管理，有多个设备时，选择特定的一个
    def add_NG_special(self,slave_ap):
        try:
            #小写转换为大写
            Slave_ap = slave_ap.upper()
            elements = self.driver.find_elements_by_css_selector("#wizardavaaps>option")
            for element in elements:
                if Slave_ap in element.text:
                    element.click()
                    #点击向右的按钮
                    self.driver.find_element_by_id("wizardright").click()
                    self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'add_NG_special' element! The reason is %s"%e)

    #设备管理，在已添加的设备中删除特定的设备
    def del_NG_special(self,slave_ap):
        try:
            #小写转换为大写
            Slave_ap = slave_ap.upper()
            elements = self.driver.find_elements_by_css_selector("#wizardap>option")
            for element in elements:
                if Slave_ap in element.text:
                    element.click()
                    #点击向右的按钮
                    self.driver.find_element_by_id("wizardleft").click()
                    self.driver.implicitly_wait(5)
        except Exception as e:
            raise Exception("webpage has not found 'del_NG_special' element! The reason is %s"%e)


    #点击关闭按钮
    def close_wizard(self):
        try:
            element = self.driver.find_element_by_id("closewizard")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(30)
            #以下检查设备服务状态的窗口是否显示，显示就循环等待5s继续检查，不显示就跳出,持续10分钟
            service_status_element = self.driver.find_element_by_id("service_status_span")
            WebDriverWait(self.driver,720,5).until_not(lambda x:service_status_element.is_displayed())
            time.sleep(10)
        except Exception as e:
            raise Exception("webpage has not found 'close_wizard' element! The reason is %s"%e)
