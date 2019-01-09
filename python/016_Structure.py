#列表可以很方便的作为一个堆栈来使用
#append()方法可以把一个元素添加到堆栈顶
#不指定索引的pop()方法可以把一个元素从堆栈顶释放出来

#列表推导式
vec = [2, 4, 6]
listtest1 = [3 * x for x in vec]
print(listtest1)

listtest2 = [[x, x ** 2] for x in vec]
print(listtest2)

fresh = ["  banana", "passion ", " straberay "]
skipstrip = [weapon.strip() for weapon in fresh]
print(skipstrip)

#可以使用if字句作为过滤器
filter1 = [3 * x for x in vec if x > 3]
print(filter1)

#关于循环的技巧
vec1 = [4, 3, -9]
multiple = [x * y for x in vec for y in vec1]
print(multiple)
orderly = [vec[index] * vec1[index] for index in range(len(vec1))]
print(orderly)
pi = [str(round(355 / 113, index)) for index in range(1, 6)]
print(pi)

#将3*4的矩阵列表转换成4*3的列表
#从外面往里面看
#可以看做print("natasha") = [row[index] for row in matrix] ==> [print("natasha") for index in range(4)]
#在看里面的实际输出即可
matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 1, 2]]
reverse = [[row[index] for row in matrix] for index in range(4)]
print(reverse)

#集合也支持推导式
testset = {x for x in "abcdefghijk" if x not in "abcd"}
print(testset)

#字典推导
dicttest1 = {x : x ** 2 for x in vec}
print(dicttest1)
#字典遍历
for key, value in dicttest1.items() :
    print(key, value)
#可以使用enumerate()函数同时得到
#enumerate自动添加索引
for key, value in enumerate(["natasha", "zain", "tracy"]) :
    print(key, value)
#同时遍历两个或更多的序列,可以使用zip()组合,返回元组
question = ["what is your name", "how old are you"]
answers = ["natasha", 22]
for q, a in zip(question, answers) :
    print("{0}? ==> {1}" .format(q, a))
#reversesd()反向遍历一个序列
#sorted()按顺序遍历一个序列
