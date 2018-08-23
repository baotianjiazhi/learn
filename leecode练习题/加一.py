class Solution:
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        if len(digits) == 0:
            digits = [1]
        elif digits[-1] == 9:
            digits = self.plusOne(digits[:-1])
            digits.append(0)
        else:
            digits[-1] = digits[-1] + 1
        return digits

s = Solution()
digits = [9, 9, 9, 9]
print(s.plusOne(digits))