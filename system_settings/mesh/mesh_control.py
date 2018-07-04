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

class MeshControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    #点击mesh
    #作者:蒋甜
    def Mesh_menu(self):
        #继承PublicControl类的menu_css方法
        PublicControl.menu_css(self,u"Mesh","Mesh")

    #关闭mesh按钮
    def close_mesh(self):
        try:
            time.sleep(2)
            elements = self.driver.find_element_by_id("field_grandstream_mesh_mesh_5g_enable")
            elements.click()
        except Exception as e:
            raise Exception("webpage has not found 'field_grandstream_mesh_mesh_5g_enable' element! The reason is %s"%e)

    #mesh界面应用按钮
    def mesh_apply(self):
        try:
            time.sleep(2)
            elements = self.driver.find_elements_by_css_selector("btn.btn-primary")[0]
            elements.click()
        except Exception as e:
            raise Exception("webpage has not found 'mesh_apply' element! The reason is %s"%e)

    #mesh界面保存按钮
    def mesh_save(self):
        try:
            time.sleep(5)
            elements = self.driver.find_element_by_xpath(".//*[@id='meshmap']/form/div[2]/div/button[1]")
            elements.click()
        except Exception as e:
            raise Exception("webpage has not found 'mesh_save' element! The reason is %s"%e)