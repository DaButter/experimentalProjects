if __name__ == '__main__':
    n = int(input())
    student_marks = {}  # creates an empty dictionary
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()

    marks = student_marks[query_name]
    print(marks)

    mark_sum, mark_count = 0, 0
    for a in range(len(marks)):
        mark_sum += marks[a]
        mark_count += 1

    print(f"Mark sum: {mark_sum}")
    print(f"Mark count: {mark_count}")

    average_mark = mark_sum/mark_count
    print("{:.2f}".format(average_mark))

# Example program I/O:
# 2
# dog 10 20 30
# cat 30 40 50
# cat
# [30.0, 40.0, 50.0]
# Mark sum: 120.0
# Mark count: 3
# 40.00