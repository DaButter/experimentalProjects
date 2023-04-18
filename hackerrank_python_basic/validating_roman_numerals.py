import re

thousand = 'M{0,3}'
hundred = '(C[MD]|D?C{0,3})'
ten = '(X[CL]|L?X{0,3})'
ones = '(I[VX]|V?I{0,3})'

regex_pattern = r"%s%s%s%s$" % (thousand, hundred, ten, ones)  # Do not delete 'r'

print(str(bool(re.match(regex_pattern, input()))))
