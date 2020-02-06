import pickle
import data_load
from mapping import applymap
import collections

DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'
recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

with open('ingredients_map.pickle', 'rb') as handle:
    ingredients_map = pickle.load(handle)

recipes_mapped = {key: applymap(recipe['ingredients'], ingredients_map) for key, recipe in recipes.items()}

with open('jaccard_similarities.pickle', 'rb') as handle:
    jaccard_similarities = pickle.load(handle)


def most_popular_ingredients(recipes_mapped,recipe_ids): # return dict with count of all items in recipes
    ingredients = []
    for recipe_id in recipe_ids:
        for ingredient in recipes_mapped:
            ingredients.append(ingredient)
    counter = collections.Counter(ingredients) #sorted
    i=0
    toplist= {}
    for ingredient in counter.keys():
        if i<5:
            toplist[ingredient]=counter[ingredient]
        i+=1
    return counter

def find_items_in_each_cluster(jaccard_sim,K):
    cluster_ingredients ={}
    for k in range(K):
        cluster_ingredients[k]= []

    for data in jaccard_sim.values():
        ingredients = data["recipe"]["ingredients"]
        cluster = data["cluster"]
        for ingredient in ingredients:
            cluster_ingredients[cluster].append(ingredient)

    ret = {}
    for k in range(K):
        ret[k] =


