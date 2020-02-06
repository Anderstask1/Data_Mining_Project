import json
import csv
from difflib import SequenceMatcher

N_SAMPLES = 9835
N_FEATURES = 169
SIMILARITY_THRESHOLD = 0.75
DATA_PATH_ITEMS = '../datasets/groceries.csv'
DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'

def similar(a, b, threshold):
    if SequenceMatcher(None, a, b).ratio() > threshold:
        return True
    else :
        return False

# read data from recipes
with open(DATA_PATH_RECIPES, 'r') as f:
    recipes = json.load(f)

print(recipes)
ingredients = []

for recipe in recipes:
    for ingredient in recipe["ingredients"]:
        ingredients.append(ingredient)

cuisines = []
for recipe in recipes:
    cuisines.append(recipe["cuisine"])
cuisines = list(dict.fromkeys(cuisines))  # remove duplicates

print("cuicines: ",len(cuisines))

print("ingredients with duplicates:", len(ingredients))
ingredients = list(dict.fromkeys(ingredients))  # remove duplicates

items = []
with open(DATA_PATH_ITEMS, 'r') as f:
    reader = csv.reader(f)
    transactions = list(reader)
for x in transactions:
    items.extend(x)
items = sorted(set(items))


#find non overlapping items
items_not_in_recipes = []

for item in items:
    if item not in ingredients:
        items_not_in_recipes.append(item)

print("length: ", len(items_not_in_recipes))
# print(items_not_in_recipes)

items_without_matches = []
match_count =0
for item in items:
    match_flag = False
    for ingredient in ingredients:
        if similar(item,ingredient, SIMILARITY_THRESHOLD) :
            if match_flag == False:
                match_count += 1 #count a match once only
            match_flag = True
            print("match found: ",item," and ",ingredient)
    if match_flag == False:
         items_without_matches.append(item)

print("transactions_items")
print("lenght: ", len(items))
print("recipes_items")
print("length: ", len(ingredients))
print("matches found: ", match_count)
print("items with no matches (",len(items_without_matches),"): ", items_without_matches)


