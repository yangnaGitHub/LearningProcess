# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:20:18 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        #方法一
#        if len(s) < 2 or s == s[::-1]:
#            return s
#        self.s_len = len(s)
#        self.str = s
#        max_len = 1
#        range_s,range_e = 0,0
#        for index,s_val in enumerate(s):
#            count_1 = self.start_match(index-1, index+1)
#            oldcount = count_1*2+1
#            deal_flag = False
#            if (index+1 < self.s_len) and (s[index+1] == s_val):
#                count_2 = self.start_match(index-1, index+2)
#                newcount = 2*count_2+2
#                if max_len < max(oldcount, newcount):
#                    max_len = max(oldcount, newcount)
#                    if newcount > oldcount:
#                        range_s = index-count_2
#                        range_e = index+count_2+1
#                    else:
#                        range_s = index-count_1
#                        range_e = index+count_1
#                deal_flag = True
#            if count_1 and (not deal_flag):
#                if max_len < oldcount:
#                    max_len = oldcount
#                    range_s = index-count_1
#                    range_e = index+count_1
#        if 0 != self.s_len:
#            return s[range_s:range_e+1]
        
        #方法二
        s_len = len(s)
        if s_len < 2 or s == s[::-1]:#特殊的条件操作有利于减少不少时间
            return s
        max_len = 0
        start = 0
        for index in range(s_len):
            skip = index - max_len
            skip_end = index+1#到当前的word的index
            #print(index, skip, skip_end)
            if skip >= 1 and s[skip-1:skip_end] == s[skip-1:skip_end][::-1]:
                start = skip-1
                max_len += 2
                continue
            if skip >=0 and s[skip:skip_end] == s[skip:skip_end][::-1]:
                start = skip
                max_len += 1
        return s[start:start+max_len]
        
    def start_match(self, start, end):
        count = 0
        while (start >= 0) and (end < self.s_len):
            if self.str[start] == self.str[end]:
                count += 1
            else:
                break
            start -= 1
            end += 1
        return count

if __name__ == '__main__':
    s_0005 = Solution()
    print(s_0005.longestPalindrome('babad'))
    print(s_0005.longestPalindrome('cbbd'))
    print(s_0005.longestPalindrome('abcdedcbabb'))
    print(s_0005.longestPalindrome('ccc'))
    print(s_0005.longestPalindrome('aaaa'))