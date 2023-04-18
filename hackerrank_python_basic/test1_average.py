#!/bin/python3

import math
import os
import random
import re
import sys


# write your code here
def avg(*nums):
    print(f"Input values: {nums}")

    sum_all = 0
    for i in range(len(nums)):
        sum_all = sum_all + nums[i]
    return sum_all/len(nums)


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nums = list(map(int, input().split()))
    res = avg(*nums)

    # fptr.write('%.2f' % res + '\n')

    # fptr.close()
