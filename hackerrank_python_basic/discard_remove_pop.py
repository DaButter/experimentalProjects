data_len = int(input())
data = set(map(int, input().split()))
operations = int(input())

for x in range(operations):
    # op[0] cmnd, op[1] attribute for cmnd
    op = input().split()
    if op[0] == "remove":
        data.remove(int(op[1]))
    elif op[0] == "discard":
        data.discard(int(op[1]))
    else:
        data.pop()

print(sum(data))
