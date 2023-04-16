import numpy

numpy.set_printoptions(sign=' ')

inp = numpy.array(input().split(), float)

print(numpy.floor(inp))
print(numpy.ceil(inp))
print(numpy.rint(inp))
