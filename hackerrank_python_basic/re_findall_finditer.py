import re

v = "aeiou"
c = "qwrtypsdfghjklzxcvbnm"

m = re.findall(r"(?<=[%s])([%s]{2,})[%s]" % (c, v, c), input(), flags=re.I)

print('\n'.join(m or ['-1']))


# Useful notes:
# re.findall()
# The expression re.findall() returns all the non-overlapping matches of patterns in a string as a list of strings
# >>> import re
# >>> re.findall(r'\w','http://www.hackerrank.com/')
# ['h', 't', 't', 'p', 'w', 'w', 'w', 'h', 'a', 'c', 'k', 'e', 'r', 'r', 'a', 'n', 'k', 'c', 'o', 'm']

# re.finditer()
# The expression re.finditer() returns an iterator yielding MatchObject instances over all non-overlapping matches for the re pattern in the string.
# >>> import re
# >>> re.finditer(r'\w', 'http://www.hackerrank.com/')
# < callable - iterator object at 0x0266C790 >
# >>> map(lambda x: x.group(), re.finditer(r'\w', 'http://www.hackerrank.com/'))
# ['h', 't', 't', 'p', 'w', 'w', 'w', 'h', 'a', 'c', 'k', 'e', 'r', 'r', 'a', 'n', 'k', 'c', 'o', 'm']



