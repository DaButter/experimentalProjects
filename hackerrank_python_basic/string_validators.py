if __name__ == '__main__':
    s = input()
    # isalnum()  # checks if all the characters of a string are alphanumeric (a-z, A-Z and 0-9)
    # isalpha()  # checks if all the characters of a string are alphabetical (a-z and A-Z)
    # isdigit()  # checks if all the characters of a string are digits (0-9)
    # islower()  # checks if all the characters of a string are lowercase characters (a-z)
    # isupper()  # checks if all the characters of a string are uppercase characters (A-Z)

    input_list = list(s)
    isAlNum, isAlpha, isDigit, isLower, isUpper = (False,)*5
    for i in range(len(input_list)):
        if input_list[i].isalnum():
            isAlNum = True
        if input_list[i].isalpha():
            isAlpha = True
        if input_list[i].isdigit():
            isDigit = True
        if input_list[i].islower():
            isLower = True
        if input_list[i].isupper():
            isUpper = True
    print(isAlNum)
    print(isAlpha)
    print(isDigit)
    print(isLower)
    print(isUpper)
