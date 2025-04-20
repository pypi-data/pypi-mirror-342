def vec3(x, y, z): return [x, y, z]

def add(a, b):
    return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

def sub(a, b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]