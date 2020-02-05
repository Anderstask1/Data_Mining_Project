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

def max_jaccard_similarity(similarity_matrix, transactions, recipes_mapped):
    jaccard_similarities = {}
    for key_transaction, transaction_similarity in similarity_matrix.items():
        max_similarity = -1
        max_similarity_key = -1
        for key_recipe in transaction_similarity:
            similarity = jaccard_similarity(transactions[key_transaction], recipes_mapped[key_recipe])
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_key = key_recipe
        if max_similarity_key != -1:
            jaccard_similarities[key_transaction] = {"key": max_similarity_key, "similarity": max_similarity}
    return jaccard_similarities