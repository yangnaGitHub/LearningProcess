# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:17:10 2017

@author: natasha1_Yang
"""

def fun( arg1, arg2='default arg', *theRest ):
    print 'arg1: ', arg1
    print 'arg2: ', arg2
    for eachArgs in theRest:
        print 'other arg: ', eachArgs

fun( 'a' )
print '----'
fun( 'a', 'b' )
print '----'
fun( 'a', 'b', 'c', 'd' )

def fun( arg1, arg2='default arg', **theRest ):
    print 'arg1: ', arg1
    print 'arg2: ', arg2
    for eachArgs in theRest.keys():
        print 'other arg [%s]: %s' % ( eachArgs, str(theRest[eachArgs]))

fun( 'a' )
print '----'
fun( 'a', 'b' )
print '----'
fun( 'a', 'b', c='3', d='4' )
#从字典中提取某个参数
def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    
    
def fun( arg1, arg2='default arg', *theRest, **theRest1 ):
    print 'arg1: ', arg1
    print 'arg2: ', arg2
    for eachArgs in theRest:
        print 'other arg: ', eachArgs
    for eachArgs in theRest1.keys():
        print 'other arg [%s]: %s' % ( eachArgs, str(theRest1[eachArgs]) )

fun( 'a' )
print '1----'
fun( 'a', 'b' )
print '2----'
fun( 'a', 'b', c='3', d='4' )
print '3----'
fun( 'a', 'b', 'e', 'f', c='3', d='4' )
print '4----'
fun( 'a', 'b', *( 'e', 'f' ), **{ 'c' : '3', 'd' : '4' } )
print '5----'
aTuple = (6, 7, 8)
aDict = {'z' : 9}
fun( 'a', 'b', 'e', 'f', c='3', d='4', *aTuple, **aDict )


#匿名函数的关键字是 lambda
def true() : return True ==> lambda: True
def add( x, y ): return x + y ==> lambda x, y: x + y
def add( x, y = 2 ): return x + y ==> lambda x, y=2: x + y
def fun( *z ): return z ==> lambda: *z: z


#内建函数
filter( fun, seq ):seq 中的元素依次代入 fun 中,filter 返回使 fun 返回 True 的元素的序列
reduce( func, seq[, init] ):reduce 从 seq 的第一个元素起将里面的元素依次遍历
    若指定 init 参数则去 init 和 seq 的第一个元素
    将这两个元素代入 func,取 func 的返回值和 seq 的下一个元素
    reduce( ( lambda x, y: x + y ), [0, 1, 2, 3, 4] )求队列里数的总和
偏函数 partial,固定其某一(部分)参数而形成的新函数就是偏函数了
int2 = functiils.partial( int, base = 2 )

#获得类的名字
class Foo(object):  
    def get_cls_name( self ):  
        return self.__class__.__name__
        
#__file__ 这个变量可以获取到当前文件（包含这个代码的文件）的路径
#os.path.dirname()就是目录的上一级

s.strip(rm) ==> 删除s字符串中开头、结尾处，位于 rm删除序列的字符
s.lstrip(rm) ==> 删除s字符串中开头处，位于 rm删除序列的字符
s.rstrip(rm) ==> 删除s字符串中结尾处，位于 rm删除序列的字符
#当rm为空时，默认删除空白符
