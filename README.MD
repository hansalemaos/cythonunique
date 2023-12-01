# Fast implementation of unique elements in an array - up to 30x faster than NumPy

## pip install cythonunique

### Tested against Windows / Python 3.11 / Anaconda

## Cython (and a C/C++ compiler) must be installed to use the optimized Cython implementation.


```python
import timeit
import numpy as np

from cythonunique import fast_unique


def generate_random_arrays(shape, dtype='float64', low=0, high=1):
    return np.random.uniform(low, high, size=shape).astype(dtype)


def fast_unique_ordered(a):
    return fast_unique(a, accept_not_ordered=False)


def fast_unique_not_ordered(a):
    return fast_unique(a, accept_not_ordered=True, uint64limit=4294967296)


size = 10000000
low = 0
high = 100000000
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
print('Ordered --------------------------')

for a in arras:
    arr = generate_random_arrays(*a)
    s = """u=fast_unique_ordered(arr)"""
    t1 = timeit.timeit(s, globals=globals(), number=reps) / reps
    print('c++ ', t1)

    s = """u=np.unique(arr)"""
    t2 = timeit.timeit(s, globals=globals(), number=reps) / reps
    print('np ', t2)
    u = fast_unique_ordered(arr)
    q = np.unique(arr)
    print(np.all(u == q))
    print('-------------------------')

print('Unordered --------------------------') # Falls back to Ordered if dtype is float or np.min(a)<0
for a in arras:
    arr = generate_random_arrays(*a)
    s = """u=fast_unique_not_ordered(arr)"""
    t1 = timeit.timeit(s, globals=globals(), number=reps) / reps
    print('c++ ', t1)

    s = """u=np.unique(arr)"""
    t2 = timeit.timeit(s, globals=globals(), number=reps) / reps
    print('np ', t2)
    u = fast_unique_not_ordered(arr)
    q = np.unique(arr)
    print(np.all(np.sort(u) == q))
    print('-------------------------')

# Ordered --------------------------
# c++  0.10320082000107504
# np  0.13888095999718644
# True
# -------------------------
# c++  0.10645331999985501
# np  0.14625759999908042
# True
# -------------------------
# c++  0.03644101999816485
# np  0.0833885799976997
# True
# -------------------------
# c++  0.03784457999863662
# np  0.08405877999903169
# True
# -------------------------
# c++  0.03909369999892078
# np  0.09831685999815817
# True
# -------------------------
# c++  0.045269479998387395
# np  0.0970024200010812
# True
# -------------------------
# c++  0.06357002000149806
# np  0.12426133999833837
# True
# -------------------------
# c++  0.04224961999861989
# np  0.09802825999795459
# True
# -------------------------
# c++  0.046695440000621605
# np  0.10013775999832433
# True
# -------------------------
# c++  0.06854987999831792
# np  0.1277739599987399
# True
# -------------------------
# Unordered --------------------------
# c++  0.10427475999749732
# np  0.13533045999938623
# True
# -------------------------
# c++  0.1188001600006828
# np  0.14714665999927093
# True
# -------------------------
# c++  0.011010520000127144
# np  0.2836028199992143
# True
# -------------------------
# c++  0.03693970000022091
# np  0.08278198000043631
# True
# -------------------------
# c++  0.021734919998561964
# np  0.29412690000026487
# True
# -------------------------
# c++  0.02548580000002403
# np  0.29879269999801183
# True
# -------------------------
# c++  0.030021439999109133
# np  0.31899350000021515
# True
# -------------------------
# c++  0.012441499999840743
# np  0.28925163999956566
# True
# -------------------------
# c++  0.015460380000877193
# np  0.2964318199985428
# True
# -------------------------
# c++  0.026127819999237543
# np  0.31972092000069097
# True
# -------------------------


```