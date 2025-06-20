from sympy import divisors
def get_factors(num):
    return divisors(num)

print(get_factors(98))