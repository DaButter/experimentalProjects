import re

# valid mobile number is a ten digit number starting with 7, 8 or 9.
for _ in range(int(input())):
    if re.match(r'[789]\d{9}$', input()):
        print('YES')
    else:
        print('NO')
