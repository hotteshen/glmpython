#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "./glm/glm/glm.hpp"

namespace glmpython {

/* Type Definitions */
/*$ BASETYPEDEF $*/

typedef struct {
	PyObject_HEAD
	PyObject *obj;
	Py_ssize_t offset;
} glm_${type}Iterator;

typedef struct {
	PyObject_HEAD
} glm_${type};

/*$ $*/
/*$ VECTORQUAT $*/

typedef struct {
	glm_Vector vector;
	glm::${p}${vectorquat}${m} ${vectorquat};
} glm_${p}${vectorquat}${m};

#define glm_${p}${vectorquat}${m}Data(o) \
	((glm_${p}${vectorquat}${m} *)o)->${vectorquat}

PyObject *glm_${p}${vectorquat}${m}New(glm::${p}${vectorquat}${m});
/*$ $*/
/*$ MATRIX $*/

typedef struct {
	glm_Matrix matrix;
	glm::${p}mat${n} mat;
} glm_${p}mat${n};

#define glm_${p}mat${n}Data(o) \
	((glm_${p}mat${n} *)o)->mat

PyObject *glm_${p}mat${n}New(glm::${p}mat${n});
/*$ $*/

}
