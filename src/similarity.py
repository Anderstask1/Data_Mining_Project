import numpy as np

def jaccard_similarity(x, y):
    """
    Jaccard Similarity J (A,B) = | Intersection (A,B) | / | Union (A,B) |
    """
    return np.bitwise_and(x, y)