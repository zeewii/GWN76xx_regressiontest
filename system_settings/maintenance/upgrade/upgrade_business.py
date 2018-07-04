#coding=utf-8
#作者：曾祥卫
#时间：2017.03.15
#描述：GWN76xx系统设置-升级的业务层


import time
from selenium.webdriver.support.ui import WebDriverWait
from system_settings.maintenance.upgrade.upgrade_control import UpgradeControl
from login.login_business import LoginBusiness
from connect.ssh import SSH
from data import data

data_basic = data.data_basic()
data_login = data.data_login()

class UpgradeBusiness(UpgradeControl):

    def __init__(self,driver):
        #继承UpgradeControl类的属性和方法
        UpgradeControl.__init__(self,driver)

    #升级开始后，一直ping ap的ip，直到无法ping通ap后，再等待120s，可确定ap升级完成
    def confirm_AP_upgrade_finish(self,host,user,pwd,version):
        try:
            #登录AP后台取出版本号
            tmp = UpgradeControl.get_router_version(self,host,user,pwd)
            #如果版本号不相同则等待，如果不相同则直接退出
            if version not in tmp:
                print "AP need to be upgraded!"
                print "-----------rick.zeng upgrade debug:1.start upgrade,go in intelligent wait!-----------"
                print "the result of ping %s is :"%host
                #以下检查是否能够ping通ap，能够ping通就循环等待5s继续检查，不能ping通就跳出,持续20分钟后还能ping通跳异常
                WebDriverWait(self.driver,1200,5).until_not(lambda ping:UpgradeControl.get_ping(self,host)==0)
                print "-----------rick.zeng upgrade debug:2.can't ping %s,and wait 2mins continue to ping-----------"%host
                time.sleep(120)
                WebDriverWait(self.driver,200,5).until(lambda ping:UpgradeControl.get_ping(self,host)==0)
                time.sleep(30)
                print "-----------rick.zeng upgrade debug:3.Quit:can ping %s,quit Smart wait time detection-----------"%host
            else:
                print "-----------rick.zeng upgrade debug:4.version is same,AP can't need to be upgraded!-----------"
            print "AP upgrade finish!"
        except Exception as e:
            raise Exception("AP upgrade occur error! The reason is %s"%e)

    #AP重启或复位后，一直ping ap的ip，直到无法ping通ap后，再等待120s，可确定ap重启完成
    def confirm_AP_reboot_finish(self,host):
        try:
            print "Start:go in Smart wait time detection..."
            print "the result of ping %s is :"%host
            #以下检查是否能够ping通ap，能够ping通就循环等待5s继续检查
            WebDriverWait(self.driver,120,5).until_not(lambda ping:UpgradeControl.get_ping(self,host)==0)
            print "can't ping %s,and wait 2mins continue to ping"%host
            time.sleep(120)
            WebDriverWait(self.driver,120,5).until(lambda ping:UpgradeControl.get_ping(self,host)==0)
            time.sleep(30)
            print "Quit:can ping %s,quit Smart wait time detection"%host
            print "AP reboot finish!"
        except Exception as e:
            raise Exception("AP reboot or set factory occur error! The reason is %s"%e)

    #AP重启升降级固件--AP重启后，检查ap是否升级完成
    def confirm_AP_upgrade_finish_after_reboot(self,host,user,pwd,version):
        try:
            #检查ap是否重启完成
            UpgradeBusiness.confirm_AP_reboot_finish(self,host)
            #检查直到能够ping通ap
            WebDriverWait(self.driver,200,5).until(lambda ping:UpgradeControl.get_ping(self,host)==0)
            #登录AP后台取出版本号
            tmp = UpgradeControl.get_router_version(self,host,user,pwd)
            #如果版本号不相同则等待，如果相同则直接退出
            if version not in tmp:
                print "AP need to be upgraded!"
                print "Start:go in Smart wait time detection..."
                print "the result of ping %s is :"%host
                #以下检查是否能够ping通ap，能够ping通就循环等待5s继续检查，不能ping通就跳出,持续15分钟后还不能ping通跳异常
                WebDriverWait(self.driver,1200,5).until_not(lambda ping:UpgradeControl.get_ping(self,host)==0)
                print "can't ping %s,and wait 2mins continue to ping"%host
                time.sleep(120)
                WebDriverWait(self.driver,200,5).until(lambda ping:UpgradeControl.get_ping(self,host)==0)
                time.sleep(30)
                print "Quit:can ping %s,quit Smart wait time detection"%host
            else:
                print "version is same,AP can't need to be upgraded!"
            print "AP upgrade finish!"
        except Exception as e:
            raise Exception("AP upgrade occur error! The reason is %s"%e)


    ###########################################################
    #以下是升级页面中的操作
    ###########################################################
    #在ap页面上执行重启
    def web_reboot(self,host):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启按钮
        UpgradeControl.reboot(self)
        #弹出的提示窗口中，点击确认
        UpgradeControl.notice_ok(self)
        UpgradeBusiness.confirm_AP_reboot_finish(self,host)
        print "set web reboot ap successfully!"

    #在ap页面上执行重启--不等待ap重启完成
    def web_reboot_backup(self):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启按钮
        UpgradeControl.reboot(self)
        #弹出的提示窗口中，点击确认
        UpgradeControl.notice_ok(self)
        print "set web reboot ap successfully!"

    #在ap页面上设置升级方式
    #输入：FW_name：new,old.mode:HTTP,HTTPS,TFTP
    def set_upgrade_mode(self,addr,mode):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        time.sleep(10)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #选择升级方式
        UpgradeControl.set_firmware_protocal(self,mode)
        #设置固件服务器，输入的地址为本机的ip地址
        UpgradeControl.set_FM_server(self,addr)
        #点击保存
        UpgradeControl.save(self)
        UpgradeControl.apply(self)
        time.sleep(10)
        print "set upgrade mode is %s successfully!"%mode

    #在ap页面上执行升级固件
    #输入：FW_name：new,old.mode:HTTP,HTTPS,TFTP
    def upgrade_web(self,host,user,pwd,version,addr,mode):
        #在ap页面上设置升级方式
        UpgradeBusiness.set_upgrade_mode(self,addr,mode)
        #点击升级按钮
        UpgradeControl.upgrade_button(self)
        #弹出的提示窗口中，点击确认
        UpgradeControl.notice_ok(self)
        UpgradeBusiness.confirm_AP_upgrade_finish(self,host,user,pwd,version)
        print "upgrade FW through %s in AP's webpage successfully!"%mode
        #ping AP的ip，ping通返回0
        result1 = UpgradeControl.get_ping(self,host)
        #登录AP后台取出版本号
        result2 = UpgradeControl.get_router_version(self,host,user,pwd)
        print result1,result2
        if (result1 == 0) and (version in result2):
            return True
        else:
            return False



    #在ap页面上执行boot升级固件
    def upgrade_boot(self,host,user,pwd,version,addr):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #升级方式切换为HTTP
        UpgradeControl.set_firmware_protocal(self,'HTTP')
        #设置固件服务器，输入的地址为本机的ip地址
        UpgradeControl.set_FM_server(self,addr)
        #取消启动时检查
        UpgradeControl.set_on_boot(self)
        #点击保存
        UpgradeControl.save(self)
        UpgradeControl.apply(self)
        #点击重启
        UpgradeControl.reboot(self)
        #弹出的提示窗口中，点击确认
        UpgradeControl.notice_ok(self)
        # time.sleep(500)
        UpgradeBusiness.confirm_AP_upgrade_finish_after_reboot(self,host,user,pwd,version)
        print "reboot and upgrade ap successfully!"
        #ping AP的ip，ping通返回0
        result1 = UpgradeControl.get_ping(self,host)
        #登录AP后台取出版本号
         #登录AP后台取出版本号
        result2 = UpgradeControl.get_router_version(self,host,user,pwd)
        print result1,result2
        if (result1 == 0) and (version in result2):
            return True
        else:
            return False

    #在页面上把AP恢复出厂设置
    def web_factory_reset_backup(self,host):
        #首先等待3分钟再复位，防止slave ap和master ap还未建立tcp连接时复位导致的问题
        time.sleep(180)
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击恢复出厂
        UpgradeControl.factory_reset(self)
        #弹出的提示窗口中，点击确认
        UpgradeControl.notice_ok(self)
        UpgradeBusiness.confirm_AP_reboot_finish(self,host)
        print "click factory reset in webpage successfully!"

    #在页面上把AP恢复出厂设置
    def web_factory_reset(self,host,user,pwd):
        UpgradeBusiness.web_factory_reset_backup(self,host)
        time.sleep(60)
        #登录AP后台取出管理员密码
        ssh1 = SSH(host,pwd)
        result = ssh1.ssh_cmd(user,"uci show grandstream.general.admin_password")
        print result


        #出厂值后登录页面需要设置管理员和用户密码
        #重新打开GWN76xx的web页面
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(10)
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        #调用实例的登录GWN76xx的web界面
        Lg.login(data_basic['superUser'],data_basic["super_defalut_pwd"])
        #第一次登录页面需要设置管理员和用户密码
        Lg.set_super_user_pwd(data_login["all"],data_login["all"],\
                              data_login["all"],data_login["all"])
        if "='admin'" in result:
            return True
        else:
            return False

     #在页面上把AP恢复出厂设置
    def web_factory_reset_backup2(self,host,user,pwd):
        UpgradeBusiness.web_factory_reset_backup(self,host)
        time.sleep(60)
        #登录AP后台取出管理员密码
        ssh1 = SSH(host,pwd)
        result = ssh1.ssh_cmd(user,"uci show grandstream.general.admin_password")
        print result
        if "='admin'" in result:
            return True
        else:
            return False


    ##webUI检查
    def check_reboot_reset_button(self):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        result1 = UpgradeControl.get_reboot(self)
        result2 = UpgradeControl.get_reset(self)
        return result1,result2

    #重启确认
    def check_reboot_confirm(self):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启
        UpgradeControl.reboot(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #点击重启后取消
    def check_cancel_reboot_confirm(self,AP_IP):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启
        UpgradeControl.reboot(self)
        #点击取消
        UpgradeControl.notice_cancel(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        print result1
        result2 = UpgradeControl.get_ping(self,AP_IP)
        return result1,result2

    #点击重启并确认
    def check_ok_reboot_confirm(self,AP_IP):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启
        UpgradeControl.reboot(self)
        #点击确定
        UpgradeControl.notice_ok(self)
        result1 = UpgradeControl.get_ping(self,AP_IP)
        time.sleep(200)
        result2 = UpgradeControl.get_ping(self,AP_IP)
        return result1,result2

    #恢复出厂确认
    def check_reset_confirm(self):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启
        UpgradeControl.factory_reset(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result = element.is_displayed()
        print result
        return result

    #点击重置后取消
    def check_cancel_reset_confirm(self,AP_IP):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启
        UpgradeControl.factory_reset(self)
        #点击取消
        UpgradeControl.notice_cancel(self)
        time.sleep(5)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result1 = element.is_displayed()
        result2 = UpgradeControl.get_ping(self,AP_IP)
        print result1,result2
        return result1,result2

    #点击重置并确认
    def check_ok_reset_confirm(self,AP_IP):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击升级菜单
        UpgradeControl.Upgrade_menu(self)
        #点击重启
        UpgradeControl.factory_reset(self)
        #点击确定
        UpgradeControl.notice_ok(self)
        time.sleep(30)
        result1 = UpgradeControl.get_ping(self,AP_IP)
        time.sleep(200)
        result2 = UpgradeControl.get_ping(self,AP_IP)
        return result1,result2

    ###########################################################
    #以下是系统日志页面中的操作
    ###########################################################
    #设置系统系统日志的地址
    def syslog_uri(self):
        #点击系统设置菜单
        UpgradeControl.System_menu(self)
        #点击外部系统日志菜单
        UpgradeControl.External_Syslog_menu(self)
        #输入系统日志服务器地址
        uri = UpgradeControl.get_localIp(self,data_basic['lan_pc'])
        UpgradeControl.set_syslog_uri(self,uri)
        #点击保存
        UpgradeControl.save(self)
        UpgradeControl.apply(self)
        print "Set %s as external syslog server successfully!"%data_basic['lan_pc']
        # pass

























