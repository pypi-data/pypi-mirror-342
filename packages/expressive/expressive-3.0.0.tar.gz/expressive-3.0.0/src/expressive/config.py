""" Copyright 2025 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy
import sympy

# FIXME this is an unstable API for now which might change between versions
#   in the future, this should have a deprecation system which can at a minimum
#   warn or error about older config settings which have been migrated, in addition
#   to continuing support until some known version
# TODO additionally fixing some schema is critical for a good config system
# TODO config value to delete inherited keys/trees and use the default (which may be absent or None)
CONFIG = {
    "warnings": {},  # TODO keep other sections or centralize?
    "translate_simplify": {  # FUTURE consider splitting
        "parse": {},  # coerce ^ -> ** Pow() warning?
        "build": {
            # attempt to reduce `Sum()` instances
            "sum": {
                # `Sum() is expressly an unevaluated summation
                # set to False to prevent this path, which first tries summation and may do other
                # simplifications on the inner function, always converting to a dedicated
                # function which loops over the given range, which may have symbolic (start,end)
                #
                # many `Sum()` instances can be converted to expressions, potentially avoiding a loop
                # of unknown length, such as here (where the range is not known in advance)
                #   >>> parse_expr("Sum(x, (x, a, b))").replace(Sum,summation)
                #  -a**2/2 + a/2 + b**2/2 + b/2
                # `Sum()` can always be replaced by `summation()`, which may produce a simpler expression
                # or the same or a simpler `Sum()` instance
                "try_algebraic_convert": True,
                # warn users after N seconds if sum() simplification is taking an excessive amount of time
                # set the value
                #  - to some positive integer for a timeout in seconds
                #  - False to disable this and never spawn a thread
                #
                # as this spawns a new Thread, some users who are careful about their thread count
                # or are using some model that clashes with them may want to disable this
                # users can also simplify their `Sum()`s before passing them in
                # similarly, Windows users may find Thread generally problematic and wish to disable this
                # TODO this feels like it would be happier in a warnings meta-section
                # TODO this may make sense as part of a general simplifications thread or process
                #   (processes can be killed and benefit from `fork()`)
                "threaded_timeout_warn": 20,  # seconds, yes this is a huge default
            }
        },
    },
    # "data": {},  # some data choices probably makes sense
    "backend": {
        "numba": {  # others?
            # "fastmath": True,
            # "parallel": True,
            # needs for like distributing cached files on a network share?.. [ISSUE 24]
        },
    },
}

DTYPES_SUPPORTED = {
    # numpy.dtype("bool"):     1,
    numpy.dtype("uint8"):    8,
    numpy.dtype("uint16"):  16,
    numpy.dtype("uint32"):  32,
    numpy.dtype("uint64"):  64,
    numpy.dtype("int8"):     8,
    numpy.dtype("int16"):   16,
    numpy.dtype("int32"):   32,
    numpy.dtype("int64"):   64,
    numpy.dtype("float32"): 32,
    numpy.dtype("float64"): 64,
    # numpy.dtype("float128"): 128,  # not supported in Numba [ISSUE 65]
    numpy.dtype("complex64"):   64,
    numpy.dtype("complex128"): 128,
    # numpy.dtype("complex256"): 256,
}

# determine a sensible fill value when creating a result array
# only called when
#  - using indexing (indexers exists)
#  - result array wasn't passed (whatever content it has is used)
# see also DTYPES_SUPPORTED
DTYPES_FILLER_HINT = {
    # numpy.dtype("bool"):,  # FUTURE (probably fail hard and force filling)
    numpy.dtype("uint8"):  0,
    numpy.dtype("uint16"): 0,
    numpy.dtype("uint32"): 0,
    numpy.dtype("uint64"): 0,
    numpy.dtype("int8"):  -1,
    numpy.dtype("int16"): -1,
    numpy.dtype("int32"): -1,
    numpy.dtype("int64"): -1,
    numpy.dtype("float32"): numpy.nan,
    numpy.dtype("float64"): numpy.nan,
    numpy.dtype("complex64"):  numpy.nan,
    numpy.dtype("complex128"): numpy.nan,
}

# SymPy floating-point Atoms
SYMPY_ATOMS_FP = (
    # straightforward floats
    sympy.Float,
    # trancendental constants
    sympy.pi,
    sympy.E,
    # FUTURE general scipy.constants support
    # common floating-point functions
    sympy.log,
    sympy.exp,
    # sympy.sqrt,  # NOTE simplifies to Pow(..., Rational(1,2))
    # sympy.cbrt,  #   can be found with expr.match(cbrt(Wild('a')))
    # trig functions
    sympy.sin, sympy.asin, sympy.sinh, sympy.asinh,
    sympy.cos, sympy.acos, sympy.cosh, sympy.acosh,
    sympy.tan, sympy.atan, sympy.tanh, sympy.atanh,
    sympy.cot, sympy.acot, sympy.coth, sympy.acoth,
    sympy.sec, sympy.asec, sympy.sech, sympy.asech,
    sympy.csc, sympy.acsc, sympy.csch, sympy.acsch,
    sympy.sinc,
    sympy.atan2,
    # LambertW?  # FUTURE results in float or complex result [ISSUE 107]
)
