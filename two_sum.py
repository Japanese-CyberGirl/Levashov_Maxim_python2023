def strav(mas, res):
    a = dict()
    for i in range(len(mas)):
        if mas[i] in a:
            return i, a[mas[i]]
        a[res - mas[i]] = i

print(strav([1,2,3,4], 6))