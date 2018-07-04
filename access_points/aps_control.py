#coding=utf-8
#作者：曾祥卫
#时间：2017.03.13
#描述：GWN76xx接入点的控制层

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
from publicControl.public_control import PublicControl
from selenium.webdriver.common.keys import Keys
from connect.ssh import SSH
from data import data
import time

data_ap = data.data_AP()
data_basic = data.data_basic()
data_login = data.data_login()

class APSControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击接入点
    def APS_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"接入点","Access Points")

    #点击搜索AP
    def discover_AP(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id('searhapbtn')
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'discover_AP' element! The reason is %s"%e)

    #获取搜索AP的text
    def get_discover_AP(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id('searhapbtn')
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_discover_AP' element! The reason is %s"%e)


    #点击升级按钮
    def upgrade(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("oper-upgrade-btn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'upgrade' element! The reason is %s"%e)

    #升级的提升窗口中点击“一次性升级”
    def one_time_upgrade(self):
        try:
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_xpath(".//div[@class='modal-footer multi-btn-wrapper']//button[@class='btn btn-primary']")
            for element in elements:
                if element.text == u"一次性升级":
                    element.click()
                    break
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'one_time_upgrade' element! The reason is %s"%e)

    #升级的提升窗口中点击“逐个升级”
    def one_by_one_upgrade(self):
        try:
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_xpath(".//div[@class='modal-footer multi-btn-wrapper']//button[@class='btn btn-primary']")
            for element in elements:
                if element.text == u"逐个升级":
                    element.click()
                    break
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'one_by_one_upgrade' element! The reason is %s"%e)

    #升级的提升窗口中点击“取消”
    def cancel_upgrade(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//div[@class='modal-footer multi-btn-wrapper']//button[@class='btn btn-cancel']")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'cancel_upgrade' element! The reason is %s"%e)

    #点击重启按钮
    def reboot(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("oper-restart-btn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'reboot' element! The reason is %s"%e)

    #点击添加到SSIDs按钮
    def add_Networks_Groups(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("oper-addtozone-btn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'add_networks_groups' element! The reason is %s"%e)

    #点击配置
    def configure(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("oper-config-btn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'configure' element! The reason is %s"%e)

    #点击最后一个设备的删除配对
    def delete_last_paired_device(self):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(180)
            #取出class name为pairedcbx的所有元素
            elements = self.driver.find_elements_by_class_name("unpairbutton")
            #取出最后一个
            element = elements[-1]
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'delete_last_paired_device' element! The reason is %s"%e)

    #选中所有的设备
    def check_all_AP(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_class_name("checkall")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_all_AP' element! The reason is %s"%e)

    #选中第一个设备
    def check_first_AP(self):
        try:
            self.driver.implicitly_wait(10)
            #取出class name为pairedcbx的所有元素
            elements = self.driver.find_elements_by_class_name("pairedcbx")
            #取出第一个
            element = elements[0]
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_first_AP' element! The reason is %s"%e)

    #选中最后一个设备
    def check_last_AP(self):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            #取出class name为pairedcbx的所有元素
            elements = self.driver.find_elements_by_class_name("pairedcbx")
            #取出最后一个
            element = elements[-1]
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_last_AP' element! The reason is %s"%e)


    #选中特定的设备
    def check_special_AP_backup(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                self.driver.implicitly_wait(10)
                print "-----------rick.zeng choose ap debug:1.start choosing ap-----------"
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element = self.driver.find_element_by_xpath(xpath)
                print "-----------rick.zeng choose ap debug:2.can find mac's xpath-----------"
                print element.text
                if MAC in element.text:
                    print "-----------rick.zeng choose ap debug:3.can find this AP mac-----------"
                    print "choose mac:%s ap!"%MAC
                    self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[1]/input"%i).click()
                    self.driver.implicitly_wait(10)
                    print "-----------rick.zeng choose ap debug:4.choose this AP successfully-----------"
                    break
                i = i+1
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'check_special_AP' element! The reason is %s"%e)

    #选中特定的设备
    def check_special_AP_backup2(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            print "-----------rick.zeng choose ap debug:1.start choosing ap-----------"
            xpath1 = ".//*[@id='paired_dev_grid']/div[2]/div[3]/div[1]"
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath1))
            print "-----------rick.zeng choose ap debug:2.can find mac's xpath-----------"
        except:
            print "-----------rick.zeng choose ap debug:3.can't find mac's xpath and goin except module-----------"
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(60)
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath1))
        finally:
            print "-----------rick.zeng choose ap debug:4.goin finally module-----------"
            MAC = mac.upper()
            i = 2
            while i<20:
                self.driver.implicitly_wait(10)
                xpath2 = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element2 = self.driver.find_element_by_xpath(xpath2)
                print "-----------rick.zeng choose ap debug:5.can find mac's xpath again-----------"
                print element2.text
                if MAC in element2.text:
                    print "-----------rick.zeng choose ap debug:6.can find this AP mac-----------"
                    for j in range(3):
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        element3 = self.driver.find_element_by_xpath(xpath_edit)
                        print "-----------rick.zeng choose ap debug:7.can find this AP edit's button-----------"
                        edit_button = element3.is_enabled()
                        print "ap'edit button is %s"%edit_button
                        #如果ap的编辑按钮可以点击
                        if edit_button:
                            print "-----------rick.zeng choose ap debug:8.this AP edit button is enabled-----------"
                            print "choose mac:%s ap!"%MAC
                            self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[1]/input"%i).click()
                            self.driver.implicitly_wait(10)
                            print "-----------rick.zeng choose ap debug:9.click choose button successfully-----------"
                            break
                        else:
                            print "-----------rick.zeng choose ap debug:10.this AP edit button is disabled-----------"
                        time.sleep(60)
                    break
                i = i+1
            time.sleep(3)

    #选中特定的设备
    def check_special_AP(self,mac):
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(3)
        MAC = mac.upper()
        i = 2
        while i<6:
            try:
                print "i=%s"%i
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng choose ap debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng choose ap debug:2.can find this AP mac-----------"
                    while True:
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath_edit))
                        print "-----------rick.zeng choose ap debug:3.can find this AP edit's button-----------"
                        element3 = self.driver.find_element_by_xpath(xpath_edit)
                        WebDriverWait(self.driver,180,5).until(lambda x:element3.is_enabled())
                        print "-----------rick.zeng choose ap debug:4.ap'edit button is enable-----------"
                        print "choose mac:%s ap!"%MAC
                        self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[1]/input"%i).click()
                        self.driver.implicitly_wait(10)
                        print "-----------rick.zeng choose ap debug:5.click choose button successfully-----------"
                        break
                    break
                elif ap_mac_text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_choose_ap_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng choose ap debug:6.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                else:
                    print "-----------rick.zeng choose ap debug:7.can't find this AP mac-----------"
            except Exception as e:
                current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                png = "error_choose_ap_%s.png"%str(current_time)
                self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                raise Exception("webpage has not found 'check_special_AP' element! The reason is %s"%e)
            i = i+1
        time.sleep(3)

    #选中除第一个设备外的所有设备
    def check_except_first(self):
        try:
            self.driver.implicitly_wait(10)
            #取出class name为pairedcbx的所有元素
            elements = self.driver.find_elements_by_class_name("pairedcbx")
            #剔除第一个
            elements.pop(0)
            #点击剔除地一个后的所有元素
            for element in elements:
                element.click()
                self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_except_first' element! The reason is %s"%e)

    #获取特定的设备的ip地址
    def g_special_AP_ip(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                print "-----------rick.zeng get ap's ip debug:1.start getting ap's ip-----------"
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element = self.driver.find_element_by_xpath(xpath)
                print "-----------rick.zeng get ap's ip debug:2.can find mac's xpath-----------"
                print element.text
                if MAC in element.text:
                    print "-----------rick.zeng get ap's ip debug:3.can find this AP mac-----------"
                    print "choose mac:%s ap!"%MAC
                    ip_element = self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[4]/div[1]"%i)
                    print "-----------rick.zeng get ap's ip debug:4.can find this AP ip's xpath-----------"
                    result = ip_element.text
                    print result
                    return result
                elif element.text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_get_ip_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng get ap's ip debug:5.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                else:
                    print "-----------rick.zeng get ap's ip debug:6.can't find this AP mac-----------"
                i = i+1
            time.sleep(3)
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_get_ip_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'g_special_AP_ip' element! The reason is %s"%e)

    #选择特定的ap，点击编辑
    #n:第几个设备
    def click_edit(self,n):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(10)
            elements = self.driver.find_elements_by_class_name("editbutton")
            elements[n-1].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'editbutton' element! The reason is %s"%e)

    #编辑特定的设备
    def edit_special_AP_backup(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "edit mac:%s ap!"%MAC
                    self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%i]/div[8]/div/button[1]"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
        except Exception as e:
            raise Exception("webpage has not found 'edit_special_AP' element! The reason is %s"%e)

    #编辑特定的设备
    def edit_special_AP_backup2(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            print "-----------rick.zeng edit ap debug:1.start editting ap-----------"
            xpath1 = ".//*[@id='paired_dev_grid']/div[2]/div[3]/div[1]"
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath1))
            print "-----------rick.zeng edit ap debug:2.can find mac's xpath-----------"
        except:
            print "-----------rick.zeng edit ap debug:3.can't find mac's xpath and goin except module-----------"
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(60)
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath1))
        finally:
            print "-----------rick.zeng edit ap debug:4.goin finally module-----------"
            MAC = mac.upper()
            i = 2
            while i<20:
                self.driver.implicitly_wait(10)
                xpath2 = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element2 = self.driver.find_element_by_xpath(xpath2)
                print "-----------rick.zeng edit ap debug:5.can find mac's xpath again-----------"
                print element2.text
                if MAC in element2.text:
                    print "-----------rick.zeng edit ap debug:6.can find this AP mac-----------"
                    for j in range(3):
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        element3 = self.driver.find_element_by_xpath(xpath_edit)
                        print "-----------rick.zeng edit ap debug:7.can find this AP edit's button-----------"
                        edit_button = element3.is_enabled()
                        print "ap'edit button is %s"%edit_button
                        #如果ap的编辑按钮可以点击
                        if edit_button:
                            print "-----------rick.zeng edit ap debug:8.this AP edit button is enabled-----------"
                            print "edit mac:%s ap!"%MAC
                            self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%i]/div[8]/div/button[1]"%i).click()
                            self.driver.implicitly_wait(10)
                            print "-----------rick.zeng edit ap debug:9.click edit button successfully-----------"
                            break
                        else:
                            print "-----------rick.zeng edit ap debug:10.this AP edit button is disabled-----------"
                        time.sleep(60)
                    break
                i = i+1
            time.sleep(3)

    #编辑特定的设备
    def edit_special_AP(self,mac):
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(3)
        MAC = mac.upper()
        i = 2
        while i<6:
            try:
                print "i=%s"%i
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng edit ap debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng edit ap debug:2.can find this AP mac-----------"
                    while True:
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath_edit))
                        print "-----------rick.zeng edit ap debug:3.can find this AP edit's button-----------"
                        element3 = self.driver.find_element_by_xpath(xpath_edit)
                        WebDriverWait(self.driver,180,5).until(lambda x:element3.is_enabled())
                        print "-----------rick.zeng edit ap debug:4.ap'edit button is enable-----------"
                        print "edit mac:%s ap!"%MAC
                        element3.click()
                        self.driver.implicitly_wait(10)
                        print "-----------rick.zeng edit ap debug:5.click edit button successfully-----------"
                        break
                    break
                elif ap_mac_text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_edit_ap_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng edit ap debug:6.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                elif ap_mac_text == None:
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_edit_ap_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng edit ap debug:7.can't find this AP mac-----------"
                    time.sleep(180)
                    i = 2
                    continue
            except Exception as e:
                current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                png = "error_edit_ap_%s.png"%str(current_time)
                self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                raise Exception("webpage has not found 'edit_special_AP' element! The reason is %s"%e)
            i = i+1
        time.sleep(3)

    #unpair特定的设备
    def unpair_special_AP_backup(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            MAC = mac.upper()
            i = 2
            while i<20:
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "unpair mac:%s ap!"%MAC
                    self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[2]"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'unpair_special_AP' element! The reason is %s"%e)

    #unpair特定的设备
    def unpair_special_AP_backup2(self,mac):
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(3)
            print "-----------rick.zeng unpair debug:1.start unpairring ap-----------"
            xpath1 = ".//*[@id='paired_dev_grid']/div[2]/div[3]/div[1]"
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath1))
            print "-----------rick.zeng unpair debug:2.can find mac's xpath-----------"
        except:
            print "-----------rick.zeng unpair debug:3.can't find mac's xpath and goin except module-----------"
            self.driver.refresh()
            self.driver.implicitly_wait(10)
            time.sleep(60)
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath1))
        finally:
            print "-----------rick.zeng unpair debug:4.goin finally module-----------"
            MAC = mac.upper()
            i = 2
            while i<20:
                self.driver.implicitly_wait(10)
                xpath2 = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                element2 = self.driver.find_element_by_xpath(xpath2)
                print "-----------rick.zeng unpair debug:5.can find mac's xpath again-----------"
                print element2.text
                if MAC in element2.text:
                    print "-----------rick.zeng unpair debug:6.can find this AP mac-----------"
                    for j in range(3):
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        element3 = self.driver.find_element_by_xpath(xpath_edit)
                        print "-----------rick.zeng unpair debug:7.can find this AP edit's button-----------"
                        edit_button = element3.is_enabled()
                        print "ap'edit button is %s"%edit_button
                        #如果ap的编辑按钮可以点击
                        if edit_button:
                            print "-----------rick.zeng unpair debug:8.this AP edit button is enabled-----------"
                            print "unpair mac:%s ap!"%MAC
                            self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[2]"%i).click()
                            self.driver.implicitly_wait(10)
                            print "-----------rick.zeng unpair debug:9.click unpair button successfully-----------"
                            break
                        else:
                            print "-----------rick.zeng unpair debug:10.this AP edit button is disabled-----------"
                        time.sleep(60)
                    break
                i = i+1
            time.sleep(5)

    #unpair特定的设备
    def unpair_special_AP_backup3(self,mac):
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(60)
        MAC = mac.upper()
        i = 2
        while i<6:
            try:
                print "i=%s"%i
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng unpair debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng unpair debug:2.can find this AP mac-----------"
                    while True:
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath_edit))
                        print "-----------rick.zeng unpair debug:3.can find this AP edit's button-----------"
                        element3 = self.driver.find_element_by_xpath(xpath_edit)
                        WebDriverWait(self.driver,180,5).until(lambda x:element3.is_enabled())
                        print "-----------rick.zeng unpair debug:4.ap'edit button is enable-----------"
                        print "unpair mac:%s ap!"%MAC
                        self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[2]"%i).click()
                        self.driver.implicitly_wait(10)
                        print "-----------rick.zeng unpair debug:5.click unpair button successfully-----------"
                        break
                    break
                elif ap_mac_text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_unpair_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng unpair debug:6.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                else:
                    print "-----------rick.zeng unpair debug:7.can't find this AP mac-----------"
            except Exception as e:
                current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                png = "error_unpair_%s.png"%str(current_time)
                self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                raise Exception("webpage has not found 'unpair_special_AP' element! The reason is %s"%e)
            i = i+1
        time.sleep(5)

    #unpair特定的设备
    def unpair_special_AP(self,mac):
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(60)
        if mac == data_ap['slave:mac1']:
            slave_ip = data_basic['slave_ip1']
        elif mac == data_ap['slave:mac2']:
            slave_ip = data_basic['slave_ip2']
        else:
            "It haven't this slave ap!"
        MAC = mac.upper()
        i = 2
        while i<6:
            try:
                print "i=%s"%i
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='paired_dev_grid']/div[%s]/div[3]/div[1]"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng unpair debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng unpair debug:2.can find this AP mac-----------"
                    while True:
                        #判断ap的编辑按钮是否可以点击，来判断ap是否可用
                        xpath_edit = ".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[1]"%i
                        WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath_edit))
                        print "-----------rick.zeng unpair debug:3.can find this AP edit's button-----------"
                        APSControl.enable_unpair_slave_ap(self,slave_ip)
                        print "-----------rick.zeng unpair debug:4.the slave ap can been unpair-----------"
                        print "unpair mac:%s ap!"%MAC
                        self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[%s]/div[8]/div/button[2]"%i).click()
                        self.driver.implicitly_wait(10)
                        print "-----------rick.zeng unpair debug:5.click unpair button successfully-----------"
                        break
                    break
                elif ap_mac_text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_unpair_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng unpair debug:6.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                else:
                    print "-----------rick.zeng unpair debug:7.can't find this AP mac-----------"
            except Exception as e:
                current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                png = "error_unpair_%s.png"%str(current_time)
                self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                raise Exception("webpage has not found 'unpair_special_AP' element! The reason is %s"%e)
            i = i+1
        time.sleep(5)

    #确定在线ap的数量
    def online_AP_num(self):
        try:
            self.driver.implicitly_wait(10)
            #取出class name为pairedcbx的所有元素
            elements = self.driver.find_elements_by_class_name("pairedcbx")
            result = len(elements)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'online_AP_num' element! The reason is %s"%e)



    #获取设备名称
    def get_name_mac(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_class_name("ipcellrow")
            for element in elements:
                result.append(element.text)
            self.driver.implicitly_wait(10)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_name_mac' element! The reason is %s"%e)

    #获取设备mac
    def get_mac(self):
        try:
            self.driver.implicitly_wait(10)
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_css_selector(".titlediv.mac-div")
            for element in elements:
                result.append(element.text)
            self.driver.implicitly_wait(10)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_mac' element! The reason is %s"%e)



    #获取主界面的运行时间
    def get_uptime1(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//*[@id='paired_dev_grid']/div[2]/div[6]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_uptime1' element! The reason is %s"%e)

    #点击故障切换
    def click_failover(self):
        try:
            element = self.driver.find_element_by_id("oper-failover-btn")
            element.click()
            time.sleep(3)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_failover' element! The reason is %s"%e)

    #获取故障切换的名称
    def get_failover_name(self):
        try:
            element = self.driver.find_element_by_id("oper_failover_span")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_failover_name' element! The reason is %s"%e)

    ###################################################
    #以下是设置故障切换AP的页面操作
    ###################################################
    #检查设置故障切换AP的页面是否显示
    def check_failover_AP_webpage(self):
        try:
            element = self.driver.find_element_by_id("a_setfailoverap")
            result = element.is_displayed()
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_failover_AP_webpage' element! The reason is %s"%e)

    #获取所有可选择的failover ap的个数
    def get_failover_AP_num(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='failoverap']/option")
            result = len(elements)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_failover_AP_num' element! The reason is %s"%e)

    #确认slave ap的mac是否在failover ap的mac list上
    def check_slave_ap(self,slave_mac):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='failoverap']/option")
            for element in elements:
                print element.text
                if element.text == slave_mac.upper():
                    print True
                    return True
            print False
            return False
        except Exception as e:
            raise Exception("webpage has not found 'check_slave_ap' element! The reason is %s"%e)



    #选择failover AP
    def set_failover_AP(self,mac):
        try:
            MAC = mac.upper()
            element = self.driver.find_element_by_id("failoverap")
            Select(element).select_by_visible_text(MAC)
            self.driver.implicitly_wait(20)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'set_failover_AP' element! The reason is %s"%e)

    #failover上点击保存
    def save_failover(self):
        try:
            element = self.driver.find_element_by_id("failover_save")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'save_failover' element! The reason is %s"%e)

    #关闭设置故障切换AP页面
    def close_failover_AP_webpage(self):
        try:
            element = self.driver.find_element_by_id("closefailoverbtn")
            element.click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'close_failover_AP_webpage' element! The reason is %s"%e)


    ###################################################
    #以下是搜索AP后的页面操作
    ###################################################
    #发现的两个个设备时，点击配对
    #输入：mac：需要配对的slave ap的mac
    def pair_AP_backup(self,mac):
        try:
            MAC = mac.upper()
            i = 2
            while i<20:
                xpath = ".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[%s]/div[2]"%i
                element = self.driver.find_element_by_xpath(xpath)
                print element.text
                if MAC in element.text:
                    print "choose mac:%s to pair"%element.text
                    self.driver.find_element_by_xpath(".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[%s]//button"%i).click()
                    self.driver.implicitly_wait(10)
                    break
                i = i+1
            time.sleep(10)
        except Exception as e:
            raise Exception("webpage has not found 'pair_AP' element! The reason is %s"%e)

    #发现的两个个设备时，点击配对
    #输入：mac：需要配对的slave ap的mac
    def pair_AP_backup2(self,mac):
        try:
            time.sleep(3)
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "pair_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            print "-----------rick.zeng pair debug:1.start pairring ap-----------"
            xpath = ".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[2]/div[2]"
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
            print "-----------rick.zeng pair debug:2.can find mac's xpath-----------"
        except:
            print "-----------rick.zeng pair debug:3.can't find mac's xpath and goin except module-----------"
            time.sleep(60)
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
        finally:
            print "-----------rick.zeng pair debug:4.goin finally module-----------"
            MAC = mac.upper()
            i = 2
            while i<20:
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[%s]/div[2]"%i
                element = self.driver.find_element_by_xpath(xpath)
                print "-----------rick.zeng pair debug:5.can find mac's xpath again-----------"
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng pair debug:6.can find this AP mac-----------"
                    print "choose mac:%s to pair"%element.text
                    element2 = self.driver.find_element_by_xpath(".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[%s]//button"%i)
                    pair_enable = element2.is_enabled()
                    print "-----------rick.zeng pair debug:7.this AP pair button is %s-----------"%pair_enable
                    element2.click()
                    self.driver.implicitly_wait(10)
                    print "-----------rick.zeng pair debug:8.click pair button successfully-----------"
                    break
                else:
                    print "-----------rick.zeng pair debug:9.can't find this AP mac-----------"
                i = i+1
            time.sleep(10)

    #发现的两个个设备时，点击配对
    #输入：mac：需要配对的slave ap的mac
    def pair_AP(self,mac):
        time.sleep(60)
        MAC = mac.upper()
        i = 2
        while i<6:
            try:
                print "i=%s"%i
                self.driver.implicitly_wait(10)
                xpath = ".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[%s]/div[2]"%i
                WebDriverWait(self.driver,180,5).until(lambda x:self.driver.find_element_by_xpath(xpath))
                print "-----------rick.zeng pair debug:1.can find mac's xpath-----------"
                element = self.driver.find_element_by_xpath(xpath)
                ap_mac_text = element.text
                print MAC,ap_mac_text
                if MAC in ap_mac_text:
                    print "-----------rick.zeng pair debug:2.can find this AP mac-----------"
                    print "choose mac:%s to pair"%element.text
                    element2 = self.driver.find_element_by_xpath(".//*[@id='discovered_dev_grid']/div[1]/div[1]/div[%s]//button"%i)
                    pair_enable = element2.is_enabled()
                    print "-----------rick.zeng pair debug:3.this AP pair button is %s-----------"%pair_enable
                    element2.click()
                    self.driver.implicitly_wait(10)
                    print "-----------rick.zeng pair debug:4.click pair button successfully-----------"
                    break
                elif ap_mac_text == "":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "error_pair_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng pair debug:5.ap_mac_text is blank-----------"
                    time.sleep(180)
                    i = 2
                    continue
                elif ap_mac_text == "00:00:00:00:00:00":
                    current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                    png = "mac_0_error_pair_%s.png"%str(current_time)
                    self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                    print "-----------rick.zeng pair debug:6.ap_mac_text is 0-----------"
                    ssh = SSH(data_basic['DUT_ip'],data_login["all"])
                    ssh.ssh_cmd(data_basic['sshUser'],"iwconfig")
                    time.sleep(180)
                    i = 2
                    continue
                else:
                    print "-----------rick.zeng pair debug:6.can't find this AP mac-----------"
            except Exception as e:
                current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
                png = "error_pair_%s.png"%str(current_time)
                self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
                raise Exception("webpage has not found 'pair' element! The reason is %s"%e)
            i = i+1
        time.sleep(10)

    #关闭搜索设备窗口
    def close_search_AP(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("closediscovedivbtn")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            raise Exception("webpage has not found 'close_search_AP' element! The reason is %s"%e)

    #获取搜索到的设备的mac
    def get_slave_mac(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_name("mac")
            for element in elements:
                #print element.text
                result.append(element.text)
            self.driver.implicitly_wait(10)
            #删除掉多余的元素
            result.remove("")
            result.remove("")
            result.remove("MAC")
            try:
                result.remove(u"名称/MAC")
            except:
                result.remove("Name/MAC")

            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_slave_mac' element! The reason is %s"%e)


    ###################################################
    #以下是添加到网络组的页面操作
    ###################################################
    #添加网络组中，点击全选
    def check_all_Networks_Groups(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("chkall")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_all_Networks_Groups' element! The reason is %s"%e)

    #添加网络组中，点击全不选
    def check_None_Networks_Groups(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("unchkall")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_None_Networks_Groups' element! The reason is %s"%e)

    #添加网络组中，只有一个网络组时，点击该网络组
    def check_group(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_css_selector(".zone-item>input")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_group' element! The reason is %s"%e)

    #添加网络组中，有多个网络组时，选择特定的一个网络组
    def check_special_group(self,n):
        try:
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_css_selector(".zone-item>input")
            elements[n-1].click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'check_group' element! The reason is %s"%e)


    #添加网络组中，点击保存
    def save_Networks_Groups(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("addtozone_save")
            element.click()
        except Exception as e:
            raise Exception("webpage has not found 'save_Networks_Groups' element! The reason is %s"%e)

    #添加网络组中，点击取消
    def cancel_Networks_Groups(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("addtozone_cancel")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'cancel_Networks_Groups' element! The reason is %s"%e)

    #添加网络组中，点击关闭
    def close_Networks_Groups(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("closeaddtozonebtn")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'close_Networks_Groups' element! The reason is %s"%e)



    ###################################################
    #以下是点击编辑弹出的窗口的页面操作
    ###################################################
    #在编辑窗口点击状态菜单
    def click_status(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("m_status")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_status' element! The reason is %s"%e)

    #在编辑窗口点击用户菜单
    def click_users(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("m_users")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_users' element! The reason is %s"%e)

    #在编辑窗口点击配置菜单
    def click_config(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("m_config")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'click_config' element! The reason is %s"%e)

    #在编辑窗口点击保存
    def click_save(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("m_save")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'click_save' element! The reason is %s"%e)

    #在编辑窗口点击关闭按钮
    def close_edit(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("closeedit")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            raise Exception("webpage has not found 'close_edit' element! The reason is %s"%e)



    ###################################################
    #以下是编辑窗口中的状态操作
    ###################################################

    #获取设备mac地址
    def get_device_mac(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("devicemac")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_device_mac' element! The reason is %s"%e)

    #获取产品型号
    def get_device_model(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("devicemodel")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_device_model' element! The reason is %s"%e)

    #获取PN值
    def get_PN(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("partnumber")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_PN' element! The reason is %s"%e)

    #获取引导程序
    def get_boot_version(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("bootversion")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_boot_version' element! The reason is %s"%e)

    #获取固件版本
    def get_firmware_version(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("firmwareversion")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_firmware_version' element! The reason is %s"%e)

    #获取IP地址
    def get_ipaddr(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("ipaddr")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_ipaddr' element! The reason is %s"%e)

    #获取运行时间
    def get_uptime(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("uptime")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_uptime' element! The reason is %s"%e)

    #获取当前时间
    def get_curtime(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("curtime")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_curtime' element! The reason is %s"%e)

    #获取平均负荷
    def get_loadaverage(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("loadaverage")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_loadaverage' element! The reason is %s"%e)

    #获取NET/POE端口的连接速度
    def get_linkspeed(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("linkspeed")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_linkspeed' element! The reason is %s"%e)

    #获取NET端口的连接速度
    def get_linkspeed2(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("linkspeed2")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_linkspeed2' element! The reason is %s"%e)

    #获取2.4G无线信道
    def get_channel2g4(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("channel2g4")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_channel2g4' element! The reason is %s"%e)

    #获取2.4G用户数量
    def get_usercount2g4(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("usercount2g4")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_usercount2g4' element! The reason is %s"%e)

    #获取5G无线信道
    def get_channel5g(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("channel5g")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_channel5g' element! The reason is %s"%e)

    #获取5G用户数量
    def get_usercount5g(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("usercount5g")
            result = element.text
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_usercount5g' element! The reason is %s"%e)



    ###################################################
    #以下是编辑窗口中的用户的页面操作
    ###################################################
    #获取所有用户设备mac地址
    def get_users_mac(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_class_name("overflow")
            for element in elements:
                result.append(element.text)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_users_mac' element! The reason is %s"%e)

    #获取所有用户设备的主机名
    def get_users_name(self):
        try:
            result = []
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_class_name("titlediv")
            for element in elements:
                result.append(element.text)
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_users_name' element! The reason is %s"%e)

    #获取所有用户设备数
    def get_users_num(self):
        try:
            self.driver.implicitly_wait(10)
            elements = self.driver.find_elements_by_class_name("overflow")
            result = len(elements)
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_users_num' element! The reason is %s"%e)



    ###################################################
    #以下是配置窗口中的配置的页面操作
    ###################################################
    #接入点页面中需要翻页操作时需要找到最底下的元素属性:接入点-编辑-配置页面-id1
    def config_pagedown1(self):
        self.driver.find_element_by_id(data_ap["config_pagedown_id1"]).send_keys(Keys.PAGE_DOWN)
        self.driver.implicitly_wait(10)
        time.sleep(3)

    #设置设备名称
    def set_device_name(self,name):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("name")
            element.clear()
            element.send_keys(name)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_device_name' element! The reason is %s"%e)



    #点击勾选固定ip
    def click_fixed_ip(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("static")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'click_fixed_ip' element! The reason is %s"%e)

     #确定固定ip是否勾选
    def check_fixed_ip(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("static")
            result = element.get_attribute('checked')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_fixed_ip' element! The reason is %s"%e)


    #设置固定ip的地址
    def set_fixed_ip(self,ip):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("ipv4_static")
            element.clear()
            element.send_keys(ip)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_fixed_ip' element! The reason is %s"%e)

    #获取固定ip的地址
    def get_fixed_ip(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("ipv4_static")
            return element.get_attribute("value")
        except Exception as e:
            raise Exception("webpage has not found 'get_fixed_ip' element! The reason is %s"%e)


    #设置固定ip的子网掩码
    def set_fixed_netmask(self,netmask):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("ipv4_static_mask")
            element.clear()
            element.send_keys(netmask)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_fixed_netmask' element! The reason is %s"%e)

    #设置固定ip的网关
    def set_fixed_gateway(self,gateway):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("ipv4_route")
            element.clear()
            element.send_keys(gateway)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_fixed_gateway' element! The reason is %s"%e)

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



    #输入：mode，要设置的频段:2.4G,5G,Dual-Band
    def set_Frequency(self,mode):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("frequency")
            if mode == "2.4GHz":
                a.send_keys("2")
            elif mode == "5GHz":
                a.send_keys("5")
            elif mode == "Dual-Band":
                a.send_keys("d")
        except Exception as e:
            raise Exception("webpage has not found 'set_Frequency' element! The reason is %s"%e)

    #切换2.4G模式
    def set_2g4_mode(self,n):
        try:
            a = self.driver.find_element_by_id("2g4_mode")
            for i in range(n):
                a.send_keys("8")
            a.send_keys(Keys.TAB)
            self.driver.implicitly_wait(10)
            time.sleep(2)
        except Exception as e:
            raise Exception("webpage has not found 'set_2g4_mode' element! The reason is %s"%e)

    #切换2.4G信道
    #输入：channel:0为自动
    def set_2g4_channel(self,channel):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(5)
            a = self.driver.find_element_by_id("2g4_channel")
            a.click()
            a.send_keys("c")
            # Select(a).select_by_value(channel)
            # Select(a).select_by_index(1)
            #a.find_element_by_xpath("//option[@value='%s']"%channel).click()
            self.driver.implicitly_wait(10)
            time.sleep(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_2g4_channel' element! The reason is %s"%e)

    #切换5G信道
    #输入：channel:0为自动
    def set_5g_channel(self,channel):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            a = self.driver.find_element_by_id("5g_channel")
            Select(a).select_by_value(channel)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_5g_channel' element! The reason is %s"%e)

    #切换5G信道
    #输入：channel:0为自动--不需要按tab键
    def set_5g_channel_backup(self,channel):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("5g_channel")
            Select(a).select_by_value(channel)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_5g_channel' element! The reason is %s"%e)


    #切换5G带宽
    #输入：mode，要设置的频段:20,40,80MHz
    def set_5g_width(self,mode):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            a = Select(self.driver.find_element_by_id("5g_width"))
            a.select_by_visible_text(mode)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_5g_width' element! The reason is %s"%e)


    #点击2.4g的短保护间隔
    def set_2g4_shortgi(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("2g4_shortgi")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_2g4_shortgi' element! The reason is %s"%e)

    #检查2.4g的短保护间隔是否是灰色，不能选择
    def check_2g4_shortgi_disable(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("2g4_shortgi")
            self.driver.implicitly_wait(10)
            result = element.get_attribute("disabled")
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_2g4_shortgi_disable' element! The reason is %s"%e)

    #检查2.4g的短保护间隔是否已经被选择
    #输出：true：被选中，None：没被选中
    def check_2g4_shortgi_checked(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("2g4_shortgi")
            self.driver.implicitly_wait(10)
            result = element.get_attribute("checked")
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_2g4_shortgi_checked' element! The reason is %s"%e)

    #点击5g的短保护间隔
    def set_5g_shortgi(self):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            element = self.driver.find_element_by_id("5g_shortgi")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'set_5g_shortgi' element! The reason is %s"%e)

    #检查5g的短保护间隔是否已经被选择
    #输出：true：被选中，None：没被选中
    def check_5g_shortgi_checked(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("5g_shortgi")
            self.driver.implicitly_wait(10)
            result = element.get_attribute("checked")
            return result
        except Exception as e:
            raise Exception("webpage has not found 'check_5g_shortgi_checked' element! The reason is %s"%e)

    #切换2.4G的激活空间流
    #输入：stream:0为自动,1,2,3
    def s_2g4_active_streams(self,stream):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("2g4_active_streams")
            a.click()
            a.send_keys(stream)
            # Select(a).select_by_value(stream)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_2g4_active_streams' element! The reason is %s"%e)

    #切换5G的激活空间流
    #输入：stream:0为自动,1,2
    def s_5g_active_streams(self,stream):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(10)
            APSControl.config_pagedown1(self)
            a = self.driver.find_element_by_id("5g_active_streams")
            Select(a).select_by_value(stream)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_5g_active_streams' element! The reason is %s"%e)

    def s_5g_active_streams_backup(self,stream):
        try:
            a = self.driver.find_element_by_id("5g_active_streams")
            Select(a).select_by_value(stream)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_5g_active_streams' element! The reason is %s"%e)


    #切换2.4G的无线功率
    #输入：power:0,1,2
    def s_2g4_power(self,power):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("2g4_power")
            Select(a).select_by_value(power)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_2g4_power' element! The reason is %s"%e)

    #切换5G的无线功率
    #输入：power:0,1,2
    def s_5g_power(self,power):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            a = self.driver.find_element_by_id("5g_power")
            Select(a).select_by_value(power)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_5g_power' element! The reason is %s"%e)

    #设置2.4G的自定义发射功率
    def s_2g4_custom_power(self,power):
        try:
            self.driver.implicitly_wait(10)
            a = self.driver.find_element_by_id("2g4_power")
            a.click()
            a.send_keys("c")
            a.send_keys(Keys.ENTER)
            # Select(a).select_by_value("3")
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            element = self.driver.find_element_by_id("custom_2g4_power")
            element.clear()
            element.send_keys(power)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_2g4_custom_power' element! The reason is %s"%e)

    #获取2.4G的自定义发射功率
    def g_2g4_custom_power(self):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            element = self.driver.find_element_by_id("custom_2g4_power")
            result =  element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_2g4_custom_power' element! The reason is %s"%e)


    #设置5G的自定义发射功率
    def s_5g_custom_power(self,power):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            a = self.driver.find_element_by_id("5g_power")
            Select(a).select_by_value("3")
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_id("custom_5g_power")
            element.clear()
            element.send_keys(power)
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 's_5g_custom_power' element! The reason is %s"%e)

    #获取5G的自定义发射功率
    def g_5g_custom_power(self):
        try:
            self.driver.implicitly_wait(10)
            APSControl.config_pagedown1(self)
            element = self.driver.find_element_by_id("custom_5g_power")
            result =  element.get_attribute("value")
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'g_5g_custom_power' element! The reason is %s"%e)

