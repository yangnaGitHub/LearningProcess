# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:29:13 2018

@author: natasha1_Yang
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import time
import sys
import re
import math

def initwebdriver():
    global driver
    #PC USER AGENT
    user_agent = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_window_size(1280,2400)
    driver.get("http://aplm.asus.com")
    pagedeal = "document.getElementById('t_147-a').click();"
    driver.execute_script(pagedeal)
    time.sleep(2)

def exitprocess():
    driver.quit()

def GetContent(mode):
    content = driver.page_source
    tr = etree.HTML(content)
    result = tr.xpath(mode)
    return result, len(result)    

def GetModuleName():
    command = re.findall('^-[mMfF]{1,1}$', sys.argv[1])[0][-1].lower()
    module = sys.argv[2]
    module_name = []
    if 'm' == command:
        module_name.append(module.upper())
    if 'f' == command:
        with open(module, 'r') as f:
            for line in f.readlines():
                module_name.append(line.strip().upper())
    return module_name
    
def EnterProject(module_name):
    result, length = GetContent('//i[@class="z-bandbox-btn"]')
    for keys,values in result[0].attrib.items():
        if keys == 'id':
            btn_value = int(values.split('_')[1].split('-')[0])
            btn_index_id = values
            break
    
    resulttext, length = GetContent('//input[@class="z-textbox"]')
    text_index_id = '0' 
    for index in range(length):
        for keys,values in resulttext[index].attrib.items():
            if keys == 'id':
                text_value = int(values.split('_')[1].split('-')[0])
                #print index, values, text_value
                if text_value > btn_value:
                    text_index_id = values
                    text_search_id = 't_' + str(text_value + 1)
        if text_index_id != '0':
            break
    
    driver.find_element_by_id(btn_index_id).click()
    driver.find_element_by_id(text_index_id).send_keys(module_name)#enter project name
    driver.find_element_by_id(text_search_id).click()
    
    #verify
    time.sleep(2)
    result, length = GetContent('//div[contains(@class,"z-listcell-cnt")]')
    mb_index = -1
    for index in range(len(result)):
        #print result[index].attrib.get('id'), result[index].text
        if module_name == result[index].text:
            mb_index = index
            click_index_id = result[index].attrib.get('id')
            break
    
    if mb_index == -1:
        exit()
    
    driver.find_element_by_id(click_index_id).click()#click project

def SearchProject():
    result, length = GetContent('//button[@class="z-button-os"]')
    for index in range(len(result)):
        if 'Clear' == result[index].text:
            clear_id = result[index].attrib.get('id')
            commit_id = 't_' + str(int(clear_id.split('_')[1]) - 1)
            break
    
    driver.find_element_by_id(commit_id).click()#click search
    time.sleep(2)
    
def GetResult(module_name):
    #加页数
    result, length = GetContent('//div[@class="z-paging-info"]')
    pagecount = int(math.ceil(float(re.findall('/ \d*', result[0].text)[0][2:])/10))
    pagenextid = result[0].attrib.get('id').split('-')[0] + '-next'
    pagefirstid = result[0].attrib.get('id').split('-')[0] + '-first'
    #print "pagecount", pagecount
    formal_index = -1
    for page in range(pagecount):
        result, length = GetContent('//tr[contains(@class,"z-listitem")]')
        finallyres = result[0].xpath('//div[contains(@class,"z-listcell-cnt")]')
        for index in range(len(finallyres)):
            #print page, index, finallyres[index].text
            if index % 2 == 0:
                biosstring = finallyres[index].text
                formal_index = biosstring.find('Formal')
                if -1 != formal_index:
                    print "Formal Bios Version:", module_name, " ==> ", biosstring[formal_index + 12:formal_index + 16]
                    break
        if -1 != formal_index:
            break
        if page != pagecount - 1:
            driver.find_element_by_id(pagenextid).click()
            time.sleep(2)
        else:
            print "Formal Bios Version:", module_name, " ==> ", "None(Not found any formal BIOS, please check it by manual)"
    driver.find_element_by_id(pagefirstid).click()
    time.sleep(2)

def dealwebdriver(module_name):
    for module in module_name:
        EnterProject(module)
        SearchProject()
        GetResult(module)

if __name__ == "__main__":
    initwebdriver()
    dealwebdriver(GetModuleName())
    exitprocess()