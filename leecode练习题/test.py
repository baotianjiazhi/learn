# class Solution:
#     def removeDuplicates(self, nums):
#         """
#         :type nums: List[int]
#         pe: int
#         """
#         nums = set(nums)
#         nums = list(nums)
#         print(nums)
#         return len(nums)
#
# nums = [1, 1, 2]
# s = Solution()
#
# print(s.removeDuplicates(nums))

# test = [1, 2, 3]
# x = lambda x: test[x]
# print(x(1))


# def test02(x):
#     yield x
#
#
# if __name__ == '__main__':
#     print()

# def test(a):
#     def test1(b):
#         return a + b
#     return test1
#
# test1 = test(1)
# print(test1(2))


# a = 3
#
# def test():
#     b = 4

# eval函数
# s = "print('abc')"
# eval(s)
# a = 10
# b = 20
# c = eval("a+b")
# print(c)
# list = [i for i in range(1, 5)]
# print(list)


#递归函数
def test():
    print("test01")
    test02()


def test02():
    print("test02")

test()


#nonlocal
a = 100

def outer():
    b = 10

    def inner():
        nonlocal b #声明外部函数的局部变量
        print("inner: b", b)
        b = 20

        global a
        a = 1000
    inner()
    print("outer: b", b)


outer()
print(a)

str = '111'
def t1():
    # str = '456'
    def t2():
        # str = '123'
        print(str)
    t2()


t1()