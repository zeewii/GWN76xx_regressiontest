#coding=utf-8
#作者：曾祥卫
#时间：2017.03.22
#描述：GWN76xx概览的业务层

from overview_control import OVControl
import time,subprocess
from data import data
from login.login_business import LoginBusiness

d = data.data_basic()

class OVBusiness(OVControl):

    def __init__(self,driver):
        #继承OVControl类的属性和方法
        OVControl.__init__(self,driver)


    #无线网卡连接ap等待6分钟，再切换会overview菜单
    def wait_changeto_overview(self,ssid,password,wlan):
        #无线网卡连接
        OVControl.connect_WPA_AP(self,ssid,password,wlan)
        #OVControl.dhcp_wlan(self,wlan)
        #等待6分钟
        time.sleep(360)
        #切换到接入点菜单
        OVControl.menu_css(self,u"接入点","Access Points")
        #切换到overview菜单
        OVControl.OV_menu(self)
        time.sleep(20)

    #已有添加一个slave ap到默认网络组后，检查AP的页面
    def check_ap(self):
        result = []
        ##获取已发现的AP数
        result1 = OVControl.get_apdiscovered(self)
        result.append(result1)
        #获取在线的AP数
        result2 = OVControl.get_aponline(self)
        result.append(result2)
        print result
        return result

    #已有添加一个slave ap到默认网络组后，检查TOP页面
    def step_001_check_top(self,master_ap,slave_ap,ssid,wlan):
        #使用无线网卡连接该AP的ssid
        #OVControl.connect_WPA_AP(self,ssid,password,wlan)
        #使无线网卡获取IP地址
        #OVControl.dhcp_wlan(self,wlan)
        #获取无线网卡的mac
        wmac = OVControl.get_wlan_mac(self,wlan)
        #mac地址转换为大写
        Master_ap = master_ap.upper()
        Slave_ap = slave_ap.upper()
        wlan_client_mac = wmac.upper()
        #切换到overview菜单
        OVControl.OV_menu(self)
        time.sleep(5)
        #获取页面上的top AP中的mac地址
        result = OVControl.get_top(self)
        print Master_ap,Slave_ap,ssid,wlan_client_mac
        print result
        if (Master_ap in result) and (Slave_ap in result) and \
                (ssid in result) and (wlan_client_mac in result):
            return True
        else:
            return False


    #点击窗口右上角可以跳转到接入点页面
    def goto_AP_webpage(self):
        #点击窗口右上角可以跳转
        OVControl.click_goto_AP_webpage(self)
        try:
            self.driver.find_element_by_id("a_accesspoint")
            return True
        except:
            return False

    #点击窗口右上角可以跳转到客户端页面
    def goto_Client_webpage(self):
        #点击窗口右上角可以跳转
        OVControl.click_goto_Clients_webpage(self)
        try:
            self.driver.find_element_by_class_name("blockbutton")
            return True
        except:
            return False

    #点击窗口右上角可以跳转到接入点页面
    def goto_TOP_AP_webpage(self):
        #点击窗口右上角可以跳转
        OVControl.click_goto_TOP_AP_webpage(self)
        try:
            self.driver.find_element_by_id("a_accesspoint")
            return True
        except:
            return False

    #点击TOP SSID右上角的三个小点，页面将跳转到网络组页面
    def goto_NG_webpage(self):
        #点击窗口右上角可以跳转
        OVControl.click_goto_NG_webpage(self)
        try:
            self.driver.find_element_by_id("newssid")
            return True
        except:
            return False

    #点击TOP clients右上角的三个小点，页面将跳转到客户端页面
    def goto_TOP_Clients_webpage(self):
        #点击窗口右上角可以跳转
        OVControl.click_goto_TOP_Clients_webpage(self)
        try:
            self.driver.find_element_by_class_name("blockbutton")
            return True
        except:
            return False



    #AP 下载流量统计的准确性---master ap
    def check_masterAP_download_backup(self,ssid,password,wlan,lan,mac):
        #无线网卡连接master ap
        OVControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        OVControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = OVControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行下载
                tmp1 = subprocess.call("iperf3 -c %s -t180 -w5M -R"%d['iperf_ip'],shell=True)
                print tmp1
                break
            else:
                OVControl.wlan_enable(self,lan)
                OVControl.dhcp_release_wlan(self,wlan)
                OVControl.dhcp_wlan(self,wlan)
                OVControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #启用有线网卡
        OVControl.wlan_enable(self,lan)
        #使无线网卡释放IP地址
        OVControl.dhcp_release_wlan(self,wlan)
        time.sleep(300)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(60)
        try:
            #获取master ap的下载流量
            result3 = OVControl.get_ap_downflow(self,mac)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top AP上没有找到该AP！"
            return "0MB",0



    #AP 上传流量统计的准确性---master ap
    def check_masterAP_upload_backup(self,ssid,password,wlan,lan,mac):
        #无线网卡连接master ap
        OVControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        OVControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = OVControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行上传
                tmp1 = subprocess.call("iperf3 -c %s -t180 -w5M"%d['iperf_ip'],shell=True)
                print tmp1
                break
            else:
                OVControl.wlan_enable(self,lan)
                OVControl.dhcp_release_wlan(self,wlan)
                OVControl.dhcp_wlan(self,wlan)
                OVControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #启用有线网卡
        OVControl.wlan_enable(self,lan)
        #使无线网卡释放IP地址
        OVControl.dhcp_release_wlan(self,wlan)
        time.sleep(300)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(60)
        try:
            #获取master ap的上传流量
            result3 = OVControl.get_ap_upflow(self,mac)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top AP上没有找到该AP！"
            return "0MB",0



    #AP 下载流量统计的准确性---slave ap
    def check_slaveAP_download_backup(self,ssid,password,wlan,lan,mac):
        #无线网卡连接master ap
        OVControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        OVControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = OVControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行下载
                tmp1 = subprocess.call("iperf3 -c %s -t180 -w5M -R"%d['iperf_ip'],shell=True)
                print tmp1
                break
            else:
                OVControl.wlan_enable(self,lan)
                OVControl.dhcp_release_wlan(self,wlan)
                OVControl.dhcp_wlan(self,wlan)
                OVControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #启用有线网卡
        OVControl.wlan_enable(self,lan)
        #使无线网卡释放IP地址
        OVControl.dhcp_release_wlan(self,wlan)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(6)
        #登录AP
        data_basic = data.data_basic()
        data_login = data.data_login()
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        time.sleep(300)
        try:
            #获取master ap的下载流量
            result3 = OVControl.get_ap_downflow(self,mac)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top AP上没有找到该AP！"
            return "0MB",0



    #AP 上传流量统计的准确性---slave ap
    def check_slaveAP_upload_backup(self,ssid,password,wlan,lan,mac):
        #无线网卡连接master ap
        OVControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        OVControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = OVControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行上传
                tmp1 = subprocess.call("iperf3 -c %s -t180 -w5M"%d['iperf_ip'],shell=True)
                print tmp1
                break
            else:
                OVControl.wlan_enable(self,lan)
                OVControl.dhcp_release_wlan(self,wlan)
                OVControl.dhcp_wlan(self,wlan)
                OVControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #启用有线网卡
        OVControl.wlan_enable(self,lan)
        #使无线网卡释放IP地址
        OVControl.dhcp_release_wlan(self,wlan)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(6)
        #登录AP
        data_basic = data.data_basic()
        data_login = data.data_login()
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        time.sleep(300)
        try:
            #获取master ap的上传流量
            result3 = OVControl.get_ap_upflow(self,mac)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top AP上没有找到该AP！"
            return "0MB",0


    #ssid 上传流量统计的准确性
    def check_ssid_upload(self):
        try:
            #获取ssid1,ssid2的下载流量
            result3_1 = OVControl.get_ssid1_up(self)
            result1_1 = result3_1.strip("MB").strip("KB").strip("B").strip("GB")
            result2_1 = int(float(result1_1))
            print result3_1,result2_1
            return result3_1,result2_1
        except:
            print u"在overview页面的Top ssid 上没有找到该ssid！"
            return "0MB",0

    #ssid 下载流量统计的准确性
    def check_ssid_download(self):
        try:
            #获取ssid1,ssid2的下载流量
            result3_1 = OVControl.get_ssid1_down(self)
            result1_1 = result3_1.strip("MB").strip("KB").strip("B").strip("GB")
            result2_1 = int(float(result1_1))
            print result3_1,result2_1
            return result3_1,result2_1
        except:
            print u"在overview页面的Top ssid 上没有找到该ssid！"
            return "0MB",0

    #client上传流量统计的准确性
    def check_client_upload(self):
        try:
            #获取client的下载流量
            result3 = OVControl.get_client_up(self)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top Clients 上没有找到该client！"
            return "0MB",0

    #client下载流量统计的准确性
    def check_client_download(self):
        try:
            #获取client的下载流量
            result3 = OVControl.get_client_down(self)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top Clients 上没有找到该client！"
            return "0MB",0



    #AP 下载/上传流量
    def set_AP_download_unload(self,ssid,password,wlan,lan):
        #无线网卡连接master ap
        OVControl.connect_DHCP_WPA_AP(self,ssid,password,wlan)
        #禁用有线网卡
        OVControl.wlan_disable(self,lan)
        i =0
        while i<3:
            tmp = OVControl.get_ping(self,d['iperf_ip'])
            if tmp == 0:
                #描述：使用iperf3进行下载
                tmp1 = subprocess.call("iperf3 -c %s -t180 -w5M -R"%d['iperf_ip'],shell=True)
                time.sleep(60)
                #描述：使用iperf3进行上传
                tmp2 = subprocess.call("iperf3 -c %s -t180 -w5M"%d['iperf_ip'],shell=True)
                print tmp1, tmp2
                break
            else:
                OVControl.wlan_enable(self,lan)
                OVControl.dhcp_release_wlan(self,wlan)
                OVControl.dhcp_wlan(self,wlan)
                OVControl.wlan_disable(self,lan)
                print "run iperf3 fail,try %s again!"%(i+1)
                i = i+1
                continue
        #启用有线网卡
        OVControl.wlan_enable(self,lan)
        #使无线网卡释放IP地址
        OVControl.dhcp_release_wlan(self,wlan)
        time.sleep(360)
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        time.sleep(60)

    #获取第一个ap下载流量
    def get_AP_download(self):
        try:
            #获取master ap的下载流量
            result3 = OVControl.get_master_down(self)
            result1 = result3.strip("MB").strip("KB").strip("B").strip("GB")
            result2 = int(float(result1))
            print result3,result2
            return result3,result2
        except:
            print u"在overview页面的Top AP上没有找到该AP！"
            return "0MB",0