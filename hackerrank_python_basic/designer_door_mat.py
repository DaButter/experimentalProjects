N, M = input().split()  # height, width
N = int(N)
M = int(M)

# Symbols used for doormat
sym_line = '-'
sym_decor = '.|.'
sym_text = "WELCOME"

# Generate pattern
counter = 1
for a in range(N):
    if a < (N-1)/2:
        print((sym_decor*counter).center(M, sym_line))
        counter += 2
    elif a == (N-1)/2:
        print(sym_text.center(M, sym_line))
    else:
        counter -= 2
        print((sym_decor*counter).center(M, sym_line))
