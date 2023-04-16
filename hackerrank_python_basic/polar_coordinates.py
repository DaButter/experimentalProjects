import cmath

inp = complex(input())
result = cmath.polar(inp)

print(*result, sep='\n')
