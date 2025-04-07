def sequence(st):
    result = {}
    for i in st:
        result[i] = 1 + result.get(i,0)
    return result

print(sequence("()"))
print(sequence("((()))()"))
print(sequence("(()()"))