def is_leap(year):
    if year < 1990 or year > 10**5:
        print("Input years out of predefined bounds!")
        return "fail"
    if year % 4 == 0:
        leap = True
        if year % 100 == 0:
            if year % 400 == 0:
                leap = True
            else:
                leap = False
    else:
        leap = False
    return leap


yearInput = int(input())
print(is_leap(yearInput))
