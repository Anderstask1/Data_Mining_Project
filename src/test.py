import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25

# set height of bar
#       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
n_cuisines = 7

cluster_0 =[0] * n_cuisines
cluster_1 =[0] * n_cuisines
cluster_2 =[0] * n_cuisines
cluster_3 =[0] * n_cuisines
cluster_4 =[0] * n_cuisines
cluster_5 =[0] * n_cuisines
cluster_6 =[0] * n_cuisines
cluster_7 =[0] * n_cuisines
cluster_8 =[0] * n_cuisines
cluster_9 =[0] * n_cuisines


italian = 0
mexican = 1
french  = 2
indian  = 3
southern= 4
chinese = 5
japanese= 6

# set height of bar
bars1 = [12, 30, 0, 8, 22]
bars2 = [28, 6, 16, 5, 10]
bars3 = [29, 3, 24, 25, 17]


# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='var1')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='var2')
plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')

# Add xticks on the middle of the group bars
plt.xlabel('group', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(bars1))], ['A', 'B', 'C', 'D', 'E'])

# Create legend & Show graphic
plt.legend()
plt.show()
