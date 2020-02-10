import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
from collections import OrderedDict

# Get cluster of transactions
with open('pop_groc_in_trans_with_match.pickle', 'rb') as handle:
    pop_ingredients_in_cluster = pickle.load(handle)

valid_clusters = [0,2,5,6,9] # more than 30 recipes
copy={}
for k in valid_clusters:
    copy[k]=pop_ingredients_in_cluster[k]

pop_ingredients_in_cluster = copy

# Constants
NUMBER_OF_TOP_INGREDIENTS = 4
NUMBER_OF_CLUSTERS = len(pop_ingredients_in_cluster)
LIST_OF_COLORS = ['#aaffc3', '#e6beff', '#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4']

# Functions
def create_map(pop_ingredients_in_cluster):
    ingredients = []
    for cluster_key, list_of_touples in pop_ingredients_in_cluster.items():
        for index in range(NUMBER_OF_TOP_INGREDIENTS):
            touple = list_of_touples[index]
            ingredients.append(touple[0])
    unique_ingredients = list(dict.fromkeys(ingredients))
    map_ = {x:i for i,x in enumerate(unique_ingredients)}
    reverse_map = {i: x for i, x in enumerate(unique_ingredients)}
    return map_, reverse_map

def set_label(rects, labels):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for index, rect in enumerate(rects):
        height = rect.get_height()
        label = reverse_map[labels[index]]
        if height != 0:
            ax.annotate('{}'.format(label),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        rotation=90,
                        size = 20)


map_, reverse_map  = create_map(pop_ingredients_in_cluster)


cluster_labels = []
ingredients_matrix = np.zeros((NUMBER_OF_CLUSTERS, NUMBER_OF_TOP_INGREDIENTS), dtype=int)
count_matrix = np.zeros((NUMBER_OF_CLUSTERS, NUMBER_OF_TOP_INGREDIENTS), dtype=int)

for key, value in pop_ingredients_in_cluster.items():
    cluster_labels.append(key)
    keys = list(pop_ingredients_in_cluster.keys())
    index = keys.index(key)
    for i in range(NUMBER_OF_TOP_INGREDIENTS):
        print(i, map_[value[i][0]])
        ingredients_matrix[index][i] = map_[value[i][0]]
        count_matrix[index][i] = value[i][1]

x = np.arange(NUMBER_OF_CLUSTERS)  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()

for i in range(NUMBER_OF_TOP_INGREDIENTS):
    pos = x + width / 2 + i * width -  (width*NUMBER_OF_TOP_INGREDIENTS)/2
    counts = count_matrix[:,i]
    colors = [LIST_OF_COLORS[ingredient] for ingredient in ingredients_matrix[:,i]]
    rects = ax.bar(pos, counts, width, color=colors)
    set_label(rects, ingredients_matrix[:,i])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of recipes', fontsize=30)
ax.set_title('Top {} ingredients for each cluster of recipes'.format(NUMBER_OF_CLUSTERS), fontsize=30)
ax.set_xticks(x)
ax.set_xticklabels(cluster_labels, fontsize=30)
ax.legend()
fig.tight_layout()
plt.show()
