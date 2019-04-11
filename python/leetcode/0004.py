# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:36:16 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        len_1 = len(nums1)
        len_2 = len(nums2)
        a_len = len_1 + len_2
        mid_1,mid_2 = (a_len-1)//2, a_len//2
        index_1 = 0
        index_2 = 0
        current_val,a_sum = 0,0
        for index in range(mid_2+1):
            if (index_1 < len_1) and (index_2 < len_2):
                if nums1[index_1] <= nums2[index_2]:
                    current_val = nums1[index_1]
                    index_1 += 1
                else:
                    current_val = nums2[index_2]
                    index_2 += 1
            elif (index_1 < len_1) and (index_2 >= len_2):
                current_val = nums1[index_1]
                index_1 += 1
            elif (index_1 >= len_1) and (index_2 < len_2):
                current_val = nums2[index_2]
                index_2 += 1              
            if mid_1 == index:
                a_sum = current_val
            if index == mid_2:
                a_sum += current_val
        return float(a_sum)/2

#        len_1 = len(nums1)
#        len_2 = len(nums2)
#        a_len = len_1 + len_2
#        mid_1,mid_2 = (a_len-1)//2,a_len//2
#        index_1 = 0
#        index_2 = 0
#        current_val,a_sum = 0,0
#        for index in range(mid_2+1):
#            if (index_1 < len_1) and (((index_2 < len_2) and (nums1[index_1] <= nums2[index_2])) or (index_2 >= len_2)):
#                current_val = nums1[index_1]
#                index_1 += 1
#            elif (index_2 < len_2) and (((index_1 < len_1) and (nums1[index_1] > nums2[index_2])) or (index_1 >= len_1)):
#                current_val = nums2[index_2]
#                index_2 += 1
#            if mid_1 == index:
#                a_sum = current_val
#            if index == mid_2:
#                a_sum += current_val
#        return float(a_sum)/2

if __name__ == '__main__':
    s_0004 = Solution()
    print(s_0004.findMedianSortedArrays([1,2], [3,4]))