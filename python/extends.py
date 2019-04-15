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
#Ҫ���һ��������������Ժͷ���������ʹ��dir()������������һ�������ַ�����list
print(dir("ABC"))
#__xxx__�����Ժͷ�����Python�ж�����������;�ģ�����__len__�������س���
class MyDog(object):
    def __len__(self):
        return 100
dog = MyDog()
print(len(dog))
#getattr()��setattr()�Լ�hasattr()�����ǿ���ֱ�Ӳ���һ�������״̬
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
#Python�Ƕ�̬���ԣ������ഴ����ʵ���������������
#��ʵ�������Զ������ʵ������������,����class�����Խ������е�ʵ��������
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
#��class������
def set_score(self, score):
    self.score = score
Student.set_score = MethodType(set_score, Student)
s1 = Student("yangna")
s1.set_score(99)
print(s1.score, s1.name)
#����ʵ��������,����һ�������__slots__�����������Ƹ�classʵ������ӵ�����
class student(object):
    __slots__ = ("name", "age")#ֻ������name��age����
#__slots__��������Խ��Ե�ǰ��ʵ�������ã��Լ̳е������ǲ������õ�
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
#Python���õ�@propertyװ�������Ǹ����һ������������Ե��õ�
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
#MixIn��Ŀ�ľ��Ǹ�һ�������Ӷ������,���ȿ���ͨ�����ؼ̳�����϶��MixIn�Ĺ��ܣ���������ƶ��εĸ��ӵļ̳й�ϵ
#��дһ�������ģʽ��TCP����
#class MyTCPServer(TCPServer, ForkingMixIn):
#    pass
#��дһ�����߳�ģʽ��UDP����
#class MyUDPServer(UDPServer, ThreadingMixIn):
#    pass
#ֱ����ʾ�������õĲ���__str__()������__repr__()�����ߵ�������__str__()�����û��������ַ�������__repr__()���س��򿪷��߿������ַ�����Ҳ����˵��__repr__()��Ϊ���Է���ġ�
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Student object (name : %s)" % self.name
    __repr__ = __str__
print(Student("natasha"))
#���һ�����뱻����for ... inѭ��������list��tuple�������ͱ���ʵ��һ��__iter__()�������÷�������һ����������
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1
    def __iter__(self):
        return self# ʵ��������ǵ������󣬹ʷ����Լ�
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100000:
            raise StopIteration();
        return self.a
for n in Fib():
    print(n)
#��list���������±�ȡ��Ԫ�أ���Ҫʵ��__getitem__()����
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
f = Fib()
print(f[0], f[1], f[2])
print(list(range(100))[5:10])
#��֮��Ӧ����__setitem__()�������Ѷ�������list��dict���Լ��ϸ�ֵ����󣬻���һ��__delitem__()����������ɾ��ĳ��Ԫ�ء�
#������ȫ��̬��__getattr__�����ǿ���д��һ����ʽ����
class Chain(object):
    def __init__(self, path = ""):
        self._path = path
    def __getattr__(self, path):
        return Chain("%s %s" % (self._path, path))
    def __str__(self):
        return self._path

    __repr__ = __str__
#����һ��__call__()�������Ϳ���ֱ�Ӷ�ʵ�����е���
class student(object):
    def __init__(self, name):
        self.name = name
    def __call__(self):
        print("Name is %s" % self.name)
s = student("natasha")
s()
#__call__()�����Զ����������ʵ������ֱ�ӵ��þͺñȶ�һ���������е���һ��
#��Ҫ�ж�һ�������Ƿ��ܱ����ã��ܱ����õĶ������һ��Callable����
from enum import Enum
Month = Enum("Month", ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))
for name, member in Month.__members__.items():
    print(name, "==>", member, ",", member.value)
#value���������Զ�������Ա��int������Ĭ�ϴ�1��ʼ����
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
#@uniqueװ�������԰������Ǽ�鱣֤û���ظ�ֵ
day1 = Weekday.Mon
print(day1)
print(Weekday["Wed"])
print(Weekday.Tue.value)
#��̬���Ժ;�̬�������Ĳ�ͬ�����Ǻ�������Ķ��壬���Ǳ���ʱ����ģ���������ʱ��̬������
class Hello(object):
    def hello(self, name = "world"):
        print("hello, %s" % name)
#type()�����ȿ��Է���һ����������ͣ��ֿ��Դ������µ�����
def fn(self, name = "world"):
    print("hello, %s" % name)
Hello = type("Hello", (object,), dict(hello = fn))
print(type(Hello))
#type()�������δ���3������
#class������
#�̳еĸ��༯�ϣ�ע��Python֧�ֶ��ؼ̳У����ֻ��һ�����࣬������tuple�ĵ�Ԫ��д��
#class�ķ��������뺯���󶨣��������ǰѺ���fn�󶨵�������hello��
#����ʹ��type()��̬���������⣬Ҫ������Ĵ�����Ϊ��������ʹ��metaclass
#metaclass��ֱ��ΪԪ��
#(������)�ȶ���metaclass��Ȼ�󴴽���
#metaclass�����㴴��������޸��ࡣ���仰˵������԰��࿴����metaclass���������ġ�ʵ����
#����Ĭ��ϰ�ߣ�metaclass������������Metaclass��β���Ա�����ر�ʾ����һ��metaclass
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs["add"] = lambda self, value: self.append(value)#method
        return type.__new__(cls, name, bases, attrs)
class MyList(list, metaclass = ListMetaclass):
    pass
#����ؼ��ֲ���metaclassʱ��ħ������Ч�ˣ���ָʾPython�������ڴ���MyListʱ��Ҫͨ��ListMetaclass.__new__()������
#__new__()�������յ��Ĳ���������
#��ǰ׼����������Ķ���
#�������
#��̳еĸ��༯��
#��ķ�������
L = MyList()
L.add(1)
print(L)
#��Ҫͨ��metaclass�޸��ඨ��ġ�ORM����һ�����͵�����
#ORMȫ�ơ�Object Relational Mapping����������-��ϵӳ�䣬���ǰѹ�ϵ���ݿ��һ��ӳ��Ϊһ������Ҳ����һ�����Ӧһ����������д������򵥣�����ֱ�Ӳ���SQL���
#��дһ��ORM��ܣ����е��඼ֻ�ܶ�̬���壬��Ϊֻ��ʹ���߲��ܸ��ݱ�Ľṹ�������Ӧ������
#����Field�࣬�����𱣴����ݿ����ֶ������ֶ�����
class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return "<%s : %s>" % (self.__class__.__name__, self.name)
#����������͵�Field������StringField��IntegerField
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
