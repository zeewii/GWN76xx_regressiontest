#coding=utf-8
#作者：曾祥卫
#时间：2018.01.22
#描述：GWN76xxssid的业务层

from ssid.ssid_control import SSIDControl
from mesh_control import MeshControl
from network_group.networkgroup_business import NGBusiness
from connect.ssh import SSH
from selenium import webdriver
from data import data
from login.login_business import LoginBusiness
from selenium.webdriver.common.keys import Keys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from clients.clients_business import ClientsBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
import time

data_basic = data.data_basic()

class MeshBusiness(MeshControl):

    def __init__(self,driver):
        #继承MeshControl类的属性和方法
        MeshControl.__init__(self,driver)

    #关闭mesh的方法
    def close_mesh(self):
        tmp = UpgradeBusiness(self.driver)
        #点击系统设置
        tmp.System_menu()
        #点击mesh菜单
        MeshControl.Mesh_menu(self)
        #点击关闭mesh
        MeshControl.close_mesh(self)
        #保存
        MeshControl.mesh_save(self)
        #点击弹出窗口中的应用
        MeshControl.apply(self)


