class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        #如果是个位数就直接返回其本身
        if -10 < x < 10:
            return x
        #把整数x转换为字符串
        str_x = str(x)
        #判断是否为负数
        if str_x[0] != '-':
            str_x = str_x[::-1]
            x = int(str_x)
        else:
            str_x = str_x[::-1].strip('-')
            x = int(str_x)
            x = -x
        return x if -2147483648 < x < 2147483647 else 0

s = Solution()
print(s.reverse(123))

