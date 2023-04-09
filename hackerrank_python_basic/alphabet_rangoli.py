# def print_rangoli(size):
#     center_length = 1
#     for _ in range(size-1):
#         center_length += 2
#
#     print(f"Count of center letters: {center_length}")
#     center_length_all = 2*center_length-1
#     print(f"Count of center symbols: {center_length_all}")
#
#     # get list of used chars
#     chars = []
#     for a in range(size):
#         chars.append(chr(96+size-a))
#     print(f"List of used chars: {chars}")
#
#     # generate rangoli
#     for itr in range(size*2-1):
#         if itr == 0 or itr == size*2-2:
#             # print the first and last lines with only one character in the center
#             print(chars[0].center(center_length_all, '-'))
#         else:
#             # stuck here
#
# if __name__ == '__main__':
#     n = int(input())
#     print_rangoli(n)


def print_rangoli(size):
    # Calculate the length of the center line
    center_length_char = size*2 - 1
    center_length = center_length_char*2 - 1
    print(f"Center length: {center_length}")

    # create a list of characters to use in the rangoli
    alphabet = [chr(ord('a')+i) for i in range(size)]
    print(f"Alphabet: {alphabet}")

    # print the top half of the rangoli
    for i in range(size-1, -1, -1):
        row_chars = alphabet[size-1:i:-1] + alphabet[i:size]
        print('-'.join(row_chars).center(center_length, '-'))

    # print the bottom half of the rangoli
    for i in range(1, size):
        row_chars = alphabet[size-1:i:-1] + alphabet[i:size]
        print('-'.join(row_chars).center(center_length, '-'))


if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)
