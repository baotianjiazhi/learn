"""
Created by Baobaobao123
Thank you 
"""
__author__ = 'Baobaobao123'

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:

    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head is None:
            return None

        a = head
        while a.next:
            if a.val == a.next.val:
                a.next = a.next.next
            else:
                a = a.next
        return head
