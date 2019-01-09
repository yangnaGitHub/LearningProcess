#while ... else
counter = 0
while counter < 3 :
    print(counter)
    counter = counter + 1
else :
    print("end %d" % counter)

#for ... else
sites = ["baidu", "google", "taobao", "yahoo"]
for site in sites :
    print(site + ".com")
else :
    print("natasha")

#内置range()函数它会生成数列
for index in range(5) :
    print(index)

#可以使range以指定数字开始并指定不同的增量(甚至可以是负数,有时这也叫做'步长')
for index in range(0, 10, 3) :
    print(index)
for index in range(-10, -100, -30) :
    print(index)
#结合range()和len()函数以遍历一个序列的索引
for index in range(len(sites)) :
    print("%d ==> %s" % (index, sites[index]))
#可以使用range()函数来建立一个列表
list(range(5))

#从for或while循环中终止,任何对应的循环 else 块将不执行
#else子句,它在穷尽列表或条件变为false导致循环终止时被执行,循环被break终止时不执行

#pass是空语句,pass不做任何事情,一般用做占位语句
