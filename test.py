logLength = 0


def back_print(log: str):
    global logLength
    back_str = logLength * '\b'
    print(back_str + log, end="")
    logLength = len(log)


if __name__ == '__main__':
    task_name = "概率论与数理统计"
    day = 77
    reverse = True

    num_list = range(day) if not reverse else range(day- 1, -1, -1)
    for i in num_list:
        print(f"{task_name}第{i+1}天计划")
