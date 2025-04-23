import numpy as np
import sys
import time


def f_one(x):
    dim = 4
    coef_1 = np.array([0, 4, 1, 2])

    ans = 1.0
    ans -= np.exp(-np.linalg.norm(x-coef_1)**2*0.001)
    return ans


def f_multi(x):
    dim = 4
    coef_1 = np.array([1, 8, 7, 7])
    coef_2 = np.array([0, 4, 1, 2])

    ans = 3.0
    ans -= np.exp(-np.linalg.norm(x-coef_1)**2*0.001)
    ans -= np.exp(-np.linalg.norm(x-coef_2)**2*0.001) * 2
    return ans


def one():
    print("Please input 4 dimensional vector: ", end="", file=sys.stderr)
    x = list(map(float, input().split()))

    for ii in range(5):
        print("\r{}".format(5-ii), end="", file=sys.stderr)
        time.sleep(1)
    print("\r{}".format(f_one(x)), file=sys.stderr)
    print("{},{},{},{},{}".format(x[0], x[1], x[2], x[3], f_one(x)))

def multi():
    print("Please input 4 dimensional vector: ", end="", file=sys.stderr)
    x = list(map(float, input().split()))

    for ii in range(5):
        print("\r{}".format(5-ii), end="", file=sys.stderr)
        time.sleep(1)

    print("\r{}".format(f_multi(x)), file=sys.stderr)
    print("{},{},{},{},{}".format(x[0], x[1], x[2], x[3], f_multi(x)))

