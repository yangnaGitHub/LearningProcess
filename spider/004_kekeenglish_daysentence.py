# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:18:16 2018

@author: Administrator
"""

import re
from lxml import etree
import urllib.request
import xlwt

response=urllib.request.urlopen('http://www.kekenet.com/kouyu/primary/chuji/')
html = response.read().decode("utf-8")
tr = etree.HTML(html)
#//div[@class="tb-btn-wait"]
#//ul[contains(@class,"J_TSaleProp")]
#//div[contains(@class,"tb-btn-buy")]/a[@id="J_LinkBuy"]
#contents = tr.xpath('//ul[@id="menu-list"]/li')

contents = tr.xpath('//div[@class="page th"]/a')
total_pages = 0
for content in contents:
    total_pages = max(total_pages, int(content.text))

book = xlwt.Workbook()
sheet = book.add_sheet('translation')
row = 0

contentTexts = {}
errorRecords = {}

for page in range(total_pages, 0, -1):
    if total_pages != page:
        response=urllib.request.urlopen('http://www.kekenet.com/kouyu/primary/chuji/List_%d.shtml' % page)
        html = response.read().decode("utf-8")
        tr = etree.HTML(html)

    allTests = tr.xpath("//text()")#所有的文本
    contents = tr.xpath('//ul[@id="menu-list"]/li/h2/a')
    prepareTexts = []
    for content in contents:
        prepareTexts.append(content.text)
    for index, allTest in enumerate(allTests):
        if allTest in prepareTexts:
            needText = allTests[index + 3].replace('\n', '').replace('，', ',').replace('。', '.')
            if re.findall('^[a-zA-Z]', needText):
                pass
            else:
                needText = allTests[index + 2].replace('\n', '').replace('，', ',').replace('。', '.')
            try:
                slicePos = needText.find(re.findall('[\u2E80-\u9FFF]+', needText)[0])
                contentTexts[needText[:slicePos].replace('\n', '')] = needText[slicePos:].replace('\n', '').replace('，', ',').replace('。', '.')
                firstStr = needText[:slicePos].replace('\n', '')
                secondStr = needText[slicePos:].replace('\n', '').replace('，', ',').replace('。', '.')
            except IndexError:
                print('find error (%d %d %d: %s)' % (page, index, row+1, allTest))
                errorRecords[str(page) + str(index) + str(row+1)] = allTests
                firstStr = ''
                secondStr = ''
            sheet.write(row, 0, firstStr)
            sheet.write(row, 1, secondStr)
            row += 1
            
book.save('translation.xlsx')

