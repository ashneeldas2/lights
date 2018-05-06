import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 16

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normal = normalize(normal)
    light[LOCATION] = normalize(light[LOCATION])
    view = normalize(view)
    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)
    return limit_color([x+y+z for x,y,z in zip(a, d, s)]) 
 
def calculate_ambient(alight, areflect):
   res = [int(alight[i] * areflect[i]) for i in range(len(alight))]
   return res 

def calculate_diffuse(light, dreflect, normal):
    if dot_product(normal, light[LOCATION]) > 0: 
        return [int(light[COLOR][i] * dreflect[i] * dot_product(normal, light[LOCATION])) for i in range(len(dreflect))]
    return [0, 0, 0]

def calculate_specular(light, sreflect, view, normal):
    if dot_product(normal, light[LOCATION]) > 0: 
        const = 2 * dot_product(normal, light[LOCATION])
        mult = []
        for i in range(len(normal)): 
            mult.append(const*normal[i]-light[LOCATION][i])
        exponent = dot_product(mult, view) ** SPECULAR_EXP
        return [int(light[COLOR][i] * sreflect[i] * exponent) for i in range(len(light[COLOR]))]
    return [0, 0, 0]

def limit_color(color):
    for i in range(len(color)): 
        if color[i] > 255: 
            color[i] = 255 
        if color[i] < 0: 
            color[i] = 0
    return color 

#vector functions
def normalize(vector):
    norm = 0
    for i in vector: 
        norm += i ** 2 
    norm = math.sqrt(norm)
    for i in range(len(vector)): 
        vector[i] = vector[i] / norm 
    return vector 

def dot_product(a, b):
    dot = 0
    for i in range(len(a)): 
        dot += a[i] * b[i] 
    return dot 

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
