logLength = 0


def back_print(log: str):
    global logLength
    back_str = logLength * '\b'
    print(back_str + log, end="")
    logLength = len(log)


if __name__ == '__main__':
    flag = False

    res = 1 if flag else 2

    print(res)
