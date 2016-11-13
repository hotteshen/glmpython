#!/usr/bin/env python3

import parseme

glmParse = parseme.Project()

# In the VECTORQUAT section,
# vectorquat is 'vec' for vectors and 'quat' for quaternions
# p is a prefix to the name
# n is the number of components in the vector
# type is the common type of the vector
# Make sure to include all three of a type because swizzling relies on them
VECTORQUAT = parseme.Section('VECTORQUAT')

# vectors
for t in (('', 'float'), ('i', 'int')):
    for n in range(2, 5):
        VECTORQUAT.add(parseme.Round(vectorquat='vec', p = t[0], n = n, m = str(n), type = t[1]))
# quaternion
VECTORQUAT.add(parseme.Round(vectorquat='quat', p = '', n = 4, m = '', type = 'float'))

glmParse.add(VECTORQUAT)

VECTORQUAT_MATH = parseme.Section('VECTORQUAT_MATH')
VECTORQUAT_MATH.add(parseme.Round(s = '+', f = 'add', only = None))
VECTORQUAT_MATH.add(parseme.Round(s = '-', f = 'subtract', only = None))
VECTORQUAT_MATH.add(parseme.Round(s = '*', f = 'multiply', only = None))
VECTORQUAT_MATH.add(parseme.Round(s = '/', f = 'true_divide', only = None))
VECTORQUAT_MATH.add(parseme.Round(s = '<<', f = 'lshift', only = 'int'))
VECTORQUAT_MATH.add(parseme.Round(s = '>>', f = 'rshift', only = 'int'))
VECTORQUAT_MATH.add(parseme.Round(s = '&', f = 'and', only = 'int'))
VECTORQUAT_MATH.add(parseme.Round(s = '^', f = 'xor', only = 'int'))
VECTORQUAT_MATH.add(parseme.Round(s = '|', f = 'or', only = 'int'))

glmParse.add(VECTORQUAT_MATH)

# In the MATRIX section,
# p is a prefix to the name
# cols and rows is the size of the vector
# type is the common type of the vector
# n is the name, such as 3x4
MATRIX = parseme.Section('MATRIX')
for cols in range(2, 5):
    for rows in range(2, 5):
        MATRIX.add(parseme.Round(p = '', rows = rows, cols = cols,
            n = (str(rows) if rows == cols else str(rows) + 'x' + str(cols)), type = 'float'))
glmParse.add(MATRIX)

# In the MATRIX_FUNCTION section,
# func is the name of the function
# func_doc is the doc string
# args is the type of arguments
# availableTo is which types support it
# path is the glm namespace path

# Matrix Transform

MATRIX_FUNCTION = parseme.Section('MATRIX_FUNCTION')
MATRIX_FUNCTION.add(parseme.Round(
    func = 'translate',
    func_doc = 'Translates a 4x4 matrix.',
    args = ('vec3',),
    availableTo = ('4',),
    path = ''
))
MATRIX_FUNCTION.add(parseme.Round(
    func = 'rotate',
    func_doc = 'Rotates a 4x4 matrix.',
    args = (float, 'vec3',),
    availableTo = ('4',),
    path = ''
))
MATRIX_FUNCTION.add(parseme.Round(
    func = 'scale',
    func_doc = 'Scales a 4x4 matrix.',
    args = ('vec3',),
    availableTo = ('4',),
    path = ''
))

# Core

MATRIX_FUNCTION.add(parseme.Round(
    func = 'inverse',
    func_doc = 'Matrix\'s inverse.',
    args = (),
    availableTo = ('2','3','4',),
    path = ''
))
MATRIX_FUNCTION.add(parseme.Round(
    func = 'transpose',
    func_doc = 'Matrix\'s transpose.',
    args = (),
    # availableTo = ('2','3','4','2x3','3x2','2x4','4x2','3x4','4x3'),
    availableTo = ('2','3','4'),
    path = ''
))

glmParse.add(MATRIX_FUNCTION)

# In the VECTORQUAT_FUNCTION section,
# vectorquat is 'vec' for vectors and 'quat' for quaternions
# func is the name of the function
# func_doc is the doc string
VECTORQUAT_FUNCTION = parseme.Section('VECTORQUAT_FUNCTION')
VECTORQUAT_FUNCTION.add(parseme.Round(func = 'abs', func_doc = 'Absolute value.'))
glmParse.add(VECTORQUAT_FUNCTION)

# In the NUMBER_FUNCTION section,
# func is the name of the function
# func_doc is the doc string
# argc is the number of arguments
# argoc is the number of optional arguments
# returns is the return type
# type is the argument type
# p is the short name of the in type, used to build value
# base the base type of the return
# path is the path to the function, i.e.
NUMBER_FUNCTION = parseme.Section('NUMBER_FUNCTION')

NUMBER_FUNCTION.add(
    parseme.Round(
        func = 'ortho',
        func_doc = 'Creates an orthographic matrix.',
        argc = 4,
        argoc = 2,
        returns = 'mat4',
        type = 'float',
        p = 'f',
        base = 'mat',
        path = ''
    )
)
NUMBER_FUNCTION.add(
    parseme.Round(
        func = 'frustum',
        func_doc = 'Creates a frustum matrix.',
        argc = 6,
        argoc = 0,
        returns = 'mat4',
        type = 'float',
        p = 'f',
        base = 'mat',
        path = ''
    )
)
NUMBER_FUNCTION.add(
    parseme.Round(
        func = 'perspective',
        func_doc = 'Creates a perspective matrix.',
        argc = 4,
        argoc = 0,
        returns = 'mat4',
        type = 'float',
        p = 'f',
        base = 'mat',
        path = ''
    )
)
NUMBER_FUNCTION.add(
    parseme.Round(
        func = 'perspectiveFov',
        func_doc = 'Creates a perspective matrix with a defined FOV.',
        argc = 5,
        argoc = 0,
        returns = 'mat4',
        type = 'float',
        p = 'f',
        base = 'mat',
        path = ''
    )
)

glmParse.add(NUMBER_FUNCTION)

# In the EXTRA_FUNCTION section,
# func is the name of the function
# func_doc is the doc string
# args is the type of arguments
# returns is the return type
# type is the common type of the matrix and vector
# path is the path to the function, i.e.
EXTRA_FUNCTION = parseme.Section('EXTRA_FUNCTION')

EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'lookAt',
        func_doc = 'Creates a look at view matrix.',
        args = ('vec3', 'vec3', 'vec3',),
        returns = 'mat4',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'project',
        func_doc = 'Map object coordinates into window coordinates.',
        args = ('vec3', 'mat4', 'mat4', 'vec4',),
        returns = 'vec3',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'unProject',
        func_doc = 'Map window coordinates into object coordinates.',
        args = ('vec3', 'mat4', 'mat4', 'vec4',),
        returns = 'vec3',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'cross',
        func_doc = 'Cross product.',
        args = ('vec3', 'vec3',),
        returns = 'vec3',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'dot',
        func_doc = 'Dot product.',
        args = ('vec3', 'vec3',),
        returns = 'float',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'angleAxis',
        func_doc = 'Build a quaternion from an angle and a normalized axis.',
        args = (float, 'vec3',),
        returns = 'quat',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'toMat4',
        func_doc = 'Converts a quaternion to a 4 * 4 matrix.',
        args = ('quat',),
        returns = 'mat4',
        type = 'float',
        path = ''
    )
)
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'normalize',
        func_doc = 'Returns a vector in the same direction but with length of 1.',
        acceptedArgs = ('vec2', 'vec3', 'vec4', 'quat',),
        type = 'float',
        path = ''
    )
)
glmParse.add(EXTRA_FUNCTION)


BASETYPEDEF = parseme.Section('BASETYPEDEF')
BASETYPEDEF.add(parseme.Round(type = 'Vector', doc = 'This is a basic vector type that you can isinstance against.  It is also used for global function checking, and in theory you could make your own vector types which define custom calls for global functions.'))
BASETYPEDEF.add(parseme.Round(type = 'Matrix', doc = 'A matrix.'))
BASETYPEDEF.add(parseme.Round(type = 'Quaternion', doc = 'This is a quaternion type that you can isinstance against.  It is also used for global function checking, and in theory you could make your own quaternion types which define custom calls for global functions.'))
glmParse.add(BASETYPEDEF)

if glmParse.parse('python.parseme.hpp', 'python.parseme.cpp') > 0:
    raise SystemExit

import shutil, os
from distutils.core import setup, Extension

glm = Extension('glm', sources = ['python.cpp'], include_dirs = ['../'])

setup(name='glm',
      version='0.9.3',
      description='glm',
      author='JacobF | G-Truc Creation',
      author_email='jacobaferrero@gmail.com | glm@g-truc.net',
      url='http://glm.g-truc.net/',
      ext_modules=[glm]
)
