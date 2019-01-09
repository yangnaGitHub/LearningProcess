#模块可以被别的程序引入
import sys#引入某一模块的方法

for index in sys.argv :#包含命令行参数的列表
    print(index)
print(sys.path)#自动查找所需模块的路径的列表
#一个模块只会被导入一次
#模块名.__name__==>模块块

#from语句让你从模块中导入一个指定的部分到当前命名空间中
#所有内容全都导入到当前的命名空间from modname import *
#模块除了方法定义,可以包括可执行的代码,一般用来初始化这个模块,只有在第一次被导入时才会被执行
#一个模块被另一个程序第一次引入时,主程序将运行
#想在模块被引入时,某一程序块不执行,可以用__name__属性来使该程序块仅在该模块自身运行时执行
#模块都有一个__name__属性,其值是'__main__'时,表明该模块自身在运行
if __name__ == "__main__" :
    print("自身 run")
else :
    print("Others run")
#dir()可以找到模块内定义的所有名称
print(dir(sys))
#winreg这个模块就只会提供给Windows系统
#模块sys内置在每一个 Python 解析器中,sys.ps1和sys.ps2定义了主提示符和副提示符所对应的字符串
#print(sys.ps1)
#print(sys.ps2)
#sys.ps1 = "==> "
#管理Python模块命名空间的形式,点模块名称,模块的名称是A.B,表示一个包A中的子模块B
#目录只有包含一个叫做__init__.py的文件才会被认作是一个包,这个文件中也可以包含一些初始化代码或者为__all__变量赋值
#导入子模块:mod:sound.effects.echo,import sound.effects.echo使用全名去访问
#from sound.effects import echo使用echo来使用
#包定义文件__init__.py存在一个叫做__all__的列表变量,在使用 from package import * 的时候就把这个列表中的所有名字作为包内容导入
#__all__ = ["echo", "surround", "reverse"],表示当使用from sound.effects import *这种用法时,只会导入包里面这三个子模块
#__path__目录列表
