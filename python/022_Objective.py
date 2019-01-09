#可以通过类名访问其属性
#类对象支持两种操作==>属性引用(obj.name)和实例化

#将对象创建为有初始状态的,定义一个名为__init__()的特殊方法(自动调用,构造方法)
#使用def关键字可以为类定义一个方法,类方法必须包含参数self,且为第一个参数
#支持类的继承,圆括号中基类的顺序,若是基类中有相同的方法名,从左到右查找基类中是否包含方法
#两个下划线开头声明该属和方法为私有,不能在类地外部被使用或直接访问
class people:
    name = ""
    age = 0
    __weight = 0#私有属性,在类外部无法直接进行访问
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.__weight = weight
    def speak(self):
        print("%s ==> %d" % (self.name, self.age))

class student(people):
    grade = 0
    def __init__(self, name, age, weight, grade):
        people.__init__(self, name, age, weight)
        self.grade = grade
    def speak(self):
        print("%s ==> %d ==> %d" % (self.name, self.age, self.grade))

stu = student("natasha", 22, 58, 2)
stu.speak()

#重写,子类重写父类的方法
class Parent:
    def method(self):
        print("Parent")
class Child(Parent):
    def method(self):
        print("Child")
child = Child()
child.method()

#类的专有方法
#__init__构造函数，在生成对象时调用
#__del__析构函数
#__repr__打印
#__setitem__按照索引赋值
#__getitem__按照索引获取值
#__len__获得长度
#__cmp__比较运算
#__call__函数调用
#__add__加运算
#__sub__减运算
#__mul__乘运算
#__div__除运算
#__mod__求余运算
#__pow__乘方

#支持运算符重载
class Vector:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
    def __str__(self):
        return "Vector(%d, %d)" % (self.val1, self.val2)
    def __add__(self, other):
        return Vector(self.val1 + other.val1, self.val2 + other.val2)
v1 = Vector(2, 10)
v2 = Vector(5, -2)
print(v1 + v2)
