def fib(n):
    prev = 0
    cur = 1

    if n == 0:
        return 0

    for i in range(n-1):
        temp = cur
        cur += prev
        prev = temp
    return cur

def fib_r(n):
    if n == 1:
        return 1
    if n == 0:
        return 0
    return (fib_r(n-1)+fib_r(n-2))

print(fib_r(5))


def is_correct_brackets_seq(seq):
    stack = []
    for i in seq:
        if i == '(': stack.append(i)
        elif i == ')':
            if len(stack) == 0:
                return False
            stack.pop()
        return not stack

print(is_correct_brackets_seq('(())'))


def plus_one(nums):
    for i , _ in reversed(list(enumerate(nums))):
        if nums[i] < 9:
            nums[i] += 1
            return nums
        else: nums[i] = 0
    return[1] + nums

    print(plus_one([1,2,3]))
    print(list(enumerate([1,2,3,4])))
    #for i in range(len(nums)-1, -1, -1):
       # if nums[i] < 9:
       #     nums[i] += 1
       #     return nums
       # else: nums[i] = 0
    #return[1] + nums

print(plus_one([9,0,9]))


def number_of_unique_characters(st):
    result = {}
    for i in st:
        result[i] = 1 + result.get(i,0)
    return result

print(number_of_unique_characters("aaasssbbff"))

def strav(mas, res):
    a = dict()
    for i in range(len(mas)):
        if mas[i] in a:
            return i, a[mas[i]]
        a[res - mas[i]] = i

print(strav([1,2,3,4], 6))

