# Analysis of `glmpython` as `Parseme` Utilization

## `setup.py`

working `parseme` specification for `glm.perspective()`
```python
NUMBER_FUNCTION.add(
    parseme.Round(
        func = 'perspective',   # module function name
        func_doc = 'Creates a perspective matrix.', # docstring
        argc = 4,               # arguments count
        argoc = 0,              # optional arguments count
        returns = 'mat4',       # return type
        type = 'float',         # argument type
        p = 'f',                # short name of the in type
        base = 'mat',           # base type of the return
        path = ''               # glm namespace path to the function
    )
)
```

`glm` source for `glm::lookAt()`
```
template <typename T, precision P>
GLM_FUNC_DECL tmat4x4<T, P> lookAt(
    tvec3<T, P> const & eye,
    tvec3<T, P> const & center,
    tvec3<T, P> const & up);
```

draft `parseme` specification for `glm.lookAt()`
```python
VECTOR3_FUNCTION.add(
    parseme.Round(
        func = 'lookAt',        # module function name
        func_doc = 'Creates a view matrix.',    # docstring
        argc = 3,               # arguments count
        argoc = 0,              # optional arguments count
        returns = 'mat4',       # return type
        type = 'glm::vec3',     # argument type
        #p = 'f',               # short name of the in type
        base = 'mat',           # base type of the return
        path = ''               # glm namespace path to the function
    )
)
```

expected C++ expansion for `glm::lookAt()`
```
PyObject *glm_function_lookAt(PyObject *module, PyObject *args) {
    glm::vec3 a0;
    glm::vec3 a1;
    glm::vec3 a2;

    if(!PyArg_ParseTuple(args, "ffff|:perspective", /* `ffff` for four float arguments,
                                                       `|` marks the begining of optional arguments,
                                                       `:` marks the end of format units list
                                                       `perspective` function name to be used in error messages
                                                    */
    &a0,
    &a1,
    &a2,
    &a3
    ))
        return NULL;

    PyObject *result = PyObject_CallObject((PyObject *)&glm_mat4Type, NULL);

    ((glm_mat4 *)result)->mat =
    glm::perspective<float>(
    a0,
    a1,
    a2,
    a3
);
```

## `python.parseme.cpp` and `python.cpp`

working `python.parseme.cpp` source for `NUMBER_FUNCTION`
```
/*$ NUMBER_FUNCTION $*/
PyObject *glm_function_${func}(PyObject *module, PyObject *args) {
/*$ {argc + argoc} $*/
    ${type} a${I};
/*$ $*/

    if(!PyArg_ParseTuple(args, "${p * argc}|${p * argoc}:${func}",
/*$ {argc + argoc} $*/
    &a${I}${', ' if I + 1 < argc + argoc else ''}
/*$ $*/
    ))
        return NULL;

    PyObject *result = PyObject_CallObject((PyObject *)&glm_${returns}Type, NULL);

    ((glm_${returns} *)result)->${base} =
    glm${path}::${func}<${type}>(
/*$ {argc + argoc} $*/
    a${I}${', ' if I + 1 < argc + argoc else ''}
/*$ $*/
);

    return result;
}
/*$ $*/
```

expanded `python.cpp` source for `NUMBER_FUNCTION`
```c++
PyObject *glm_function_perspective(PyObject *module, PyObject *args) {
    float a0;
    float a1;
    float a2;
    float a3;

    if(!PyArg_ParseTuple(args, "ffff|:perspective",
    &a0,
    &a1,
    &a2,
    &a3
    ))
        return NULL;

    PyObject *result = PyObject_CallObject((PyObject *)&glm_mat4Type, NULL);

    ((glm_mat4 *)result)->mat =
    glm::perspective<float>(
    a0,
    a1,
    a2,
    a3
);

    return result;
}
```

---

working `python.parseme.cpp` source for `NUMBER_FUNCTION` (docstring)
```c++
/*$ NUMBER_FUNCTION $*/
PyDoc_STRVAR(glm_function_${func}__doc__, "${func_doc}");
/*$ $*/
```

expanded `python.cpp` source for `NUMBER_FUNCTION` (docstring)
```c++
```

working `python.parseme.cpp` source for `NUMBER_FUNCTION` (module methods)
```
static
PyMethodDef glmmodule_methods[] = {
/*$ VECTOR_FUNCTION $*/
    {"${func}", (PyCFunction) glm_function_${func}, METH_O, glm_function_${func}__doc__},
/*$ $*/
/*$ MATRIX_FUNCTION $*/
    {"${func}", (PyCFunction) glm_function_${func}, METH_VARARGS, glm_function_${func}__doc__},
/*$ $*/
/*$ NUMBER_FUNCTION $*/
    {"${func}", (PyCFunction) glm_function_${func}, METH_VARARGS, glm_function_${func}__doc__},
/*$ $*/
    {NULL, NULL},
};
```

expanded `python.cpp` source for `NUMBER_FUNCTION` (module methods)
```c++
static
PyMethodDef glmmodule_methods[] = {
    {"abs", (PyCFunction) glm_function_abs, METH_O, glm_function_abs__doc__},
    {"translate", (PyCFunction) glm_function_translate, METH_VARARGS, glm_function_translate__doc__},
    {"rotate", (PyCFunction) glm_function_rotate, METH_VARARGS, glm_function_rotate__doc__},
    {"scale", (PyCFunction) glm_function_scale, METH_VARARGS, glm_function_scale__doc__},
    {"inverse", (PyCFunction) glm_function_inverse, METH_VARARGS, glm_function_inverse__doc__},
    {"ortho", (PyCFunction) glm_function_ortho, METH_VARARGS, glm_function_ortho__doc__},
    {"frustum", (PyCFunction) glm_function_frustum, METH_VARARGS, glm_function_frustum__doc__},
    {"perspective", (PyCFunction) glm_function_perspective, METH_VARARGS, glm_function_perspective__doc__},
    {"perspectiveFov", (PyCFunction) glm_function_perspectiveFov, METH_VARARGS, glm_function_perspectiveFov__doc__},
    {NULL, NULL},
};
```


## python

working python usage example for `glm.perspective()`
```python
import glm
fov = 45
aspect_ratio = 4 / 3
near = 0.1
far 100

m = glm.perspective(fov, aspect_ratio, near, far)

assert type(m) == glm.mat4()

```


## Assorted (Random Facts)

* Vector types have `__abs__()` special method defined for **global** built-in
  function `abs()`. Not to be confused with `glm.abs()` or `abs()` vector methods.