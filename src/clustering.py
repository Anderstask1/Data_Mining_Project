from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def kmean_clustering(transactions_matrix, k_array):
    # elbow methold for optimal K.
    distortions = []
    inertias = []
    mapping1 = {}
    mapping2 = {}

    for k in k_array:
        # Building and fitting the model
        kmeanModel = KMeans(n_clusters=k).fit(transactions_matrix)
        kmeanModel.fit(transactions_matrix)

        distortions.append(sum(np.min(cdist(transactions_matrix, kmeanModel.cluster_centers_,
                                            'euclidean'), axis=1)) / transactions_matrix.shape[0])
        inertias.append(kmeanModel.inertia_)

        mapping1[k] = sum(np.min(cdist(transactions_matrix, kmeanModel.cluster_centers_,
                                       'euclidean'), axis=1)) / transactions_matrix.shape[0]
        mapping2[k] = kmeanModel.inertia_

    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method using Distortion')
    plt.show()

    plt.plot(K, inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.show()

    K = 8  # found by elbow method

    kmeanModel = KMeans(n_clusters=K).fit(transactions_matrix)
    kmeanModel.fit(transactions_matrix)

    # results = kmeanModel.predict(transactions_matrix)

    # with open('k_mean_results.pickle', 'wb') as handle:
    #	pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('k_mean_results.pickle', 'rb') as handle:
        results = pickle.load(handle)

    counter = collections.Counter(results)

    print(counter)

    return results