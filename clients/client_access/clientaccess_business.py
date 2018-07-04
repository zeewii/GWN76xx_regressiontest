#coding=utf-8
#作者：曾祥卫
#时间：2017.03.29
#描述：GWN76xx客户端的业务层


from clientaccess_control import ClientAccessControl
from clients.clients_business import ClientsBusiness
from connect.ssh import SSH
from data import data
from login.login_business import LoginBusiness
import time

data_basic = data.data_basic()

class ClientAccessBusiness(ClientAccessControl):

    def __init__(self,driver):
        #继承ClientAccessControl类的属性和方法
        ClientAccessControl.__init__(self,driver)

    #添加一个只有一个mac地址的访问列表
    def add_accesslist_onemac(self,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #点击添加按钮
        ClientAccessControl.add_button(self)
        #在添加窗口输入一个mac地址
        ClientAccessControl.set_mac(self,mac)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #删除只添加了一个新增访问列表
    def del_firest_list(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        ClientAccessControl.del_first_button(self)
        #弹出的提示窗口中，点击确认
        ClientAccessControl.notice_ok(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #删除特定的访问列表
    def del_Access_list_n(self,name):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #删除对应的access list
        ClientAccessControl.del_access_list_n(self,name)
        #弹出的提示窗口中，点击确认
        ClientAccessControl.notice_ok(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #删除只添加了一个新增访问列表时，web页面是否有提示该列表被使用
    def check_del_first_list(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        ClientAccessControl.del_first_button(self)
        # #弹出的提示窗口中，点击确认
        # ClientAccessControl.notice_ok(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result


    #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
    def edit_accesslist_onemac(self,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #只有一个新增访问列表时，点击编辑
        ClientAccessControl.edit_button(self)
        #在添加窗口输入一个mac地址
        ClientAccessControl.set_mac(self,mac)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #编辑特定的访问列表---只修改mac，不添加
    def edit_accesslist_n_onemac(self,name,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #编辑对应的access list
        ClientAccessControl.edit_access_list_n(self,name)
        #在添加窗口输入一个mac地址
        ClientAccessControl.set_mac(self,mac)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)
        print "edit access list:%s successfully!"%name

    #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
    def edit_accesslist_manymac(self,n):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #只有一个新增访问列表时，点击编辑
        ClientAccessControl.edit_button(self)
        for i in range(n):
            #添加窗口，点击+号，输入一个mac地址
            ClientAccessControl.set_add_addmac(self)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

     #编辑特定的访问列表---添加n个mac地址，第一个mac地址不修改
    def edit_accesslist_n_manymac(self,name,n):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #编辑对应的access list
        ClientAccessControl.edit_access_list_n(self,name)
        for i in range(n):
            #添加窗口，点击+号，输入一个mac地址
            ClientAccessControl.set_add_addmac(self)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
    def del_accesslist_manymac(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #只有一个新增访问列表时，点击编辑
        ClientAccessControl.edit_button(self)
        #添加窗口，一直点击-号，删除所有的mac，只保留第一个mac地址
        ClientAccessControl.del_all_addmac(self)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #编辑特定的访问列表--删除所有的mac，只保留第一个mac地址
    def del_accesslist_n_manymac(self,name):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #编辑对应的access list
        ClientAccessControl.edit_access_list_n(self,name)
        #添加窗口，一直点击-号，删除所有的mac，只保留第一个mac地址
        ClientAccessControl.del_all_addmac(self)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #获取Global Blacklist的mac地址
    def get_Global_Blacklist_mac(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        result = ClientAccessControl.get_Global_Blacklist(self)
        return result

    #删除Global Blacklist里面的所有的mac
    def del_Global_Blacklist_mac(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #编辑Global Blacklist
        ClientAccessControl.edit_Global_Blacklist_button(self)
        #添加窗口，一直点击-号，删除所有的mac，不保留第一个mac地址
        ClientAccessControl.del_all_addmac_backup(self)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #手动添加两个相同的mac地址到acces list1
    def check_two_same_mac_access_list1(self,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)

        #添加一个相同的mac
        ClientAccessControl.edit_access_list_n(self,"Access List 1")
        element = self.driver.find_element_by_css_selector(".btn.btn-success.macbtn.addmac")
        element.click()
        self.driver.implicitly_wait(20)
        elements = self.driver.find_elements_by_css_selector(".form-control.luci2-field-validate.macinput.tableinput")
        elements[-1].clear()
        elements[-1].send_keys(mac)
        self.driver.implicitly_wait(20)
        #点击保存
        ClientAccessControl.save(self)

        #获取access list1的mac地址
        result = ClientAccessControl.get_Access_List1(self)
        return result

    #获取access list1的mac地址
    def get_access_list1_mac(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        result = ClientAccessControl.get_Access_List1(self)
        return result

    #########以下是客户端访问的方法#############################

    #检查页面上是否有添加和编辑按钮，来判断UI页面正常
    def check_clientaccess_UI(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        try:
            element1 = self.driver.find_element_by_id("newbmRules")
            element2 = self.driver.find_element_by_class_name("editbutton")
            result1 = element1.is_displayed()
            result2 = element2.is_displayed()
            print result1,result2
            if result1 and result2:
                return True
            else:
                return False
        except:
            return False

    #页面默认参数检查
    def check_webpage_default_parameter(self,mac):
        #添加一个只有一个mac地址的访问列表
        ClientAccessBusiness.add_accesslist_onemac(self,mac)
        #获取页面上所有的标题
        result = ClientAccessControl.g_all_title(self)
        #删除只添加了一个新增访问列表
        ClientAccessBusiness.del_firest_list(self)
        if ("Global Blacklist" in result) and ("Access List 1" in result):
            return True
        else:
            return False

    #Global Blacklist默认状态检查
    def check_global_blacklist_default(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #检查默认Global Blacklist的默认列表
        result1 = ClientAccessControl.get_Global_Blacklist(self)
        #获取Global Blacklist的删除的显示状态
        result2 = ClientAccessControl.get_global_del_button_status(self)
        #编辑Global Blacklist
        ClientAccessControl.edit_Global_Blacklist_button(self)
        #获取Global Blacklist的名称的显示状态
        result3 = ClientAccessControl.get_global_name_status(self)
        print result1,result2,result3
        return result1,result2,result3

    #终端在client页面被block后，显示到Global Blacklist中
    def check_block_client(self,mac,host,user,pwd):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        tmp.block_client(mac)
        # #获取客户端的离线状态
        # result1 = tmp.get_offline_status(mac)
        #获取Global Blacklist的mac地址
        result2 = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        ssh = SSH(host,pwd)
        result3 = ssh.ssh_cmd(user,"iptables -nvL")
        if (mac.upper() in result2) and (mac not in result3):
            return True
        else:
            return False

    #删除Global Blacklist中的终端后检查web页面的列表和iptables规则
    def check_del_Global_Blacklist_mac(self,mac,host,user,pwd):
        #删除Global Blacklist里面的所有的mac
        ClientAccessBusiness.del_Global_Blacklist_mac(self)
        #获取Global Blacklist的mac地址
        result1 = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"iptables -nvL")
        if (mac.upper() not in result1) and (mac not in result2):
            return True
        else:
            return False

    #手动添加mac地址到Global Blacklist,并检查是否添加成功
    def check_add_mac_Global_Blacklist(self,mac,host,user,pwd):
        ClientAccessBusiness.edit_accesslist_onemac(self,mac)
        #获取Global Blacklist的mac地址
        result1 = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show wireless.ath0.macfilter")
        result3 = ssh.ssh_cmd(user,"uci show wireless.ath1.macfilter")
        result4 = ssh.ssh_cmd(user,"uci show wireless.ath0.maclist")
        result5 = ssh.ssh_cmd(user,"uci show wireless.ath1.maclist")
        if (mac.upper() in result1) and ('deny' in result2) and ('deny' in result3) \
            and (mac in result4) and (mac in result5):
            return True
        else:
            return False

    #检查mac地址是否添加到macfilter blacklist
    def check_macfilter_blacklist(self,mac,host,user,pwd):
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show wireless.ath0.macfilter")
        result3 = ssh.ssh_cmd(user,"uci show wireless.ath1.macfilter")
        result4 = ssh.ssh_cmd(user,"uci show wireless.ath0.maclist")
        result5 = ssh.ssh_cmd(user,"uci show wireless.ath1.maclist")
        if ('deny' in result2) and ('deny' in result3) \
            and (mac in result4) and (mac in result5):
            return True
        else:
            return False

    #检查mac地址是否添加到macfilter whitelist
    def check_macfilter_whitelist(self,mac,host,user,pwd):
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show wireless.ath0.macfilter")
        result3 = ssh.ssh_cmd(user,"uci show wireless.ath1.macfilter")
        result4 = ssh.ssh_cmd(user,"uci show wireless.ath0.maclist")
        result5 = ssh.ssh_cmd(user,"uci show wireless.ath1.maclist")
        if ('allow' in result2) and ('allow' in result3) \
            and (mac in result4) and (mac in result5):
            return True
        else:
            return False

    #手动添加多条mac地址到Global Blacklist中
    def check_add_many_macs_Global_Blacklist(self,n,mac,host,user,pwd):
        ClientAccessBusiness.edit_accesslist_manymac(self,n)
        #获取Global Blacklist的mac地址
        result1 = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        ssh = SSH(host,pwd)
        result2 = ssh.ssh_cmd(user,"uci show wireless.ath0.macfilter")
        result3 = ssh.ssh_cmd(user,"uci show wireless.ath0.maclist")
        result4 = ssh.ssh_cmd(user,"uci show wireless.ath1.macfilter")
        result5 = ssh.ssh_cmd(user,"uci show wireless.ath1.maclist")
        if (mac.upper() in result1) and ("(%s)"%(n+1) in result1) and \
            ('deny' in result2) and (mac in result3) and \
            ('deny' in result4) and (mac in result5)  :
            return True
        else:
            return False

    #手动添加两个相同的mac地址到Global Blacklist
    def check_two_same_mac_Global_Blacklist(self,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)

        #添加一个相同的mac
        ClientAccessControl.edit_button(self)
        element = self.driver.find_element_by_css_selector(".btn.btn-success.macbtn.addmac")
        element.click()
        self.driver.implicitly_wait(20)
        elements = self.driver.find_elements_by_css_selector(".form-control.luci2-field-validate.macinput.tableinput")
        elements[-1].clear()
        elements[-1].send_keys(mac)
        self.driver.implicitly_wait(20)
        #点击保存
        ClientAccessControl.save(self)

        #获取Global Blacklist的mac地址
        result = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        return result

    #手动添加mac地址后检查Global Blacklist中的mac地址统计
    def check_Global_Blacklist_statistics_through_add_mac(self,n):
        ClientAccessBusiness.edit_accesslist_manymac(self,n)
        #获取Global Blacklist的mac地址
        result1 = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        #删除所有的mac，只保留第一个mac地址
        ClientAccessBusiness.del_accesslist_manymac(self)
        #获取Global Blacklist的mac地址
        result2 = ClientAccessBusiness.get_Global_Blacklist_mac(self)
        if ("(%s)"%(n+1) in result1) and ("(1)" in result2)  :
            return True
        else:
            return False

    #Global Blacklist中mac地址输入非法格式
    def check_invalid_address_Global_Blacklist(self,values):
        result = []
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #只有一个新增访问列表时，点击编辑
        ClientAccessControl.edit_button(self)
        for value in values:
            #在添加窗口输入一个mac地址
            ClientAccessControl.set_mac(self,value)
            #判断输入框下方是否有错误提示,有则返回True，没有则返回False
            tmp = ClientAccessControl.check_error(self)
            result.append(tmp)
        #在添加窗口点击关闭
        ClientAccessControl.close_edit(self)
        print result
        return result

    #Access list1中mac地址输入非法格式
    def check_invalid_address_Access_list(self,values):
        result = []
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #只有一个新增访问列表时，点击编辑
        ClientAccessControl.edit_button(self)
        for value in values:
            #在添加窗口输入一个mac地址
            ClientAccessControl.set_mac(self,value)
            #判断输入框下方是否有错误提示,有则返回True，没有则返回False
            tmp = ClientAccessControl.check_error(self)
            result.append(tmp)
        #在添加窗口点击关闭
        ClientAccessControl.close_edit(self)
        print result
        return result


    #修改列表名称
    def change_list_name(self,name1,name2):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #编辑对应的access list
        ClientAccessControl.edit_access_list_n(self,name1)
        #修改list的名称
        ClientAccessControl.set_list_name(self,name2)
        #点击保存
        ClientAccessControl.save(self)
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)

    #修改两个相同名称的access list
    def check_same_name_list(self,name1,name2):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #编辑对应的access list
        ClientAccessControl.edit_access_list_n(self,name1)
        #修改list的名称
        ClientAccessControl.set_list_name(self,name2)
        #点击保存
        ClientAccessControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #能够添加两个相同mac的的access list会弹出提示
    def check_same_mac_in_different_lists(self,mac):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击客户端访问菜单
        ClientAccessControl.clientaccess_menu(self)
        #点击添加按钮
        ClientAccessControl.add_button(self)
        #在添加窗口输入一个mac地址--相同mac
        ClientAccessControl.set_mac(self,mac)
        #点击保存
        ClientAccessControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        #弹出窗口中，点击应用
        ClientAccessControl.apply(self)
        print result
        return result
