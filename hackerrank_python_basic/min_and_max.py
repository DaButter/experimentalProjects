import numpy

N, M = input().split()
N = int(N)
M = int(M)

arr = []
for i in range(N):
    row = input().split()
    row = [int(x) for x in row]
    arr.append(row)

sub_result = numpy.min(arr, axis=1)
print(numpy.max(sub_result))
