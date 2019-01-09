#!/usr/bin/python3
#变量不需要声明,但在使用前都必须赋值,赋值后的变量才会被创建
#变量就是变量,没有类型(变量所指的内存中对象的类型)
counter = 100
miles = 1000.0
name = "natasha"

print(counter)
print(miles)
print(name)

#多个变量赋值,通过赋值指向不同类型的对象
a = b = c = 1#3个变量被分配到相同的内存空间(引用)
a, b, c = 1, 2, "natasha"#多个对象同时指定多个变量

#标准的数据类型
#Number==>数字
#String==>字符串
#List==>列表[]
#Tuple==>元组()
#Sets==>集合{}
#Dictionary==>字典{}
#type()函数可以用来查询变量所指的对象类型
a, b, c, d = 20, 5.5, True, 4 + 3j
print(type(a), type(b), type(c), type(d))

#可以使用del语句来删除一些对象引用(单个或是多个)

#数值运算
#+ - * /(除法,得到浮点数) //(除法,得到整数) %(取余) **(乘方)

#字符串
#字符串截取语法格式==>变量[头下标:尾下标]
#index从0开始,-1为从末尾开始的位置
#+字符串的连接,*赋值当前字符串(紧跟数值为赋值的次数)
str = "natasha1_yang"
print(str)
print(str[0:-1])
print(str[0])
print(str[2:9])
print(str[2:])
print(str * 2)
print(str + "@asus.com")

#反斜杠(\)代表转义字符和多行,如果不想转义,就在字串前面加r或R,同时...可以跨越多行
#字符串不能被改变

####List
#可以包含各种数据类型,包括自身(List)
#方括号[]之间,用逗号分隔的元素列表
#可以被索引和截取(截取格式和字符串一致),截取后返回一个包含所需元素的新列表
soulist = ["abcd", 786, 2.23, "natasha", 70.2]
tinylist = [123, "yang"]
print(soulist)
print(soulist[0])
print(soulist[2:])
print(tinylist * 2)
print(soulist + tinylist)
#列表中的元素是可变的
a = [1, 2, 3, 4, 5]
a[0] = 6
a[2:5] = []#删除
print(a)

####Tuple
#和List一样,只是不能修改元素
#元组写在小括号()中,并用逗号分隔开
#和List的操作一样
tinytuple = (123, "natasha")
print(tinytuple)
#可以把字符串看着一种特殊的元组
#tuple元素不可变,但可以包含可变的对象(list等对象)
#tup1 = ()
#tup2 = (20, )
#string,list,tuple都属于sequence(序列)

####Set
#无序不重复元素的序列
#进行成员关系测试和删除重复元素
#使用{}或是set()函数创建集合,创建一个空集合必须用set()而不是{},{}是用来创建一个空字典
student = {"Tom", "Zain", "Tracy", "Natasha", "Cubi", "Odin", "Alan", "Tom"}
print(student)#自动删除重复的元素
#成员测试
if("Natasha" in student) :
    print("Natasha is Student")
else :
    print("Natasha is not Student")
#可进行集合运算
a = set("abcdefghijk")
b = set("abdefgklmn")
print(a)
print(a - b)#a和b的差集
print(a | b)#a和b的并集
print(a & b)#a和b的交集
print(a ^ b)#a和b中不同时存在的元素

####Dictionary
#内置数据类型
#列表是有序的对象结合,字典是无序的对象结合,字典当中的元素是通过键来存取,而不是通过[偏移存取
#是一种映射类型,用{}标识,是一个无序的Key:Value对集合
#在同一个字典中,Key是唯一的
mydict = {}
mydict["one"] = "natasha"
mydict[2] = "tracy"
tinydict = {"name":"natasha", "age":22, "sex":"female", "nation":"china"}
print(mydict["one"])
print(mydict[2])
print(tinydict)
print(tinydict.keys())
print(tinydict.values())
print({x: x ** 2 for x in (2, 4, 5)})#x取2, 4, 5然后value是x ** 2(x的平方)
print(dict(natasha = 1, tracy = 2))
#关键字是不可变类型,且不能重复
#创建空字典使用{}

####数据转换
#int(x[, base])==>将x转换为一个整数
#float(x)==>将x转换到一个浮点数
#complex(real[, imag])==>创建一个复数
#str(x)==>将对象 x 转换为字符串
#repr(x)==>将对象 x 转换为表达式字符串
#eval(str)==>用来计算在字符串中的有效Python表达式,并返回一个对象
#tuple(s)==>将序列 s 转换为一个元组
#list(s)==>将序列 s 转换为一个列表
#set(s)==>转换为可变集合
#dict(s)==>创建一个字典。d 必须是一个序列 (key,value)元组。
#frozenset(s)==>转换为不可变集合
#chr(x)==>将一个整数转换为一个字符
#unichr(x)==>将一个整数转换为Unicode字符
#ord(x)==>将一个字符转换为它的整数值
#hex(x)==>将一个整数转换为一个十六进制字符串
#oct(x)==>将一个整数转换为一个八进制字符串
