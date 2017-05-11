import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import random, randint
from Ant_Grid import AntGrid
from Ant_Graph import AntGraph
from Ant import Ant
from Ant_Colony import AntColony

def Dijkstra(graph):
    node_start = graph.node_index(graph.start)
    node_end = graph.node_index(graph.end)
    dist = [sys.maxint for i in range(graph.num_nodes)]
    prev = [-1 for i in range(0, graph.num_nodes)]
    choosed = [0 for i in range(0, graph.num_nodes)]
    for i in range(0, graph.num_nodes):
        dist[i] = graph.adj_mat[node_start][i]
        prev[i] = node_start

    dist[node_start], prev[node_start], choosed[node_start] = 0, -1, 1

    num_visited = 1
    while num_visited < graph.num_nodes:
        min_dist = sys.maxint
        min_index = -1

        #choose the node with min dist to update path
        for i in range(0, graph.num_nodes):
            if choosed[i] == 1:
                continue
            if dist[i] < min_dist:
                min_dist = dist[i]
                min_index = i
        if min_index == -1:
            break
        else:
            choosed[min_index] = 1
            num_visited+=1

        #update path
        for i in range(0, graph.num_nodes):
            if choosed[i] == 1:
                continue
            if dist[min_index] + graph.adj_mat[min_index][i] < dist[i]:
                dist[i] = dist[min_index] + graph.adj_mat[min_index][i]
                prev[i] = min_index

    print "Dist: " + str(dist)
    print "Prev: " + str(prev)

    curr_index = node_end
    prev_index = prev[node_end]
    path = []
    while prev_index != -1:
        path.append(curr_index)
        curr_index = prev_index
        prev_index = prev[prev_index]
    path.append(curr_index)
    path = list(reversed(path))
    print "Shortest Path from Start to End: " + str(path) + " Cost: " + str(dist[node_end])

if __name__ == '__main__':
    myMap = AntGrid('./Dataset/P3ds0.txt')
    myMap.info()
    myGraph = AntGraph(myMap)
    myGraph.adj_info()
    myGraph.reset_tau()
    Dijkstra(myGraph)

    num_ants = 10
    num_iterations = 30
    num_repetitions = 1 #times for running ACO algorithm
    best_path_vec = None
    best_path_cost = sys.maxint

    #for i in range(0, num_repetitions):
    myAntColony = AntColony(myGraph, num_ants, num_iterations)
    myAntColony.ants_run()
