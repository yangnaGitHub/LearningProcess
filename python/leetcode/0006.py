# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:54:05 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        #方案一
#        s_len = len(s)
#        mydict = {}
#        for index in range(numRows):
#            mydict[index] = []
#        x_index = [index for index in range(numRows)]
#        x_index.extend([index for index in range(numRows-2, 0, -1)])
#        y_index = ([0]*numRows)
#        y_index.extend([index for index in range(1, numRows-1, 1)])
#        count = 0
#        index = 0
#        while True:
#            skip = index*(numRows-1)
#            for x_val,y_val in zip(x_index, y_index):
#                y_end = y_val+skip
#                diff = y_end - len(mydict[x_val]) + 1
#                mydict[x_val].extend([' ']*diff)
#                mydict[x_val][y_end] = s[count]
#                count += 1
#                if count == s_len:
#                    index = -1
#                    break
#            if -1 == index:
#                break
#            index += 1
#        t_str = ''
#        for index in range(numRows):
#            for s_char in mydict[index]:
#                t_str += s_char
#            t_str += '\n'
#        return t_str
        
        #方案2
        if len(s) < numRows or numRows == 1:
            return s
        mylist = ['']*numRows
        index = 0
        step = 1
        for s_char in s:
            mylist[index] += s_char
            index += step
            if (numRows-1) == index:
                step = -1
            elif 0 == index:
                step = 1
        return ''.join(mylist)
  
        #方案3
#        if len(s)<numRows or numRows == 1:
#            return s
#        mydict = {}
#        for index in range(numRows):
#            mydict[index] = ''
#        x_index = [index for index in range(numRows)]
#        x_index.extend([index for index in range(numRows-2, 0, -1)])
#        s_len = len(x_index)
#        for index,val in enumerate(s):
#            mydict[x_index[index%s_len]] += val
#        t_str = ''
#        for index in range(numRows):
#            t_str += mydict[index]
#        return t_str

if __name__ == '__main__':
    s_0006 = Solution()
    #print(s_0006.convert('PAYPALISHIRING', 3))
    print(s_0006.convert('AB', 1))