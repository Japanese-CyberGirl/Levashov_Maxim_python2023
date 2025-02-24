#recursion
def fibonacci_recursion(n):
    if n == 1: return 1
    if n == 2: return 1
    return (fibonacci_recursion(n-1) + fibonacci_recursion(n-2))

#cycle
def fibonacci_cycle(n):
    prev = 0
    current = 1

    if n == 1:
        return 1

    for i in range(n-1):
        temp = current
        current += prev
        prev = temp
    return current

n = int(input())

print(fibonacci_cycle(n))
print(fibonacci_recursion((n)))