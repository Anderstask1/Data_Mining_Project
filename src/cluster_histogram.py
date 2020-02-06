import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import pickle

with open(DATA_PATH_RECIPES, 'r') as f:
    recipes = json.load(f)

cuisines = []
for recipe in recipes:
    cuisines.append(recipe["cuisine"])
cuisines = list(dict.fromkeys(cuisines))  # remove duplicates



with open('customer_clusters.pickle', 'rb') as handle:
    customer_clusters = pickle.load(handle)

print(customer_clusters)
n_bins = 42

# Generate a normal distribution, center at x=0 and y=5
cluster2= []
for recipe in customer_clusters[2].keys():
    #print(customer_clusters[2][recipe])
    cluster2.append(customer_clusters[2][recipe])

print(cluster2)

cluster2_names = []
for recipe in customer_clusters[2].keys():
    #print(customer_clusters[2][recipe])
    cluster2_names.append(str(recipe))

x = np.arange(42)

print(x)

plt.bar(x, height= cluster2, color= [colors])
plt.xticks(x, cluster2_names)

plt.show()