#coding=utf-8
#作者：曾祥卫
#时间：2017.05.26
#描述：GWN76xx系统设置-访问的控制层

from publicControl.public_control import PublicControl


class AccessControl(PublicControl):

    def __init__(self,driver):
        #继承PublicControl类的属性和方法
        PublicControl.__init__(self,driver)

    ###########################################################
    #以下是访问页面中的操作
    ###########################################################
    #输入当前管理员密码
    def set_pass0(self,pwd):
        try:
            element = self.driver.find_element_by_id("field_grandstream___password___password_pass0")
            element.clear()
            element.send_keys(pwd)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_pass0' element! The reason is %s"%e)

    #获取当前管理员密码的输入框类型
    def get_pass0_type(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("field_grandstream___password___password_pass0")
            result = element.get_attribute('type')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_pass0_type' element! The reason is %s"%e)

    #点击显示当前管理员密码
    def click_pass0(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='node_grandstream___password___password___default__']//button")
            elements[0].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_pass0' element! The reason is %s"%e)


    #输入管理员新密码
    def set_pass1(self,pwd):
        try:
            element = self.driver.find_element_by_id("field_grandstream___password___password_pass1")
            element.clear()
            element.send_keys(pwd)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_pass1' element! The reason is %s"%e)

    #获取管理员新密码的输入框类型
    def get_pass1_type(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("field_grandstream___password___password_pass1")
            result = element.get_attribute('type')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_pass1_type' element! The reason is %s"%e)

    #点击显示管理员新密码
    def click_pass1(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='node_grandstream___password___password___default__']//button")
            elements[1].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_pass1' element! The reason is %s"%e)


    #输入确认管理员新密码
    def set_pass2(self,pwd):
        try:
            element = self.driver.find_element_by_id("admin_pass2")
            element.clear()
            element.send_keys(pwd)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_pass2' element! The reason is %s"%e)

    #获取确认管理员新密码的输入框类型
    def get_pass2_type(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("admin_pass2")
            result = element.get_attribute('type')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_pass2_type' element! The reason is %s"%e)

    #点击显示确认管理员新密码
    def click_pass2(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='node_grandstream___password___password___default__']//button")
            elements[2].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_pass2' element! The reason is %s"%e)

    #输入用户新密码
    def set_userpass1(self,pwd):
        try:
            element = self.driver.find_element_by_id("field_grandstream___password___password_userpass1")
            element.clear()
            element.send_keys(pwd)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_userpass1' element! The reason is %s"%e)

    #获取用户新密码的输入框类型
    def get_userpass1_type(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("field_grandstream___password___password_userpass1")
            result = element.get_attribute('type')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_userpass1_type' element! The reason is %s"%e)

    #点击显示用户新密码
    def click_userpass1(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='node_grandstream___password___password___default__']//button")
            elements[3].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_userpass1' element! The reason is %s"%e)

    #输入确认用户新密码
    def set_userpass2(self,pwd):
        try:
            element = self.driver.find_element_by_id("user_pass2")
            element.clear()
            element.send_keys(pwd)
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'set_userpass2' element! The reason is %s"%e)

    #获取确认用户新密码的输入框类型
    def get_userpass2_type(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("user_pass2")
            result = element.get_attribute('type')
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_userpass2_type' element! The reason is %s"%e)

    #点击显示确认用户新密码
    def click_userpass2(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='node_grandstream___password___password___default__']//button")
            elements[4].click()
            self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_userpass2' element! The reason is %s"%e)

    #依次点击所有显示按钮
    def click_all_display(self):
        try:
            elements = self.driver.find_elements_by_xpath(".//*[@id='node_grandstream___password___password___default__']//button")
            for element in elements:
                element.click()
                self.driver.implicitly_wait(20)
        except Exception as e:
            raise Exception("webpage has not found 'click_all_display' element! The reason is %s"%e)

    #获取admin两次输入密码不一致时，弹出的提示信息
    def get_admin_tip_info(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='node_grandstream___password___password___default__']/div[3]/div[1]/div[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_admin_tip_info' element! The reason is %s"%e)

    #获取user两次输入密码不一致时，弹出的提示信息
    def get_user_tip_info(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_xpath(".//*[@id='node_grandstream___password___password___default__']/div[5]/div[1]/div[2]")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_user_tip_info' element! The reason is %s"%e)






