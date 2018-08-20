class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        #先判断字符串的长度是否为0或者是否为偶数
        if len(s) % 2 != 0:
            return False
        if len(s) == 0:
            return True
        if s[0] == ')' or s[0] == '}' or s[0] == ']':
            return False
        #用栈解决
        l = []
        index = ''
        for i in s:
            if (i == '(' or i == '[' or i == '{'):
                l.append(i)
            else:
                index = l.pop()
                if (index == '(' and i == ')') or (index == '[' and i == ']') or (index == '{' and i  == '}'):
                    continue
                else:
                    return False
        if len(l) != 0:
            return False
        return True


s = Solution()
str = ''
print(s.isValid(str))