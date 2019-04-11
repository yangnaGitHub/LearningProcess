# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 08:17:03 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

def get_square(mylist):
    i_index,j_index = 0,len(mylist)-1
    i_data,j_data = 0,0
    new_list = []
    while True:
        if i_index > j_index:
            break
        i_data = mylist[i_index]**2
        j_data = mylist[j_index]**2
        #print(i_data, j_data)
        if i_data > j_data:
            new_list.append(i_data)
            i_index += 1
        else:
            new_list.append(j_data)
            j_index -= 1
    #print(new_list[::-1])
    return new_list[::-1]

if __name__ == '__main__':
    print(get_square([-5, -3, -2, 1, 3, 7]))