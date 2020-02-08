import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
from collections import OrderedDict

# Get cluster of transactions
with open('pop_ing_in_trans_no_match.pickle', 'rb') as handle:
    pop_ing_in_trans_no_match = pickle.load(handle)

for k in range(8):
    print(pop_ing_in_trans_no_match[k])

print(pop_ing_in_trans_no_match)
print(pop_ing_in_trans_no_match[0])
print(pop_ing_in_trans_no_match[0][0])
print(pop_ing_in_trans_no_match[0][0][0])

def remove_shopping_bags(data, k_clusters):
    copy={}
    for cluster in range(k_clusters):
        top_list_no_bags=[]
        top_groceries = [data[cluster][rank] for rank in range(8)]
        for grocery in top_groceries:
            if grocery[0] != 'shopping bags':
                top_list_no_bags.append(grocery)
        copy[cluster]=top_list_no_bags
    return copy

clean_data = remove_shopping_bags(pop_ing_in_trans_no_match,8)

def find_labels(data, top_n, k_clusters):
    ret = []
    for cluster in range(k_clusters):
        top_groceries = [data[cluster][rank][0] for rank in range(top_n)]
        for grocery in top_groceries:
            ret.append(grocery)
    ret = list(OrderedDict.fromkeys(ret)) #remove duplicates

    return ret

print(find_labels(pop_ing_in_trans_no_match,4,8))

labels = find_labels(clean_data,4,8)

men_means = [20, 34, 30, 35, 27]
women_means = [25, 32, 34, 20, 25]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width)
rects2 = ax.bar(x + width/2, women_means, width)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects, label):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(label),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    rotation=90)


autolabel(rects1, "Men")
autolabel(rects2, "Women")

fig.tight_layout()

plt.show()