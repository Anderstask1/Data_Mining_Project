
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import pickle
from datasketch import MinHash

#from data_analysis import match_analysis

import data_load
from mapping import create_item_map, applymap, create_grocery_map
from clustering import kmean_clustering
from similarity import jaccard_similarity

N_SAMPLES = 9835
N_RECIPES = 39774
N_FEATURES = 169
SIMILARITY_THRESHOLD = 0.7
JACCARDIAN_THRESHOLD = 0
K = range(1, 20)
DATA_PATH_ITEMS = '../datasets/groceries.csv'
DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'


if __name__=='__main__':

	# Load data, extract unique elements
	transactions, items = data_load.load_data(DATA_PATH_ITEMS)
	recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

	print("ingredients:", len(ingredients))

	data1 = transactions[2]
	data2 = recipes[1]['ingredients']

	m1, m2 = MinHash(), MinHash()
	for d in data1:
		m1.update(d.encode('utf8'))
	for d in data2:
		m2.update(d.encode('utf8'))
	approximated_jaccard =  m1.jaccard(m2)
	print("Estimated Jaccard for data1 and data2 is", approximated_jaccard)

	s1 = set(data1)
	s2 = set(data2)
	actual_jaccard = float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
	print("Actual Jaccard for data1 and data2 is", actual_jaccard)

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

	one_ingredientset = [[ingredientset] for ingredientset in ingredients]
	ingredientset = [applymap(ingredientset, groceries_map) for ingredientset in one_ingredientset]
	recipes_mapped = [applymap(recipe['ingredients'], groceries_map) for recipe in recipes]

	# create boolean transaction matrix
	transactions_matrix = np.zeros((N_SAMPLES,N_FEATURES),dtype=int)
	for sample_index in range(len(transactions_mapped)):
		for item_index in transactions_mapped[sample_index]:
			transactions_matrix[sample_index][item_index] = 1

	# create boolean recipes matrix
	recipes_matrix = np.zeros((N_RECIPES, N_FEATURES), dtype=int)
	for sample_index in range(len(recipes_mapped)):
		for item_index in recipes_mapped[sample_index]:
			if item_index != -1:
				recipes_matrix[sample_index][item_index] = 1

	#results = kmean_clustering(transactions_matrix, K)
	with open('k_mean_results.pickle', 'rb') as handle:
		results = pickle.load(handle)

	similarity_vector = []
	for transaction in transactions_matrix:
		similar_recipes = {}
		for index, recipe in enumerate(recipes_matrix):
			jacc_similarity = jaccard_similarity(transaction, recipe)
			if jacc_similarity > JACCARDIAN_THRESHOLD:
				similar_recipes[index%168] = jacc_similarity #169 elements in shingle, modulo 168 give index
		similarity_vector.append(similar_recipes)

print(similarity_vector)

'''
		with open('../results/cluster_results.txt', 'w') as f:
			for item in results:
				f.write("%s\n" % item)
	
'''