# A = input().split()
# B = input().split()
#
# # convert input to int
# for i in range(len(A)):
#     A[i] = int(A[i])
# for i in range(len(B)):
#     B[i] = int(B[i])
# # print(f"A: {A}  B: {B}")
#
# # create combinations
# results = []
# for i in range(len(A)):
#     for j in range(len(B)):
#         results.append((A[i], B[j]))
#
# # results.sort(key=lambda x: (x[0], x[1])) # sort by first and second element
# results.sort()
#
# for i in range(len(results)):
#     print(results[i], end=' ')


# ======= when using itertools library =======
import itertools

A = input().split()
B = input().split()

for i in range(len(A)):
    A[i] = int(A[i])
for i in range(len(B)):
    B[i] = int(B[i])

results = list(itertools.product(A, B))
results.sort()
for i in range(len(results)):
    print(results[i], end=' ')
