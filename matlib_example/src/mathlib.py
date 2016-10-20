"""
Testing fibo

@author: neliel
"""

def fibo_old(n):
    if n == 0:
        return 0
    
    if n < 0:
        raise ValueError()
        
    if n > 2:
        return fibo(n - 1) + fibo(n -2)
    else:
        return 1

def tailsum(seq, n=2):
    """
    Get the sum of the last n entries in seq. Use negative n to skip the first -n entries of seq.
    """
    return sum(seq[-n:])
        
f = [0, 1]
def fibo(n):
    """
    Calculates the n-th Fibonacci number without recursion.
    """
    while len(f) < n + 1:
        f.append(tailsum(f))
    return f[n]
        