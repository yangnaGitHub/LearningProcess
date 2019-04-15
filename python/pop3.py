#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Python内置一个poplib模块，实现了POP3协议，可以直接用来收邮件
#POP3协议收取的不是一个已经可以阅读的邮件本身，而是邮件的原始文本
#第一步：用poplib把邮件的原始文本下载到本地
#第二部：用email解析原始文本，还原为邮件对象
import poplib
email = input("Email: ")
password = input("Password: ")
pop3_server = input("POP3 server: ")

