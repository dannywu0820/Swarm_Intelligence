import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import random, randint

def read_map(file_name):
    myMap = {}
    fp = open(file_name, 'r')
    lines = fp.readlines()
    myMap['size'] = int(lines[0])
    points = lines[-1].split()
    myMap['start'] = [(myMap['size']-1)-int(points[1]), int(points[0])]
    myMap['end'] = [(myMap['size']-1)-int(points[3]), int(points[2])]
    myMap['heights'] = []
    for line in lines[1:len(lines)-1]:
        data = line.split()
        numbers = []
        for number in data:
            numbers.append(int(number))
        if len(numbers) != 0:
            myMap['heights'].append(numbers)

    return myMap

def map_info(myMap):
    print "Map Size: " + str(myMap['size'])
    print "Start Point: " + str(myMap['start'])
    print "End Point:   " + str(myMap['end'])
    print np.array(myMap['heights'])
    start_x, start_y = myMap['start'][0], myMap['start'][1]
    print myMap['heights'][start_x][start_y]
    end_x, end_y = myMap['end'][0], myMap['end'][1]
    print myMap['heights'][end_x][end_y]

def map_to_graph(myMap):
    num_nodes = myMap['size']*myMap['size']
    adjacency = [[10000 for x in range(num_nodes)] for y in range(num_nodes)]
    for x in range(0, myMap['size']):
        for y in range(0, myMap['size']):
            node_index = x*myMap['size'] + y #x = index/size, y = index%size
            if x != 0:
                height_diff = myMap['heights'][x][y] - myMap['heights'][x-1][y]
                edge = height_diff * height_diff
                adjacency[node_index][node_index-myMap['size']] = edge
                adjacency[node_index-myMap['size']][node_index] = edge
            elif x != myMap['size']-1:
                height_diff = myMap['heights'][x][y] - myMap['heights'][x+1][y]
                edge = height_diff * height_diff
                adjacency[node_index][node_index+myMap['size']] = edge
                adjacency[node_index+myMap['size']][node_index] = edge
            else:
                pass

            if y != 0:
                height_diff = myMap['heights'][x][y] - myMap['heights'][x][y-1]
                edge = height_diff * height_diff
                adjacency[node_index][node_index-1] = edge
                adjacency[node_index-1][node_index] = edge
            elif y != myMap['size']-1:
                height_diff = myMap['heights'][x][y] - myMap['heights'][x][y+1]
                edge = height_diff * height_diff
                adjacency[node_index][node_index+1] = edge
                adjacency[node_index+1][node_index] = edge
            else:
                pass

    print np.array(adjacency)
    return adjacency

def dijkstra(adjacency, myMap):
    start_index = myMap['start'][0]*myMap['size'] + myMap['start'][1]
    end_index = myMap['end'][0]*myMap['size'] + myMap['end'][1]
    num_nodes = myMap['size']*myMap['size']

    dist = [10000 for i in range(0, num_nodes)]
    prev = [-1 for i in range(0, num_nodes)]
    for i in range(0, num_nodes):
        dist[i] = adjacency[start_index][i]
        prev[i] = start_index
    dist[start_index] = 0
    prev[start_index] = -1
    choosed = [0 for i in range(0, num_nodes)]
    choosed[start_index] = 1
    fin_cnt = 1
    while fin_cnt < num_nodes:
        min_dist = 10000
        min_index = -1

        #choose the node with min dist to update path
        for i in range(0, num_nodes):
            if choosed[i] == 1:
                continue
            if dist[i] < min_dist:
                min_index = i
                min_dist = dist[i]
        if min_index == -1:
            break
        else:
            choosed[min_index] = 1
            fin_cnt+=1

        #update path
        for i in range(0, num_nodes):
            if choosed[i] == 1:
                continue
            if dist[min_index] + adjacency[min_index][i] < dist[i]:
                dist[i] = dist[min_index] + adjacency[min_index][i]
                prev[i] = min_index
    print dist[end_index]
    print dist
    print prev

    curr_index = end_index
    prev_index = prev[end_index]
    path = []
    while prev_index != -1:
        path.append(curr_index)
        curr_index = prev_index
        prev_index = prev[prev_index]
    path.append(curr_index)
    path = list(reversed(path))
    print path

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
    myMap = read_map('./Dataset/P3ds0.txt')
    map_info(myMap)
    adjacency = map_to_graph(myMap)
    dijkstra(adjacency, myMap)
