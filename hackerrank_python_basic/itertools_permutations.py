import itertools

text, count = input().split()
count = int(count)


results = list(itertools.permutations(text, count))
results.sort()

for i in range(len(results)):
    print(''.join(results[i]))
