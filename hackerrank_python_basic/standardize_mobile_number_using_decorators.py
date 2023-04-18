def wrapper(f):
    def fun(l):
        f(["+91 "+c[-10:-5]+" "+c[-5:] for c in l])
    return fun


# The wrapper function is then used as a decorator on the sort_phone
# function using the @wrapper syntax.
# This means that whenever the sort_phone function is called,
# it is automatically wrapped with the wrapper function,
# which modifies the phone numbers in the input list before passing it to sort_phone
@wrapper
def sort_phone(l):
    print(*sorted(l), sep='\n')


if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    sort_phone(l)


