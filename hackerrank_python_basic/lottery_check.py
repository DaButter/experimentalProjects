def check_win(N):
    ls = [10, 34, 35, 19, 23, 17, 14, 38]
    for i in range(len(ls)):
        if ls[i] == N:
            print(f"You won!!!!! No.: {N}")
            return
    print(f"No. {N} did not win!")


if __name__ == '__main__':
    while True:
        N = int(input())
        if N == 0:
            break
        check_win(N)

