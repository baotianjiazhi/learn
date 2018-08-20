class Solution:
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if nums == []:
            return 0

        for i in range(len(nums)):
            if nums[i] == target:
                return i
            elif i != len(nums) - 1:
                if nums[i] < target and nums[i + 1] > target:
                    return i + 1
        if target > nums[-1]:
            return len(nums)
        else:
            return 0


s = Solution()
nums = [1, 2, 3, 5]
target = 7
print(s.searchInsert(nums, target))