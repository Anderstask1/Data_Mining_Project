import pickle
import data_load
from mapping import applymap
import collections
import operator

DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'
recipes, ingredients = data_load.load_json(DATA_PATH_RECIPES)

with open('ingredients_map.pickle', 'rb') as handle:
    ingredients_map = pickle.load(handle)

recipes_mapped = {key: applymap(recipe['ingredients'], ingredients_map) for key, recipe in recipes.items()}

recipes_cleaned = {key: recipe["ingredients"] for key, recipe in recipes.items()}


with open('k_mean_results.pickle', 'rb') as handle:
    clustering_results = pickle.load(handle)


def most_popular_ingredients(recipes_mapped,recipe_ids): # return dict with count of all items in recipes of ids
    ingredients = []
    for recipe_id in recipe_ids:
        for ingredient in recipes_mapped[recipe_id]:
            ingredients.append(ingredient)
    #counter = collections.Counter(ingredients)
    toplist = collections.Counter(ingredients).most_common(10) #top 10

    return toplist

def find_ingredients_in_each_cluster(recipes_mapped,cluster_results,K):
    cluster_recipes ={}
    ret={}
    for k in range(K):
        cluster_recipes[k]= []
        ret = {}

    for recipe_id, cluster in enumerate(cluster_results):
        cluster_recipes[cluster].append(recipe_id)

    for k in range(K):
        ret[k] = most_popular_ingredients(recipes_mapped,cluster_recipes[k])

    return ret

def find_cuisines(recipes,cluster_results,K):
    cluster_cuisines ={}
    ret={}
    for k in range(K):
        cluster_cuisines[k]= []
        ret = {}

    for recipe_id, cluster in enumerate(cluster_results):
        cluster_cuisines[cluster].append(recipes[recipe_id]["cuisine"])

    for k in range(K):
        ret[k] =collections.Counter(cluster_cuisines[k])

    return ret

pop_ingredients_in_clusters = find_ingredients_in_each_cluster(recipes_mapped,clustering_results,10)

#for k in range(10):
#    print(pop_ingredients_in_clusters[k])

#pop items in clusters of transactions without any match
with open('clustering_transaction_results.pickle', 'rb') as handle:
    clustering_transaction_results = pickle.load(handle)

with open('unmatched_transactions.pickle', 'rb') as handle:
    unmatched_transactions = pickle.load(handle)

pop_ing_in_trans_no_match = find_ingredients_in_each_cluster(unmatched_transactions,clustering_transaction_results,8)
with open('pop_ing_in_trans_no_match.pickle', 'wb') as handle:
    pickle.dump(pop_ing_in_trans_no_match, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
for k in range(8):
    print(k,": ",pop_ing_in_trans_no_match[k])


with open('pop_ingredients_in_clusters.pickle', 'wb') as handle:
        pickle.dump(pop_ingredients_in_clusters, handle, protocol=pickle.HIGHEST_PROTOCOL)


#clustering without mapping
with open('clustering_results_not_mapped.pickle', 'rb') as handle:
    clustering_results_not_mapped = pickle.load(handle)

#print(clustering_results_not_mapped)
pop_ingredients_in_cluster_not_mapped = find_ingredients_in_each_cluster(recipes_cleaned,clustering_results_not_mapped,10)
#for k in range(10):
    #print(k,": ",pop_ingredients_in_cluster_not_mapped[k])

'''
recipes_cuisines = find_cuisines(recipes, clustering_results_not_mapped, 10)
for k in range(10):
    print(k,": ",recipes_cuisines[k])

with open('recipes_cuisines.pickle', 'wb') as handle:
    pickle.dump(recipes_cuisines, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''


