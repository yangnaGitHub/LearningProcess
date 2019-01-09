# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:09:55 2017

@author: natasha1_Yang
"""

import requests
from bs4 import BeautifulSoup
import sys
import csv

if __name__ == "__main__":
    url_main = "http://su.lianjia.com/"
    f = open(u"苏州二手房20170124.csv", "wb")
    f.write('\xEF\xBB\xBF')#文件头
    writer = csv.writer(f)

    writer.writerow(["区域", "小区名称", "户型", "面积", "价格(万)", "单价(元/平米)", "地址", "朝向", "装修", "楼层", "年代"])
    res = requests.get("http://su.lianjia.com/ershoufang")
    res = res.text.encode(res.encoding).decode("utf-8")
    soup = BeautifulSoup(res, "html.parser")
    #print soup.prettify()
    districts = soup.find(name="div", attrs={'class':'item-list'})
    #遍历每个地区,每个district是一个地区
    for district in districts.find_all(name='a'):
        district_name = district.text#区域
        url = '%s%s' % (url_main, district["href"])
        #url = "http://su.lianjia.com/ershoufang/gaoxin1"
        res = requests.get(url)
        res = res.text.encode(res.encoding).decode("utf-8")
        soup = BeautifulSoup(res, "html.parser")
        
        #每个地区有多少页total_page
        pages = soup.find(name="div", attrs={"class":"page-box house-lst-page-box"})#翻页处的class,计算有多少页
#        if not page:#没有房源
#            continue
        #total_page = dict(eval(page["page-data"]))["totalPage"]
        total_page = 0;
        for page in pages.find_all(name='a'):
            total_page = max(total_page, int((page["href"].split('/'))[3][1:]))
        
        #遍历每个地区的每一页
        for index in range(1, total_page + 1):
            url_page = "%s/d%d" % (url, index)#http://su.lianjia.com/ershoufang/gaoxin1/d2
            res = requests.get(url_page)
            res = res.text.encode(res.encoding).decode("utf-8")
            soup = BeautifulSoup(res, "html.parser")
            
            #Get每一页的房源信息详细页的链接selectDetail
            sells = soup.find(name="ul", attrs={"class":"house-lst"})
            for sell in sells.find_all(name="li"):
                DivselectDetail = sell.find(name="div", attrs={"class":"pic-panel"})
                selectDetail = DivselectDetail.find(name="a")
                urlselectDetail = "%s%s" % (url_main, selectDetail["href"].strip('/'))#http://su.lianjia.com/ershoufang/su4184121.html
                res = requests.get(urlselectDetail)
                res = res.text.encode(res.encoding).decode("utf-8")
                soup = BeautifulSoup(res, "html.parser")
                #获得价格price_all,房型room_all,面积area_all其他的信息TableValue
                price = soup.find(name="div", attrs={"class":"mainInfo bold"})
                price_all = price.text.strip('\n')
                room = soup.find(name="div", attrs={"class":"room"})
                room_all = room.text.strip('\n')
                area = soup.find(name="div", attrs={"class":"area"})
                area_all = area.text.strip('\n')
                others = soup.find(name="table", attrs={"class":"aroundInfo hideAnswerFast"})
                infromations = [u"小区", u"单价", u"地址", u"朝向", u"装修", u"楼层", u"年代", u"首付", u"月供"]
                TableValue = {}
                for other in others.find_all(name="tr"):
                    for td in other.find_all(name="td"):
                        infromation = td.text.replace(' ', '').replace('\n', '').replace('\t', '').split(u'\uff1a')
                        if infromation[0] in infromations:
                            TableValue[infromation[0]] = infromation[1]
                #将每个Item写到文件中
                #GetAllData==>WriteToFile
                #"区域", "小区名称", "户型", "面积", "价格(万)", "单价(元/平米)", "地址", "朝向", "装修", "楼层", "年代"
                Mylist = [district_name, TableValue[infromations[0]], room_all, area_all, price_all, TableValue[infromations[1]], TableValue[infromations[2]], TableValue[infromations[3]], TableValue[infromations[4]], TableValue[infromations[5]], TableValue[infromations[6]]]
                for test in range(11):#unicode==>utf-8
                    Mylist[test] = Mylist[test].encode("utf-8")
                writer.writerow(Mylist)
                #print district_name, TableValue[infromations[0]], room_all, area_all, price_all, TableValue[infromations[1]], TableValue[infromations[2]], TableValue[infromations[3]], TableValue[infromations[4]], TableValue[infromations[5]], TableValue[infromations[6]]
                #break#每个Item的终止
            #break#页的终止
        #break#地区的终止
    f.close()