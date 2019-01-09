#os模块提供了不少与操作系统相关联的函数
#shutil针对日常的文件和目录管理任务

#glob模块提供了一个函数用于从目录通配符搜索中生成文件列表
import glob
print(glob.glob('*.py'))

#re模块为高级字符串处理提供了正则表达式工具
import re
print(re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest'))
print(re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat'))

#math模块为浮点运算提供了对底层C函数库的访问

#urllib.request用于处理从urls接收的数据
#smtplib用于发送电子邮件

#datetime模块为日期和时间处理同时提供了简单和复杂的方法
from datetime import date
now = date.today()
print(now)
print(now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B."))
birthday = date(1994, 5, 12)
age = now - birthday
print(age.days)

#模块直接支持通用的数据打包和压缩格式zlib,gzip,bz2,zipfile,tarfile
import zlib
s = b'witch which has which witches wrist watch'
t = zlib.compress(s)
print(len(s), len(t))
print(zlib.decompress(t))
print(zlib.crc32(s))

#timeit度量工具

#doctest扫描模块并根据程序中内嵌的文档字符串执行测试
def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>>print(average([20, 30, 70]))
    40.0
    """
    return sum(values) / len(values)
#import doctest
#doctest.testmod()
#unittest模块,可以在一个独立的文件里提供一个更全面的测试集
