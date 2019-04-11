# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:48:45 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        #怎么降低空间复杂度
        mydict = {}
        result = []
        for index,num in enumerate(nums):
            if num in mydict:
                result.extend([mydict[num], index])
                del(mydict[num])#减少Key可以降低遍历时间
            else:
                mydict[target - num] = index
        return result

if __name__ == '__main__':
    s_0001 = Solution()
    print(s_0001.twoSum([2, 7, 11, 15], 9))