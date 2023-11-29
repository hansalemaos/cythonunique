# Fast implementation of unique elements in an array using parallel sorting

## pip install cythonunique

### Tested against Windows / Python 3.11 / Anaconda

## Cython (and a C/C++ compiler) must be installed to use the optimized Cython implementation.


```python

This module provides a fast implementation of unique elements in an array using parallel sorting.

Functions:
- fast_unique(arr): Returns an array containing unique elements from the input array.

import timeit
import numpy as np

from cythonunique import fast_unique


def generate_random_arrays(shape, dtype='float64', low=0, high=1):
    return np.random.uniform(low, high, size=shape).astype(dtype)


size = 10000000
low = 0
high = 254
arras = [
    (size, 'float32', low, high),
    (size, 'float64', low, high),
    (size, np.uint8, low, high),
    (size, np.int8, low, high),
    (size, np.int16, low, high),
    (size, np.int32, low, high),
    (size, np.int64, low, high),
    (size, np.uint16, low, high),
    (size, np.uint32, low, high),
    (size, np.uint64, low, high),
]
reps = 5

for a in arras:
    arr = generate_random_arrays(*a)
    s = """u=fast_unique(arr)"""
    t1 = timeit.timeit(s, globals=globals(), number=reps) / reps
    print(t1)

    s = """u=np.unique(arr)"""
    t2 = timeit.timeit(s, globals=globals(), number=reps) / reps
    print(t2)
    u = fast_unique(arr)
    q = np.unique(arr)
    print(np.all(u == q))
    print('-------------------------')

# 0.10624040000111563
# 0.14222411999944598
# True
# -------------------------
# 0.10455849999998464
# 0.1573818399992888
# True
# -------------------------
# 0.03686119999911171
# 0.0845491200001561
# True
# -------------------------
# 0.03726967999973567
# 0.08551521999906982
# True
# -------------------------
# 0.038274600000295325
# 0.10370338000066112
# True
# -------------------------
# 0.046226339999702756
# 0.10226724000094692
# True
# -------------------------
# 0.06615012000111165
# 0.1257952400002978
# True
# -------------------------
# 0.04093761999974958
# 0.10167090000031749
# True
# -------------------------
# 0.04656872000050498
# 0.10330443999991985
# True
# -------------------------
# 0.06586845999991056
# 0.13191485999996075
# True
# -------------------------

```