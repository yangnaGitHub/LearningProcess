# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:53:06 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        #方案一
#        i_str = str(x)
#        i_str = int((i_str[0] + i_str[:0:-1]) if '-' == i_str[0] else i_str[::-1])
#        if (i_str > 2**31-1) or (i_str < -2**31):
#            i_str = 0
#        return i_str
        
        #方案二
        flag = False
        if x < 0:
            x = -x
            flag=True
            
        Reminder,r_s = 0,0
        while (x > 0):
            Reminder = x % 10
            r_s = (r_s * 10) + Reminder
            x = x // 10
        x = r_s    
        if not (abs(int(x))>2147483647):
            return -int(x) if flag else int(x)
        return 0

if __name__ == '__main__':
    s_0007 = Solution()
    print(s_0007.reverse(1534236469))