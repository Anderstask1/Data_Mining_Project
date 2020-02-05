
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import pickle

#from data_analysis import match_analysis

import data_load
from mapping import create_item_map, applymap, create_grocery_map
from clustering import kmean_clustering
from similarity import jaccard_similarity
from locality_sensitive_hashing import minhash_lsh

N_SAMPLES = 9835
N_RECIPES = 39774
N_FEATURES = 169
#SIMILARITY_THRESHOLD = 0.7
JACCARDIAN_THRESHOLD = 0.5
PERMUTATIONS = 128
K = range(1, 20)
DATA_PATH_ITEMS = '../datasets/groceries.csv'
DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'


if __name__=='__main__':

	# Load data, extract unique elements
	transactions, items = data_load.load_data(DATA_PATH_ITEMS)
	recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

	print("ingredients:", len(ingredients))

	#item_map, reverse_map = create_item_map(items)

	#one_itemset = [[itemset] for itemset in items]
	#items_mapped = [applymap(itemset, item_map) for itemset in one_itemset]
	#transactions_mapped = [applymap(transaction, item_map) for transaction in transactions]
	#print("mapped transactions")

	#groceries_map = create_grocery_map(items, ingredients, SIMILARITY_THRESHOLD)

	#with open('groceries_map.pickle', 'wb') as handle:
	#	pickle.dump(groceries_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('groceries_map.pickle', 'rb') as handle:
		groceries_map = pickle.load(handle)

	one_ingredientset = [[ingredientset] for ingredientset in ingredients]
	ingredientset = [applymap(ingredientset, groceries_map) for ingredientset in one_ingredientset]
	recipes_mapped = [applymap(recipe['ingredients'], groceries_map) for recipe in recipes]

	# create boolean transaction matrix
	#transactions_matrix = np.zeros((N_SAMPLES,N_FEATURES),dtype=int)
	#for sample_index in range(len(transactions_mapped)):
	#	for item_index in transactions_mapped[sample_index]:
	#		transactions_matrix[sample_index][item_index] = 1

	# create boolean recipes matrix
	recipes_matrix = np.zeros((N_RECIPES, N_FEATURES), dtype=int)

	#results = kmean_clustering(transactions_matrix, K)
	with open('k_mean_results.pickle', 'rb') as handle:
		results = pickle.load(handle)

	# Find recipes index with approximate similarity above threshold to all transactions
	#similarity_matrix = minhash_lsh(recipes_mapped, transactions, JACCARDIAN_THRESHOLD, PERMUTATIONS)

	#with open('similarity_matrix.pickle', 'wb') as handle:
	#	pickle.dump(similarity_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('similarity_matrix.pickle', 'rb') as handle:
		similarity_matrix = pickle.load(handle)

	jaccard_similarities = {}
	remaining_similarity_matrix = []
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

	similarity_matrix = minhash_lsh(recipes_mapped, transactions, JACCARDIAN_THRESHOLD/2, PERMUTATIONS)

	for index_t, similarity_list in enumerate(similarity_matrix):
		print("transaction with index:", index_t, "is similar to:", len(similarity_list), " recipes")

'''
		with open('../results/cluster_results.txt', 'w') as f:
			for item in results:
				f.write("%s\n" % item)
	
'''