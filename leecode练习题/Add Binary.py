class Solution:
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        sa = list(a)
        sb = list(b)
        if len(sb) < len(sa):
            temp = sb[:]
            sb = sa[:]
            sa = temp[:]
        i = len(sa) - len(sb)
        for j in range(i):
            sb.append(0)
        sb = sb[::-1]
        for i in range(-1, -len(sa)):



