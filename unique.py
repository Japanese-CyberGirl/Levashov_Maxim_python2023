def unique(arr, n):
    dic = {}
    for i, num in enumerate(arr):
        diff = n - num
        if diff in dic:
            return [i, dic[diff]]
        dic[num] = i
print(unique([5,6,5,5,7,8,9],7))