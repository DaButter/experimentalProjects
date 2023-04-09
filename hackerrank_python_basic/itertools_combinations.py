import itertools

text, count = input().split()
count = int(count)


for i in range(count):
    results = list(itertools.combinations(text, i+1))
    if i > 0:
        print("Using sorted()")
        results = sorted(results, key=lambda x: (x[0], x[1]))
        results = sorted(results, key=lambda x: (x[0], x[1] if x[0] != 'H' else x[1::-1]))
    else:
        print("Using sort()")
        results.sort()
    print(results)
    for j in range(len(results)):
        print(''.join(results[j]))
