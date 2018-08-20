class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        pe: int
        """
        for i in nums:
            j = nums.index(i) + 1
            while j <= len(nums) - 1:
                if i == nums[j]:
                    nums.remove(nums[j])
                else:
                    j = j + 1
        return len(nums)

nums = [1,1,2]
s = Solution()
print(s.removeDuplicates(nums))