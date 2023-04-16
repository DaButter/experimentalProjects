import re

# .*\+ : Valid regex.
# .*+: Has the error multiple repeat. Hence, it is invalid

for _ in range(int(input())):
    ans = True
    try:
        reg = re.compile(input())
    except re.error:
        ans = False
    print(ans)
