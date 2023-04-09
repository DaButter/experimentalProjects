user_list = []
input_list = []

if __name__ == '__main__':
    N = int(input())
    for _ in range(N):
        try:
            line = input().strip()
            if not line:
                continue
            input_list.append(line)
        except EOFError:
            break

    print(f"All user commands: {input_list}")
    for command in range(len(input_list)):
        command_name, *command_index = input_list[command].split()
        print(f"Command name: {command_name}")
        print(f"Command indexes: {command_index}")

        if command_name == "print":
            print(user_list)
        if command_name == "insert":
            user_list.insert(int(command_index[0]), int(command_index[1]))
        if command_name == "append":
            user_list.append(int(command_index[0]))
        if command_name == "reverse":
            user_list.reverse()
        if command_name == "sort":
            user_list.sort()
        if command_name == "pop":
            user_list.pop(len(user_list)-1)
        if command_name == "remove":
            user_list.remove(int(command_index[0]))
