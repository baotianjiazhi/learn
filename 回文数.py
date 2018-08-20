class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        # 如果是个位数就直接返回其本身
        if 0 <= x < 10:
            return True
        # 把整数x转换为字符串
        else:
            if x % 10 == 0:
                return False
            else:
                str_x = str(x)
                # 判断是否为负数
                if str_x[0] != '-':
                    str_x = str_x[::-1]
                    a = int(str_x)
                    if a == x:
                        return True
                    else:
                        return False
                return False

s = Solution()
print(s.isPalindrome(123))