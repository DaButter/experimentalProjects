if __name__ == '__main__':
    student_list = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        student_list.append([name, score])

    print(f"Full student list: {student_list}")

    # find second-lowest score
    # set() removes duplicate scores
    sorted_scores = sorted(set([x[1] for x in student_list]))
    second_lowest_score = sorted_scores[1]
    print(f"second_lowest_score: {second_lowest_score}")

    # find student names with second-lowest score
    second_lowest_students = []
    for name, score in sorted(student_list):
        if score == second_lowest_score:
            second_lowest_students.append(name)

    # print sorted student names in alphabetical order
    second_lowest_students = sorted(second_lowest_students)
    for element in second_lowest_students:
        print(element)
