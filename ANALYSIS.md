# Analysis of `glmpython` as `Parseme` Utilization


## Working Examples

* `glm.rotate()`: `MATRIX_FUNCTION`. Chosen for deeper analysis for it's
  proximity to the argument types of the wanted
* `glm.perspective()`: `NUMBER_FUNCTION`. Studied first but discarded as
  taking only `float` arguments


### Python Use

```python
>>> import math, glm
>>> m = glm.mat4().rotate(math.pi / 4, glm.vec3(1))
>>> assert type(m) == glm.mat4()
```


### Specification (`setup.py`)

```python
MATRIX_FUNCTION.add(parseme.Round(
    func = 'rotate',
    func_doc = 'Rotates a 4x4 matrix.',
    args = (float, 'vec3',),
    availableTo = ('4',),
    path = ''
))
```


### Source (`python.parseme.cpp`) and Expanded (`python.cpp`)


#### `/* * * Matrix Functions * * */` section

Source in `python.parseme.cpp`:
```c++
/*$ MATRIX_FUNCTION $*/
$?{availableTo == 'all' or n in availableTo
static
PyObject *glm_${p}mat${n}_function_${func}(PyObject *self, PyObject *args) {
$?{args
/*$ {len(args)} $*/
    ${'PyObject *' if isinstance(args[I], str) else args[I].__name__} argument${I};
/*$ $*/

    if(!PyArg_ParseTuple(args, "${''.join('f' if t == float else 'i' if t == int else 'O' for t in args)}:${func}"
/*$ {len(args)} $*/
    , &argument${I}
/*$ $*/
    ))
        return NULL;

/*$ {len(args)} $*/
$?{isinstance(args[I], str)
    if(1 != PyObject_IsInstance(argument${I}, (PyObject *)&glm_${args[I]}Type)) {
        std::stringstream ss;
        ss << "Argument ${I + 1} must be of type '${'glm.' + args[I] if isinstance(args[I], str) else args[I].__name__}' not '" << Py_TYPE(argument${I})->tp_name << "'.";
        std::string s = ss.str();
        PyErr_SetString(PyExc_TypeError, s.c_str());
        return NULL;
    }
$?}
/*$ $*/
$?}

    glm::${p}mat${n} computed;
    PyObject *result;
    computed = glm${path}::${func}(glm_${p}mat${n}Data(self)
/*$ {len(args)} $*/
$?{isinstance(args[I], str)
    , glm_${args[I]}Data(argument${I})
$??{
    , argument${I}
$?}
/*$ $*/
    );

    result = glm_${p}mat${n}New(computed);

    return result;
}
$?}
/*$ $*/
```

and expanded code in `python.cpp`:
```c++
static
PyObject *glm_mat4_function_rotate(PyObject *self, PyObject *args) {
    float argument0;
    PyObject * argument1;

    if(!PyArg_ParseTuple(args, "fO:rotate"
    , &argument0
    , &argument1
    ))
        return NULL;

    if(1 != PyObject_IsInstance(argument1, (PyObject *)&glm_vec3Type)) {
        std::stringstream ss;
        ss << "Argument 2 must be of type 'glm.vec3' not '" << Py_TYPE(argument1)->tp_name << "'.";
        std::string s = ss.str();
        PyErr_SetString(PyExc_TypeError, s.c_str());
        return NULL;
    }

    glm::mat4 computed;
    PyObject *result;
    computed = glm::rotate(glm_mat4Data(self)
    , argument0
    , glm_vec3Data(argument1)
    );

    result = glm_mat4New(computed);

    return result;
}
```


#### `/* * * Functions * * */` section

Source in `python.parseme.cpp`:
```c++
/*$ MATRIX_FUNCTION $*/
PyObject *glm_function_${func}(PyObject *) {
    PyErr_SetString(PyExc_TypeError, "GLM functions only accept GLM types...or numbers.");
    return NULL;
}
```

and expanded code in `python.cpp`:
```c++
PyObject *glm_function_rotate(PyObject *) {
    PyErr_SetString(PyExc_TypeError, "GLM functions only accept GLM types...or numbers.");
    return NULL;
}
```


#### `/* * * GLM Module * * */` section

Source in `python.parseme.cpp`:
```
/*$ MATRIX_FUNCTION $*/
PyDoc_STRVAR(glm_function_${func}__doc__, "${func_doc}");
/*$ $*/

static
PyMethodDef glmmodule_methods[] = {
    // ...
/*$ MATRIX_FUNCTION $*/
    {"${func}", (PyCFunction) glm_function_${func}, METH_VARARGS, glm_function_${func}__doc__},
/*$ $*/
    // ...
    {NULL, NULL},
};
```

and expanded code in `python.cpp`:
```c++
/* * * GLM Module * * */

PyDoc_STRVAR(glm_function_rotate__doc__, "Rotates a 4x4 matrix.");

// ...

static
PyMethodDef glmmodule_methods[] = {
    // ...
    {"perspective", (PyCFunction) glm_function_perspective, METH_VARARGS, glm_function_perspective__doc__},
    // ...
    {NULL, NULL},
};
```


## Wanted Specification


C++ source for `glm::lookAt()` in `glm/gtc/matrix_transform.hpp`:
```
template <typename T, precision P>
GLM_FUNC_DECL tmat4x4<T, P> lookAt(
    tvec3<T, P> const & eye,
    tvec3<T, P> const & center,
    tvec3<T, P> const & up);
```


Specification in `setup.py` (modeled after `MATRIX_FUNCTION` section):
```python
EXTRA_FUNCTION.add(
    parseme.Round(
        func = 'lookAt',
        func_doc = 'Creates a look at view matrix.',
        args = ('vec3', 'vec3', 'vec3'),
        availableTo = ('4',),
        type = 'float',
        path = ''
    )
)
```

Expected code in `python.cpp`:
```c++
static
PyObject *glm_function_lookAt(PyObject *module, PyObject *args) {
    PyObject * argument0;
    PyObject * argument1;
    PyObject * argument2;

    if(!PyArg_ParseTuple(args, "OOO:lookAt"
    , &argument0
    , &argument1
    , &argument2
    ))
        return NULL;

    if(1 != PyObject_IsInstance(argument0, (PyObject *)&glm_vec3Type)) {
        std::stringstream ss;
        ss << "Argument 1 must be of type 'glm.vec3' not '" << Py_TYPE(argument0)->tp_name << "'.";
        std::string s = ss.str();
        PyErr_SetString(PyExc_TypeError, s.c_str());
        return NULL;
    }
    if(1 != PyObject_IsInstance(argument1, (PyObject *)&glm_vec3Type)) {
        std::stringstream ss;
        ss << "Argument 2 must be of type 'glm.vec3' not '" << Py_TYPE(argument1)->tp_name << "'.";
        std::string s = ss.str();
        PyErr_SetString(PyExc_TypeError, s.c_str());
        return NULL;
    }
    if(1 != PyObject_IsInstance(argument2, (PyObject *)&glm_vec3Type)) {
        std::stringstream ss;
        ss << "Argument 3 must be of type 'glm.vec3' not '" << Py_TYPE(argument2)->tp_name << "'.";
        std::string s = ss.str();
        PyErr_SetString(PyExc_TypeError, s.c_str());
        return NULL;
    }

    glm::mat4 computed;
    PyObject *result;
    computed = glm::lookAt<float>(
    glm_vec3Data(argument0), 
    glm_vec3Data(argument1), 
    glm_vec3Data(argument2)
    );

    result = glm_mat4New(computed);

    return result;
}
```


## Assorted (Random Facts)

* Vector types have `__abs__()` special method defined for **global** built-in
  function `abs()`. Not to be confused with `glm.abs()` or `abs()` vector methods.
