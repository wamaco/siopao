# naive approach

def fib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# top down approach

memo: dict[int, int] = {}

def fib1(n: int) -> int:
    if n == 0:
        memo[0] = 0
        return 0
    elif n == 1:
        memo[1] = 1
        return 1
    elif n in memo:
        return memo[n]
    else:
        result: int = fib1(n-1) + fib1(n-2)
        memo[n] = result
        return result
    
# bottom up approach

def fib2(n: int) -> int:
    dp = [0] * (n+1)
    dp[0], dp[1] = 0, 1

    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]