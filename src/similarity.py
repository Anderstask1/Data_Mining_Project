import numpy as np

def jaccard_similarity_boolean(x, y):
    """
    Jaccard Similarity J (A,B) = | Intersection (A,B) | / | Union (A,B) |
    """

    if len(x) != len(y):
        print("arrays not the same length")
        return -1

    x = np.array(x)
    y = np.array(y)

    intersection = np.sum(np.bitwise_and(x,y))
    #union = np.sum(np.bitwise_or(x,y))
    return intersection


def jaccard_similarity(x, y):
    set_x = set(x)
    set_y = set(y)
    return float(len(set_x.intersection(set_y))) / float(len(set_x.union(set_y)))
