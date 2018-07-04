#coding=utf-8
#作者：曾祥卫
#时间：2017.12.07
#描述：GWN76xx客户端的禁止的客户端业务层


from bannedclients_control import BannedClientsControl
from clients.clients_business import ClientsBusiness
from connect.ssh import SSH
from data import data
from login.login_business import LoginBusiness
import time

data_basic = data.data_basic()

class BannedClientsBusiness(BannedClientsControl):

    def __init__(self,driver):
        #继承BannedClientsControl类的属性和方法
        BannedClientsControl.__init__(self,driver)

    #解锁客户端
    def unblock_clients(self, n):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        BannedClientsControl.bannedclients_menu(self)
        try:
            #点击解锁按钮
            BannedClientsControl.unblock_button(self, n)
            #弹出的提示窗口中，点击确认
            BannedClientsControl.notice_ok(self)
        except:
            pass


    #获取禁止的客户端页面所有标题
    def get_bannedclients_title(self):
        #刷新页面重新登录ap页面
        Lg = LoginBusiness(self.driver)
        Lg.refresh_login_ap()
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        BannedClientsControl.bannedclients_menu(self)
        #获取页面所有标题
        result = BannedClientsControl.get_titlediv(self)
        print result
        return result

