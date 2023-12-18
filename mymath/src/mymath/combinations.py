from .factorial import *

def comb(n, k):
    if not (type(n) is int and type(k) is int):
        raise TypeError("Wrong type: n and k must be integers.")
    if n < 0 or k < 0:
        raise ValueError("n and k must be a positive values.")
    if k > n:
        return 0
    return fact(n) / fact(k) / fact(n - k)
