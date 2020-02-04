
from sklearn.cluster import KMeans
from sklearn import metrics	
from time import time
import numpy as np
import pickle
from scipy.spatial.distance import cdist

import matplotlib.pyplot as plt


from data_analysis import match_analysis
import data_load
from mapping import create_item_map, applymap, create_grocery_map
from clustering import kmean_clustering
from similarity import jaccard_similarity

N_SAMPLES = 9835
N_RECIPES = 39774
N_FEATURES = 169
SIMILARITY_THRESHOLD = 0.7
JACCARDIAN_THRESHOLD = 1
K = range(1, 20)
DATA_PATH_ITEMS = '../datasets/groceries.csv'
DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'


if __name__=='__main__':

	# Load data, extract unique elements
	transactions, items = data_load.load_data(DATA_PATH_ITEMS)
	recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

	print("ingredients:", len(ingredients))

	item_map, reverse_map = create_item_map(items)

	one_itemset = [[itemset] for itemset in items]
	items_mapped = [applymap(itemset, item_map) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, item_map) for transaction in transactions]
	print("mapped transactions")

	#groceries_map = create_grocery_map(items, ingredients, SIMILARITY_THRESHOLD, item_map)

	#with open('groceries_map.pickle', 'wb') as handle:
	#	pickle.dump(groceries_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('groceries_map.pickle', 'rb') as handle:
		groceries_map = pickle.load(handle)

	print("1")
	one_ingredientset = [[ingredientset] for ingredientset in ingredients]
	print("2")
	ingredientset = [applymap(ingredientset, groceries_map) for ingredientset in one_ingredientset]
	print("3")
	recipes_mapped = [applymap(recipe['ingredients'], groceries_map) for recipe in recipes]
	print("mapped recipes")

	# create boolean transaction matrix
	transactions_matrix = np.zeros((N_SAMPLES,N_FEATURES))
	for sample_index in range(len(transactions_mapped)):
		for item_index in transactions_mapped[sample_index]:
			transactions_matrix[sample_index][item_index] = 1

	# create boolean recipes matrix
	recipes_matrix = np.zeros((N_RECIPES, N_FEATURES))
	for sample_index in range(len(recipes_mapped)):
		for item_index in recipes_mapped[sample_index]:
			recipes_matrix[sample_index][item_index] = 1

	results = kmean_clustering(transactions_matrix, K)

	similarity_vector = []
	for transaction in transactions_matrix:
		similar_recipes = []
		for recipe in recipes_matrix:
			jacc_similarity = jaccard_similarity(transaction, recipe)
			if jacc_similarity > JACCARDIAN_THRESHOLD:
				similar_recipes[recipe["id"]] = jacc_similarity
		similarity_vector.append(similar_recipes)
	'''
		with open('../results/cluster_results.txt', 'w') as f:
			for item in results:
				f.write("%s\n" % item)
	
	'''





#todo bruk results til å dele inn tranaskjsoner etter custer. for hver kluster, sjekk hvilke n oppskrifter som er nærmest.




