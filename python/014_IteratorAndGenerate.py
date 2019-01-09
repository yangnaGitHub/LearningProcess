#迭代是访问集合元素的一种方式,可以记住遍历的位置的对象,迭代器只能往前不会后退
#两个基本的方法:iter()和next()
#字符串,列表或元组对象都可用于创建迭代器
import sys

mylist = [1, 2, 3, 4]
it = iter(mylist)
print(next(it))
print(next(it))
for index in it :
    print(index, end = " ")

#listtest1 = [1, 2, 3, 4, 5]
#ittest1 = iter(listtest1)
#while True :
#    try :
#        print(next(ittest1))
#    except StopIteration :
#        sys.exit()
#使用了yield的函数被称为生成器
#生成器是一个返回迭代器的函数,只能用于迭代操作
#遇到yield时函数会暂停并保存当前所有的运行信息,返回yield的值,并在下一次执行next()方法时从当前位置继续运行
def fibonacci(n) : #生成器函数
    a, b, counter = 0, 1, 0
    while True :
        if (counter > n) :
            return
        yield a
        a, b = b, a + b
        counter += 1

f = fibonacci(10)#是一个迭代器,有生成器返回生成
while True :
    try :
        print(next(f), end = " ")
    except StopIteration :
        sys.exit()
