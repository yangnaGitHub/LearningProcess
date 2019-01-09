#运行期检测到的错误被称为异常
#ZeroDivisionError
#NameError
#TypeError
#ValueError
#KeyboardInterrupt
#一个except子句可以同时处理多个异常,异常将被放在一个括号里成为一个元组
#最后一个except子句可以忽略异常的名称,被当作通配符使用
import sys

try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])#打印异常
    raise#异常抛出
#try except语句还有一个可选的else子句,必须放在所有的except子句之后,try子句没有发生任何异常的时候执行
for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except IOError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
#使用raise语句抛出一个指定的异常,raise唯一的一个参数指定了要被抛出的异常
#可以通过创建一个新的exception类来拥有自己的异常,异常应该继承自Exception类
class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
try:
    raise MyError(2*2)
except MyError as e:
    print('My exception occurred, value:', e.value)

#try语句还有另外一个可选的子句,定义了无论在任何情况下都会执行的清理行为
#不管try子句里面有没有发生异常,finally子句都会执行,如果except没有把异常截住,在finally中异常会再次被抛出

#预定义的清理行为
#关键词with语句就可以保证诸如文件之类的对象在使用完之后一定会正确的执行他的清理方法
with open("myfile.txt") as f:#文件总会关闭
    for line in f:
        print(line, end="")
