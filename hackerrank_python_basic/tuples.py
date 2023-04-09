if __name__ == '__main__':
    # Get input from user
    # random.seed(2)
    n = int(input())
    input_list = input().split()

    # Convert input_list to a tuple using tuple() constructor
    t = tuple(map(int, input_list))

    # Print the resulting tuple
    print(t)
    print(hash(t))
