import numpy as np

def jaccard_similarity(x, y):
    """
    Jaccard Similarity J (A,B) = | Intersection (A,B) | / | Union (A,B) |
    """

    if len(x) != len(y):
        print("arrays not the same length")
        return -1

    x = np.array(x)
    y = np.array(y)

    intersection = np.sum(np.bitwise_and(x,y))
    union = np.sum(np.bitwise_or(x,y))
    return intersection/union


a= [0,0,0,1,1,1]

b= [0,1,0,0,1,0]

c= jaccard_similarity(a,b)


print(c)
