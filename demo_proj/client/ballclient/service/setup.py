# -*- coding=UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("GBK")
from distutils.core import setup
from Cython.Build import cythonize
import numpy as np
setup(
    ext_modules=cythonize("djs.pyx"),
    include_dirs=[np.get_include()]
)
