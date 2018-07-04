#coding=utf-8
#作者：曾祥卫
#时间：2017.05.26
#描述：GWN76xx系统设置-基本的业务层


from basic_control import BasicControl
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from connect.ssh import SSH
from data import data
import time
from access_points.aps_business import APSBusiness
from ssid.ssid_business import SSIDBusiness

data_countrycode = data.data_countrycode()
data_basic = data.data_basic()
data_login = data.data_login()
data_timezone = data.data_timezone()
data_AP = data.data_AP()

class BasicBusiness(BasicControl):

    def __init__(self,driver):
        #继承BasicControl类的属性和方法
        BasicControl.__init__(self,driver)


    #选择不同时区，然后登录ap后台来判断是否正确
    def check_time_zone(self):
        tmp = UpgradeBusiness(self.driver)
        result = []
        fail_info = []
        #点击系统设置
        tmp.System_menu()
        #点击基本菜单
        tmp.Basic_menu()
        timezone_list = data_timezone['timezone_list']
        timezone_str = data_timezone['timezone_str']
        for i in range(len(timezone_list)):
            #选择设置不同的时区
            BasicControl.set_time_zone(self,timezone_list[i])
            tmp.save()
            tmp.apply()
            print "change timezone: %s successfully!"%timezone_list[i]
            #登录AP后台判断字符串是否正确
            ssh = SSH(data_basic['DUT_ip'],data_login["all"])
            result1 = ssh.ssh_cmd(data_basic['sshUser'],"date -R")
            if timezone_str[i] in result1:
                result.append(True)
            else:
                timezone_fail_info = "%s\t\t\t%s\t\t\t%s"%(timezone_list[i],result1,timezone_str[i])
                fail_info.append(timezone_fail_info)
                result.append(False)
        #如果有fail信息，则打印
        if fail_info != []:
            print "timezone\t\t\ttest result\t\t\tcorrect result"
            fail_info_str = "\n".join(fail_info)
            print fail_info_str
        return result

      ###########################################################
    #以下是设置国家代码的操作
    ###########################################################
    #设置当前国家 China code=156
    def set_country(self,country_code):
        #点击系统设置菜单
        tmp = UpgradeBusiness(self.driver)
        tmp.System_menu()
        #选择当前的国家代码
        BasicControl.set_country_code(self,country_code)
        #点击保存
        tmp.save()
        tmp.apply()
        time.sleep(80)


    #从后台取出当前国家应该有的所有信道
    def get_correct_channel(self,host,user,pwd,code):
        #从ap或router后台取出当前国家应该有的所有信道
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"ubus call iwpriv_dfs_wifi_cap get_channels '{\\\"country\\\":\\\"%s\\\"}'| grep channel"%code)

        list =  result.replace("\r\n\t\t","").split("\n")
        list_2g =list[1]
        list_5g = list[2]
        chan_2g = list_2g.replace("	\"channel\": ","")
        chan_5g = list_5g.replace("	\"channel\": ","")
        chan_2g_list = chan_2g.split("[",1)[1].split(",")
        chan_5g_list = chan_5g.split("[",1)[1].split(",")
        chan_2g_list.pop()
        chan_5g_list.pop()
        correct_chan_2g = ",".join(chan_2g_list)
        correct_chan_5g = ",".join(chan_5g_list)
        print correct_chan_2g
        print correct_chan_5g
        return correct_chan_2g,correct_chan_5g

    #检查AP当前可用2.4/5G channel
    def check_current_channel(self,host,user,pwd,ath):
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"iwlist %s channel"%ath)
        lists =  result.split("\r\n")[2:-3]
        list = []
        for i in range(len(lists)):
            tmp = lists[i].replace("Channel ","").split(":")[0].strip(" ")
            if  (int(tmp) <= 48) or (int(tmp) >= 149):
                list.append(str(int(tmp)))
        channels = ",".join(list)
        print channels
        return channels

    # 检查2.4G/5G发射功率
    def check_tx_power(self,host,user,pwd,ath):
        try:
            ssh = SSH(host,pwd)
            result = ssh.ssh_cmd(user,"iwconfig %s |grep Tx-Power"%ath)
            list = result.split("=",1)
            power = list[1].split(" ",1)[0]
            print power
            return power
        except:
            print "can't find %s interface"%ath
            return None


    def check_country_channel_power(self,host,user,pwd):
        chan_2g4 = []
        chan_5g = []
        rate_2g4 = []
        rate_5g_1 = []
        rate_5g_2 = []
        fail_info = []
        country = data_countrycode['country']
        countrycode = data_countrycode['ctycode']
        rate2 = data_countrycode['rate_2g']
        rate51 = data_countrycode['rate_5g_band1']
        rate52 = data_countrycode['rate_5g_band2']
        for i in range(len(country)):
            #从后台取出当前国家应该有的所有信道
            correct_chan_2g,correct_chan_5g = BasicBusiness.get_correct_channel(self,host,user,pwd,countrycode[i])
            # 循环设置国家
            BasicBusiness.set_country(self,countrycode[i])
            print "set country is %s successfully!"%country[i]
            # 检查2.4G当前可用信道，返回值与预期结果比较
            result1 = BasicBusiness.check_current_channel(self,host,user,pwd,"ath0")
            if result1 == correct_chan_2g:
                chan_2g4.append(True)
            else:
                print "Fail!!!The country:%s testing 2.4g channel is %s"%(country[i],result1)
                chan_2g4_fail_info = "%s\t\t\t%s\t\t\t2.4G channel\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result1,correct_chan_2g)
                fail_info.append(chan_2g4_fail_info)
                chan_2g4.append(False)
            # 检查5G当前可用信道，返回值与预期结果比较
            result2 = BasicBusiness.check_current_channel(self,host,user,pwd,"ath1")
            if result2 == correct_chan_5g:
                chan_5g.append(True)
            else:
                print "Fail!!!The country:%s testing 5g channel is %s"%(country[i],result2)
                chan_5g_fail_info = "%s\t\t\t%s\t\t\t5G channel\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result2,correct_chan_5g)
                fail_info.append(chan_5g_fail_info)
                chan_5g.append(False)


            #检查2.4的Tx-Power
            result3 = BasicBusiness.check_tx_power(self,host,user,pwd,"ath0")
            if result3 == rate2[i]:
                rate_2g4.append(True)
            else:
                print "Fail!!!The country:%s testing 2.4g power is %s"%(country[i],result3)
                rate_2g4_fail_info = "%s\t\t\t%s\t\t\t2.4G power\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result3,rate2[i])
                fail_info.append(rate_2g4_fail_info)
                rate_2g4.append(False)


            #1如果没有5G信号的
            if correct_chan_5g == "":
                rate_5g_1.append(True)
                rate_5g_2.append(True)
            #2有5G信号，但没有5g band2
            elif (correct_chan_5g != "") and ("149" not in correct_chan_5g):
                #检查5G的Tx-Power,结果追加到rate1
                result41 = BasicBusiness.check_tx_power(self,host,user,pwd,"ath1")
                if result41 == rate51[i]:
                    rate_5g_1.append(True)
                else:
                    print "Fail!!!The country:%s testing 5g power1 is %s"%(country[i],result41)
                    rate_5g1_fail_info = "%s\t\t\t%s\t\t\t5G power1\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result41,rate51[i])
                    fail_info.append(rate_5g1_fail_info)
                    rate_5g_1.append(False)
                #将True追加到rate2
                rate_5g_2.append(True)
            #3有5G信号，但没有5g band1
            elif (correct_chan_5g != "") and ("36" not in correct_chan_5g):
                #将True追加到rate1
                rate_5g_1.append(True)
                #检查5G的Tx-Power,结果追加到rate2
                result42 = BasicBusiness.check_tx_power(self,host,user,pwd,"ath1")
                if result42 == rate52[i]:
                    rate_5g_2.append(True)
                else:
                    print "Fail!!!The country:%s testing 5g power2 is %s"%(country[i],result42)
                    rate_5g2_fail_info = "%s\t\t\t%s\t\t\t5G power2\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result42,rate52[i])
                    fail_info.append(rate_5g2_fail_info)
                    rate_5g_2.append(False)
            #4有5G信号，既有5g band1，又有5g band2
            else:
                tmp1 = SSIDBusiness(self.driver)
                #修改freq为5GHz
                tmp1.change_AP_Freq("5GHz")
                #由于后面需要改5G信道来进行测试，而有些国家40M的模式下没有信道选项，所有先需要修改5G带宽为20M后才能修改信道
                #一起修改5G的带宽和信道36
                tmp = APSBusiness(self.driver)
                tmp.change_5g_width_channel("20MHz","36")
                #检查5G的Tx-Power,结果追加到rate1
                result51 = BasicBusiness.check_tx_power(self,host,user,pwd,"ath0")
                if result51 == rate51[i]:
                    rate_5g_1.append(True)
                else:
                    print "Fail!!!The country:%s testing 5g power1 is %s"%(country[i],result51)
                    rate_5g1_fail_info1 = "%s\t\t\t%s\t\t\t5G power1\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result51,rate51[i])
                    fail_info.append(rate_5g1_fail_info1)
                    rate_5g_1.append(False)
                #修改信道为149
                tmp.set_master_ap_5g_channel_backup("149")
                #检查5G的Tx-Power,结果追加到rate1
                result52 = BasicBusiness.check_tx_power(self,host,user,pwd,"ath0")
                if result52 == rate52[i]:
                    rate_5g_2.append(True)
                else:
                    print "Fail!!!The country:%s testing 5g power2 is %s"%(country[i],result52)
                    rate_5g1_fail_info2 = "%s\t\t\t%s\t\t\t5G power2\t\t\t%s\t\t\t%s"%(country[i],countrycode[i],result52,rate52[i])
                    fail_info.append(rate_5g1_fail_info2)
                    rate_5g_2.append(False)
                #修改回freq为Dual-Band
                tmp1.change_AP_Freq("Dual-Band")
        #如果有fail信息，则打印
        if fail_info != []:
            print "country\t\t\tcountrycode\t\t\ttest item\t\t\ttest result\t\t\tcorrect result"
            fail_info_str = "\n".join(fail_info)
            print fail_info_str
        return chan_2g4,chan_5g,rate_2g4,rate_5g_1,rate_5g_2


