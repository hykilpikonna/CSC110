# Output two different ways you can enter a time duration on the microwave
if __name__ == '__main__':
    while True:
        s = int(input())
        print(f'{s // 60}:{s % 60:02}')
        if s >= 60:
            print(f'{s // 60 - 1}:{s - (s // 60 - 1) * 60:02}')
