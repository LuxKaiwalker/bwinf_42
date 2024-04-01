def fibonacci(n):
    fib_seq = [0, 1]
    while len(fib_seq) < n:
        next_num = fib_seq[-1] + fib_seq[-2]
        fib_seq.append(next_num)
    return fib_seq

n = int(input("Enter the number of Fibonacci numbers to generate: "))
fib_numbers = fibonacci(n)
print(fib_numbers)
sum_fib = sum(fib_numbers)
print("Sum of Fibonacci numbers:", sum_fib)