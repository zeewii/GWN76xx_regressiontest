#coding=utf-8
#作者：曾祥卫
#时间：2017.03.10
#描述：GWN7610登录的业务层,包含所有的测试步骤


from login_control import LoginControl
from data import data
from setupwizard.setupwizard_business import SWBusiness
import time

data_basic = data.data_basic()
data_login = data.data_login()

class LoginBusiness(LoginControl):

    def __init__(self,driver):
        #继承LoginControl类的属性和方法
        LoginControl.__init__(self,driver)
        #self.driver = driver

    #登录GWN7610的web界面
    def login(self,username,pwd):
        current_time = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
        print "The current time of running this case is %s"%current_time
        #通过控制层对象LoginControl建一个实例,并指定该实例的属性：username,password
        Lg = LoginControl(self.driver,username,pwd)
        #输入用户名
        Lg.set_username()
        #输入密码
        Lg.set_pwd()
        #点击登录
        Lg.submit()
        print "Input username:%s and password:%s,click submit!"%(username,pwd)

    #登录后判断登录后的“概览”的页面元素，如果有返回True，如果没有返回False,来检测是否登录成功
    def login_test(self):
        try:
            time.sleep(10)
            self.driver.find_element_by_css_selector(".overview-overview.menuselected>a")
            print "login AP successfully!"
            return True
        except Exception:
            print "login AP failed!"
            return False

    #第一次登录页面需要设置管理员和用户密码
    def set_super_user_pwd(self,super_pwd1,super_pwd2,user_pwd1,user_pwd2):
        #继承LoginControl类的部分方法
        #输入管理员密码
        LoginControl.set_super_pwd1(self,super_pwd1)
        #确定输入管理员密码
        LoginControl.set_super_pwd2(self,super_pwd2)
        #输入用户密码
        LoginControl.set_user_pwd1(self,user_pwd1)
        #确定用户密码
        LoginControl.set_user_pwd2(self,user_pwd2)
        #点击保存
        LoginControl.save(self)

    #判断登录页面是否有用户名的元素
    def web_login_test(self):
        try:
            time.sleep(10)
            self.driver.find_element_by_id("username")
            print "login web have username!"
            return True
        except Exception:
            print "login web haven't username!"
            return False

    #判断登录页面是否有“该设备已配对”的元素
    def web_login_dialog_tip(self):
        try:
            time.sleep(10)
            element = self.driver.find_element_by_id("login-dialog-tip")
            result = element.text
            print result
            if (u"该设备已配对" or "The AP is paired") in result:
                print "The AP is paired!"
                return True
            print "The AP isn't paired!"
            return False
        except :
            print "login web haven't paired element!"
            return False



    #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
    def login_again(self):
        #逻辑类对象，建一个实例
        Lg = LoginBusiness(self.driver)
        if Lg.login_test() == False:
            #出厂值后登录页面需要设置管理员和用户密码
            #重新打开GWN7610的web页面
            self.driver.get(data_basic['DUT_web'])
            self.driver.implicitly_wait(10)
            #调用实例的登录GWN7610的web界面
            Lg.login(data_basic['superUser'],data_basic["super_defalut_pwd"])
            #第一次登录页面需要设置管理员和用户密码
            Lg.set_super_user_pwd(data_login["all"],data_login["all"],\
                              data_login["all"],data_login["all"])
            #关掉下次显示，并关闭设置向导
            tmp1 = SWBusiness(self.driver)
            tmp1.hidenexttime()
            tmp1.close_wizard()
            print "login AP successfully again!"

    #刷新页面重新登录ap页面
    def refresh_login_ap(self):
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        self.driver.refresh()
        self.driver.implicitly_wait(60)
        #登录AP
        Lg = LoginBusiness(self.driver)
        if Lg.login_test() == False:
            Lg.login(data_basic['superUser'],data_login['all'])