if __name__ == '__main__':
    # input number of integers
    n = int(input())
    # input the array, integer coynt = n
    arr = list(map(int, input().split()))

    maxScore = max(arr)
    oldDiff = maxScore*2+1
    runnerUpIndex = 0

    for i in range(n):
        newDiff = abs(maxScore - arr[i])
        # print(f"newDiff: {newDiff}")
        # print(f"oldDiff: {oldDiff}")
        if newDiff == 0:
            continue
        if oldDiff > newDiff:
            oldDiff = newDiff
            runnerUpIndex = i

    # print(f"Max value is: {maxScore}")
    # print(f"Runner up value: {arr[runnerUpIndex]}")
    print(arr[runnerUpIndex])
