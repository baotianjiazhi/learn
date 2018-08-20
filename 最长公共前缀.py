class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        #选出最短的字符串放在开头
        if strs == []:
            return ""
        str_list = sorted(strs, key=lambda i: len(i), reverse=False)
        short_word = str_list[0]
        max_len = len(str_list[0])
        for i in range(max_len):
            for one_word in str_list:
                if short_word[i] != one_word[i]:
                    return short_word[:i]
        return short_word


if __name__ == '__main__':
    s = Solution()
    print(s.longestCommonPrefix([]))
