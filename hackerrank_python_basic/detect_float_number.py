import re

# Number can start with +, - or . symbol, f.e.:
# 12. is False
# -+4.3 is False
# -1.0 is True

for _ in range(int(input())):
    print(re.search(r'^([-\+])?\d*\.\d+$', input()) is not None)
