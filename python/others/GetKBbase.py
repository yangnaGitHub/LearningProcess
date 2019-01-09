# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 09:35:06 2018

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import os
import xml.etree.ElementTree as ET

class TreeNode:
    def __init__(self, child):
        self.semantic = child.find('semantic').text
        self.answer = child.find('answer').text
        self.childNode = []
        self.child = child
        self.dealchild()
    
    def dealchild(self):
        for node in self.child.findall('./tree/qa'):
            self.insertchindNode(node)
    
    def insertchindNode(self, Node):
        self.childNode.append(TreeNode(Node))
    
class KBdes:
    def __init__(self, xmltype, sheetname, child, myid):
        self.xmltype = xmltype
        self.sheetname = sheetname
        self.id = myid
        self.parseXml(child)
        self.quest = set()
        self.quest_length = 0
    
    def parseXml(self, child):
        if child is None:
            return
        if 'FAQ' == self.xmltype:
            self.semantic = child.find('semantic').text
            self.answer = child.find('answer').text
        elif 'TREE' == self.xmltype:
            self.semantic = child.find('semantic').text
            self.treeNode = TreeNode(child)
        elif 'LINE' == self.xmltype:
            pass

    def setquests(self, questlists):
        for quest in questlists:
            if quest.startswith('[EXPECT]'):
                continue
            else:
                self.quest.add(quest)
        self.quest_length = len(self.quest)
        
    def addquest(self, quest):
        self.quest.add(str(quest).strip())

    def getid(self):
        return self.id
    
    def getquests(self, splitindex=-1, len_limit=5):
        self.quest_length = len(self.quest)
        if self.quest_length >= len_limit:
            questlists = list(self.quest)
            return questlists[:splitindex], questlists[splitindex:]
        return None, None

def getRootconf(Path='NoPath'):
    if 'NoPath' == Path:
        print('[getRootconf]:Path error[%s]' % Path)
        return None
    
    with open(Path, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            if line.startswith('personalKB = '):
                rootConf = line.split('=')[1].strip().split(',')
                break
    return rootConf

def GetKBbase(rootConf, Path='NoPath', Export_Path='NoPath', IDstart=10000):
    if ('NoPath' == Path) or ('NoPath' == Export_Path):
        print('[getTestcase]:Path error[%s][%s]' % (Path, Export_Path))
        return None
    if  rootConf is None:
        print('[GetKBbase]:rootConf none')
        return None
    
    #GetAllXml limited by rootConf
    fullpaths = {}
    for dirpath, dirnames, filenames in os.walk(Path):
        for file in filenames:
            if file.endswith('.xml'):
                fullpath = os.path.join(dirpath, file).replace('\\', '/')
                if fullpath[fullpath.rfind('IVR'):] in rootConf:
                    fullpaths[dirpath[dirpath.rfind('IVR'):]] = os.path.join(dirpath, file)
    
    #Construct Kbdes
    #fullpath = 'E:\\linuxshare\\IVR_engine\\data\\IVR\\YLerqi\\在线支付\\zaixianzhifu\\tree\\zaixianzhifutree.xml'
    #fullpath = 'E:\linuxshare\IVR_engine\data\IVR\YLerqi\在线支付\zaixianzhifu\FAQ\zaixianzhifuFAQ.xml'
    KBbase = {}
    findmode = {'FAQ':'qa', 'TREE':'./tree/qa', 'LINE':'scenario'}
    for dirpath, fullpath in fullpaths.items():
        #fullpath = 'E:\\linuxshare\\IVR_engine\\data\\IVR\\YLerqi\\在线支付\\zaixianzhifu\\Line\\zaixianzhifuLine.xml'
        tree = ET.parse(fullpath)
        xmltype = tree.getroot().get('type').upper()
        
        for child in tree.getroot().findall(findmode[xmltype]):
            if 'LINE' == xmltype:
                KBbase[child.get('name')] = KBdes(xmltype, dirpath, child, IDstart)
            else:
                KBbase[child.find('semantic').text] = KBdes(xmltype, dirpath, child, IDstart)
            IDstart += 1
    with open(Export_Path, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            line = line.split('\t')
            if line[0] not in KBbase:
                KBbase[line[0]] = KBdes('FAQ', 'UNKNOW', None, IDstart)
            
#        with open(fullpath, 'r', encoding='utf-8') as fd:
#            recusiveCount = 0
#            string = ''
#            content = ''
#            for line in fd.readlines():
#                if line.startswith('<scml'):
#                    startpos = line[line.find('type'):].find('"')
#                    endpos = line[startpos+1:].find('"')
#                    xmltype = line[startpos+1: endpos]
#                if -1 != line.find('</scml>'):
#                    break
#                if -1 != line.find('<qa>'):
#                    recusiveCount = (recusiveCount << 1) + 1
#                    string = string + line
#                if -1 != line.find('</qa>'):
#                    string = string + line
#                    recusiveCount = (recusiveCount >> 1)
#                if (1 == recusiveCount) and ('' == content):
#                    if -1 != line.find('<semantic>'):
#                        startpos_sem = line.find('<semantic>') + len('<semantic>')
#                        endpos_sem = line.find('</semantic>')
#                        content = line[startpos_sem:endpos_sem]
#                if (0 == recusiveCount) and ('' != string):
#                    KBbase[content] = KBdes(xmltype, dirpath, string)
#                    KBbase[content].setid(IDstart)
#                    IDstart += 1
#                    string = ''
#                    content = ''
    return KBbase, IDstart

def getTestcase(KBbase, Path='NoPath'):
    if 'NoPath' == Path:
        print('[getTestcase]:Path error[%s]' % Path)
        return None
    if  KBbase is None:
        print('[getTestcase]:KBbase none')
        return None
    unKnowquest = []
    with open(Path, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            findKB = False
            if -1 != line.find('[EXPECT]'):
                questlists = line.split('\t')
                for quest in questlists:
                    if quest in KBbase:
                        findKB = True
                        KBbase[quest].setquests(questlists)
                        break
                if False == findKB:
                    unKnowquest.append(questlists)
    return unKnowquest

def getOutresult(KBbase, Path='NoPath', Export_Path='NoPath'):
    if ('NoPath' == Path) or ('NoPath' == Export_Path):
        print('[getTestcase]:Path error[%s][%s]' % (Path, Export_Path))
        return None
    if  KBbase is None:
        print('[getTestcase]:KBbase none')
        return None
    unKnowquest = []
    with open(Path, 'r', encoding='utf-8') as fd:
        nextskip = False
        for line in fd.readlines():
            if nextskip:
                nextskip = False
                continue
            if -1 != line.find('==测试报告=='):
                break
            line = line.split('\t')
            if line[0].startswith('[FAILED]'):
                nextskip = True
                unKnowquest.append(line[1])
                continue
            if len(line) < 2:
                print('line:', line)
                continue
            
            content = line[1]
            findKB = False
            while True:
                startpos = content.find('semantic')
                if -1 != startpos:
                    content = content[startpos+len('semantic":[{"'):]
                else:
                    break
                
                endpos = content.find('":"')
                if -1 != endpos:
                    tmpcontent = content[:endpos]
                    content = content[endpos:]
                else:
                    break
                if tmpcontent in KBbase:
                    findKB = True
                    KBbase[tmpcontent].addquest(line[0])
                    break
            if not findKB:
                unKnowquest.append([line[0], tmpcontent])

    with open(Export_Path, 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            line = line.split('\t')
            for quest in line:
                KBbase[line[0]].addquest(quest)
            
    return unKnowquest
    
def summaryKBbase(KBbase, unKnowquest, Path='NoPath', split_word='\t', multi_split_word='#&#&#'):
    if 'NoPath' == Path:
        print('[summaryKBbase]:Path error[%s]' % Path)
        return None
    if  KBbase is None:
        print('[summaryKBbase]:KBbase none')
        return None
    with open(Path, 'w', encoding='utf-8') as fd:
        for content, value in KBbase.items():
            string = str(value.getid()) + split_word + content + split_word
            trains, tests = value.getquests(splitindex=-1, len_limit=2)
            if trains is not None:
                for train in trains:
                    string += (train + multi_split_word)
                string = string[:string.rfind(multi_split_word)] + split_word
                for test in tests:
                    string += (test + multi_split_word)
                string = string[:-len(multi_split_word)]
                fd.write(string + '\n')
    summarydir, summaryname = os.path.split(Path)
    unKnowsummary = summarydir + '\\unKnowsummary.txt'
    with open(unKnowsummary, 'w', encoding='utf-8') as fd:
        for quest in unKnowquest:
            fd.write(str(quest) + '\n')

if __name__ == '__main__':
    File_Path = 'E:\\linuxshare\\IVR_engine\\data'
    IVR_Path = File_Path + '\\IVR'
    Export_Path = File_Path + '\\exportOther.txt'
    rootConf = getRootconf(File_Path + '\\root.conf')
    KBbase, IDstart = GetKBbase(rootConf, IVR_Path, Export_Path)
    unKnowquest = getOutresult(KBbase, File_Path+ '\\out.txt', Export_Path)#getTestcase(KBbase, File_Path+ '\\test_二期.txt')
    summaryKBbase(KBbase, unKnowquest, File_Path+'\\summary.txt')