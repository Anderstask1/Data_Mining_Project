
from sklearn.cluster import KMeans
from sklearn import metrics	
from time import time
import numpy as np

import matplotlib.pyplot as plt


import data_analysis
import data_load
from mapping import create_item_map, applymap, create_grocery_map


N_SAMPLES = 9835
N_FEATURES = 169
SIMILARITY_THRESHOLD = 0.75
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

	groceries_map = create_grocery_map(items, ingredients, SIMILARITY_THRESHOLD, item_map)

	for k in groceries_map.keys():
		print(groceries_map[k])

	print("1")
	one_ingredientset = [[ingredientset] for ingredientset in ingredients]
	print("2")
	ingredientset = [applymap(ingredientset, groceries_map) for ingredientset in one_ingredientset]
	print("3")
	recipes_mapped = [applymap(recipe['ingredients'], groceries_map) for recipe in recipes]
	print("mapped recipes")

#create boolean matrix
	data_matrix = np.zeros((N_SAMPLES,N_FEATURES))
	for sample in range(len(transactions_mapped)):
		for item in range(len(transactions_mapped[sample])):
			data_matrix[sample][item] = 1

	#bench_k_means(KMeans(init='k-means++', n_clusters=clusters, n_init=10), name="k-means++", data=data_matrix)
	#bench_k_means(KMeans(init='random', n_clusters=clusters, n_init=10), name="random", data=data_matrix)

	#elbow methold for optimal K.
	distortions = []
	inertias = []
	mapping1 = {}
	mapping2 = {}
	K = range(1,20)

	for k in K:
		#Building and fitting the model
		kmeanModel = KMeans(n_clusters=k).fit(data_matrix)
		kmeanModel.fit(data_matrix)

		distortions.append(sum(np.min(cdist(data_matrix, kmeanModel.cluster_centers_,
		                  'euclidean'),axis=1)) / data_matrix.shape[0])
		inertias.append(kmeanModel.inertia_)

		mapping1[k] = sum(np.min(cdist(data_matrix, kmeanModel.cluster_centers_,
		             'euclidean'),axis=1)) / data_matrix.shape[0]
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

	K = 8 #found by elbow method

	kmeanModel = KMeans(n_clusters=K).fit(data_matrix)
	kmeanModel.fit(data_matrix)

	results = kmeanModel.predict(data_matrix)

	counter = collections.Counter(results)

	print(counter)

	'''
		with open('../results/cluster_results.txt', 'w') as f:
			for item in results:
				f.write("%s\n" % item)
	
	'''





#todo bruk results til å dele inn tranaskjsoner etter custer. for hver kluster, sjekk hvilke n oppskrifter som er nærmest.




