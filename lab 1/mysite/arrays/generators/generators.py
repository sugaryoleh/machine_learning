import sys

import numpy as np

class Rounder_1D:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        m = self.func(*args)
        for i, el in enumerate(m):
            m[i] = round(el, 3)
        return m

class Rounder_2D:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        m = self.func(*args)
        for i, row in enumerate(m):
            for j, el in enumerate(row):
                m[i][j] = round(el, 3)
        return m

# base

class CustomRandGenerator:

    __rnd = None
    @staticmethod
    def init():
        raise NotImplementedError()

    @staticmethod
    def generate(*args):
        raise NotImplementedError()

class FloatGenerator_1D(CustomRandGenerator):

    @staticmethod
    def init():
        FloatGenerator_1D.__rnd = np.random

    @staticmethod
    @Rounder_1D
    def generate(*args):
        # return FloatGenerator_1D.rnd.normal(args[0], args[1], args[2])
        return FloatGenerator_1D.__rnd.uniform(low=args[0], high=args[1], size=args[2])

class IntegerGenerator_1D(CustomRandGenerator):

    @staticmethod
    def init():
        IntegerGenerator_1D.__rnd = np.random.default_rng(sys.maxsize)

    @staticmethod
    def generate(*args):
        return IntegerGenerator_1D.__rnd.integers(low=args[0], high=args[1], size=args[2])

class FloatGenerator_2D(FloatGenerator_1D):

    @staticmethod
    def init():
        FloatGenerator_2D.__rnd = np.random

    @staticmethod
    @Rounder_2D
    def generate(*args):
        return FloatGenerator_2D.__rnd.uniform(low=args[0], high=args[1], size=(args[2], args[3]))

class IntegerGenerator_2D(IntegerGenerator_1D):

    @staticmethod
    def init():
        IntegerGenerator_2D.__rnd = np.random.default_rng(sys.maxsize)

    @staticmethod
    def generate(*args):
        return IntegerGenerator_2D.__rnd.integers(low=args[0], high=args[1], size=(args[2], args[3]))

# by task

class Zero_OneGenerator_1D(FloatGenerator_1D):

    @staticmethod
    def generate(cnt):
        FloatGenerator_1D.init()
        return FloatGenerator_1D.generate(0, 1, cnt)

class mTen_TenGenerator_1D(IntegerGenerator_1D):

    @staticmethod
    def generate(cnt):
        IntegerGenerator_1D.init()
        return IntegerGenerator_1D.generate(-10, 10, cnt)

class Zero_FiftyGenerator_1D(IntegerGenerator_1D):

    @staticmethod
    def generate(cnt):
        IntegerGenerator_1D.init()
        return IntegerGenerator_1D.generate(0, 50, cnt)


class Zero_OneGenerator_2D(FloatGenerator_2D):

    @staticmethod
    def generate(n, m):
        FloatGenerator_2D.init()
        return FloatGenerator_2D.generate(0, 1, n, m)

class mTen_TenGenerator_2D(IntegerGenerator_2D):

    @staticmethod
    def generate(n, m):
        IntegerGenerator_2D.init()
        return IntegerGenerator_2D.generate(-10, 10, n, m)

class Zero_FiftyGenerator_2D(IntegerGenerator_2D):

    @staticmethod
    def generate(n ,m):
        IntegerGenerator_2D.init()
        return IntegerGenerator_2D.generate(0, 50, n, m)

a = Zero_OneGenerator_2D.generate(5, 2)

def task_1(array):
    p_el_list=[]
    m_el_list=[]
    for el in array:
        if el < 0:
            m_el_list.append(el)
        else:
            p_el_list.append(el)
    m_el_list.extend(p_el_list)
    return m_el_list

def task_2(matrix):
    l = []
    for i, row in enumerate(matrix):
        if not (i % 2):
            l.append(row.sum())
    return l

m = mTen_TenGenerator_2D.generate(5, 5)
l = task_2(m)
print(m)
print(l)
