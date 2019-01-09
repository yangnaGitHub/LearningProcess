#re.match尝试从字符串的起始位置匹配一个模式,如果不是起始位置匹配成功的话返回none
#re.match(pattern, string, flags=0)
#使用group(num),groups()匹配对象函数来获取匹配表达式
import re
line = "Cats are smarter than dogs"
matchObj = re.match(r"(.*) are (.*?) .*", line, re.M | re.I)
if matchObj:
    print(matchObj.group())
    print(matchObj.group(1))
    print(matchObj.group(2))

#re.search扫描整个字符串并返回第一个成功的匹配
#re.match只匹配字符串的开始,如果字符串开始不符合正则表达式匹配失败,re.search匹配整个字符串

#re.sub用于替换字符串中的匹配项
#re.sub(pattern, repl, string, count=0)count是模式匹配后替换的最大次数,0表示替换所有的匹配
phone = "177-5166-5173 # natasha_yang"
num = re.sub(r"#.*$", "", phone)
print(num)
num = re.sub(r"\D", "", phone)
print(num)

