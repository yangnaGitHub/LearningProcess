# -*- coding: utf-8 -*-

class People:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.__score = score
        self.print_people()
        #self.__print_people()
    
    def print_people(self):
        string = u'%s的年龄：%d，成绩为：%.2f' % (self.name, self.age, self.__score)
        print string
    
    __print_people = print_people
    
class Student(People):
    def __init__(self, name, age, score):
        People.__init__(self, name, age, score)
        self.name = 'Student ' + self.name

    def print_people(self):
        string = u'%s的年龄：%d' % (self.name, self.age)
        print string

def func(p):
    p.age = 11

if __name__ == "__main__":
    p = People('natasha', 10, 3.14159)
    func(p)
    p.print_people()
    print
    
    j = Student('Jerry', 12, 2.71828)
    print
    
    p.print_people()
    j.print_people()
    print
    
    People.print_people(p)
    People.print_people(j)