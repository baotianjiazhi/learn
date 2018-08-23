class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        sum = 0
        dict = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
        for i in range(len(s) - 1): #这里减1防止最后一个数加一后越界，在返回值时加上即可
            if dict[s[i]] < dict[s[i+1]]:
                sum = sum - dict[s[i]]
            else:
                sum = sum + dict[s[i]]
        return sum + dict[s[-1]]


a=Solution()
print(a.romanToInt("MCDLXXVI"))