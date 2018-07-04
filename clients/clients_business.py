#coding=utf-8
#作者：曾祥卫
#时间：2017.03.29
#描述：GWN76xx客户端的业务层


from clients_control import ClientsControl
from connect.ssh import SSH
from data import data
from login.login_business import LoginBusiness
import time

data_basic = data.data_basic()

class ClientsBusiness(ClientsControl):

    def __init__(self,driver):
        #继承ClientsControl类的属性和方法
        ClientsControl.__init__(self,driver)

    #判断无线客户端mac是否在列表中
    def check_client(self,wlan):
        try:
            #点击客户端菜单
            ClientsControl.clients_menu(self)
            self.driver.refresh()
            self.driver.implicitly_wait(30)
            #获取无线客户端的mac
            mac = ClientsControl.get_wlan_mac(self,wlan)
            #将mac地址去掉冒号，转换为小写
            mac1 = mac.split(":")
            mac = ''.join(mac1)
            id = 'mac_%s'%mac
            print id
            self.driver.find_element_by_id(id)
            return True
        except:
            return False

    #客户端离线后再上线，其连接时间重新开始更新
    def disconnect_connect_uptime(self,wlan):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #断开客户端wifi
        ClientsControl.wlan_disable(self,wlan)
        #再启用客户端wifi
        ClientsControl.wlan_enable(self,wlan)
        time.sleep(30)
        #获取第一个客户端的连接时间
        mac = ClientsControl.get_wlan_mac(self,data_basic['wlan_pc'])
        result = ClientsControl.get_client_time(self,mac)
        if result[0:5] == "00:00":
            return True
        else:
            return False

    #Group+有线+客户端显示
    def check_ssid(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击编辑按钮
        ClientsControl.set_edit(self,mac)
        #获取客户端mac
        client_mac = ClientsControl.get_edit_client_mac(self)
        #获取ssid
        ssid_name = ClientsControl.get_edit_ssid(self)
        #获取连接方式
        connecttype = ClientsControl.get_edit_connecttype(self)
        #获取已连接的AP的mac
        conap = ClientsControl.get_edit_conap(self)
        return client_mac,ssid_name,connecttype,conap


    #ssid的客户端信息过滤
    def check_ssid_filter(self,link,wlan):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #通过ssid过滤
        ClientsControl.ssid_filter(self,link)
        #判断无线客户端mac是否在列表中
        try:
            #获取无线客户端的mac
            mac = ClientsControl.get_wlan_mac(self,wlan)
            #将mac地址去掉冒号，转换为小写
            mac1 = mac.split(":")
            mac = ''.join(mac1)
            id = 'mac_%s'%mac
            print id
            self.driver.find_element_by_id(id)
            return True
        except:
            return False





     #修改客户端名称
    def change_client_name(self,mac,name):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击编辑按钮
        ClientsControl.set_edit(self,mac)
        #点击配置菜单
        ClientsControl.config_menu(self)
        #输入客户端名称
        ClientsControl.set_client_name(self,name)
        #点击保存
        ClientsControl.client_save(self)
        #弹出窗口中，点击应用
        ClientsControl.apply(self)


    #客户端名称设置为不合法时
    def check_set_client_name(self,mac,err_name):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击编辑按钮
        ClientsControl.set_edit(self,mac)
        #点击配置菜单
        ClientsControl.config_menu(self)
        #输入客户端名称
        ClientsControl.set_client_name(self,err_name)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = ClientsControl.check_error(self)
        #点击保存
        ClientsControl.client_save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2


    #获取客户端的名称
    def check_client_name(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        result = ClientsControl.get_client_name(self,mac)
        return result


    #获取客户端所连接的ap的mac
    def get_AP_names(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #获取客户端所连接的AP的mac
        result = ClientsControl.get_AP_name(self,mac)
        return result

    #获取客户端所连接的ap的名称
    def get_AP_names_no_mac(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #获取客户端所连接的AP的名称
        result = ClientsControl.get_AP_name_no_mac(self,mac)
        return result

    ##################################################################
    ################以下是客户端隔离#####################################
    ##################################################################
    #Block client时的确认框
    def check_confirm_box(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击阻塞按钮
        ClientsControl.set_block(self,mac)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        #点击取消
        ClientsControl.notice_cancel(self)
        return result


     #只有一个客户端，阻塞该客户端
    def block_client(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击阻塞按钮
        ClientsControl.set_block(self,mac)
        #弹出的提示窗口中，点击确认
        ClientsControl.notice_ok(self)
        ClientsControl.apply(self)
        time.sleep(60)

    #只有一个客户端被禁止时，获取该客户端的mac地址
    def check_block_client(self):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        #获取被block的客户端的mac地址
        result = ClientsControl.get_block_client(self)
        return result

    #只有一个客户端被禁止时，去掉该禁用的客户端
    def unblock_client(self):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        #点击减号按钮
        ClientsControl.click_minus(self)
        #点击保存
        ClientsControl.save(self)
        #弹出窗口中，点击应用
        ClientsControl.apply(self)

    #Banned Client MAC列表手动添加MAC验证
    def add_block_mac(self,mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        #设置block的客户端的mac地址
        ClientsControl.set_block_client(self,mac)
        #点击保存
        ClientsControl.save(self)
        #弹出窗口中，点击应用
        ClientsControl.apply(self)

    #Banned Client MAC列表重复MAC地址验证
    def add_same_block_mac(self):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        #取随机mac地址
        random_mac = ClientsControl.randomMAC(self)
        Random_Mac = random_mac.upper()
        #设置block的客户端的mac地址
        ClientsControl.set_block_client(self,Random_Mac)
        #点击加号按钮
        ClientsControl.click_plus(self)
        elements1 = self.driver.find_elements_by_xpath(".//*[@id='banned_mac']//input")
        elements1[-1].clear()
        elements1[-1].send_keys(Random_Mac)
        self.driver.implicitly_wait(20)
        #点击保存
        ClientsControl.save(self)
        #弹出窗口中，点击应用
        ClientsControl.apply(self)

    #Banned Client MAC列表MAC地址输入验证（非法）
    def check_add_block_mac(self,err_mac):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        #设置block的客户端的mac地址
        ClientsControl.set_block_client(self,err_mac)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = ClientsControl.check_error(self)
        #点击保存
        ClientsControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        print result1,result2
        return result1,result2

    #添加N个mac地址，点击保存应用
    #输入：n：表示多少个mac地址
    def add_many_mac(self,n):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        for i in range(n):
            #添加mac地址输入框,并输入随机mac地址
            ClientsControl.set_addmac(self)
        #点击保存
        ClientsControl.save(self)
        #点击弹出窗口中的应用
        ClientsControl.apply(self)

    #删除所有mac地址，点击保存应用
    def del_many_mac(self,n):
        #点击客户端菜单
        ClientsControl.clients_menu(self)
        #点击禁止客户端按钮
        ClientsControl.click_banned_client(self)
        for i in range(n):
            #删除所有mac输入框
            ClientsControl.del_addmac(self)
        #点击保存
        ClientsControl.save(self)
        #点击弹出窗口中的应用
        ClientsControl.apply(self)

    #登录路由后台，判断Banned mac地址
    def check_banned_mac(self,host,user,pwd):
        ssh = SSH(host,pwd)
        tmp = ssh.ssh_cmd(user,"cat /etc/config/grandstream | grep client_ban")
        tmp1 = tmp.split("\r\n\t")
        result = len(tmp1)-1
        print result
        return result
