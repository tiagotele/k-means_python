#!/usr/bin/env python
# encoding:utf8

import csv
import os

os.system('clear')

database = []

clusters_number = 3

column_index = 0


def carrega_csv(nome_do_arquivo, array_destino):
    with open(nome_do_arquivo, 'r') as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) == 0: continue
            array_destino.append(r)
    f.close()


carrega_csv('iris.csv', database)

# Ratio of first split on my cluster
ratio = len(database) // clusters_number
print(ratio)

ratio_aux = ratio

# Used to define the centroid index
centroid_index = 0

centroids = {}

# First loop: to initiali split a specific row on equistant centroids
for database_line in range(len(database)):

    key = ('c' + str(centroid_index))
    if not (key in centroids):
        centroids['c' + str(centroid_index)] = {}
    centroids['c' + str(centroid_index)]['line' + str(database_line + 1)] = database[database_line][column_index]

    # print('c' + str(centroid_index) ,'-----', 'line' + str(database_line+1))

    if database_line > ratio_aux:
        print("ratio aux", ratio_aux)
        print("centroid_index", centroid_index)
        ratio_aux += ratio
        centroid_index += 1



# Algorithm
# Calculate mean for each centroid

print("----")
for centroids_index in range(len(centroids)):
    print("Centroid index = ", centroids_index)
    mean = 0
    for item in centroids[str('c') + str(centroids_index)]:
        # print(centroids[str('c') + str(centroids_index)][item])
        mean += float(centroids[str('c') + str(centroids_index)][item])
    mean /= float(len(centroids[str('c') + str(centroids_index)]))
    centroids[str('c') + str(centroids_index)]['mean'] = mean
    print("Mean for centroid ", centroid_index, mean)

#print(centroids)


def get_closes_centroid_name(value):
    centroid_item = ''
    first_difference = -1

    for centroid in centroids:
        if first_difference == -1:
            first_difference = abs(float(value) - centroids[centroid]['mean'])
            centroid_item = centroid
            continue

        difference = abs(float(value) - centroids[centroid]['mean'])

        if(first_difference > difference):
            first_difference = difference
            centroid_item = centroid
    return centroid_item

#Itereate over each centroid
for centroid in centroids:

    #Iterate over each centorid item
    for line in centroids[centroid]:
        if line != 'mean':
            print(centroid, line, centroids[centroid][line]," closest to centroid ", get_closes_centroid_name(centroids[centroid][line]))