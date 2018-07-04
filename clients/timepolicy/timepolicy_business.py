#coding=utf-8
#作者：曾祥卫
#时间：2017.12.06
#描述：GWN76xx客户端的业务层


from timepolicy_control import TimePolicyControl
from clients.clients_business import ClientsBusiness
from connect.ssh import SSH
from data import data
from login.login_business import LoginBusiness
import time

data_basic = data.data_basic()

class TimePolicyBusiness(TimePolicyControl):

    def __init__(self,driver):
        #继承TimePolicyControl类的属性和方法
        TimePolicyControl.__init__(self,driver)

    #新建时间策略，输入相应的数据，检查页面上是否有提示
    def check_new_timepolicy_tip(self, n, name, t, t_out, text, unit):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击添加按钮
        TimePolicyControl.add_button(self)
        #设置名称
        TimePolicyControl.set_name(self, n, name)
        #点击开启
        TimePolicyControl.click_enable_disable(self, n)
        #设置客户端连接限制时间
        TimePolicyControl.set_connection_time(self, n, t)
        #设置客户端连接限制时间的单位
        TimePolicyControl.set_connection_time_unit(self, unit)
        #设置每天的第几小时重连
        TimePolicyControl.set_reset_hour(self, n, t_out)
        #判断页面上提示信息是否正确
        result = TimePolicyControl.check_error(self,text)
        return result

    #按照默认配置，新建一个时间策略
    def new_timepolicy_default(self, n, name, t, t_out, unit):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击添加按钮
        TimePolicyControl.add_button(self)
        #设置名称
        TimePolicyControl.set_name(self, n, name)
        #点击开启
        TimePolicyControl.click_enable_disable(self, n)
        #设置客户端连接限制时间
        TimePolicyControl.set_connection_time(self, n, t)
        #设置客户端连接限制时间的单位
        TimePolicyControl.set_connection_time_unit(self, unit)
        #设置每天的第几小时重连
        TimePolicyControl.set_reset_hour(self, n, t_out)
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)

    #按照默认配置，编辑一个时间策略
    def edit_timepolicy_default(self, n, name, t, t_out, unit):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #设置名称
        TimePolicyControl.set_name(self, n, name)
        # #点击开启
        # TimePolicyControl.click_enable_disable(self, n)
        #设置客户端连接限制时间
        TimePolicyControl.set_connection_time(self, n, t)
        #设置客户端连接限制时间的单位
        TimePolicyControl.set_connection_time_unit(self, unit)
        #设置每天的第几小时重连
        TimePolicyControl.set_reset_hour(self, n, t_out)
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)

    #删除所有的时间策略
    def del_all_timepolicy(self):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #依次点击所有组的删除按钮
        TimePolicyControl.del_all_button(self)
        TimePolicyControl.apply(self)

    #编辑一个时间策略，点击Enable
    def enable_disable_timepolicy(self, n):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #点击开启或关闭
        TimePolicyControl.click_enable_disable(self, n)
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)

    #编辑一个时间策略，修改客户端重连超时类型为每小时
    def change_timeout_hourly(self, n):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #设置客户端重连超时类型
        TimePolicyControl.set_reconnect_type(self, n, "hourly")
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)

    #编辑一个时间策略，修改客户端重连超时类型为每周
    def change_timeout_weekly(self, n, text, t_out):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #设置客户端重连超时类型
        TimePolicyControl.set_reconnect_type(self, n, "weekly")
        #设置每周的第几天
        TimePolicyControl.set_reset_day(self, n, text)
        #设置每天的第几小时重连
        TimePolicyControl.set_reset_hour(self, n, t_out)
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)

    #修改客户端重连超时类型为每周后，检查页面上是否显示对应的礼拜
    def check_timeout_weekly(self, n, t_out):
        result = []
        for text in [u"星期日",u"星期一",u"星期二",u"星期三",u"星期四",u"星期五",u"星期六"]:
            #编辑一个时间策略，修改客户端重连超时类型为每周
            TimePolicyBusiness.change_timeout_weekly(self, n, text, t_out)
            #获取页面所有标题
            tmp = TimePolicyControl.get_titlediv(self)
            tmp1 = text+" "+t_out+":00"
            print tmp1
            if tmp1 in tmp:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #修改客户端重连超时类型为每周后，并每天的第几小时，能够保存
    def check_timeout_weekly_reset_hour(self, n):
        result = []
        for t_out in ["0", "10", "20", "23"]:
            #编辑一个时间策略，修改客户端重连超时类型为每周
            TimePolicyBusiness.change_timeout_weekly(self, n, u"星期二", t_out)
            #获取页面所有标题
            tmp = TimePolicyControl.get_titlediv(self)
            tmp1 = u"星期二"+" "+t_out+":00"
            print tmp1
            if tmp1 in tmp:
                result.append(True)
            else:
                result.append(False)
        for t_out2 in ["1", "8", "15", "22"]:
            #编辑一个时间策略，修改客户端重连超时类型为每周
            TimePolicyBusiness.change_timeout_weekly(self, n, u"星期六", t_out2)
            #获取页面所有标题
            tmp = TimePolicyControl.get_titlediv(self)
            tmp1 = u"星期六"+" "+t_out2+":00"
            print tmp1
            if tmp1 in tmp:
                result.append(True)
            else:
                result.append(False)
        print result
        return result

    #Hour of the Day不合法字符
    def check_timeout_weekly_reset_hour_invalid(self, n, t_outs):
        result = []
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        for t_out in t_outs:
            #设置每天的第几小时重连
            TimePolicyControl.set_reset_hour(self, n, t_out)
            #判断页面上提示信息是否正确
            tmp = TimePolicyControl.check_error(self,u"必须是一个0到23的整数")
            result.append(tmp)
        print result
        return result


    #编辑一个时间策略，修改客户端重连超时类型为根据时间
    def change_timeout_timed(self, n, value, unit):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #设置客户端重连超时类型
        TimePolicyControl.set_reconnect_type(self, n, "timed")
        #设置客户端重连超时
        TimePolicyControl.set_connection_timeout(self, n, value)
        #设置客户端重连超时的单位
        TimePolicyControl.set_connection_timeout_unit(self,unit)
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)

    #检查客户端重连超时为非法字符时的情况
    def check_edit_timeout_timed_tip(self, n, value, unit, text):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #设置客户端重连超时类型
        TimePolicyControl.set_reconnect_type(self, n, "timed")
        #设置客户端重连超时
        TimePolicyControl.set_connection_timeout(self, n, value)
        #设置客户端重连超时的单位
        TimePolicyControl.set_connection_timeout_unit(self,unit)
        #判断页面上提示信息是否正确
        result = TimePolicyControl.check_error(self,text)
        return result

    #编辑一个时间策略，修改客户端重连超时类型为每天
    def change_timeout_daily(self, n, value):
        #点击客户端菜单
        tmp = ClientsBusiness(self.driver)
        tmp.clients_menu()
        #点击时间策略菜单
        TimePolicyControl.timepolicy_menu(self)
        #点击编辑按钮
        TimePolicyControl.edit_button(self, n)
        #设置客户端重连超时类型
        TimePolicyControl.set_reconnect_type(self, n, "daily")
        #设置每天的第几小时重连
        TimePolicyControl.set_reset_hour(self, n, value)
        #点击保存
        TimePolicyControl.click_save(self)
        TimePolicyControl.apply(self)