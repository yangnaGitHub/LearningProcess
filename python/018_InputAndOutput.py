#文件对象的write()方法,标准输出文件可以用sys.stdout引用
#使用str.format()函数来格式化输出值
#字符串对象的rjust()方法,将字符串靠右在左边填充空格(ljust()和center())
#zfill()会在数字的左边填充0
#str.format()括号及其里面的字符(称作格式化字段)将会被format()中的参数替换
import math
import pickle, pprint
print('{}网址："{}!"'.format('菜鸟教程','www.runoob.com'))
#在括号中的数字用于指向传入对象在format()中的位置
print('{0}和{1}'.format('Google','Runoob'))
print('{1}和{0}'.format('Google','Runoob'))
#在format()中使用了关键字参数,它们的值会指向使用该名字的参数
print('{name}网址：{site}'.format(name='菜鸟教程',site='www.runoob.com'))
#'!a'(使用ascii()),'!s'(使用str())和'!r'(使用repr())可以用于在格式化某个值之前对其进行转化
print('常量PI的值近似为：{!r}.'.format(math.pi))
print('常量PI的值近似为{0:.3f}.'.format(math.pi))
table={'Google':1,'Runoob':2,'Taobao':3}
for name,number in table.items():
    print('{0:10}==>{1:10d}'.format(name,number))
print('Runoob:{0[Runoob]:d};Google:{0[Google]:d};Taobao:{0[Taobao]:d}'.format(table))
print('Runoob:{Runoob:d};Google:{Google:d};Taobao:{Taobao:d}'.format(**table))
#%操作符也可以实现字符串格式化,作为类似sprintf()式的格式化字符串

#input可以接收一个Python表达式作为输入

#open(filename,mode)将会返回一个file对象
#read(size)将读取一定数目的数据,作为字符串或字节对象返回,size被忽略了或者为负,那么该文件的所有内容都将被读取并且返回
#readline()会从文件中读取单独的一行,换行符为'\n',f.readline()如果返回一个空字符串,说明已经已经读取到最后一行
#readlines()将返回该文件中包含的所有行,设置可选参数sizehint,则读取指定长度的字节,并且将这些字节按行分割
#迭代一个文件对象然后读取每行
#write(string)将string写入到文件中,然后返回写入的字符数,要写入一些不是字符串的东西,那么将需要先进行转换
#tell()返回文件对象当前所处的位置
#seek(offset,from_what)改变文件当前的位置
#close()

#pickle模块实现了基本的数据序列和反序列化
#pickle模块的序列化操作能够将程序中运行的对象信息永久存储到文件中去
#pickle模块的反序列化操作能够从文件中创建上一次程序保存的对象
#pickle.dump(obj, file, [,protocol])
#使用pickle模块将数据对象保存到文件
data1 = {'a' : [1, 2.0, 3, 4 + 6j],
         'b' : ("string", u"unicode string"),
         'c' : None}
selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)
output = open("018_testdata.pkl", "wb")
pickle.dump(data1, output)
pickle.dump(selfref_list, output, -1)
output.close()
#使用pickle模块从文件中重构Python对象
pkl_file = open("018_testdata.pkl", "rb")
data1 = pickle.load(pkl_file)
pprint.pprint(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)

pkl_file.close()

