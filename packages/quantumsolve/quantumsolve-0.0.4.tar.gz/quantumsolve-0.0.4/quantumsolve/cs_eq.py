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

# Additional equations
def mean(values):
    return sum(values) / len(values)

def variance(values):
    mean_val = mean(values)
    return sum((x - mean_val) ** 2 for x in values) / len(values)

def standard_deviation(values):
    return math.sqrt(variance(values))

def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

def manhattan_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))

def dot_product(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))

def cross_entropy_loss(y_true, y_pred):
    return -sum(y * math.log(p) for y, p in zip(y_true, y_pred) if p > 0)

def mean_squared_error(y_true, y_pred):
    return sum((y - p) ** 2 for y, p in zip(y_true, y_pred)) / len(y_true)

def root_mean_squared_error(y_true, y_pred):
    return math.sqrt(mean_squared_error(y_true, y_pred))

def harmonic_mean(values):
    return len(values) / sum(1 / x for x in values if x > 0)

def geometric_mean(values):
    product = math.prod(values)
    return product ** (1 / len(values))

def softmax(vector):
    exp_values = [math.exp(x) for x in vector]
    total = sum(exp_values)
    return [x / total for x in exp_values]

def log_loss(y_true, y_pred):
    return -sum(y * math.log(p) + (1 - y) * math.log(1 - p) for y, p in zip(y_true, y_pred) if 0 < p < 1)

def cosine_similarity(vector1, vector2):
    dot = dot_product(vector1, vector2)
    norm1 = math.sqrt(dot_product(vector1, vector1))
    norm2 = math.sqrt(dot_product(vector2, vector2))
    return dot / (norm1 * norm2)

def exponential_moving_average(values, alpha):
    ema = values[0]
    for value in values[1:]:
        ema = alpha * value + (1 - alpha) * ema
    return ema

def quadratic_formula(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None  # No real roots
    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
    return root1, root2

def kl_divergence(p, q):
    return sum(p[i] * math.log(p[i] / q[i]) for i in range(len(p)) if p[i] > 0 and q[i] > 0)

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union