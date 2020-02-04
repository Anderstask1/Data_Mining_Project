import json
import csv

def load_json(path):

    #read data from recipes
    with open(path, 'r') as f:
        recipes = json.load(f)

    ingredients = []

    for recipe in recipes:
        for ingredient in recipe["ingredients"]:
            ingredients.append(ingredient)

    print("ingredients with duplicates:", len(ingredients))
    ingredients = list(dict.fromkeys(ingredients))  # remove duplicates

    print("ingredients after:", len(ingredients))


    return recipes, ingredients

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

