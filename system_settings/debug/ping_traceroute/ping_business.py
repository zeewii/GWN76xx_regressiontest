#coding=utf-8
#作者：曾祥卫
#时间：2017.06.13
#描述：GWN76xx系统设置-调试-Ping/路由跟踪的的业务层

import time
from system_settings.debug.ping_traceroute.ping_control import PingControl
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from data import data




data_basic = data.data_basic()
data_login = data.data_login()

class PingBusiness(PingControl):

    def __init__(self,driver):
        #继承PingControl类的属性和方法
        PingControl.__init__(self,driver)

    #点击系统设置菜单，然后在点击调试菜单
    def System_Debug_menu(self):
        #点击系统设置菜单
        tmp = UpgradeBusiness(self.driver)
        tmp.System_menu()
        #点击系统设置-调试
        PingControl.Debug_menu(self)
        #点击Ping/路由跟踪 菜单
        PingControl.Ping_menu(self)

    #选择工具，输入目标地址，点击开始
    def run_ping(self,text,value):
        #点击系统设置菜单，然后在点击调试菜单
        PingBusiness.System_Debug_menu(self)
        #选择工具
        PingControl.set_ping_tool(self,text)
        #输入目标值
        PingControl.set_ping_target(self,value)
        #点击开始
        PingControl.click_ping_run(self)
        time.sleep(20)
