#time和calendar模块可以用于格式化日期和时间
#时间间隔是以秒为单位的浮点小数
#时间戳都以自从1970年1月1日午夜经过了多长时间来表示
#time.time()用于获取当前时间戳
import time
ticks=time.time()
print("当前时间戳为:",ticks)
#用一个元组装起来的9组数字处理时间
#返回浮点数的时间辍方式向时间元组转换,将浮点数传递给如localtime之类的函数
localtime=time.localtime(ticks)
print("本地时间为:",localtime)
#根据需求选取各种格式,最简单的获取可读的时间模式的函数是asctime()
localtime=time.asctime(localtime)
print("本地时间为:",localtime)
#strftime方法来格式化日期time.strftime(format[,t])
#格式化成2016-03-20 11:45:39形式
print(time.strftime("%Y-%m-%d%H:%M:%S",time.localtime()))
#格式化成Sat Mar 28 22:24:24 2016形式
print(time.strftime("%a %b %d %H:%M:%S %Y",time.localtime()))
#将格式字符串转换为时间戳
a="Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y")))
