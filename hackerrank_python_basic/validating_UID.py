import re

# A valid UID must follow the rules below:
# It must contain at least 2 uppercase English alphabet characters.
# It must contain at least 3 digits (0-9).
# It should only contain alphanumeric characters (a-z,A-Z & 0-9).
# No character should repeat.
# There must be exactly 10 characters in a valid UID.

for _ in range(int(input())):
    u = ''.join(sorted(input()))
    try:
        assert re.search(r'[A-Z]{2}', u)
        assert re.search(r'\d\d\d', u)
        assert not re.search(r'[^a-zA-Z0-9]', u)
        assert not re.search(r'(.)\1', u)
        assert len(u) == 10
    except:
        print('Invalid')
    else:
        print('Valid')
