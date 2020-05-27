import os


def generator():
    cnt = 0
    while True:
        yield f'{os.getpid()}_{cnt}_qw'
        cnt += 1


gen = generator()
