memo = {}

def fastest_resilience(n_0: int) -> int:
    if n_0 in memo:
        return memo[n_0]
    elif n_0 <= 0:
        memo[n_0] = 0
        return 0
    else:
        # if i != 0 is needed to prevent loops in the recursion (e.g. 10 recursively calls f_r(10-1^2) and f_r(10-0^2))
        result = 1 + min([fastest_resilience(n_0-(int(i)**2)) for i in str(n_0) if i != '0'])
        memo[n_0] = result
        return result
