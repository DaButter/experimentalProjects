for _ in range(int(input())):
    countB, A, countA, B = input(), set(input().split()), input(), set(input().split())
    print(A.issubset(B))
