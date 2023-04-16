from collections import deque

d = deque()

for _ in range(int(input())):
    inp = input().split()
    # inp[0] - attribute for d, inp[1] argument for attribute (if needed), else []
    getattr(d, inp[0])(*[inp[1]] if len(inp) > 1 else [])

print(*[item for item in d])
