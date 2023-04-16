from collections import defaultdict

A = defaultdict(list)
list1 = []

# size of group A and group B
n, m = map(int, input().split())

for i in range(1, n+1):  # from 1 to n+1
    A[input()].append(str(i))

for i in range(m):
    B = input()
    if B in A:
        print(' '.join(A[B]))
    else:
        print(-1)
