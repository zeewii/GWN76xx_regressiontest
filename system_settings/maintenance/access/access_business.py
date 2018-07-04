#coding=utf-8
#作者：曾祥卫
#时间：2017.05.26
#描述：GWN76xx系统设置-访问的业务层


from system_settings.maintenance.access.access_control import AccessControl
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from login.login_business import LoginBusiness,LoginControl
from navbar.navbar_business import NavbarBusiness
from connect.ssh import SSH
from data import data
import time

data_basic = data.data_basic()
data_login = data.data_login()

class AccessBusiness(AccessControl):

    def __init__(self,driver):
        #继承AccessControl类的属性和方法
        AccessControl.__init__(self,driver)


    ###########################################################
    #以下是访问页面中的操作
    ###########################################################
    #确认当前管理员密码，管理员新密码，确认管理员新密码，用户新密码，确认用户新密码默认隐藏密钥
    def check_pwd_default_disappear(self):
        tmp = UpgradeBusiness(self.driver)
        #点击系统设置菜单
        tmp.System_menu()
        #点击访问菜单
        tmp.Access_menu()
        #获取所有密码的类型
        result1 = AccessControl.get_pass0_type(self)
        result2 = AccessControl.get_pass1_type(self)
        result3 = AccessControl.get_pass2_type(self)
        result4 = AccessControl.get_userpass1_type(self)
        result5 = AccessControl.get_userpass1_type(self)
        result = [result1,result2,result3,result4,result5]
        return result

    #点击显示，确认所有密码都能显示
    def check_pwd_display(self):
        tmp = UpgradeBusiness(self.driver)
        #点击系统设置菜单
        tmp.System_menu()
        #点击访问菜单
        tmp.Access_menu()
        #依次点击所有显示按钮
        AccessControl.click_all_display(self)
        #获取所有密码的类型
        result1 = AccessControl.get_pass0_type(self)
        result2 = AccessControl.get_pass1_type(self)
        result3 = AccessControl.get_pass2_type(self)
        result4 = AccessControl.get_userpass1_type(self)
        result5 = AccessControl.get_userpass1_type(self)
        result = [result1,result2,result3,result4,result5]
        return result

    #修改所有密码，点击保存
    def change_pwd(self,current_pwd,admin_pwd,user_pwd):
        tmp = UpgradeBusiness(self.driver)
        #点击系统设置菜单
        tmp.System_menu()
        #点击访问菜单
        tmp.Access_menu()
        #输入当前管理员密码
        AccessControl.set_pass0(self,current_pwd)
        #输入管理员新密码
        AccessControl.set_pass1(self,admin_pwd)
        #输入确认管理员新密码
        AccessControl.set_pass2(self,admin_pwd)
        #输入用户新密码
        AccessControl.set_userpass1(self,user_pwd)
        #输入确认用户新密码
        AccessControl.set_userpass2(self,user_pwd)
        #点击保存
        tmp.save()

    #修改管理员密码，点击保存
    def change_admin_pwd(self,current_pwd,admin_pwd1,admin_pwd2):
        tmp = UpgradeBusiness(self.driver)
        #点击系统设置菜单
        tmp.System_menu()
        #点击访问菜单
        tmp.Access_menu()
        #输入当前管理员密码
        AccessControl.set_pass0(self,current_pwd)
        #输入管理员新密码
        AccessControl.set_pass1(self,admin_pwd1)
        #输入确认管理员新密码
        AccessControl.set_pass2(self,admin_pwd2)
        #点击保存
        tmp.save()

    #修改user密码，点击保存
    def change_user_pwd(self,user_pwd1,user_pwd2):
        tmp = UpgradeBusiness(self.driver)
        #点击系统设置菜单
        tmp.System_menu()
        #点击访问菜单
        tmp.Access_menu()
        #输入用户新密码
        AccessControl.set_userpass1(self,user_pwd1)
        #输入确认用户新密码
        AccessControl.set_userpass2(self,user_pwd2)
        #点击保存
        tmp.save()

    #修改所有密码时，当前密码错误时，弹出提示
    def check_pass0_err(self,err_pwd,pwd):
        #修改所有密码，点击保存
        AccessBusiness.change_pwd(self,err_pwd,pwd,pwd)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        return result

    #修改管理员密码时，当前密码错误时，弹出提示
    def check_admin_pass0_err(self,err_pwd,pwd):
        #修改管理员密码，点击保存
        AccessBusiness.change_admin_pwd(self,err_pwd,pwd,pwd)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        return result

    #修改所有密码后，登录路由后台，验证是否修改成功
    def check_change_pwd(self,current_pwd,admin_pwd,user_pwd,host,ssh_user):
        #修改所有密码，点击保存
        AccessBusiness.change_pwd(self,current_pwd,admin_pwd,user_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        ssh = SSH(host,admin_pwd)
        result1 = ssh.ssh_cmd(ssh_user,"uci show grandstream.general.admin_password")
        result2 = ssh.ssh_cmd(ssh_user,"uci show grandstream.general.user_password")
        return result1,result2

    #修改管理员密码后，登录路由后台，验证是否修改成功
    def check_change_admin_pwd(self,current_pwd,admin_pwd,host,ssh_user):
        #修改管理员密码，点击保存
        AccessBusiness.change_admin_pwd(self,current_pwd,admin_pwd,admin_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        ssh = SSH(host,admin_pwd)
        result1 = ssh.ssh_cmd(ssh_user,"uci show grandstream.general.admin_password")
        return result1

    #修改user密码后，登录路由后台，验证是否修改成功
    def check_change_user_pwd(self,admin_pwd,user_pwd,host,ssh_user):
        #修改user密码，点击保存
        AccessBusiness.change_user_pwd(self,user_pwd,user_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        ssh = SSH(host,admin_pwd)
        result1 = ssh.ssh_cmd(ssh_user,"uci show grandstream.general.user_password")
        return result1

    #修改所有密码后，确认密码是隐藏密钥
    def check_pwd_disappear_again(self,current_pwd,admin_pwd,user_pwd):
        #修改所有密码，点击保存
        AccessBusiness.change_pwd(self,current_pwd,admin_pwd,user_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        result = AccessBusiness.check_pwd_default_disappear(self)
        return result

    #修改admin密码后，确认密码是隐藏密钥
    def check_admin_pwd_disappear_again(self,current_pwd,admin_pwd):
        #修改admin密码，点击保存
        AccessBusiness.change_admin_pwd(self,current_pwd,admin_pwd,admin_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        result = AccessBusiness.check_pwd_default_disappear(self)
        return result

    #修改user密码后，确认密码是隐藏密钥
    def check_user_pwd_disappear_again(self,user_pwd):
        #修改user密码，点击保存
        AccessBusiness.change_user_pwd(self,user_pwd,user_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        result = AccessBusiness.check_pwd_default_disappear(self)
        return result

    #修改admin密码，修改后使用某个密码登录，确定是否登录成功
    def use_pwd_login(self,current_pwd,admin_pwd,lgoin_name,login_pwd):
        #修改管理员密码，点击保存
        AccessBusiness.change_admin_pwd(self,current_pwd,admin_pwd,admin_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        #点击页面上的退出按钮
        tmp = NavbarBusiness(self.driver)
        tmp.logout()
        #使用旧密码登录GWN7610的web界面
        tmp1 = LoginBusiness(self.driver)
        tmp1.login(lgoin_name,login_pwd)
        #判断是否登录成功
        result = tmp1.login_test()
        return result

    #修改admin密码时输入两次不一致的新密码,会弹出提示
    def check_admin_pwd_different(self,current_pwd,admin_pwd1,admin_pwd2):
        #修改管理员密码，点击保存
        AccessBusiness.change_admin_pwd(self,current_pwd,admin_pwd1,admin_pwd2)
        result = AccessControl.get_admin_tip_info(self)
        return result

    #修改user密码时输入两次不一致的新密码,会弹出提示
    def check_user_pwd_different(self,user_pwd1,user_pwd2):
        #修改user密码，点击保存
        AccessBusiness.change_user_pwd(self,user_pwd1,user_pwd2)
        result = AccessControl.get_user_tip_info(self)
        return result

    #修改admin密码时只输入一次新密码
    def check_admin_pwd_once(self,current_pwd,admin_pwd1,host,ssh_user):
        #修改管理员密码，点击保存
        AccessBusiness.change_admin_pwd(self,current_pwd,admin_pwd1,"")
        #登录路由后台，确认密码没有改变
        ssh = SSH(host,current_pwd)
        result = ssh.ssh_cmd(ssh_user,"uci show grandstream.general.admin_password")
        return result

    #修改user密码时只输入一次新密码
    def check_user_pwd_once(self,user_pwd1,admin_pwd,host,ssh_user):
        #修改user密码，点击保存
        AccessBusiness.change_user_pwd(self,user_pwd1,"")
        #登录路由后台，确认密码没有改变
        ssh = SSH(host,admin_pwd)
        result = ssh.ssh_cmd(ssh_user,"uci show grandstream.general.user_password")
        return result

    #登录web时先输入密码后输入用户名
    def check_exchange_admin_pwd(self,username,pwd):
        #退出登录
        tmp1 = NavbarBusiness(self.driver)
        tmp1.logout()
        #交换用户名和密码登录GWN7610的web界面
        tmp = LoginControl(self.driver,username,pwd)
        #输入密码
        tmp.set_pwd()
        #输入用户名
        tmp.set_username()
        #点击登录
        tmp.submit()
        #判断是否登录成功
        tmp2 = LoginBusiness(self.driver)
        result = tmp2.login_test()
        return result

    #修改admin密码时，不输入当前密码，直接输入两次新密码
    def change_admin_no_current_pwd(self,pwd):
        return AccessBusiness.check_admin_pass0_err(self,"",pwd)

    #修改admin密码时，不输入当前密码，直接输入1次新密码
    def change_once_admin_no_current_pwd(self,pwd):
        #修改管理员密码，点击保存
        AccessBusiness.change_admin_pwd(self,"",pwd,"")
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        return result

    #修改user密码，修改后使用某个密码登录，确定是否登录成功
    def use_user_pwd_login(self,user_pwd,lgoin_name,login_pwd):
        #修改user密码，点击保存
        AccessBusiness.change_user_pwd(self,user_pwd,user_pwd)
        #弹出窗口中，点击应用
        AccessControl.apply(self)
        #点击页面上的退出按钮
        tmp = NavbarBusiness(self.driver)
        tmp.logout()
        #使用某个密码登录GWN7610的web界面
        tmp1 = LoginBusiness(self.driver)
        tmp1.login(lgoin_name,login_pwd)
        #判断是否登录成功
        result = tmp1.login_test()
        return result

    #登录后判断登录后的“网络组”的页面元素，如果有返回True，如果没有返回False,来检测用户权限
    def user_login_test(self):
        try:
            self.driver.find_element_by_link_text(u"网络组")
            return True
        except Exception:
            return False

    #user账号的权限验证
    def check_user_range(self,lgoin_name,login_pwd):
        #点击页面上的退出按钮
        tmp = NavbarBusiness(self.driver)
        tmp.logout()
        #使用user用户登录GWN7610的web界面
        tmp1 = LoginBusiness(self.driver)
        tmp1.login(lgoin_name,login_pwd)
        result = AccessBusiness.user_login_test(self)
        print result
        return result
