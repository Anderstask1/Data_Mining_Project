import collections
from scipy.spatial.distance import cdist
from difflib import SequenceMatcher

def create_item_map(items):
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


# Boolean function finding similar items with threshold
def similar(a, b, threshold):
    if SequenceMatcher(None, a, b).ratio() > threshold:
        return True
    else :
        return False

match_count=0
items_without_matches = []

# Mapping from grocerie to int, dependent on item map
def create_grocery_map(items, ingredients, threshold, item_map):
    grocery_map = {}
    similarities = {}

    for ingredient in ingredients:
        for item in items:
            similarities[ingredient] = - 1
            similarity = SequenceMatcher(None, item, ingredient).ratio()
            if similarity > threshold and similarity > similarities[ingredient]: #make sure 1-1 mapping by only using best similarity
                similarities[ingredient] = similarity #save highest similarity
                mapped_int = item_map[item]
                grocery_map[ingredient]= mapped_int
    return grocery_map