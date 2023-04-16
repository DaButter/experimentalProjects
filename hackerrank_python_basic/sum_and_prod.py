import numpy
from functools import reduce


N, M = input().split()
N = int(N)
M = int(M)

arr = []
for i in range(N):
    row = input().split()
    row = [int(x) for x in row]
    arr.append(row)

sub_result = (numpy.sum(arr, axis=0))

# use reduce() to calculate the product of all numbers in the list
result = reduce(lambda x, y: x * y, sub_result)
print(result)
