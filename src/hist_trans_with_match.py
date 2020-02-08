import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
from collections import OrderedDict

# Get cluster of transactions
with open('pop_groc_in_trans_with_match.pickle', 'rb') as handle:
    data = pickle.load(handle)


# number of transactions in each cluster. only plot cluster with more than 50 transactions.
# Counter({5: 2159, 9: 73, 6: 68, 2: 64, 0: 58, 8: 30, 4: 13, 7: 11, 1: 5})

valid_clusters = [0,2,5,6,9] # more than 30 recipes


def remove_shopping_bags(data,valid_clusters):
    copy = {}
    for cluster in valid_clusters:
        top_list_no_bags = []
        top_groceries = [data[cluster][rank] for rank in range(8)]
        for grocery in top_groceries:
            if grocery[0] != 'shopping bags':
                top_list_no_bags.append(grocery)
        copy[cluster] = top_list_no_bags
    return copy


def find_labels(data, top_n,valid_clusters):
    ret = []
    non_valid_clusters =[]
    for cluster in valid_clusters:
        top_groceries = [data[cluster][rank][0] for rank in range(top_n)]
        for grocery in top_groceries:
            ret.append(grocery)
    ret = list(OrderedDict.fromkeys(ret))  # remove duplicates

    return ret


def make_plotting_matrix(data_cleaned, top_n, valid_clusters, map):
    matrix = np.zeros((k_clusters, len(map.keys())), dtype=int)

    for cluster in data_cleaned:
        top_groceries = [data_cleaned[cluster][rank] for rank in range(top_n)]
        for grocey in top_groceries:
            label_index = map[grocey[0]]
            label_value = grocey[1]
            matrix[cluster][label_index] = label_value
    return matrix


if __name__ == '__main__':
    #print(find_labels(data, 4, 10,valid_clusters))


    labels = find_labels(data, 4,valid_clusters)

    map = {x: i for i, x in enumerate(labels)}

    matrix = make_plotting_matrix(data, 4, map)

    transpose = np.transpose(matrix)

    x = np.arange(8)  # the label locations
    width = 0.2  # the width of the bars

    first = -(2 * width) + (0.5 * width)
    second = -(width) + (0.5 * width)
    third = width - (0.5 * width)
    fourth = (2 * width) - (0.5 * width)

    fig, ax = plt.subplots()
    rects0 = ax.bar([0 + first, 1 + third, 2, 3, 4, 5 + third, 6, 7], transpose[0], width, color='#ffd8b1')
    rects1 = ax.bar([0 + second, 1, 2, 3, 4, 5, 6 + first, 7], transpose[1], width, color='#9a6324')
    rects2 = ax.bar([0 + third, 1, 2, 3, 4, 5, 6, 7], transpose[2], width, color='#808000')
    rects3 = ax.bar([0 + fourth, 1 + second, 2 + third, 3 + fourth, 4 + fourth, 5 + fourth, 6, 7 + fourth],
                    transpose[3], width, color='#469990')
    rects4 = ax.bar([0, 1 + first, 2, 3 + second, 4, 5, 6, 7 + second], transpose[4], width, color='#fabebe')
    rects5 = ax.bar([0, 1 + fourth, 2, 3, 4 + third, 5, 6, 7], transpose[5], width, color='#f032e6')
    rects6 = ax.bar([0, 1, 2 + first, 3, 4, 5, 6, 7], transpose[6], width, color='#911eb4')
    rects7 = ax.bar([0, 1, 2 + second, 3, 4, 5, 6 + third, 7], transpose[7], width, color='#4363d8')
    rects8 = ax.bar([0, 1, 2 + fourth, 3, 4, 5, 6, 7], transpose[8], width, color='#42d4f4')
    rects9 = ax.bar([0, 1, 2, 3 + first, 4, 5, 6, 7], transpose[9], width, color='#3cb44b')
    rects10 = ax.bar([0, 1, 2, 3 + third, 4, 5 + first, 6, 7 + first], transpose[10], width, color='#bfef45')
    rects11 = ax.bar([0, 1, 2, 3, 4 + first, 5, 6, 7], transpose[11], width, color='#ffe119')
    rects12 = ax.bar([0, 1, 2, 3, 4 + second, 5, 6, 7], transpose[12], width, color='#f58231')
    rects13 = ax.bar([0, 1, 2, 3, 4, 5 + second, 6, 7 + third], transpose[13], width, color='#e6194B')
    rects14 = ax.bar([0, 1, 2, 3, 4, 5, 6 + second, 7], transpose[14], width, color='#e6beff')
    rects15 = ax.bar([0, 1, 2, 3, 4, 5, 6 + fourth, 7], transpose[15], width, color='#aaffc3')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Purchases')
    ax.set_title('4 most bought groceries of clusters without match')
    ax.set_xticks(x)
    ax.set_xlabel('Cluster')
    labeling = [str(i) for i in range(8)]
    ax.set_xticklabels(labeling)


    # ax.legend()

    def autolabel(rects, label):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            if height > 570:
                height = 570
            if height != 0:  # dont label bars of height 0
                ax.annotate('{}'.format(label),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom',
                            rotation=90)


    print("labels: ", labels)
    autolabel(rects0, labels[0])
    autolabel(rects1, labels[1])
    autolabel(rects2, labels[2])
    autolabel(rects3, labels[3])
    autolabel(rects4, labels[4])
    autolabel(rects5, labels[5])
    autolabel(rects6, labels[6])
    autolabel(rects7, labels[7])
    autolabel(rects8, labels[8])
    autolabel(rects9, labels[9])
    autolabel(rects10, labels[10])
    autolabel(rects11, labels[11])
    autolabel(rects12, labels[12])
    autolabel(rects13, labels[13])
    autolabel(rects14, labels[14])
    autolabel(rects15, labels[15])

    fig.tight_layout()

    plt.show()