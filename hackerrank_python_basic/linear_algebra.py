import numpy

# matrix dimensions
N = int(input())
matrix = []

# loop over the rows of the matrix
for i in range(N):
    # read a line of input and split it into its individual values
    row = input().split()
    # convert each value to a float and add it to the current row
    row = [float(x) for x in row]
    # append the current row to the matrix
    matrix.append(row)

result = numpy.linalg.det(matrix)
print(round(result, 2))
# print(*matrix)
