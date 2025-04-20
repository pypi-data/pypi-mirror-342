import math
from collections import Counter

def mean(data):
    return sum(data) / len(data)

def stddev(data):
    mu = mean(data)
    return math.sqrt(sum((x - mu) ** 2 for x in data) / len(data))

def bayes(p_b_given_a, p_a, p_b):
    return (p_b_given_a * p_a) / p_b

def combinations(n, r):
    from math import comb
    return comb(n, r)

def prob_independent(p_a, p_b):
    return p_a * p_b

# Additional equations
def variance(data):
    mu = mean(data)
    return sum((x - mu) ** 2 for x in data) / len(data)

def z_score(value, mean, std_dev):
    return (value - mean) / std_dev

def correlation_coefficient(x, y):
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) * sum((y[i] - mean_y) ** 2 for i in range(n)))
    return numerator / denominator

def covariance(x, y):
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n

def median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]

def mode(data):
    freq = Counter(data)
    max_count = max(freq.values())
    return [key for key, count in freq.items() if count == max_count]

def percentile(data, percent):
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percent / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])

def range_stat(data):
    return max(data) - min(data)

def skewness(data):
    mu = mean(data)
    sigma = stddev(data)
    return sum(((x - mu) / sigma) ** 3 for x in data) / len(data)

def kurtosis(data):
    mu = mean(data)
    sigma = stddev(data)
    return sum(((x - mu) / sigma) ** 4 for x in data) / len(data) - 3

def geometric_mean(data):
    product = math.prod(data)
    return product ** (1 / len(data))

def harmonic_mean(data):
    return len(data) / sum(1 / x for x in data if x > 0)

def chi_square(observed, expected):
    return sum((o - e) ** 2 / e for o, e in zip(observed, expected))

def poisson_probability(lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)

def binomial_probability(n, k, p):
    from math import comb
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

def exponential_distribution(lmbda, x):
    return lmbda * math.exp(-lmbda * x)

def normal_distribution(x, mu, sigma):
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)