def average(array):
    mark_sum = sum(set(array))
    average_value = mark_sum/len(set(array))
    return average_value


if __name__ == '__main__':
    # input count of marks
    N = int(input())

    # inpyt all marks
    marks = input().split()
    marks = [int(x) for x in marks]

    result = round(average(marks), 3)
    print(result)
