# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         for i in range(len(nums)):
#             j = i + 1
#             for j in range(len(nums)):
#                 if nums[i] + nums[j] == target and i != j:
#                     return i, j
#
# nums = [3, 2, 4]
# target = 6
# s = Solution()
# print(s.twoSum(nums, target))

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i, v in enumerate(nums):
            if target - v in nums[i + 1:]:
                return i, nums[i + 1:].index(target - v) + i + 1

nums = [3, 2, 4]
target = 6
s = Solution()
print(s.twoSum(nums, target))

