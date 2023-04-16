N = int(input())
headers = list(input().split())

total = 0
for _ in range(N):
    # sums total number of MARKS
    total += int(list(input().split())[headers.index('MARKS')])

# print out average mark
print(total/N)
