# if __name__ == '__main__':
    # x = int(input())
    # y = int(input())
    # z = int(input())
    # n = int(input())
x = 2
y = 2
z = 2
n = 2

ListOfNumbers = [[a, b, c] for a in range(x+1) for b in range(y+1) for c in range(z+1) if (a+b+c)!=n]
print(ListOfNumbers)