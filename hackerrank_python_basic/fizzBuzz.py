#!/bin/python3


def fizzBuzz(n):
    for i in range(n):
        if (i+1) % 3 == 0 and (i+1) % 5 == 0:
            print("FizzBuzz")
        elif (i+1) % 3 == 0:
            print("Fizz")
        elif (i+1) % 5 == 0:
            print("Buzz")
        else:
            print(i+1)


if __name__ == '__main__':
    n = int(input().strip())
    fizzBuzz(n)
