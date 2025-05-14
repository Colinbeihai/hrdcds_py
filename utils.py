from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_list(numbers):
    current_lcm = 1
    for num in numbers:
        current_lcm = lcm(current_lcm, num)
    return current_lcm
