def print_formatted(number):
    # create decimal list
    dec_list = []
    for a in range(number):
        dec_list.append(a+1)
    oct_list = [oct(x) for x in dec_list]
    hex_list = [hex(x) for x in dec_list]
    bin_list = [bin(x) for x in dec_list]

    space_padding_max = " "*(len(bin_list[len(bin_list)-1])-2)
    print(f"Length of last bin_list element: {len(space_padding_max)}")

    for a in range(len(dec_list)):
        if oct_list[a].startswith("0o"):
            oct_list[a] = oct_list[a][2:]
        if hex_list[a].startswith("0x"):
            hex_list[a] = hex_list[a][2:].upper()
        if bin_list[a].startswith("0b"):
            bin_list[a] = bin_list[a][2:]

        space_padding_dec = " "*(len(space_padding_max)-len(str(dec_list[a])))
        space_padding_oct = " "*(len(space_padding_max)-len(str(oct_list[a]))+1)
        space_padding_hex = " "*(len(space_padding_max)-len(str(hex_list[a]))+1)
        space_padding_bin = " "*(len(space_padding_max)-len(str(bin_list[a]))+1)
        print(f"{space_padding_dec}{dec_list[a]}"
              f"{space_padding_oct}{oct_list[a]}"
              f"{space_padding_hex}{hex_list[a]}"
              f"{space_padding_bin}{bin_list[a]}")


if __name__ == '__main__':
    n = int(input())
    print_formatted(n)
