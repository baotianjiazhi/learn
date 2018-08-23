class Solution:
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        pre_nums = 0    #定义一个累加数组，如果这个数组小于或等于零说明前面的累加值对于后面是无益的
        total_max = nums[0] #最大子序和
        for i in nums:
            if pre_nums < 0:
                pre_nums = i
            else:
                pre_nums += i
            if pre_nums > total_max:
                total_max = pre_nums
        return total_max


s = Solution()
nums = [-1, 2, 3, -2, 4, 5]
print(s.maxSubArray(nums))