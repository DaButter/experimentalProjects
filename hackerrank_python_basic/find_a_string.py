def count_substring(string, sub_string):
    match_index = 0
    count = 0
    while True:
        match_index = string.find(sub_string, match_index, len(string))
        if match_index == -1:
            # did not find matching string, end loop
            break
        match_index += 1
        count += 1
    return count


if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()

    count = count_substring(string, sub_string)
    print(count)
