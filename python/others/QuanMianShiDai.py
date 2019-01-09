# -*- coding: utf-8 -*-
"""
Created on Mon May 14 09:34:34 2018

@author: Administrator
"""

import os
import pandas as pd
import numpy as np
import jieba
import random
import re

def Change_Workdir(workpath='E:\AboutStudy\code\python'):
    if not os.path.exists(workpath):
        os.makedirs(workpath)
    if os.getcwd() != workpath:
        os.chdir(workpath)

def Get_Tests_Dict(filename='quanmian_ol_chat_record.sql'):
    datasources = []
    lines = []
    with open(filename, encoding='utf8', mode='r+') as fd:
        skiprow = 0
        for line in fd.readlines():
            if 0 == skiprow:
                skiprow = -1
                continue
            start = line.find(line.split(',')[7])
            end = line.find('\'', start+2) if -1 != start else -1
            if -1 != end:
                lines = line[end:]
                line = line[:start] + line[start:end].replace(',', '\t') + lines
            datasources.append(line.strip('\n').split(', '))
    return datasources

def GetChatindex(datasources):
    ChatIdMap = {}
    vaildIndexs = []
    vaildIndexsall = []
    diffChatid = []
    for datasource in datasources:
        if datasource[2] in ChatIdMap:
            ChatIdMap[datasource[2]] += 1
        else:
            ChatIdMap[datasource[2]] = 1
    if ChatIdMap:
        sortlists = sorted(list(ChatIdMap.values()), reverse=True)
        startChatid = sortlists[5000]
        diffChatcount = 5000 - [1 if sortlist > startChatid else 0 for sortlist in sortlists].count(1)
    for index, chatid in enumerate(ChatIdMap.keys()):
        if (index < diffChatcount) and (startChatid-1 == ChatIdMap[chatid]) and (random.random() > 0.5):
            diffChatid.append(chatid)
        if index == diffChatcount:
            break
    for index, datasource in enumerate(datasources):
        if ChatIdMap[datasource[2]] > 10:
            vaildIndexsall.append(index)
        if ChatIdMap[datasource[2]] > startChatid:
            vaildIndexs.append(index)
        else:
            if datasource[2] in diffChatid:
                vaildIndexs.append(index)
                
    return vaildIndexs, vaildIndexsall

special_list = ['?', '？', '，', '.', '。', '、', ';', '：', '!', 'ˉ', '∶', ':', '"', '`', '·', '…', '—', '～', '-', '〃', '‘', '’', '“', '”', '〝', '〞', ' ', '\t']
def GetChatContent(datasources, vaildIndexsall):
    ChatContent = []
    UserDict = []
    for vaildIndex in vaildIndexs:
        line = datasources[vaildIndex][7]
        count = 0
        while True:
            startpos = line.find('<', 0)
            endpos = line.find('>', 0)
            count += 1
            if count > 5:
                break
            if (-1 == startpos) or (-1 == endpos):
                break
            if 0 == startpos:
                tmpline = line[endpos+1:]
            else:
                tmpline = line[0:startpos] + line[endpos+1:]
            line = tmpline
        cutdicts = list(jieba.cut(line, cut_all = False))
        for cutdict in cutdicts:
            if (cutdict not in UserDict) and (cutdict not in special_list):
                UserDict.append(cutdict)
        #UserDict.append(cutdict)
        ChatContent.append(line)

replacelists = ['天猫', '淘宝', '全棉时代', '棉柔巾', '朋友圈', '棉巾', '尿布', '沙尿裤', '尿裤', '棉制品', '毛巾', '联通', '面膜',
                '京东', '苏宁', '奈丝', '棉纤维', '梳棉机', '微软', '卫生巾', '比奈丝', '隔尿裤', '旺旺', '百度', '电信', '顺丰', '移动', '花王',
                '隔尿垫', '营业执照', '七度空间', '税务', '连体服', '汇通', '棉服', '猎豹', '地方', '明珠', '苹果电脑', '内衣', '尿不湿',
                '欣园', '浴袍', '棉线', '棉粉', '无纺布', '伊藤春熙', '卫生棉', '内裤', '手提袋', '化妆棉', '棉布', '枕头', '枕套', '秋冬',
                '邮政', '速递', '望京', '春熙' '伊藤', '洋华堂', '加微', '联通', '移动', '电信', '纸尿裤', '棉尿裤', '比丝诺', '罗森',
                '莘庄仲盛店', '中通', '韵达', '黄冈', '申通', '泉林本色', '三星', '隔奶巾', '棉之春', '银耳', '海藻', '面尿裤', '沐浴露',
                '惠氏', '卷巾', '丰园', '佳运', '柔巾纸', '润滑油', '订单号', '帐号',
                '帮宝适', '白玉堂', '宜信', '卓越', '合生汇', '锦华', '科全', '微信', '支付宝',
                '罗斯福', '恒隆', '顺丰', '百利威', '银泰', '微博', '博主', '电话', '热线', '面柔巾', '国瑞城', 
                '星河', '盛世', '棉棉', '丽莎', '登记证', '银行', '账号', '被子']
Context = []
ContextAll = []
def replacedata(datasources, vaildIndexs, vaildIndexsall):
    #处理数据
    dealdata = []
    for index, vaildIndex in enumerate(vaildIndexsall):
        line = datasources[vaildIndex][7]
        count = 0
        while True:
            startpos = line.find('<', 0)
            endpos = line.find('>', 0)
            if (-1 == startpos) or (-1 == endpos):
                break
            count += 1
            if count > 7:
                break
            if 0 == startpos:
                tmpline = line[endpos+1:]
            else:
                tmpline = line[0:startpos] + line[endpos+1:]
            line = tmpline
        dealdata.append(line.strip('\'').strip('\r').strip('\n'))
    oldChatid = ''
    for index, vaildIndex in enumerate(vaildIndexsall):
        line = dealdata[index]
        tmpline = ''
        Chatid = datasources[vaildIndex][2]
        
        replacestr = re.findall(r'http://(.*)?.html', line)
        if replacestr:
            for sreplace in replacestr:
                line = line.replace('http://' + sreplace, '555555')#身份证号没有深度判断
        replacestr = re.findall(r'\d{13}', line)#订单
        if replacestr:
            for sreplace in replacestr:
                line = line.replace(sreplace, '111111')#身份证号没有深度判断
        if replacestr:
            line = line.replace(replacestr[0], '222222')#电话号码
        replacestr = re.findall(r'\d{11}', line)
        if replacestr:
            line = line.replace(replacestr[0], '333333')#
        replacestr = re.findall(r'\d{18}', line)
        if replacestr:
            line = line.replace(replacestr[0], '444444')#身份证号没有深度判断
        replacestr = re.findall(r'<img(.*)?>', line)
        if replacestr:
            for sreplace in replacestr:
                line = line.replace('<img' + sreplace + '>', '666666')#身份证号没有深度判断
        
        if 0 == (index % 10000):
            print(index)
        for replacedict in replacelists:
            if replacedict in line:
                line = line.replace(replacedict, ('词典%d' % replacelists.index(replacedict)))
        if oldChatid != Chatid:
            if oldChatid == '':
                tmpline = ('%s:\n' % Chatid.strip('\''))
            else:
                tmpline = ('\n%s:\n' % Chatid.strip('\''))
            oldChatid = Chatid
        line = tmpline + ('%s: ' % datasources[vaildIndex][3].strip('\'')) + line.strip('\r').strip('\n')
        if vaildIndex in vaildIndexs:
            Context.append(line)
        ContextAll.append(line)
    return Context, ContextAll

def WriteDictFile(filename, listdict):
    with open(filename, encoding='utf8', mode='w+') as fd:
        for words in listdict:
            fd.write(words + '\n')
    
if __name__ == '__main__':
    Change_Workdir()
    datasources = Get_Tests_Dict()
    vaildIndexs, vaildIndexsall = GetChatindex(datasources)
    vaild, vaildall = replacedata(datasources, vaildIndexs, vaildIndexsall)
    WriteDictFile('5000.txt', vaild)
    WriteDictFile('大于10.txt', vaildall)
    WriteDictFile('词典.txt', replacelists)
    WriteDictFile('5000.txt', Context)
    WriteDictFile('大于10.txt', ContextAll)
    WriteDictFile('词典.txt', replacelists)