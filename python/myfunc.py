#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#函数参数:
# 必选参数
# 默认参数
# 可变参数
# 关键参数
# 命名关键参数
def my_abs(val):
    if val >= 0:
        return val
    else:
        return -val

print(my_abs(-1))

#Null function
#pass可以用来当作占位符
def nop():
	pass
#数据类型检查可以用内置函数isinstance()实现
def abs1(val):
	if not isinstance(val, (int, float)):
		raise TypeError("bad operand type")
	if val >= 0:
		return val
	else:
		return -val
print(abs1(-1))
#多值返回的返回值是一个tuple
import math
def move(xp, yp, step, angle = 0):
	nx = xp + step * math.cos(angle)
	ny = yp + step * math.sin(angle)
	return nx, ny
mx, my = move(100, 100, 60, math.pi / 6)
print(mx, " ", my)
All = move(100, 100, 60, math.pi / 6)
print(All)

def second(sec, fir, zer):
	diff = math.sqrt((fir * fir) - (4 * sec * zer))
	val1 = -fir + diff
	val2 = -fir - diff
	val1 = val1 / (2 * sec)
	val2 = val2 / (2 * sec)
	return val1, val2
Val = second(2, 3, 1)
print(Val)

#可以使用默认参数、可变参数和关键字参数
#一是必选参数在前，默认参数在后
#把变化大的参数放前面，变化小的参数放后面
def power(val, count = 2):
	mysum = 1;
	while count > 0:
		count = count -1
		mysum = mysum * val
	return mysum
print(power(5), " ", power(5, 3))

def enroll(name, gender, age = 6, city = "beijing"):
	print("name = %s gender = %s age = %d city = %s" % (name, gender, age, city))

enroll("yangna", "M", city = "sichuan")	

#定义默认参数要牢记一点：默认参数必须指向不变对象
def add_end(List = []):
	List.append("END")
	return List
print(add_end())
print(add_end())
#str、None这样的不变对象,不变对象一旦创建，对象内部的数据就不能修改，这样就减少了由于修改数据导致的错误
def add_end_0(List = None):
	if List is None:
		List = []
	List.append("END")
	return List
print(add_end_0(), " ", add_end_0())
#可变参数就是传入的参数个数是可变的
def calc(Sets):
	mysum = 0
	for index in Sets:
		mysum = mysum + index * index
	return mysum
#List
print("[1, 2, 3] = ", calc([1, 2, 3]))
#tuple
print("(1, 2, 3, 4) = ", calc((1, 2, 3, 4)))
def calccha(*many):
	mysum = 0
	for index in many:
		mysum = mysum + index * index
	return mysum
print("1, 2 = ", calccha(1, 2))
print("Null = ", calccha())
List = [2, 3, 4]
print("[2, 3, 4] = ", calccha(*List))

#关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    print('name: ', name, "age: ", age)
    print("other: ", kw)

print(person("natasha", 21))
print(person("nancy", 19, city = "liuzhou"))
print(person("twilight", 45, city = "anshun", gender = "M"))
para = {"city": "suzhou", "job": "engineer"}
print(person("natasha", 21, **para))#kw获得extra的一份拷贝

def manyper(name, age, **kw):
    if "city" in kw:
        print("city addition")
    if "job" in kw:
        print("job addition")
    print('name: ', name, "age: ", age)
    print("other: ", kw)
para = {"city": "suzhou", "job": "engineer"}
print(person("natasha", 21, **para))#kw获得extra的一份拷贝

#限制的关键字参数,*是分割符
def limperson(name, age, *, city, job):
    print('name: ', name, "age: ", age)
    print("city: ", city, "job: ", job)

#print(person("twilight", 45, "anshun", "engineer"))==>error
print(person("twilight", 45, city = "anshun", job = "engineer"))

#参数混合
def mix(a, b = 1, *args, **kw):
    print("a = ", a, "b = ", b, "args = ", args, "kw = ", kw)
print(mix(1, 2))
print(mix(1, 2, "a", "b"))
print(mix(1, 2, "a", "b", kwargs = 3))
args = (1, 2, 3)
kw = {"kw1": 100, "kw2": "yang"}
print(mix(*args, **kw))
args = (1, 2, 3, 4)
kw = {"kw1": 100, "kw2": "yang"}
print(mix(*args, **kw))
#小结
#默认参数一定要用不可变对象，如果是可变对象，程序运行时会有逻辑错误！
#*args是可变参数，args接收的是一个tuple
#**kw是关键字参数，kw接收的是一个dict
#可变参数既可以直接传入：func(1, 2, 3)，又可以先组装list或tuple，再通过*args传入
#关键字参数既可以直接传入：func(a=1, b=2)，又可以先组装dict，再通过**kw传入
#命名的关键字参数是为了限制调用者可以传入的参数名，同时可以提供默认值
#定义命名的关键字参数不要忘了写分隔符*，否则定义的将是位置参数
