import random
import time


def qsort(l):
    # print(l)
    if not l:
        return l
    pivot = l[0]
    left, right = [], []
    for o in l[1:]:
        if o < pivot:
            left += [o]
        else:
            right += [o]
    # print('%s : %s : %s' % (left, pivot, right))
    return qsort(left) + [pivot] + qsort(right)


def mersort(l):
    x = len(l)
    if x < 2:
        return l
    x //= 2
    left, right = mersort(l[:x]), mersort(l[x:])
    out = []
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]:
            out += [left.pop(0)]
        else:
            out += [right.pop(0)]
    return out + left + right


def bubsort(l):
    l = l[:]
    swap = True
    while swap:
        swap = False
        for i in range(len(l) - 1):
            if l[i] > l[i + 1]:
                l[i], l[i + 1] = l[i + 1], l[i]
                swap = True
    return l


def insort(l):
    l = l[:]
    for i in range(len(l)):
        m = i
        for j in range(i, len(l)):
            if l[j] < l[m]:
                m = j
        l[i], l[m] = l[m], l[i]
    return l


l = [random.randrange(-1000, 1000, 1) for i in range(2000)]


def record(f):
    def x(*args, **kwargs):
        s = time.time()
        return f(*args, **kwargs), time.time() - s

    return x


def fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a+b


def gr():
    total, no, old = 0, 0, 1
    for f in fib():
        total += (f/old)
        no += 1
        old = f
        yield f, total/no


def add(*args):
    return sum(args)

