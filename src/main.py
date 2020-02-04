import csv
from sklearn.cluster import KMeans
from sklearn import metrics	
from time import time
import numpy as np
import collections
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import json

def load_data(path):
	'''
	Function to read itemsets from file.

	Parameters
	----------
	path : string
	    path to file containinng transactions.

	Returns
	----------
	transactions : list
		list containing all transactions. Each transaction is a list of
		items present in that transaction.
	items : list
		list containing all the unique items.
	'''
	items = []
	with open(path, 'r') as f:
	    reader = csv.reader(f)
	    transactions = list(reader)
	for x in transactions:
		items.extend(x)
	items=sorted(set(items))
	return transactions, items

def create_map(items):
	'''
	Function to map unique items to integers.

	Parameters
	----------
	items : list
	    list of unique items.

	Returns
	----------
	map_ : dict
		Items --> integers mapping.
	reverse_map : dict
		Integers --> items mapping.
	'''
	map_ = {x:i for i,x in enumerate(items)}
	reverse_map = {i:x for i,x in enumerate(items)}
	return map_, reverse_map

def applymap(transaction, map_):
	'''
	Function to apply mapping to items.

	Parameters
	----------
	transaction : list
	    single transaction.
	map_ : dict
	    mapping.

	Returns
	----------
	ret : dict
		mapped transaction.
	'''
	ret = []
	for item in transaction:

		if item not in map_.keys(): #assign -1 to items nonexistent in transactions
			ret.append(-1)

		ret.append(map_[item])
	return ret



if __name__=='__main__':
	data_path = '../datasets/groceries.csv'
	transactions, items = load_data(data_path)
	map_, reverse_map = create_map(items)
	# pickle.dump(reverse_map, open('reverse_map.pkl', 'wb+'))
	one_itemset = [[itemset] for itemset in items]
	items_mapped = [applymap(itemset, map_) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, map_) for transaction in transactions]

	n_samples = 9835
	n_features = 169

	#create boolean matrix
	data_matrix = np.zeros((n_samples,n_features))
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




