# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 11:02:28 2018

@author: natasha1_Yang
"""

import datetime
import time
import re
import json
from copy import deepcopy
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import matplotlib.pyplot as plt #plt用于显示图片
import matplotlib.image as mpimg
#from PIL import Image
#img1=Image.open('QRFile.png')
#img1.show()
######看这儿#########
#操作流程
 #1>根据提示输入淘宝商品的url(演示,直接给定的url)
 #2>根据提示输入对应的商品ID号(不同类别,只要输入后面3位就可以)
 #3>拿出手机扫码登录(账号密码登录要验证,还没有搞定)

#那些还没有做
 #1>只做到下订单的操作
 #2>账号密码登录要拖动滑块操作,还不知道怎么弄
 #3>直接可以购买的页面测试,等待购买的页面还没有测试,只测试了天猫的,淘宝的还没有测试

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0"
}

#class CategoryValue:
#    def __init__(self, kindname, kindid, kindcheck):
#        self.kindname = kindname
#        self.kindid = kindid
#        self.kindcheck = kindcheck
#    def SetCheck(self, kindcheck):
#        self.kindcheck = kindcheck
#
#class CategoryInfo:
#    self.categoryvalue = []
#    def __init__(self, categoryname):
#        self.category = categoryname
#    def AddCategoryValue(self, categoryvalue):
#        self.categoryvalue.append(categoryvalue)
#
#class Category:
#    self.cetegoryinfo = []
#    def __init__(self, categoryinfo):
#        self.categoryinfo.append(catogoryinfo)

def initwebdriver():
    global driver
    user_agent = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_window_size(1280,2400) 

def exitprocess():
    driver.quit()
    
def GetContent(mode):
    content = driver.page_source
    tr = etree.HTML(content)
    result = tr.xpath(mode)
    return result

def GetParams():
#    global taobaoID
#    global taobaoPS
    global taobaoURL
#    taobaoID = raw_input('taobaoID:')
#    taobaoPS = raw_input('taobaoPS:')
    #taobaoURL = raw_input('taobaoURL:')
    taobaoURL = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.76583598T5Gesl&id=559825936395&areaId=320500&user_id=2675798390&cat_id=2&is_b=1&rn=4e13a49fc77f05a4efeb954792fbba43'
    driver.get(taobaoURL)
    WebDriverWait(driver, 5).until(lambda the_driver: the_driver.find_element_by_xpath('//ul[contains(@class,"J_TSaleProp")]'))

def GetGoodsInfo(content):
    Kinds = {}
    KindName = []
    KindsXpath = GetContent('//ul[contains(@class,"J_TSaleProp")]')
    if len(KindsXpath) == 0:
        return None, None
    for Kind in KindsXpath:
        KindName.append(Kind.attrib.get('data-property'))
    ReIdStrings = re.findall('data-value=\"[0-9]{2,}:[0-9]{2,}\"', content)
    KindsDes = {}
    IdType = ""
    KindsType = 0
    for IdString in ReIdStrings:
        IdString = IdString[IdString.find('"') + 1: -1]
        CurIdType = IdString[:IdString.find(':')]
        if IdType != CurIdType:
            IdType = CurIdType
            if KindsDes:
                Kinds[KindName[KindsType]] = deepcopy(KindsDes)
                KindsType += 1
                KindsDes.clear()
        SearchMode = '//ul[contains(@class,"J_TSaleProp")]/li[@data-value="%s"]/a/span' % IdString
        KindChoose = GetContent(SearchMode)[0].text#保存ID和TEXT
        #Notice!!!考虑是否有存货,对默认选中和用户选中都有意义
        KindsDes[KindChoose] = {IdString:False}#设置默认未选中
    Kinds[KindName[KindsType]] = KindsDes
    skuMap = re.findall('\"skuMap\":\{.*\},\"valLogin', content)[0]
    skuMap = '{' + skuMap[:skuMap.rfind(',')]
    skuMap = json.loads(skuMap).get('skuMap')
    return Kinds, skuMap

def GetWaitAndInfo():
    #0 输入URL
    #1 获取商品信息,就是商品可选
    #2 判断是否要等待
       # 需要等待就GET要等待的时间
       # 不需要等待就直接购买
    #3 返回值
       # 商品信息(是否可选,可选的种类) + 等待时间(不需要等待的时间为0)  
    #https://detail.tmall.com/item.htm?spm=a1z10.3754-b-s.w4949-17906149764.2.653e1dcdOXhTzB&id=564904157856
    Kinds, MixKinds = GetGoodsInfo(driver.page_source)
    CanBuy = False
    BuyLinks = GetContent('//div[contains(@class,"tb-btn-buy")]/a[@id="J_LinkBuy"]')
    if BuyLinks:
        for BuyLink in BuyLinks:
            if BuyLink.text == u'立即购买':
                CanBuy = True
    if CanBuy:
        return None, Kinds, MixKinds
    
    #需要等待,获取等待时间(需要测试)
    ResTime = []
    wait_hrefs = GetContent('//div[@class="tb-btn-wait"]')
    if wait_hrefs:
        for waitlink in wait_hrefs:
            if waitlink.text == u'即将开始 · · · ':
                wait_exist = True
                break
    if wait_exist:
        timesset = GetContent('//div[@class="tm-countdown-timer"]')
        if timesset:
            searchModes = [u'(.*?)天', u'(.*?)小时', u'(.*?)分']
            for timeset in timesset:
                for index in range(len(searchModes)):
                    Count = re.findall(searchModes[index], timeset.text)
                    if Count:
                        Count = int(Count[0])
                        ResTime.append(Count)
                        if index < (len(searchModes) - 1):
                            searchModes[index + 1] = searchModes[index][-1] + searchModes[index + 1]
                    else:
                        ResTime.append(0)
                break
    if ResTime:
        return ResTime, Kinds, MixKinds
    else:
        return None, Kinds, MixKinds
    
    return None, None, None

def GetWaitTime(ResTime):
    if ResTime is None:
        return None
    time_now = datetime.datetime.now()
    finally_time = time_now + datetime.timedelta(days=ResTime[0]) + datetime.timedelta(hours=ResTime[1]) + datetime.timedelta(minutes=ResTime[2])
    finally_time = finally_time - datetime.timedelta(seconds=time_now.second)
    print finally_time.strftime("%Y-%m-%d %H:%M:%S")
    return finally_time

def CmdChoose(Kinds):
    Count = 1
    for KindKey, KindValue in Kinds.items():
        MaxNameLen = 0
        printstringheader = u'类名'
        printstringbody = ''
        for KindName, KindId in KindValue.items():
            MaxNameLen = max(MaxNameLen, len(KindName))
            printstringbody += KindKey + ' ' + KindName + ' ' + KindId.keys()[0] + '\n'
        for index in range(len(KindKey) - len(u'类名') + 1):
            printstringheader += u' '
        printstringheader += u'类别'
        for index in range(MaxNameLen - len(u'类别') + 1):
            printstringheader += u' '
        printstringheader += u'ID'
        print printstringheader
        print printstringbody
        ChooseId = raw_input('InputGoodsID:')#用户输入
        #只输入后面3位的更新Check
        Kinds[KindKey].values()[0].update(map(lambda index:{index:index[-3:]==ChooseId}, [index for index in [Goods.keys()[0] for Goods in Kinds[KindKey].values()]])[0])
        
    return Count    

def CustomChoose(Kinds, MixKinds, overstock=False):
    #等待用户选择 提供给前端,前端处理返回每一类的ID号,这边直接CMD输出ID
    #"skuMap":
    #   {";20509:28314;1627207:3883690;":{"price":"997.00","priceCent":99700,"skuId":"3650068754841","stock":855},
    #   ";20509:28315;1627207:3883690;":{"price":"997.00","priceCent":99700,"skuId":"3650068754842","stock":855},
    #   ";20509:28316;1627207:3883690;":{"price":"997.00","priceCent":99700,"skuId":"3650068754843","stock":754},
    #   ";20509:28317;1627207:3883690;":{"price":"997.00","priceCent":99700,"skuId":"3661494135844","stock":703}}
    #前端处理输出
    ChooseGoodsInfo = {}
    Count = 1
    #ChooseStart = datetime.datetime.now()
    while not overstock:
        Count = CmdChoose(Kinds)
        
        SearchSkuIds = []
        for KindKey, KindValue in Kinds.items():
            for KindName, KindId in KindValue.items():
                if KindId.values()[0] == True:
                    SearchSkuIds.append(KindId.keys()[0])
                    break
        if not SearchSkuIds:
            continue
        for skuKey, skuValue in MixKinds.items():
            if False not in (map(lambda index: index in skuKey, [SearchSkuId for SearchSkuId in SearchSkuIds])):
                ChooseGoodsInfo[skuKey] = skuValue#返回给用户
                for infoname, infovalue in skuValue.items():
                    print infoname, infovalue
                    if (infoname == 'stock') and (infovalue < Count):
                        ChooseGoodsInfo.clear()
                        print "overstock!!!"
                        overstock = True
                        break
                break
        if ChooseGoodsInfo:
            break
        
    return ChooseGoodsInfo, Count

#提前3分钟登录
def SetWait(finally_time):
    if finally_time is None:
        return None
    prepare_time = finally_time - datetime.timedelta(minutes=3)
    time.sleep((prepare_time - datetime.datetime.now()).seconds)

#淘宝登录
def TaobaoLogin(taobaoID='defaultUser', taobaoPS='defaultPs'):
    results = GetContent('//a[@class="sn-login"]')
    if results:
        for result in results:
            if result.text == u'请登录':
                driver.find_element_by_class_name('sn-login').click()
                break
    WebDriverWait(driver, 2).until(lambda the_driver: the_driver.find_element_by_xpath('//iframe[@id="J_loginIframe"]'))
    results = GetContent('//iframe[@id="J_loginIframe"]')
    if results:
        login_form_src = [result.attrib.get('src') for result in results][0]
    driver.get('https:' + login_form_src)
    WebDriverWait(driver, 2).until(lambda the_driver: the_driver.find_element_by_xpath('//a[contains(@class,"J_Quick2Static")]'))
    #用户账号密码登录
#    switchs = GetContent('//div[contains(@class, "module-static")]')
#    results = GetContent('//a[contains(@class,"J_Quick2Static")]')
#    if (len(switchs) == 0) and results:
#        for result in results:
#            if result.text == u'密码登录':
#                driver.find_element_by_class_name('J_Quick2Static').click()
#                break
#    driver.find_element_by_xpath('//input[@id="TPL_username_1"]').send_keys(taobaoID)
#    driver.find_element_by_xpath('//input[@id="TPL_password_1"]').send_keys(taobaoPS)
    #Verify拖动条
#    if GetContent('//span[contains(@class,"btn_slide")]'):
#        btn_slide = driver.find_element_by_xpath('//span[contains(@class,"btn_slide")]')
#        btn_slide = driver.find_element_by_xpath('//div[@id="nc_1_n1t"]')
#        
#        action = ActionChains(driver)
#        action.click_and_hold(btn_slide).move_to_element_with_offset(btn_slide, 256, 0).release().perform()
    #提交账户密码
#    driver.find_element_by_id('J_SubmitStatic').click()
    
    #扫码登录
    print u"拿出手机淘宝扫码登录"
    switchs = GetContent('//div[contains(@class, "module-quick")]')
    if not switchs:
        driver.find_element_by_xpath('//i[@id="J_Static2Quick"]').click()#切换到扫码登录
    while True:
        if GetContent('//div[contains(@class,"qrcode-login-error")]'):
            print u"QRCode过期"
            driver.find_element_by_xpath('//a[contains(@class,"J_QRCodeRefresh")]').click()
            WebDriverWait(driver, 2).until(lambda the_driver: the_driver.find_element_by_xpath('//div[@id="J_QRCodeImg"]/img'))
        #保存QRCode
        VerifyAddr = 'http:' + GetContent('//div[@id="J_QRCodeImg"]/img')[0].attrib.get('src')
        session = requests.session()
        QRCode = session.get(VerifyAddr, headers = headers, verify = False)
        with open('QRFile.png', "wb") as QRCodeFile:
            QRCodeFile.write(QRCode.content)
        im = mpimg.imread('QRFile.png')
        plt.imshow(im)
        plt.axis('off')#不显示坐标轴
        plt.show()
        #等用户扫码登录购买界面
        timercount = 120
        while timercount:
            time.sleep(1)
            if GetContent('//ul[contains(@class,"J_TSaleProp")]'):
                break
            timercount -= 1
        if GetContent('//ul[contains(@class,"J_TSaleProp")]'):
                break
#下订单,支付
def BuyGoods(ChooseGoodsInfo, taobaoCount, finally_time):
    if ChooseGoodsInfo is None:
        return None
    GoodsId = ChooseGoodsInfo.keys()[0][1:-1].split(';')
    for Goods in GoodsId:
        SearchMode = '//ul[contains(@class,"J_TSaleProp")]/li[@data-value="%s"]/a' % Goods
        driver.find_element_by_xpath(SearchMode).click()
    if taobaoCount > 1:
        results = GetContent('//input[contains(@class,"mui-amount-input")]')
        if [link.attrib.get('title') == u'请输入购买量' for link in results][0]:
            driver.find_element_by_class_name('mui-amount-input').send_keys(taobaoCount)
    if finally_time is not None:
        while (datetime.datetime.now() - finally_time).seconds < 0:
            pass
    
    BuyLinks = GetContent('//div[contains(@class,"tb-btn-buy")]/a[@id="J_LinkBuy"]')
    if BuyLinks:
        if [link.text == u'立即购买' for link in BuyLinks][0]:
            print u"立即购买"
            driver.find_element_by_xpath('//div[contains(@class,"tb-btn-buy")]/a[@id="J_LinkBuy"]').click()#按下立即购买
#    time.sleep(2)
#    print "SLEEP"
    WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath('//h2[@class="buy-th-title"]'))
    if GetContent('//h2[@class="buy-th-title"]')[0].text == u'确认订单信息':
        if GetContent('//a[@class="go-btn"]')[0].text == u'提交订单':
            print u"提交订单"
            driver.find_element_by_xpath('//a[@class="go-btn"]').click()
    WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath('//div[@class="sixDigitPassword"]'))
    #div/sixDigitPassword支付
    
if __name__ == '__main__':
    try:
        initwebdriver()
        GetParams()
        ResTime, Kinds, MixKinds = GetWaitAndInfo()
        finally_time = GetWaitTime(ResTime)
        ChooseGoodsInfo, Count = CustomChoose(Kinds, MixKinds)
        SetWait(finally_time)
        TaobaoLogin()#taobaoID, taobaoPS
        BuyGoods(ChooseGoodsInfo, Count, finally_time)
    except Exception, Arguments:
        print "Error:", Arguments
    finally:
        exitprocess()