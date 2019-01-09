#函数代码块以def关键词开头,函数内容以冒号起始,不带return表达式的相当于返回 None
#所有参数(变量)都是按引用传递
#参数类型
#必需参数
#关键字参数,函数调用使用关键字参数来确定传入的参数值,使用关键字参数允许函数调用时参数的顺序与声明时不一致
def printinfo(name, age) :
    print("name ==>", name)
    print("age ==>", age)
    return
printinfo(age = 22, name = "natasha")
#默认参数
def printinfo1(name, age, sex = "female") :
    print("name ==>", name)
    print("age ==>", age)
    print("sex ==>", sex)
    return
printinfo1(name = "natasha", age = 22)
#不定长参数,加了星号(*)的变量名会存放所有未命名的变量参数,在函数调用时没有指定参数就是一个空元组
def printinfo2(name, *vartuple) :
    print(name)
    for var in vartuple :
        print(var)
    return
printinfo2("natasha", 22, "female")

#匿名函数
#使用lambda来创建匿名函数,lambda只是一个表达式,lambda函数拥有自己的命名空间,不能访问自有参数列表之外或全局命名空间里的参数
#不等同于C或C++的内联函数(不占用栈内存从而增加运行效率)
#lambda [arg1 [,arg2,.....argn]]:expression
mysum = lambda before, after : before + after
print(mysum(10, 20))
