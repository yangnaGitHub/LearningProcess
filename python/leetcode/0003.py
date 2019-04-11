# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:35:41 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        #方案1:开辟固定空间
#        mylist = [-1]*128
#        max_len,start_val = 0,-1
#        for index,s_char in enumerate(s):
#            i_chr = ord(s_char)
#            print(start_val, mylist[i_chr], mylist[i_chr] > start_val)
#            if mylist[i_chr] > start_val:
#                start_val = mylist[i_chr]
#            mylist[i_chr] = index
#            print(start_val, mylist[ord('a')], mylist[ord('b')], mylist[ord('c')])
#            max_len = max(max_len, index-start_val)
#        return max_len
        
        #方案2:使用字典
        #少了ord(s_char)这样一个步骤能节省不少时间
        mydict = {}
        max_len,start_val = 0,-1
        for index,s_char in enumerate(s):
            if (s_char in mydict) and (mydict[s_char] > start_val):
                start_val = mydict[s_char]
            mydict[s_char] = index
            max_len = max(max_len, index-start_val)
        return max_len
        
        #方案3
#        mydict = {}
#        max_len,start_val = 0,0
#        for index,s_char in enumerate(s):
#            if s_char in mydict:
#                max_len = max(max_len, index-start_val)
#                start_val = max(start_val, mydict[s_char]+1)
#            mydict[s_char] = index
#        return max(max_len, len(s)-start_val)

if __name__ == '__main__':
    s_0003 = Solution()
    print(s_0003.lengthOfLongestSubstring(' '))
    print(s_0003.lengthOfLongestSubstring('abcabcbb'))
    print(s_0003.lengthOfLongestSubstring('bvbw'))