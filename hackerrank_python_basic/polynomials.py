import numpy

# Task
# You are given the coefficients of a polynomial P.
# Your task is to find the value of P at point x.

P_coeff = list(map(float, input().split()))
x = int(input())

# print(f"Pol coeff: {P_coeff}, value x: {x}")

result = numpy.polyval(P_coeff, x)
print(result)