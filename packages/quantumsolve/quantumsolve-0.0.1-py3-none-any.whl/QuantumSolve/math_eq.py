import math

def pythagorean(a, b):
    return math.sqrt(a**2 + b**2)

def quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)
    return (x1, x2)

def euler_identity():
    return complex(math.e)**(complex(0, math.pi)) + 1

def area_circle(r):
    return math.pi * r**2

def circumference(r):
    return 2 * math.pi * r

def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)

def log_identity(x, y, base=10):
    return math.log(x*y, base) == math.log(x, base) + math.log(y, base)

def derivative_approx(f, x, h=1e-6):
    return (f(x + h) - f(x)) / h

def integral_approx(f, a, b, n=1000):
    dx = (b - a) / n
    total = sum(f(a + i*dx) for i in range(n))
    return dx * total

def binomial_expansion(a, b, n):
    from math import comb
    return [comb(n, k) * (a**(n-k)) * (b**k) for k in range(n+1)]
