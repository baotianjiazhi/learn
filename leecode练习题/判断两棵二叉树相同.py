"""
Created by Baobaobao123
Thank you 
"""
__author__ = 'Baobaobao123'

class Solution:
    def isSameTree(self, p, q):
        """
        :type p: TreeNode
        :type q: TreeNode
        :rtype: bool
        """

        if not p and not q:
            return True

        if p and q and q.val == p.val:
            l = self.isSameTree(p.left, q.left)
            r = self.isSameTree(p.right, q.right)
            return l and r

        else:
            return False