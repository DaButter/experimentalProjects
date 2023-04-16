from itertools import combinations_with_replacement

text, count = input().split()
count = int(count)

results = list(combinations_with_replacement(text, count))

if count > 1:
    for i in range(len(results)):
        # need to sort tuples chars inside tuples
        # make it as a list, sort it, then make it back as a tuple:
        results[i] = tuple(sorted(list(results[i])))
    # then need to sort tuples themselves
    results = sorted(results)
else:
    results.sort()

for j in range(len(results)):
    print(''.join(results[j]))
