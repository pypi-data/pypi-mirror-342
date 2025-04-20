import math

def big_o_example(n):
    return n * math.log(n)  # O(n log n)

def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def accuracy(tp, tn, fp, fn):
    return (tp + tn) / (tp + tn + fp + fn)

def gradient_descent(theta, grad, alpha):
    return theta - alpha * grad

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
