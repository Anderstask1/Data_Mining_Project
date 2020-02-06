from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import collections

def kmean_clustering(matrix, k_array):
    print("Running kmeans Clustering")
    # elbow methold for optimal K.
    distortions = []
    inertias = []
    mapping1 = {}
    mapping2 = {}

    for k in k_array:
        print("round: ",k)
        # Building and fitting the model
        kmeanModel = KMeans(n_clusters=k).fit(matrix)
        kmeanModel.fit(matrix)

        distortions.append(sum(np.min(cdist(matrix, kmeanModel.cluster_centers_,
                                            'euclidean'), axis=1)) / matrix.shape[0])
        inertias.append(kmeanModel.inertia_)

        mapping1[k] = sum(np.min(cdist(matrix, kmeanModel.cluster_centers_,
                                       'euclidean'), axis=1)) / matrix.shape[0]
        mapping2[k] = kmeanModel.inertia_

    plt.plot(k_array, distortions, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method using Distortion')
    plt.show()

    plt.plot(k_array, inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.show()

    K = 10  # found by elbow method

    kmeanModel = KMeans(n_clusters=K).fit(matrix)
    kmeanModel.fit(matrix)

    results = kmeanModel.predict(matrix)

    counter = collections.Counter(results)

    print(counter)

    return results