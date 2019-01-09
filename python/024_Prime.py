# -*- coding: UTF-8 -*-
num = int(input("enter: "))
if num > 1:
    for index in range(2, num):
        if not(num % index):
            print("NO")
            break
    else:
        print("YES")
else:
    print("NO")
