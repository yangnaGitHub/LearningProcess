# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:54:52 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#加密轮盘
 #加密轮盘分为内圈和外圈,内圈是密钥,外圈是待加密的信息
 #外圈上带黑点的A对应内圈字母的编号就是密钥的号码
 #The secret password is Rosebud
  #密钥是8
 #Bpm amkzmb xiaaewzl qa Zwamjcl

def encode(t_str, code_num=8):
    mydict = {}
    for index in range(ord('A'), ord('Z')+1, 1):
        end_index = index+code_num
        if end_index > ord('Z'):
            end_index -= 26
        mydict[chr(index)] = chr(end_index)
    result = ''
    for s_str in t_str:
        if ' ' == s_str:
            result += ' '
            continue
        if s_str.islower():
            result += mydict[s_str.upper()].lower()
            continue
        result += mydict[s_str]
    return result

#相反的过程
def decode(t_str, code_num=8):
    mydict = {}
    for index in range(ord('A'), ord('Z')+1, 1):
        end_index = index-code_num
        if end_index < ord('A'):
            end_index += 26
        mydict[chr(index)] = chr(end_index)
    result = ''
    for s_str in t_str:
        if ' ' == s_str:
            result += ' '
            continue
        if s_str.islower():
            result += mydict[s_str.upper()].lower()
            continue
        result += mydict[s_str]
    return result

if __name__ == '__main__':
    t_str = 'The secret password is Rosebud'
    e_str = encode(t_str)
    print(e_str)
    print(decode(e_str))