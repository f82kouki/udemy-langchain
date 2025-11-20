from scripy.optimize import newton
import math

def f(x):
    return x-math.cos(x)
def fp(x):
    return 1.0+math.sin(x)
print(newton(f,1,fprime=fp))