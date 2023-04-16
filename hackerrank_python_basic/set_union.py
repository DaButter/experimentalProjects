n = int(input())
A = list(input().split())

m = int(input())
B = list(input().split())

s1 = set(A)
s2 = set(B)

print(len(s1.union(s2)))
