import data_load
from clustering import kmean_clustering
from mapping import create_item_map
import numpy as np
import clustering
from sklearn.cluster import KMeans
import pickle


K = 10 #todo skal k settes her eller returneres av clustering?
K_ARRAY = range(1, 20)


DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'
recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

map_, reverse_map = create_item_map(ingredients)

# Encode recipes into binary vectors
binary_shingle_matrix = np.zeros((len(recipes), len(ingredients)))
for recipe_id in range(len(recipes)):
    for ingredient in recipes[recipe_id]["ingredients"]:
        binary_shingle_matrix[recipe_id][map_[ingredient]] = 1


#clustering_results = kmean_clustering(binary_shingle_matrix, K_ARRAY)
K = 10  # found by elbow method

kmeanModel = KMeans(n_clusters=K).fit(binary_shingle_matrix)
kmeanModel.fit(binary_shingle_matrix)

results = kmeanModel.predict(binary_shingle_matrix)

with open('clustering_results_not_mapped.pickle', 'wb') as handle:
    pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)