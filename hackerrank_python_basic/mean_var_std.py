import numpy as np

n, m = map(int, input().split())
k = np.array([input().split() for _ in range(n)], dtype=int)

std_dev = np.std(k)
print(np.mean(k, axis=1), np.var(k, axis=0), round(std_dev, 11), sep='\n')
