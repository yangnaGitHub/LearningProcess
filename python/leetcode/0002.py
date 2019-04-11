# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:25:13 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

class ListNode(object):
    def __init__(self, val):
        self.val = val
        self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        result = temp = ListNode(0)
        save_val = 0
        while l1 or l2 or save_val:
            if l1:
                save_val += l1.val
                l1 = l1.next
            if l2:
                save_val += l2.val
                l2 = l2.next
            temp.next = ListNode(save_val%10)
            temp = temp.next
            save_val = save_val//10
        return result.next

def gen_ListNode(mylist):
    head = ListNode(mylist[0])
    temp = head
    for val in mylist[1:]:
        temp.next = ListNode(val)
        temp = temp.next
    return head

def print_ListNode(mylistnode):
    while mylistnode:
        print(mylistnode.val, end=' ')
        mylistnode = mylistnode.next

if __name__ == '__main__':
    s_0002 = Solution()
    print_ListNode(s_0002.addTwoNumbers(gen_ListNode([2,4,3]), gen_ListNode([5,6,4])))