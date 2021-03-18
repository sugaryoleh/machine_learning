from pandas import Series, DataFrame

d = {'one':Series([1, 2, 3], index=['a', 'b', 'c'], dtype=int),
     'two':Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'], dtype=int)
     }
df = DataFrame(d)

