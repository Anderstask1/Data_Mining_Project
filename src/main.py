import csv

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
		ret.append(map_[item])
	return ret


if __name__=='__main__':
	data_path = '/home/anderstask1/Documents/Kyb/DataMining/Data_Mining_Project/datasets/groceries.csv'
	transactions, items = load_data(data_path)
	map_, reverse_map = create_map(items)
	# pickle.dump(reverse_map, open('reverse_map.pkl', 'wb+'))
	one_itemset = [[itemset] for itemset in items]
	items_mapped = [applymap(itemset, map_) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, map_) for transaction in transactions]
