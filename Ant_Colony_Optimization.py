import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import random, randint
from Ant_Grid import AntGrid
from Ant_Graph import AntGraph

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
    print "Shortest Path from Start to End: " + str(path) + " Length: " + str(dist[node_end])

def ACO():
    '''
    #initialization
    #1.transform grid into graph
    #2.num_ants
    #3.tau
    #4.lau = 0.8 or 0.9
    #5.alpha = 0.5, beta = 0.5

    iterations = 100
    time = 0
    while(time < iterations){
        #one or multiple ants find their solution path from start point to end point
        #use transition probability
        unvisited_nearby_nodes = []
        numerator = (tau[i][j] ^ alpha) * (1/adjacency[i][j] ^ beta)
        denominator = sum(numerator in unvisited_nearby_nodes)
        if(unvisited and nearby)
            probability_of_node = numerator/denominator
        else
            probability_of_node = 0
        choose the node that its probability_of_node is closest to random()

        #update pheromone on graph
        #use evaporation mechanism
        Q = 1 or 100
        delta = Q/path_length
        tau[i][j] = (1-lau) * tau[i][j] + delta[i][j]

        #update best path among all solution path
        time = time+1
    }
    '''

if __name__ == '__main__':
    myMap = AntGrid('./Dataset/P2ds0.txt')
    myMap.info()
    myGraph = AntGraph(myMap)
    myGraph.adj_info()
    Dijkstra(myGraph)
