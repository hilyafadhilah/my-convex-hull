#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find Convex Hull"""
import random

import pandas as pd 
import matplotlib.pyplot as plt
from sklearn import datasets

from view import colors, displayHeader, displayList, inputInt, toTitle
from hull import myConvexHull

datasetlst = [
    { 'label': 'Iris', 'loader': datasets.load_iris },
    { 'label': 'Digits', 'loader': datasets.load_digits },
    { 'label': 'Wine', 'loader': datasets.load_wine },
    { 'label': 'Breast Cancer', 'loader': datasets.load_breast_cancer },
]

# Choose dataset
displayHeader('Choose dataset')
displayList(datasetlst, key='label')
inp = inputInt('Dataset>', 1, len(datasetlst)) - 1
data = datasetlst[inp]['loader']()

# Choose X and Y axis property
properties = list(map(lambda x: toTitle(x), data.feature_names))
displayHeader('Choose X and Y axis')
displayList(properties)
xAxis = inputInt('X Axis>', 1, len(properties)) - 1
yAxis = inputInt('Y Axis>', 1, len(properties), exclude=[xAxis + 1]) - 1

displayHeader('Results will be shown shortly')
print('   Note: The colors are chosen and random. In order\n'
      '         to get suitable colors, run this program over\n'+
      '         and over until you get the best results.')

# Create dataframe
df = pd.DataFrame(data.data, columns=data.feature_names) 
df['Target'] = pd.DataFrame(data.target) 

# Display preprocessing

xLabel = properties[xAxis]
yLabel = properties[yAxis]

plt.figure(figsize = (10, 6))
plt.title(f"{xLabel} vs {yLabel}")
plt.xlabel(xLabel)
plt.ylabel(yLabel)

random.shuffle(colors)

displayHeader('Convex Hull algorithm')

# Display each data group and its convex hull
targetNames = list(map(lambda x: toTitle(x), data.target_names))
for i in range(len(targetNames)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:, [xAxis, yAxis]].values
    plt.scatter(bucket[:, 0], bucket[:, 1], label=targetNames[i], alpha=0.5, c=colors[i])

    hull = myConvexHull(bucket)
    for s in hull.simplices:
        plt.plot(s[0], s[1], alpha=0.7, c=colors[i])

    print(f"   [{targetNames[i]}]\n" +
          f"     Point Count   : {bucket.shape[0]}\n" +
          f"     Divide Count  : {hull.divideCount}\n" +
          f"     Operate Count : {hull.operateCount}\n")

# Done ;)

plt.legend()
plt.show()

displayHeader('Thank you for using our service >_<')
