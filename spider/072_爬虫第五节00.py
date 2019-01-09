# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:32:41 2017

@author: natasha1_Yang
"""

#from lxml import etree
import selenium
import re

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Charset':'utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Connection': 'keep-alive'
    }
    
if __name__ == "__main__":
    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.customHeaders.{}".format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.setttings.userAgent"] = \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
    
    jd_item_url = "https://item.jd.com/3659174.html"
    item_id = re.findall("/\d{7}.html", jd_item_url)[0][1:8]
    driver = webdriver.PhantomJS(service_args=["--ignore-ssl-errors = true"])
    driver.set_window_size(1280, 2400)
    driver.get(jd_item_url)
    #driver.execute_script('window.scrollTo(0, (document.body.scrollHeight))')
    #driver.save_screenshot('screen.png') # save a screenshot to disk
    max_try = 2
    num_try = 0
    while num_try < max_try:
        try:
            element = driver.find_element_by_class_name("comment-percent")
            print element.find_element_by_tag_name("strong").text
            price_element = driver.find_element_by_class_name("J-p-%s"%(item_id))
            print re.findall("\d.*", price_element.get_attribute('innerHTML'))[0]
            break
        except selenium.common.exceptions.NoSuchElementException, Arguments:
            num_try += 1
            print Arguments
    
    print "items:"
    for url in re.findall('href="//item.jd.com/\d{7}.html"', driver.page_source):
        print url
    print "\n\nlists:"
    for url in re.findall('href="//list.jd.com/list.html*\d{3, 9}"', driver.page_source):
        print url
    driver.quit()
                                                