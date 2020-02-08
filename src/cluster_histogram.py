import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import pickle
import json
import collections
import operator

DATA_PATH_RECIPES = '../datasets/recipe-ingredients-dataset/train.json'

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


#histograms of cuisines in recipe clusters

with open('recipes_cuisines.pickle', 'rb') as handle:
    recipes_cuisines = pickle.load(handle)

def histogram_plot(recipes_cluster, cluster, toplist=False):
    cuisine_dict = dict(recipes_cluster[cluster])
    labels =[]
    cuisine_values =[]

    sorted_cuisine = sorted(cuisine_dict.items(), key=operator.itemgetter(1),reverse = True)
    cuisine_dict = collections.OrderedDict(sorted_cuisine)
    for label in cuisine_dict.keys():
        labels.append(label)
        cuisine_values.append(cuisine_dict[label])

    if toplist:#only include top 6 in histogram
        labels_top=[labels[i] for i in range(7)]
        cuisine_values_top = [cuisine_values[i] for i in range(7)]
        y_pos = np.arange(len(labels_top))  # hva skjer her?

        plt.bar(y_pos, cuisine_values_top, align='center', alpha=0.5)
        plt.xticks(y_pos, labels)
        plt.xlabel('Cuisines')
        plt.ylabel('Recipes')
        plt.title('Cluster of Asia')

        plt.show()
        return
    #print("labels ",labels)
    #print("values:" , cuisine_values)
    y_pos = np.arange(len(labels)) #hva skjer her?

    plt.bar(y_pos, cuisine_values, align='center', alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.xticks(rotation=90)
    plt.ylabel('Antall')
    plt.title('Cuicines')

    plt.show()


histogram_plot(recipes_cuisines,5, True)

#make common plot for all top 3 cuisines
def top_3_histogram_plot(recipes_clusters):
    barWidth = 0.25

    n_clusters = 10 # 7 cuisines among top 3

    cluster_0 =[0] * n_clusters
    cluster_1 =[0] * n_clusters
    cluster_2 =[0] * n_clusters
    cluster_3 =[0] * n_clusters
    cluster_4 =[0] * n_clusters
    cluster_5 =[0] * n_clusters
    cluster_6 =[0] * n_clusters
    cluster_7 =[0] * n_clusters
    cluster_8 =[0] * n_clusters
    cluster_9 =[0] * n_clusters

    clusters =[cluster_0,
               cluster_1,
               cluster_2,
               cluster_3,
               cluster_4,
               cluster_5,
               cluster_6,
               cluster_7,
               cluster_8,
               cluster_9,]

    cuisine_mapping={}
    cuisine_mapping["italian"]= 0
    cuisine_mapping["mexican"]= 1
    cuisine_mapping["french"]= 2
    cuisine_mapping["indian"]= 3
    cuisine_mapping["southern_us"]= 4
    cuisine_mapping["chinese"]= 5
    cuisine_mapping["japanese"]= 6
    cuisine_mapping["korean"]= 7



    #fill inn cluster lists
    cuisines_dict = dict(recipes_clusters)
    for k in range(10):  # cast data structre from counter to dict
        cuisines_dict[k]= dict(cuisines_dict[k])
        sorted_cuisines = sorted(cuisines_dict[k].items(), key=operator.itemgetter(1),reverse = True)
        cuisines_dict[k] = collections.OrderedDict(sorted_cuisines)

    rank =0

    for cluster in cuisines_dict.keys():
        rank =0
        cluster_done =False
        for cuisine in dict(cuisines_dict[cluster]).keys():
            if cluster_done:
                break
            if rank < 3:
                clusters[cluster][cuisine_mapping[cuisine]] = cuisines_dict[cluster][cuisine]
            rank+=1
        else:
            cluster_done=True

    # remove comment to plot in percentages

    n_recipes =[] #holding number of recipes in every cluster
    for cluster in cuisines_dict.keys():
        sum =0
        for cuisine in dict(cuisines_dict[cluster]).keys():
                sum+=cuisines_dict[cluster][cuisine]
        n_recipes.append(sum)

    for cluster in cuisines_dict.keys():
        rank =0
        cluster_done =False
        for cuisine in dict(cuisines_dict[cluster]).keys():
            if cluster_done:
                break
            if rank < 3:
                percentage = (cuisines_dict[cluster][cuisine] / n_recipes[cluster]) * 100
                clusters[cluster][cuisine_mapping[cuisine]] = percentage
                clusters[cluster][cuisine_mapping[cuisine]] = cuisines_dict[cluster][cuisine]
            rank+=1
        else:
            cluster_done=True


    cluster_0 = clusters[0]
    cluster_1 = clusters[1]
    cluster_2 = clusters[2]
    cluster_3 = clusters[3]
    cluster_4 = clusters[4]
    cluster_5 = clusters[5]
    cluster_6 = clusters[6]
    cluster_7 = clusters[7]
    cluster_8 = clusters[8]
    cluster_9 = clusters[9]

    print("0",cluster_0)
    print("1",cluster_1)
    print("2",cluster_2)
    print("3",cluster_3)
    print("4",cluster_4)
    print("5",cluster_5)
    print("6",cluster_6)
    print("7",cluster_7)
    print("8",cluster_8)
    print("9",cluster_9)

    matrix = [cluster_0,
              cluster_1,
              cluster_2,
              cluster_3,
              cluster_4,
              cluster_5,
              cluster_6,
              cluster_7,
              cluster_8,
              cluster_9,]

    transpose = np.transpose(matrix)
    a = transpose
    b= list(a)
    print(a)

    # Set position of bar on X axis
    r1 = np.arange(len(transpose[0]))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    r6 = [x + barWidth for x in r5]
    r7 = [x + barWidth for x in r6]
    r8 = [x + barWidth for x in r7]

    #trikse for hånd for å ordne spacing
    r4[1] -=barWidth            #cluster2
    r5[2] -=(barWidth * 2)      #cluster3
    r5[3] -=(barWidth * 2)      #cluster4
    r3[4] -= barWidth           #cluster5
    r5[4] -= barWidth*2         #cluster5
    r6[5] -=barWidth*5          #cluster6
    r7[5]  -=barWidth*5         #cluster6
    r8[5]  -=barWidth*5         #cluster6 
    r5[6] -= barWidth*2
    r4[7] -= barWidth
    r4[8] -= barWidth
    r5[9]  -=barWidth*2

    # Make the plot
    plt.bar(r1, list(transpose[0]), color='#4e79a7', width=barWidth, edgecolor='white', label='italian')
    plt.bar(r2, list(transpose[1]), color='#f28e2b', width=barWidth, edgecolor='white', label='mexican')
    plt.bar(r3, list(transpose[2]), color='#e15759', width=barWidth, edgecolor='white', label='french')
    plt.bar(r4, list(transpose[3]), color='#76b7b2', width=barWidth, edgecolor='white', label='indian')
    plt.bar(r5, list(transpose[4]), color='#59a14f', width=barWidth, edgecolor='white', label='southern')
    plt.bar(r6, list(transpose[5]), color='#edc948', width=barWidth, edgecolor='white', label='chinese')
    plt.bar(r7, list(transpose[6]), color='#b07aa1', width=barWidth, edgecolor='white', label='japanese')
    plt.bar(r8, list(transpose[7]), color='#9c755f', width=barWidth, edgecolor='white', label='korean')
    #plt.bar(r9, list(transpose[8]), color='#2d7f5e', width=barWidth, edgecolor='white', label='var9')
    #plt.bar(r10,list(transpose[9]), color='#2d7f5e', width=barWidth, edgecolor='white', label='var10')

    # Add xticks on the middle of the group bars
    plt.xlabel('Clusters', fontweight='bold')
    plt.ylabel('Recipes (Percent)',fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(transpose[0]))], ['1', '2', '3', '4', '5','6','7','8','9','10'])

    # Create legend & Show graphic
    plt.legend()
    plt.show()

top_3_histogram_plot(recipes_cuisines)

