#coding=utf-8
#作者：曾祥卫
#时间：2017.03.22
#描述：GWN76xx概览的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from publicControl.public_control import PublicControl
import time

class OVControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击页面上概览
    def OV_menu(self):
        PublicControl.menu_css(self,u"概览",'Overview')


    #################################################
    #以下是AP图的获取
    #################################################
    #获取全部AP数
    def get_aptotal(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='apChannel']/div/div[2]/div/span")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_aptotal' element! The reason is %s"%e)



    #获取已发现的AP数
    def get_apdiscovered(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_class_name("apDiscovered-num")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_apdiscovered' element! The reason is %s"%e)

    #获取在线的AP数
    def get_aponline(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_class_name("apOnline-num")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_aponline' element! The reason is %s"%e)

    #获取离线的AP数
    def get_apoffline(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_class_name("apOffline-num")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_apoffline' element! The reason is %s"%e)

    #点击窗口右上角可以跳转
    def click_goto_AP_webpage(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".pageFastenter")
            elements[0].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_goto_AP_webpage' element! The reason is %s"%e)

    #获取特定ap的上传流量
    def get_ap_upflow(self,mac):
        try:
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<6:
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='TopAp']/fieldset/div/div[%s]/div[3]/div"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng get ap's upflow debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng get ap's upflow debug:2.can find this AP mac-----------"
                    print "choose mac:%s ap!"%MAC
                    up_element = self.driver.find_element_by_xpath(".//*[@id='TopAp']/fieldset/div/div[%s]/div[6]/div/span[3]/span[2]"%i)
                    print "-----------rick.zeng get ap's upflow debug:3.can find this AP upflow's xpath-----------"
                    result = up_element.text
                    print result
                    return result
                else:
                    print "-----------rick.zeng get ap's upflow debug:4.can't find this AP mac-----------"
                i = i+1
            time.sleep(3)
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_get_ap_upflow_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'get_ap_upflow' element! The reason is %s"%e)

    #获取特定ap的下载流量
    def get_ap_downflow(self,mac):
        try:
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<6:
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='TopAp']/fieldset/div/div[%s]/div[3]/div"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng get ap's downflow debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng get ap's downflow debug:2.can find this AP mac-----------"
                    print "choose mac:%s ap!"%MAC
                    down_element = self.driver.find_element_by_xpath(".//*[@id='TopAp']/fieldset/div/div[%s]/div[6]/div/span[2]/span[2]"%i)
                    print "-----------rick.zeng get ap's downflow debug:3.can find this AP downflow's xpath-----------"
                    result = down_element.text
                    print result
                    return result
                else:
                    print "-----------rick.zeng get ap's downflow debug:4.can't find this AP mac-----------"
                i = i+1
            time.sleep(3)
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_get_ap_downflow_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'get_ap_downflow' element! The reason is %s"%e)


    #获取master ap的下载流量
    def get_master_down(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopAp']/fieldset/div/div[2]/div[6]/div/span[2]/span[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_master_down' element! The reason is %s"%e)

    #
    #获取master ap的上传流量
    # def get_master_up(self):
    #     try:
    #         self.driver.implicitly_wait(10)
    #         element = self.driver.find_element_by_xpath(".//*[@id='TopAp']/fieldset/div/div[2]/div[6]/div/span[3]/span[2]")
    #         result = element.text
    #         print result
    #         return result
    #     except Exception as e:
    #         raise Exception("webpage has not found 'get_master_up' element! The reason is %s"%e)
    #
    # #获取slave1 ap的下载流量
    # def get_slave1_down(self):
    #     try:
    #         self.driver.implicitly_wait(10)
    #         element = self.driver.find_element_by_xpath(".//*[@id='TopAp']/fieldset/div/div[3]/div[6]/div/span[2]/span[2]")
    #         result = element.text
    #         print result
    #         return result
    #     except Exception as e:
    #         raise Exception("webpage has not found 'get_slave1_down' element! The reason is %s"%e)
    #
    # #获取slave1 ap的上传流量
    # def get_slave1_up(self):
    #     try:
    #         self.driver.implicitly_wait(10)
    #         element = self.driver.find_element_by_xpath(".//*[@id='TopAp']/fieldset/div/div[3]/div[6]/div/span[3]/span[2]")
    #         result = element.text
    #         print result
    #         return result
    #     except Exception as e:
    #         raise Exception("webpage has not found 'get_slave1_up' element! The reason is %s"%e)



    #################################################
    #以下是客户端图的获取
    #################################################
    #获取全部客户端数
    def get_clientstotal(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='clientsChannel']/div/div[2]/div/span")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_clientstotal' element! The reason is %s"%e)

    #获取2.4G客户端数
    def get_2g4_client(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_class_name("clientsSmallChannel-num")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_2g4_client' element! The reason is %s"%e)

    #获取5G客户端数
    def get_5g_client(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_class_name("clientsBigChannel-num")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_5g_client' element! The reason is %s"%e)

    #点击窗口右上角可以跳转
    def click_goto_Clients_webpage(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".pageFastenter")
            elements[1].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_goto_Clients_webpage' element! The reason is %s"%e)


    #################################################
    #以下是TOP AP图的获取
    #################################################
    #点击窗口右上角可以跳转
    def click_goto_TOP_AP_webpage(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".pageFastenter")
            elements[2].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_goto_TOP_AP_webpage' element! The reason is %s"%e)


    #################################################
    #以下是TOP SSID图的获取
    #################################################
    #点击窗口右上角可以跳转
    def click_goto_NG_webpage(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".pageFastenter")
            elements[3].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_goto_NG_webpage' element! The reason is %s"%e)

     #获取ssid1的下载流量
    def get_ssid1_down(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopSsid']/fieldset/div/div[2]/div[5]/div/span[2]/span[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_ssid1_down' element! The reason is %s"%e)

    #获取ssid1的上传流量
    def get_ssid1_up(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopSsid']/fieldset/div/div[2]/div[5]/div/span[3]/span[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_ssid1_up' element! The reason is %s"%e)

    #获取ssid2的下载流量
    def get_ssid2_down(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopSsid']/fieldset/div/div[3]/div[5]/div/span[2]/span[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_ssid1_down' element! The reason is %s"%e)

    #获取ssid2的上传流量
    def get_ssid2_up(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopSsid']/fieldset/div/div[3]/div[5]/div/span[3]/span[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_ssid2_up' element! The reason is %s"%e)

    #################################################
    #以下是TOP Clients图的获取
    #################################################
    #点击窗口右上角可以跳转
    def click_goto_TOP_Clients_webpage(self):
        try:
            elements = self.driver.find_elements_by_css_selector(".pageFastenter")
            elements[4].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_goto_TOP_Clients_webpage' element! The reason is %s"%e)

    #获取client的上传流量
    def get_client_up(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopClients']/fieldset/div/div[2]/div[6]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_client_up' element! The reason is %s"%e)

    #获取client的下载流量
    def get_client_down(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='TopClients']/fieldset/div/div[2]/div[5]/div")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_client_down' element! The reason is %s"%e)



    #获取TOP AP,TOP SSID,TOP Clients的内容
    def get_top(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_css_selector('.titlediv')
            for element in elements:
                result.append(element.text)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_top' element! The reason is %s"%e)
