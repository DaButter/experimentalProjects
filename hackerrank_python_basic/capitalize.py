# Complete the solve function below.
# def solve(s):
#     split_result = s.split()
#     # print(f"Split result: {split_result}")
#     result = []
#     for itr in range(len(split_result)):
#         result.append(split_result[itr].capitalize())
#     # print(f"Result before join: {result}")
#     result = ' '.join(result)
#     print(result)
#     return result

# def solve(s):
#     result = s.title()
#     return result

def solve(s):
    words = s.split(' ')
    print(f"Words splitted: {words}")
    capitalized_words = []
    for word in words:
        if len(word) > 0:
            capitalized_word = word[0].upper() + word[1:]
            print(f"word[0].upper(): {word[0].upper()}, and word[1:]: {word[1:]}")
            capitalized_words.append(capitalized_word)
        else:
            print("I appended a space")
            capitalized_words.append(word)
    result = ' '.join(capitalized_words)
    print(result)
    return result


if __name__ == '__main__':
    s = input()
    result = solve(s)
