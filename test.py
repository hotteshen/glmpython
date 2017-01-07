import glm
import random
import numpy

def _randomVector3():
    return glm.vec3(random.random(), random.random(), random.random())


def _randomMatrix4():
	m = glm.mat4()
	for row in range(4):
		for col in range(4):
			m[row * 4 + col] = random.random()
	return m


def _randomQuaternion():
	return glm.quat(_randomVector3(), random.random())


# lookAt()
eye = _randomVector3()
center = glm.vec3(0, 0, 0)
up = glm.vec3(0, 1, 0)

lookAt_matrix = glm.lookAt(eye, center, up)
print(lookAt_matrix)

assert type(lookAt_matrix) == glm.mat4

# project()
obj = _randomVector3()
model = glm.mat4()
proj = lookAt_matrix
viewport = glm.vec4([0, 0, 1024, 768])

win = glm.project(obj, model, proj, viewport)
print(obj)
print(win)

assert type(win) == glm.vec3

# unProject()
obj = glm.unProject(win, model, proj, viewport)
print(win)
print(obj)

assert type(obj) == glm.vec3

# transpose()
m = _randomMatrix4()
print(m)
print(m.transpose())

assert type(m) == glm.mat4
assert type(m.transpose()) == glm.mat4

# slerp()
q1, q2 = _randomQuaternion(), _randomQuaternion()
print(glm.slerp(q1, q2, 0.5))

assert type(glm.slerp(q1, q2, random.random())) == glm.quat
assert numpy.isclose(glm.slerp(q1, q2, 0.0), q1, atol=0.001).all()
assert numpy.isclose(glm.slerp(q1, q2, 1.0), q2, atol=0.001).all()

# conjugate()
q0 = _randomQuaternion()
q1 = glm.conjugate(q0)
assert q0.w == q1.w
print(q0, q1)
