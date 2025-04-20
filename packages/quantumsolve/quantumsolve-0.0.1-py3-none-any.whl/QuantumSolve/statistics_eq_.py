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
