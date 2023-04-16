import numpy

inp = map(int, input().split())

result = str(numpy.eye(*inp))
# result = str(numpy.eye(*inp, k=1)) move ones by one up

result = result.replace('1', ' 1').replace('0', ' 0')
print(result)
