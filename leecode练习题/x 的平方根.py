class Solution:
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        left = 0
        right = x
        while left < right:
            mid = int((left + right) / 2)
            if x < mid ** 2:
                right = mid
            else:
                left = mid + 1
        if left > 1:
            return left - 1
        else:
            return left