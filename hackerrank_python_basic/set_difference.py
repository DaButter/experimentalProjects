# Enter your code here. Read input from STDIN. Print output to STDOUT
count1 = int(input())
set1 = set(map(int, input().split()))

count2 = int(input())
set2 = set(map(int, input().split()))

print(len(set1-set2))
