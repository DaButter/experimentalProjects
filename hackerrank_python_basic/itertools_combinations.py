import itertools

text, count = input().split()
count = int(count)


for i in range(count):
    results = list(itertools.combinations(text, i+1))  # specifies count of chars to slice
    if i > 0:
        for i in range(len(results)):
            # need to sort tuples chars inside tuples
            # make it as a list, sort it, then make it back as a tuple:
            results[i] = tuple(sorted(list(results[i])))
        # then need to sort tuples themselves
        results = sorted(results)
    else:
        results.sort()

    # print sorted:
    for j in range(len(results)):
        print(''.join(results[j]))
