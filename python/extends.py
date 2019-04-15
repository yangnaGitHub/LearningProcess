#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
class Animal(object):
    def run(self):
        print("Running")

class Dog(Animal):
    pass
class Cat(Animal):
    pass
dog = Dog()
dog.run()
cat = Cat()
cat.run()
class Dog1(Animal):
    def run(self):
        print("Dog is running")

class Cat1(Animal):
    def run(self):
        print("Cat is running")

dog = Dog1()
dog.run()
cat = Cat1()
cat.run()

def run_oth(animal):
    animal.run()
run_oth(Animal())
run_oth(Dog1())
run_oth(Cat1())
#type
print(type(123))
print(type(abs))
import types
print(type(abs) == types.BuiltinFunctionType)
print(isinstance(dog, Animal))
#要获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list
print(dir("ABC"))
#__xxx__的属性和方法在Python中都是有特殊用途的，比如__len__方法返回长度
class MyDog(object):
    def __len__(self):
        return 100
dog = MyDog()
print(len(dog))
#getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态
class MyObject(object):
    def __init__(self):
        self.x = 9
    def power(self):
        return self.x * self.x
obj = MyObject()
print(hasattr(obj, "x"), hasattr(obj, "y"))
setattr(obj, "y", 19)
print(hasattr(obj, "y"), getattr(obj, "y"))
fn = getattr(obj, "power")
print(fn())
#Python是动态语言，根据类创建的实例可以任意绑定属性
#给实例绑定属性对另外的实例并不起作用,而给class绑定属性将对所有的实例起作用
class Student(object):
    def __init__(self, name):
        self.name = name
s = Student("natasha")
s.score = 90
print(s.score, s.name);
def set_age(self, age):
    self.age = age
from types import MethodType
s.set_age = MethodType(set_age, s)
s.set_age(21)
print(s.age)
#给class绑定属性
def set_score(self, score):
    self.score = score
Student.set_score = MethodType(set_score, Student)
s1 = Student("yangna")
s1.set_score(99)
print(s1.score, s1.name)
#限制实例的属性,定义一个特殊的__slots__变量，来限制该class实例能添加的属性
class student(object):
    __slots__ = ("name", "age")#只允许定义name和age属性
#__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
class student(object):
    def get_score(self):
        return self._score
    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be an integer")
        if value < 0 or value > 100:
            raise ValueError("score must between 0 ~ 100")
        self._score = value
s = student();
s.set_score(80)
print(s.get_score())
#Python内置的@property装饰器就是负责把一个方法变成属性调用的
class student(object):
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be an integer")
        if value < 0 or value > 100:
            raise ValueError("score must between 0 ~ 100")
        self._score = value
s = student()
s.score = 70
print(s.score)
class Animal(object):
    pass
class Mammal(Animal):
    pass
class Bird(Animal):
    pass
class Runnable(object):
    def run(self):
        print("Running")
class Flyable(object):
    def fly(self):
        print("Flying")
class Dog(Mammal, Runnable):
    pass
class Bat(Mammal, Flyable):
    pass
#MixIn的目的就是给一个类增加多个功能,优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系
#编写一个多进程模式的TCP服务
#class MyTCPServer(TCPServer, ForkingMixIn):
#    pass
#编写一个多线程模式的UDP服务
#class MyUDPServer(UDPServer, ThreadingMixIn):
#    pass
#直接显示变量调用的不是__str__()，而是__repr__()，两者的区别是__str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的。
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Student object (name : %s)" % self.name
    __repr__ = __str__
print(Student("natasha"))
#如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，该方法返回一个迭代对象
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1
    def __iter__(self):
        return self# 实例本身就是迭代对象，故返回自己
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100000:
            raise StopIteration();
        return self.a
for n in Fib():
    print(n)
#像list那样按照下标取出元素，需要实现__getitem__()方法
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
f = Fib()
print(f[0], f[1], f[2])
print(list(range(100))[5:10])
#与之对应的是__setitem__()方法，把对象视作list或dict来对集合赋值。最后，还有一个__delitem__()方法，用于删除某个元素。
#利用完全动态的__getattr__，我们可以写出一个链式调用
class Chain(object):
    def __init__(self, path = ""):
        self._path = path
    def __getattr__(self, path):
        return Chain("%s %s" % (self._path, path))
    def __str__(self):
        return self._path

    __repr__ = __str__
#定义一个__call__()方法，就可以直接对实例进行调用
class student(object):
    def __init__(self, name):
        self.name = name
    def __call__(self):
        print("Name is %s" % self.name)
s = student("natasha")
s()
#__call__()还可以定义参数。对实例进行直接调用就好比对一个函数进行调用一样
#需要判断一个对象是否能被调用，能被调用的对象就是一个Callable对象
from enum import Enum
Month = Enum("Month", ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))
for name, member in Month.__members__.items():
    print(name, "==>", member, ",", member.value)
#value属性则是自动赋给成员的int常量，默认从1开始计数
from enum import Enum, unique
@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
#@unique装饰器可以帮助我们检查保证没有重复值
day1 = Weekday.Mon
print(day1)
print(Weekday["Wed"])
print(Weekday.Tue.value)
#动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的
class Hello(object):
    def hello(self, name = "world"):
        print("hello, %s" % name)
#type()函数既可以返回一个对象的类型，又可以创建出新的类型
def fn(self, name = "world"):
    print("hello, %s" % name)
Hello = type("Hello", (object,), dict(hello = fn))
print(type(Hello))
#type()函数依次传入3个参数
#class的名称
#继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法
#class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上
#除了使用type()动态创建类以外，要控制类的创建行为，还可以使用metaclass
#metaclass，直译为元类
#(创建类)先定义metaclass，然后创建类
#metaclass允许你创建类或者修改类。换句话说，你可以把类看成是metaclass创建出来的“实例”
#按照默认习惯，metaclass的类名总是以Metaclass结尾，以便清楚地表示这是一个metaclass
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs["add"] = lambda self, value: self.append(value)#method
        return type.__new__(cls, name, bases, attrs)
class MyList(list, metaclass = ListMetaclass):
    pass
#传入关键字参数metaclass时，魔术就生效了，它指示Python解释器在创建MyList时，要通过ListMetaclass.__new__()来创建
#__new__()方法接收到的参数依次是
#当前准备创建的类的对象
#类的名字
#类继承的父类集合
#类的方法集合
L = MyList()
L.add(1)
print(L)
#需要通过metaclass修改类定义的。ORM就是一个典型的例子
#ORM全称“Object Relational Mapping”，即对象-关系映射，就是把关系数据库的一行映射为一个对象，也就是一个类对应一个表，这样，写代码更简单，不用直接操作SQL语句
#编写一个ORM框架，所有的类都只能动态定义，因为只有使用者才能根据表的结构定义出对应的类来
#定义Field类，它负责保存数据库表的字段名和字段类型
class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return "<%s : %s>" % (self.__class__.__name__, self.name)
#定义各种类型的Field，比如StringField，IntegerField
class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, "varchar(100)")
class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, "bigint")
#ModelMetaclass
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        print("Found Model: %s" % name)
        mapping = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print("Found mapping: %s ==> %s" % (k, v))
                mapping[k] = v
        for k in mapping.keys():
            attrs.pop(k)
        attrs["__mapping__"] = mapping
        attrs["__table__"] = name
        return type.__new__(cls, name, bases, attrs)
#Model
class Model(dict, metaclass = ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("Model object has no Attribute %s" % key)
    def __setattr__(self, key, value):
        self[key] = value
    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mapping__.items():
            fields.append(v.name)
            params.append("?")
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) values (%s)" % (self.__table__, ",".join(fields), ",".join(params))
        print("SQL: %s" % sql)
        print("ARGS: %s" % str(args))
class User(Model):
    id = IntegerField("id")
    name = StringField("username")
    email = StringField("email")
    password = StringField("password")
u = User(id = 12345, name = "natasha", email = "natasha1_yang@asus.com", password = "1234")
u.save()
