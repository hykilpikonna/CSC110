def p(x):
    return 1 < x < 8


def q(x):
    return x < 8


if __name__ == '__main__':
    print('Statement 1:', all([p(x) and q(x) for x in range(10)]))
    print('Statement 2:', all([not p(x) or q(x) for x in range(10)]))
