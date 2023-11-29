import os
import subprocess
import sys
import numpy as np


def _dummyimport():
    import Cython


try:
    from .fastuniq import fastuni
except Exception as e:
    cstring = r"""# distutils: language=c++
# distutils: extra_compile_args=/openmp
# distutils: extra_link_args=/openmp
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=True
# cython: language_level=3
cimport cython
import numpy as np
cimport numpy as np
import cython


ctypedef fused parasort:
    cython.char
    cython.uchar
    cython.short
    cython.ushort
    cython.int
    cython.uint
    cython.long
    cython.ulong
    cython.longlong
    cython.ulonglong
    cython.float
    cython.double


cdef extern from "<ppl.h>" namespace "concurrency":
    cdef void parallel_sort[T](T first, T last) nogil

cdef void parallelsort(parasort[:] a):
    parallel_sort(&a[0], &a[a.shape[0]])

cpdef void fastuni(parasort[:] arr,parasort[:] resultarray,  cython.int[:] lastval):
    parallelsort(arr)
    cdef Py_ssize_t i
    cdef Py_ssize_t j=1
    cdef Py_ssize_t k=0
    cdef Py_ssize_t arralen=arr.shape[0]
    resultarray[0]=arr[0]
    with nogil:
        for i in range(1,arralen):
            if(arr[i]!=arr[k]):
                
                resultarray[j]=arr[i]
                lastval[0]=j
                j+=1
            k+=1
    
"""
    pyxfile = f"fastuniq.pyx"
    pyxfilesetup = f"fastuniqcompiled_setup.py"

    dirname = os.path.abspath(os.path.dirname(__file__))
    pyxfile_complete_path = os.path.join(dirname, pyxfile)
    pyxfile_setup_complete_path = os.path.join(dirname, pyxfilesetup)

    if os.path.exists(pyxfile_complete_path):
        os.remove(pyxfile_complete_path)
    if os.path.exists(pyxfile_setup_complete_path):
        os.remove(pyxfile_setup_complete_path)
    with open(pyxfile_complete_path, mode="w", encoding="utf-8") as f:
        f.write(cstring)
    numpyincludefolder = np.get_include()
    compilefile = (
            """
	from setuptools import Extension, setup
	from Cython.Build import cythonize
	ext_modules = Extension(**{'py_limited_api': False, 'name': 'fastuniq', 'sources': ['fastuniq.pyx'], 'include_dirs': [\'"""
            + numpyincludefolder
            + """\'], 'define_macros': [], 'undef_macros': [], 'library_dirs': [], 'libraries': [], 'runtime_library_dirs': [], 'extra_objects': [], 'extra_compile_args': [], 'extra_link_args': [], 'export_symbols': [], 'swig_opts': [], 'depends': [], 'language': None, 'optional': None})

	setup(
		name='fastuniq',
		ext_modules=cythonize(ext_modules),
	)
			"""
    )
    with open(pyxfile_setup_complete_path, mode="w", encoding="utf-8") as f:
        f.write(
            "\n".join(
                [x.lstrip().replace(os.sep, "/") for x in compilefile.splitlines()]
            )
        )
    subprocess.run(
        [sys.executable, pyxfile_setup_complete_path, "build_ext", "--inplace"],
        cwd=dirname,
        shell=True,
        env=os.environ.copy(),
    )
    try:
        from .fastuniq import fastuni
    except Exception as fe:
        sys.stderr.write(f'{fe}')
        sys.stderr.flush()


def fast_unique(arr):
    try:
        a = np.ascontiguousarray(arr)
        b = np.zeros_like(a)
        c = np.array([0], dtype=np.int32)
        fastuni(a, b, c)
        return b[:c[0] + 1]
    except Exception as fe:
        sys.stderr.write(f'{fe} - trying it with numpy\n')
        sys.stderr.flush()
        return np.unique(arr)
