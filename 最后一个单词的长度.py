class Solution:
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        if not len(s.strip()):
            return 0
        else:
            word_list = s.split()
            l = len(word_list[-1])
        return l

t = Solution()
s = '          '
print(t.lengthOfLastWord(s))