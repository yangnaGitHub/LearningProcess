# -*- coding: UTF-8 -*-
for index in range(1, 10):
    for count in range(1, index + 1):
        print("{} * {} = {}\t".format(index, count, index * count), end = " ")
    print()
