
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import pickle

#from data_analysis import match_analysis

import data_load
from mapping import create_item_map, applymap, create_grocery_map
from clustering import kmean_clustering
from similarity import jaccard_similarity, max_jaccard_similarity
from data_cleaning import clean_dictionary


N_SAMPLES = 9835
N_RECIPES = 39774
N_FEATURES = 169
SIMILARITY_THRESHOLD = 0.7
JACCARDIAN_THRESHOLD = 0.5
PERMUTATIONS = 128
K = 10 #todo skal k settes her eller returneres av clustering?
K_ARRAY = range(1, 20)
DATA_PATH_ITEMS = '../datasets/groceries.csv'
DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'


if __name__=='__main__':

	# Load data, extract unique elements
	transactions, items = data_load.load_data(DATA_PATH_ITEMS)
	recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

	# Remove all groceries in transaction not in ingredients
	transactions = clean_dictionary(transactions, ingredients)

	print("ingredients:", len(ingredients))

	item_map, item_reverse_map = create_item_map(items)

	# Map Transactions
	one_itemset = [[itemset] for itemset in items]
	items_mapped = [applymap(itemset, item_map) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, item_map) for transaction in transactions.values()]
	print("mapped transactions")


	#groceries_map = create_grocery_map(items, ingredients, SIMILARITY_THRESHOLD)

	#with open('groceries_map.pickle', 'wb') as handle:
	#	pickle.dump(groceries_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

	with open('groceries_map.pickle', 'rb') as handle:
		groceries_map = pickle.load(handle)

	one_ingredientset = [[ingredientset] for ingredientset in ingredients]
	ingredientset = [applymap(ingredientset, groceries_map) for ingredientset in one_ingredientset]
	recipes_mapped = {key: applymap(recipe['ingredients'], groceries_map) for key, recipe in recipes.items()}

	# Encode recipes into binary vectors
	binary_shingle_matrix = np.zeros((N_RECIPES, N_FEATURES))
	for recipe in range(len(recipes_mapped)):
		for ingredient in range(len(recipes_mapped[recipe])):
			binary_shingle_matrix[recipe][ingredient] = 1

	# Returns list with cluster (int) at corresponding index
	#clustering_results = kmean_clustering(binary_shingle_matrix, K_ARRAY)

	# Save clustering results
	#with open('k_mean_results.pickle', 'wb') as handle:
	#	pickle.dump(clustering_results, handle, protocol=pickle.HIGHEST_PROTOCOL)


	with open('k_mean_results.pickle', 'rb') as handle:
		clustering_results = pickle.load(handle)

	# Find recipes key with approximate similarity above threshold to all transactions
	#similarity_matrix = minhash_lsh(recipes_mapped, transactions, JACCARDIAN_THRESHOLD, PERMUTATIONS)

	# Save similarities
	#with open('similarity_matrix.pickle', 'wb') as handle:
	#	pickle.dump(similarity_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)

	# Get jaccard similarities of transactions and recipes
	with open('similarity_matrix.pickle', 'rb') as handle:
		similarity_matrix = pickle.load(handle)

	print(similarity_matrix)
	# Find highest true jaccard similarities for each transaction
	jaccard_similarities = max_jaccard_similarity(similarity_matrix, transactions, recipes_mapped)

	# Find keys to transaction without similar recipe
	#missing_similarity_keys = [key for key, x in similarity_matrix.items() if x == []]

	# Create ned dictionary with only transactions without similar recipe
	#filtered_transactions = {}
	#for key in missing_similarity_keys:
	#	filtered_transactions[key] = transactions[key]

	# Find recipes key with approximate similarity above threshold to all filtered transactions
	#filtered_similarity_matrix = minhash_lsh(recipes_mapped, filtered_transactions, JACCARDIAN_THRESHOLD/2, PERMUTATIONS)

	#with open('filtered_similarity_matrix.pickle', 'wb') as handle:
	#	pickle.dump(filtered_similarity_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)

	#with open('filtered_similarity_matrix.pickle', 'rb') as handle:
	#	filtered_similarity_matrix = pickle.load(handle)

	# Find highest true jaccard similarities for each filtered transaction
	#filtered_jaccard_similarities = max_jaccard_similarity(filtered_similarity_matrix, transactions, recipes_mapped)

	# Merge dictionaries of true jaccard similarities
	#jaccard_similarities.update(filtered_jaccard_similarities)


	print("jaccard_similarities: ", jaccard_similarities)

	# Add cluster value to transactions
	for transaction_id, data in jaccard_similarities.items():
		recipe_id = data["recipe"]
		data["cluster"] = clustering_results[recipe_id]
		jaccard_similarities[transaction_id] = data

	print("jaccard_similarities after: ", jaccard_similarities)

	# Find most similar recipes in every cluster
	customer_clusters = {}
	for k in range(K):
		customer_clusters[k] = {}

	for transaction_id, data in jaccard_similarities.items():
		cluster = data["cluster"]
		recipe = data["recipe"]
		similarity = data["similarity"]

		# Add recipe to cluster in not already found
		if recipe not in customer_clusters[cluster].keys():
			customer_clusters[cluster][recipe] = similarity
		# Sum all similarities for every recipe
		else:
			customer_clusters[cluster][recipe] += similarity

	print(customer_clusters)

	for k in range(K):
		print("antall recipes in cluster ",k,": ",len(customer_clusters[k].keys()))

	# Delete all recipes below threshold
	copy = customer_clusters
	for k in range(K):
		for recipe in list(customer_clusters[k].keys()):
			if customer_clusters[k][recipe] < 1:
				try:
					del copy[k][recipe]
				except KeyError:
					print("Key not found")

	customer_clusters = copy


	for k in range(K):
		print("antall recipes in cluster ",k," after trimming: ",len(customer_clusters[k].keys()))

	print(customer_clusters)

	with open('customer_clusters.pickle', 'wb') as handle:
		pickle.dump(customer_clusters, handle, protocol=pickle.HIGHEST_PROTOCOL)

	print(recipes[35169])
	print(recipes[7666])
	print(recipes[2226])

	print("finito")
