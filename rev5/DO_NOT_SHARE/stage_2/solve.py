import sys
sys.setrecursionlimit(10**6)
sys.set_int_max_str_digits(0)

MOD = 1000000007

def matrix_multiply(a, b):
    result = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                result[i][j] += a[i][k] * b[k][j]
                result[i][j] %= MOD
    return result

def matrix_power(m, n):
    size = len(m)
    if n == 0:
        identity = [[0] * size for _ in range(size)]
        for i in range(size):
            identity[i][i] = 1
        return identity

    if n == 1:
        return m

    half_power = matrix_power(m, n // 2)
    result = matrix_multiply(half_power, half_power)

    if n % 2 == 1:
        result = matrix_multiply(result, m)

    return result

def fib(n):
    fib_matrix = [[1, 1], [1, 0]]
    result = matrix_power(fib_matrix, n - 1)
    return result[0][0]

def solve():
    n = int(open('inp.txt').read())
    fib_str = str(fib(n))
    print("rentry.co/"+fib_str)

def main():
    tc = 1
    for _ in range(tc):
        solve()

if __name__ == '__main__':
    main()