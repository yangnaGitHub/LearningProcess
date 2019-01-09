#!/usr/bin/python3
#单字符在Python中作为一个字符串使用
#对已存在的字符串进行修改,并赋值给另一个变量就是对字符串的修改
#\v==>纵向制表符
#\t==>横向制表符
#\r==>回车
#\f==>换页

#%==>格式化字符串
print("my name is %s, and %d years old!" % ("natasha", 22))
#同C语言格式化处理是一致的
#%p==>十六进制格式化变量的地址
#*==>定义宽度或者小数点精度
#-==>左对齐
#+==>在正数前面添加正号
#<sp>==>在正数前面显示空格
##==>在八进制前面显示0,在十六进制前面显示0x或是0X
#0==>显示数字前面填充的0,而不是空格
#%==>输出一个单一的%
#(var)==>映射变量(字典参数)
#m.n==>m是显示的最小总宽度,n是小数点后的位数

#三引号
#当需要一块HTML或者是SQL时,使用三引号

#inner函数
#capitalize()==>将字符串的第一个字符转换为大写
#center(width, fillchar)==>返回一个指定的宽度width居中的字符串,fillchar为填充的字符,默认为空格
#count(str, beg= 0,end=len(string))==>返回str在string里面出现的次数,如果beg或者end指定则返回指定范围内str出现的次数
#decode(encoding='UTF-8',errors='strict')==>使用指定编码来解码字符串,默认编码为字符串编码
#encode(encoding='UTF-8',errors='strict')==>以encoding指定的编码格式编码字符串,如果出错默认报一个ValueError 的异常,除非errors指定的是'ignore'或者'replace'
#expandtabs(tabsize=8)==>把字符串string中的tab符号转为空格,tab符号默认的空格数是8
#find(str, beg=0 end=len(string))==>检测str是否包含在字符串string中,如果beg和end指定范围,则检查是否包含在指定范围内,如果是返回开始的索引值,否则返回-1
#endswith(suffix, beg=0, end=len(string))==>检查字符串是否以obj结束,如果beg或者end指定则检查指定的范围内是否以obj结束
#详情见string_inner
