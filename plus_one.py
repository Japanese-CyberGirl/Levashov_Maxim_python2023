def plus_one(nums):
    for i in range(len(nums)-1, -1, -1):
        if nums[i] < 9:
            nums[i] += 1
            return nums
        else:
            nums[i] = 0
    return [1] + nums

print(plus_one([9,9,9]))