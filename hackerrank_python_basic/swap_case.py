def swap_case(s):
    s = s.swapcase()
    return s


if __name__ == '__main__':
    input_string = input()
    result = swap_case(input_string)
    print(result)
