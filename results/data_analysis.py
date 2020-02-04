import json
import csv
from difflib import SequenceMatcher



#read data from recipes

filename = "../datasets/recipe-ingredients-dataset/train.json"
with open(filename, 'r') as f:
    recipes = json.load(f)

#print(recipes)
#print(recipes[00000]["ingredients"])

recipes_items = []

for recipe in recipes:
    for ingredient in recipe["ingredients"]:
        recipes_items.append(ingredient)

recipes_items = list(dict.fromkeys(recipes_items)) #remove duplicates

#read data from transactions

path = '../datasets/groceries.csv'
items = []
with open(path, 'r') as f:
    reader = csv.reader(f)
    transactions = list(reader)
for x in transactions:
    items.extend(x)
items = sorted(set(items))

transactions_items = items


print("transactions_items")
print("lenght: ",len(transactions_items))
print("recipes_items")
print("length: ",len(recipes_items))

items_not_in_recipes = []

for item in transactions_items:
    if item not in recipes_items:
        items_not_in_recipes.append(item)

print("length: ", len(items_not_in_recipes))
#print(items_not_in_recipes)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

match_count=0
items_without_matches = []
for trans_item in transactions_items:
    match_flag = False
    for recipe_item in recipes_items:
        if similar(trans_item,recipe_item) >0.8:
            if match_flag == False:
                match_count += 1 #count a match once only
            match_flag = True
            print("match found: ",trans_item," and ",recipe_item)
    if match_flag == False:
         items_without_matches.append(trans_item)

print("matches found: ", match_count)

print("items with no matches (",len(items_without_matches),"): ", items_without_matches)