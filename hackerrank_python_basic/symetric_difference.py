if __name__ == '__main__':
    input1_size = input()
    input1 = input().split()
    input2_size = input()
    input2 = input().split()

    set1 = set(list(map(int, input1)))
    set2 = set(list(map(int, input2)))

    print(f"set 1: {set1}")
    print(f"set 2: {set2}")

    diff1 = set1.difference(set2)
    print(diff1)
    diff2 = set2.difference(set1)
    print(diff2)

    # Need to combine diff1 and diff2 and sort in ascending order, one per line
    diff1_list = list(diff1)
    diff2_list = list(diff2)
    diff_list = diff1_list + diff2_list
    diff_list.sort()
    for a in range(len(diff_list)):
        print(diff_list[a])
