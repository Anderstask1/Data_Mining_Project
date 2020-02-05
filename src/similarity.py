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
    for index_transaction, transaction_similarity in enumerate(similarity_matrix):
        max_similarity = -1
        max_similarity_index = -1
        for index_recipe in transaction_similarity:
            similarity = jaccard_similarity(transactions[index_transaction], recipes_mapped[index_recipe])
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_index = index_recipe
        if max_similarity_index != -1:
            jaccard_similarities[index_transaction] = [max_similarity, max_similarity_index]
    return jaccard_similarities