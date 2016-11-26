#!/usr/bin/env python
# encoding:utf8

import csv
import os
import copy


def load_csv(nome_do_arquivo, array_destino):
    with open(nome_do_arquivo, 'r') as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) == 0: continue
            array_destino.append(r)
    f.close()


# First loop: to initiali split a specific row on equidistant centroids
def generate_first_centroids_distribuition():
    global centroid_index
    global ratio_aux

    for database_line in range(len(database)):

        key = ('c' + str(centroid_index))
        if not (key in centroids):
            centroids['c' + str(centroid_index)] = {}
        centroids['c' + str(centroid_index)]['line' + str(database_line + 1)] = database[database_line][column_index]

        if database_line > ratio_aux:
            ratio_aux += ratio
            centroid_index += 1


def get_closes_centroid_name(value):
    centroid_item = ''
    first_difference = -1

    for centroid in centroids:
        if first_difference == -1:
            first_difference = abs(float(value) - centroids[centroid]['mean'])
            centroid_item = centroid
            continue

        difference = abs(float(value) - centroids[centroid]['mean'])

        if first_difference > difference:
            first_difference = difference
            centroid_item = centroid
    return centroid_item


# Algorithm
# Calculate mean for each centroid

print("----")


def calculate_means_for_each_centroid():
    for centroids_index in range(len(centroids)):
        mean = 0
        for item in centroids[str('c') + str(centroids_index)]:
            mean += float(centroids[str('c') + str(centroids_index)][item])
        mean /= float(len(centroids[str('c') + str(centroids_index)]))
        centroids[str('c') + str(centroids_index)]['mean'] = mean


# Iterate over each centroid
def alocate_elements_in_rigth_centroid():
    global elements_changed
    elements_changed = False
    for centroid in centroids:

        # Iterate over each centroid item
        for line in centroids[centroid]:
            if line != 'mean':
                correct_centroid = get_closes_centroid_name(centroids[centroid][line])
                if not correct_centroid == centroid:
                    centroids_changed[correct_centroid][line] = {}
                    centroids_changed[correct_centroid][line] = centroids_changed[centroid][line]
                    del centroids_changed[centroid][line]
                    elements_changed = True


os.system('clear')

database = []

# Number of cluster to split the database
clusters_number = 3

# Column of database to be classified
column_index = 0

# Used when splitting database into clusters
centroid_index = 0

# Dictionary that holds database classified in clusters
centroids = {}

# Auxiliary dictionary
centroids_changed = {}

load_csv('iris.csv', database)

# Ratio of first split on my cluster
ratio = len(database) // clusters_number
ratio_aux = ratio
generate_first_centroids_distribuition()

if __name__ == "__main__":

    iterations = 0
    elements_changed = True
    while elements_changed:
        iterations += 1
        calculate_means_for_each_centroid()
        centroids_changed = copy.deepcopy(centroids)
        alocate_elements_in_rigth_centroid()
        centroids = copy.deepcopy(centroids_changed)

    print("Iterations = ", iterations)
    print(centroids)
