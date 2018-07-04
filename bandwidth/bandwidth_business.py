#coding=utf-8
#作者：蒋甜
#时间：2018.03.29
#描述：GWN76xx带宽规则的业务层
from bandwidth_control import BandwidthControl
import time
from data import data
import subprocess
from connect.ssh import SSH
d = data.data_basic()

class BandwidthBusiness(BandwidthControl):
    def __init__(self,driver):
        #继承BandwidthControl类的属性和方法
        BandwidthControl.__init__(self,driver)

    ########################################################
    ###############添加带宽规则################################
    ########################################################

    #添加一条带宽规则，范围选择全部，仅输入上传速率
    def add_bandwidth_rule_upstream(self,upstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #清空之前的下游规则
        BandwidthControl.clear_Downstream_Rate(self)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)
        time.sleep(10)

    #添加一条带宽规则，范围选择全部，仅输入下载速率
    def add_bandwidth_rule_downstream(self,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #清空下游规则
        BandwidthControl.clear_Upstream_Rate(self)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)
        time.sleep(10)

    #添加带宽规则，选择特定的ssid
    def add_bandwidth_rule_range_select_ssid(self,n,upstream,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.select_n_ssid(self,n)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)
        time.sleep(10)

    #添加一条带宽规则，范围选择全部，输入上游规则和下游规则
    def add_bandwidth_rule_up_downstream(self,upstream,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)
        time.sleep(10)

        #16个ssid的情况，需要添加翻页，添加一条带宽规则，范围选择全部，输入上游规则和下游规则
    def add_bandwidth_rule_up_downstream_backup(self,upstream,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #翻页
        BandwidthControl.pagedown_16ssid(self)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #添加带宽规则，范围选择mac
    def add_bandwidth_rule_range_mac(self,type,mac,upstream,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入mac地址
        BandwidthControl.Mac_Address(self,mac)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)
        time.sleep(5)

    #添加带宽规则，范围选择mac
    def add_bandwidth_rule_range_mac_ssid(self,type,mac,upstream,downstream,n):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.select_n_ssid(self,n)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入mac地址
        BandwidthControl.Mac_Address(self,mac)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #添加带宽规则，范围选择mac,单位为kbps
    def add_bandwidth_rule_range_mac_unit(self,type,mac,upstream,downstream,unit):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入mac地址
        BandwidthControl.Mac_Address(self,mac)
         #修改上游规则的单位为unit
        BandwidthControl.set_Upstream_Rate_unit(self,unit)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #修改上游规则的单位为unit
        BandwidthControl.set_Downstream_Rate_unit(self,unit)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #添加带宽规则，范围选择mac,范围输入错误的mac
    def add_bandwidth_rule_range_error_mac(self,type,mac):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入mac地址
        BandwidthControl.Mac_Address(self,mac)
        time.sleep(5)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = BandwidthControl.check_error(self)
        #保存
        BandwidthControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        return result1,result2

    #新建一条带宽规则，检查全选按钮
    def check_all(self):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #检查ssid是否被选择
        result = BandwidthControl.ssid_checkd(self)
        return  result

      #新建一条带宽规则，检查全选按钮
    def check_none(self):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #点击none按钮
        BandwidthControl.check_none_ssid(self)
        #检查ssid是否被选择
        result = BandwidthControl.ssid_checkd(self)
        return  result

    #添加一条带宽规则，不保存
    def add_bandwidth_rule_cancel(self,upstream,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        BandwidthControl.bandwidth_cancel(self)

     #添加一条带宽规则，范围选择全部，输入上游规则和下游规则,单位为kbps
    def add_bandwidth_rule_up_downstream_unit(self,upstream,downstream,unit):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #修改上游规则的单位为unit
        BandwidthControl.set_Upstream_Rate_unit(self,unit)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #修改上游规则的单位为unit
        BandwidthControl.set_Downstream_Rate_unit(self,unit)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #新增带宽页面的规则
    def add_bandwidth_ip_rule(self,type,ip,upstream,downstream):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入ip地址
        BandwidthControl.IP_Address(self,ip)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        BandwidthControl.save(self)
        BandwidthControl.apply(self)
        time.sleep(20)

    #新增带宽页面的规则
    def add_bandwidth_ip_rule_upstream(self,type,ip,upstream):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入ip地址
        BandwidthControl.IP_Address(self,ip)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.clear_Downstream_Rate(self)
        BandwidthControl.save(self)
        BandwidthControl.apply(self)
        time.sleep(10)

       #新增带宽页面的规则
    def add_bandwidth_ip_rule_downstream(self,type,ip,downstream):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.add_Bandwidth_Rule_Bt(self)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #选择所有SSID
        BandwidthControl.check_all_ssid(self)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入ip地址
        BandwidthControl.IP_Address(self,ip)
        #输入上游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #输入下游规则
        BandwidthControl.clear_Upstream_Rate(self)
        BandwidthControl.save(self)
        BandwidthControl.apply(self)
        time.sleep(10)

    ########################################################
    ###############编辑带宽规则################################
    ########################################################
    #编辑带宽规则，填入上行流量,下行流量
    def edit_bandwidth_up_downstream(self,n,upstream,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.click_edit_button(self,n)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)


    #编辑带宽规则，填入上行流量,清空下行流量,选择范围选择mac
    def edit_bandwidth_up(self,n,upstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.click_edit_button(self,n)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #输入下游规则
        BandwidthControl.clear_Downstream_Rate(self)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #编辑带宽规则，填入上行流量,清空下行流量,选择范围选择mac
    def edit_bandwidth_down(self,n,downstream):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.click_edit_button(self,n)
        #清空上游规则
        BandwidthControl.clear_Upstream_Rate(self)
        #输入下游规则
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #编辑第n条策略的带宽规则的上行策略输入框异常情况
    def edit_bandwidth_upstream_error(self,n,upstream):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.click_edit_button(self,n)
        #输入上游规则
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #保存
       #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = BandwidthControl.check_error(self)
        #保存
        BandwidthControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        element.click()
        BandwidthControl.bandwidth_cancel(self)
        return result1,result2

    #编辑第n条策略的带宽规则的上行策略输入框异常情况
    def edit_bandwidth_downstream_error(self,n,upstream):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.click_edit_button(self,n)
        #输入上游规则
        BandwidthControl.set_Downstream_Rate(self,upstream)
        #保存
       #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = BandwidthControl.check_error(self)
        #保存
        BandwidthControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        element.click()
        BandwidthControl.bandwidth_cancel(self)
        return result1,result2

     #编辑第n条带宽规则，点击enable/disable按钮
    def bandwidth_rule_enadle_dis(self,n):
        #点击带宽规则菜单
        BandwidthControl.Bw_menu(self)
        #点击带宽规则添加按钮
        BandwidthControl.click_edit_button(self,n)
        #点击勾选带宽规则
        BandwidthControl.enable_dis_Bandwidth(self)
        #保存
        BandwidthControl.save(self)
        #应用
        BandwidthControl.apply(self)

    #编辑带宽页面的ip规则
    def edit_bandwidth_ip_rule(self,n,type,ip):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.click_edit_button(self,n)
        #选择范围
        BandwidthControl.select_Range_Constraint(self,type)
        #填入ip地址
        BandwidthControl.IP_Address(self,ip)
        BandwidthControl.save(self)
        BandwidthControl.apply(self)

    #编辑带宽页面的规则，查看是否有错误提示
    def edit_bandwidth_ip_rule_error(self,n,ip):
        BandwidthControl.Bw_menu(self)
        #编辑第n个带宽规则
        BandwidthControl.click_edit_button(self,n)
        #填入ip地址
        BandwidthControl.IP_Address(self,ip)
        time.sleep(5)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = BandwidthControl.check_error(self)
        #保存
        BandwidthControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        return result1,result2




     ########################################################
    ###############检查带宽规则################################
    ########################################################

    #检查第n条带宽规则开启
    def check_n_bandwidth_enable_dis(self,n):
        BandwidthControl.Bw_menu(self)
        result = BandwidthControl.check_enable_bandwidth(self,n)
        print result
        if "enableicon" == result:
            return True
        if "disableicon" == result:
            return False

    #第n个ssid的名称
    def check_ssid_in_bandwidth(self,ssid):
        BandwidthControl.Bw_menu(self)
        result = BandwidthControl.check_ssid_name(self,ssid)
        return result

    #带宽规则界面判断范围
    def bandwidth_range(self,n):
        BandwidthControl.Bw_menu(self)
        result = BandwidthControl.check_range(self,n)
        return result

    #检查带宽规则的mac/ip与添加是否一致
    def check_mac_ip_range(self,mac,n):
        BandwidthControl.Bw_menu(self)
        result = BandwidthControl.check_mac_ip(self,mac,n)
        return result

    #检查上游速率是否与添加的一致
    def check_upstream(self,n,upstream):
        BandwidthControl.Bw_menu(self)
        result = BandwidthControl.check_upstream_rule(self,n,upstream)
        return result

    #检查上游速率 单位为kbps/mbps时是否超过边界值
    def edit_upstream_unit_error(self,n,upstream,unit):
        BandwidthControl.Bw_menu(self)
        BandwidthControl.click_edit_button(self,n)
        BandwidthControl.set_Upstream_Rate_unit(self,unit)
        BandwidthControl.set_Upstream_Rate(self,upstream)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = BandwidthControl.check_error(self)
        #保存
        BandwidthControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        element.click()
        BandwidthControl.bandwidth_cancel(self)
        return result1,result2

    #检查下游速率 单位为kbps/mbps时是否超过边界值
    def edit_downstream_unit_error(self,n,downstream,unit):
        BandwidthControl.Bw_menu(self)
        BandwidthControl.click_edit_button(self,n)
        BandwidthControl.set_Downstream_Rate_unit(self,unit)
        BandwidthControl.set_Downstream_Rate(self,downstream)
        #判断输入框下方是否有错误提示,有则返回True，没有则返回False
        result1 = BandwidthControl.check_error(self)
        #保存
        BandwidthControl.save(self)
        #判断是否会弹出提示框,有则返回True，没有则返回False
        element =self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
        result2 = element.is_displayed()
        element.click()
        BandwidthControl.bandwidth_cancel(self)
        return result1,result2

    #检查页面带宽规则
    def check_bandwidth_n(self,n):
        BandwidthControl.Bw_menu(self)
        result = BandwidthControl.check_edit_button(self,n)
        return result

    #检查设备带宽规则，上行和下行同时
    def check_bandwidth(self,n,value,host,user,pwd):
        ssh = SSH(host,pwd)
        if int(value)<100:
            value = ("%sM")%value
        else:
            value = ("%sK")%value
        result = ssh.ssh_cmd(user,"uci show grandstream.rule%s.urate"%n)
        result1 = ssh.ssh_cmd(user,"uci show grandstream.rule%s.drate"%n)
        result2 = result.strip()
        result3 = result1.strip()
        print(result2,result3)
        if ("grandstream.rule%s.urate='%sbps'"%(n,value)==result2) and \
                ("grandstream.rule%s.drate='%sbps'"%(n,value)==result3):
            return True
        else:
            return False

    #检查设备带宽规则，上行和下行同时
    def check_bandwidth_not_set(self,n,host,user,pwd):
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"uci show grandstream.rule%s.urate"%n)
        result1 = ssh.ssh_cmd(user,"uci show grandstream.rule%s.drate"%n)
        result2 = result.strip()
        result3 = result1.strip()
        print(result2,result3)
        if ("uci: Entry not found"==result2) and \
                ("uci: Entry not found"==result3):
            return True
        else:
            return False

    #检查设备带宽规则，仅上行
    def check_bandwidth_upstream(self,n,value,host,user,pwd):
        ssh = SSH(host,pwd)
        if int(value)<100:
            value = ("%sM")%value
        else:
            value = ("%sK")%value
        result = ssh.ssh_cmd(user,"uci show grandstream.rule%s.urate"%n)
        result1 = ssh.ssh_cmd(user,"uci show grandstream.rule%s.drate"%n)
        result2 = result.strip()
        result3 = result1.strip()
        print(result2,result3)
        if ("grandstream.rule%s.urate='%sbps'"%(n,value)==result2) and \
                ("uci: Entry not found"==result3):
            return True
        else:
            return False

    #检查设备带宽规则，仅下行
    def check_bandwidth_downstream(self,n,value,host,user,pwd):
        ssh = SSH(host,pwd)
        if int(value)<100:
            value = ("%sM")%value
        else:
            value = ("%sK")%value
        result = ssh.ssh_cmd(user,"uci show grandstream.rule%s.urate"%n)
        result1 = ssh.ssh_cmd(user,"uci show grandstream.rule%s.drate"%n)
        result2 = result.strip()
        result3 = result1.strip()
        print(result2,result3)
        if ("grandstream.rule%s.drate='%sbps'"%(n,value)==result3)and \
                ("uci: Entry not found"==result2):
            return True
        else:
            return False






    ########################################################
    ###############删除带宽规则################################
    ########################################################

    #删除带宽规则界面的ssid(不保存)
    def del_bandwidth_rule(self):
        BandwidthControl.Bw_menu(self)
        BandwidthControl.del_bandwidth_rule_button(self)
        # BandwidthControl.notice_ok(self)

    #删除带宽规则界面的ssid(保存)
    def del_bandwidth_rule_save(self):
        BandwidthControl.Bw_menu(self)
        BandwidthControl.del_bandwidth_rule_button(self)
        # BandwidthControl.save(self)
        print("del bandwidth_rule_save successful")
        BandwidthControl.apply(self)
        # BandwidthControl.notice_ok(self)

    #删除特定的ssid的带宽规则
    def del_special_bandwidth_ssid(self,n):
        BandwidthControl.Bw_menu(self)
        BandwidthControl.del_special_bandwidth_rule(self,n)
        BandwidthControl.notice_ok(self)
        BandwidthControl.apply(self)

    ########################################################
    ###############上下行流量################################
    ########################################################

    #上行流量
    def check_upstream_iperf(self,ssid,password,wlan,lan):
        #无线网卡连接ssid
        BandwidthControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        BandwidthControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = BandwidthControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行上传
                try:
                    tmp1 = subprocess.check_output("iperf3 -c %s -t60 -w5M"%d['iperf_ip'],shell=True)
                    print tmp1
                    a = tmp1.split("\n")
                    print a
                    b = a[-4].split("bits/sec")
                    print b
                    c = b[0].split(" ")
                    print c
                    print c[-2],c[-1]
                    if float(c[-2])>100:
                        result1 = float(c[-2])/1000
                        result2 = "%sbits/sec"%c[-1]
                        print result1,result2
                    else:
                        result1 = float(c[-2])
                    #使无线网卡释放IP地址
                    BandwidthControl.dhcp_release_wlan(self,wlan)
                    #启用有线网卡
                    BandwidthControl.wlan_enable(self,lan)
                    self.driver.refresh()
                    self.driver.implicitly_wait(10)
                    time.sleep(60)
                    return float(result1)
                except:
                    print "iperf3 occur error "
                    #使无线网卡释放IP地址
                    BandwidthControl.dhcp_release_wlan(self,wlan)
                    #启用有线网卡
                    BandwidthControl.wlan_enable(self,lan)
                    BandwidthControl.dhcp_wlan(self,wlan)
                    BandwidthControl.wlan_disable(self,lan)
                    time.sleep(10)
            else:
                BandwidthControl.dhcp_release_wlan(self,wlan)
                BandwidthControl.wlan_enable(self,lan)
                BandwidthControl.dhcp_wlan(self,wlan)
                BandwidthControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #如果无法ping通iperf服务器，则返回100
        return 100

    #下行流量
    def check_downstream_iperf(self,ssid,password,wlan,lan):
        #无线网卡连接ssid
        BandwidthControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        BandwidthControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = BandwidthControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行上传
                try:
                    tmp1 = subprocess.check_output("iperf3 -c %s -t60 -w5M -R"%d['iperf_ip'],shell=True)
                    print tmp1
                    a = tmp1.split("\n")
                    print a
                    b = a[-4].split("bits/sec")
                    print b
                    c = b[0].split(" ")
                    print c
                    print c[-2],c[-1]
                    if float(c[-2])>100:
                        result1 = float(c[-2])/1000
                        result2 = "%sbits/sec"%c[-1]
                        print result1,result2
                    else:
                        result1 = float(c[-2])
                    #使无线网卡释放IP地址
                    BandwidthControl.dhcp_release_wlan(self,wlan)
                    #启用有线网卡
                    BandwidthControl.wlan_enable(self,lan)
                    self.driver.refresh()
                    self.driver.implicitly_wait(10)
                    time.sleep(60)
                    return float(result1)
                except:
                    #使无线网卡释放IP地址
                    BandwidthControl.dhcp_release_wlan(self,wlan)
                    #启用有线网卡
                    BandwidthControl.wlan_enable(self,lan)
                    BandwidthControl.dhcp_wlan(self,wlan)
                    BandwidthControl.wlan_disable(self,lan)
                    time.sleep(10)
            else:
                BandwidthControl.dhcp_release_wlan(self,wlan)
                BandwidthControl.wlan_enable(self,lan)
                BandwidthControl.dhcp_wlan(self,wlan)
                BandwidthControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #如果无法ping通iperf服务器，则返回100
        return 100

    #连接wifi后，获取无线网卡的ip
    def get_ip_after_connect(self,ssid,password,wlan):
        #连接wifi，并使客户端获取到ip
        BandwidthControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #获取无线网卡的ip
        ip = BandwidthControl.get_localIp(self,wlan)
        #释放无线网卡的ip
        BandwidthControl.dhcp_release_wlan(self,wlan)
        return ip











