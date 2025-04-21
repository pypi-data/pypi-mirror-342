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

# Additional equations
def factorial(n):
    return math.factorial(n)

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def degrees_to_radians(degrees):
    return math.radians(degrees)

def radians_to_degrees(radians):
    return math.degrees(radians)

def compound_interest(principal, rate, time, n=1):
    return principal * (1 + rate / n) ** (n * time)

def distance_3d(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def heron_area(a, b, c):
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))

def arithmetic_mean(values):
    return sum(values) / len(values)

def geometric_mean(values):
    product = math.prod(values)
    return product ** (1 / len(values))

def harmonic_mean(values):
    return len(values) / sum(1 / x for x in values if x > 0)

def median(values):
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    else:
        return sorted_values[mid]

def mode(values):
    from collections import Counter
    freq = Counter(values)
    max_count = max(freq.values())
    return [key for key, count in freq.items() if count == max_count]

def variance(values):
    mean_val = arithmetic_mean(values)
    return sum((x - mean_val) ** 2 for x in values) / len(values)

def standard_deviation(values):
    return math.sqrt(variance(values))

def z_score(value, mean, std_dev):
    return (value - mean) / std_dev

def exponential_growth(initial, rate, time):
    return initial * math.exp(rate * time)

def logistic_growth(initial, rate, time, carrying_capacity):
    return carrying_capacity / (1 + (carrying_capacity - initial) / initial * math.exp(-rate * time))

def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return (x, y)

def cartesian_to_polar(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return (r, theta)