import sys
from math import pow
from random import random, shuffle
from threading import *

class Ant(Thread): #inherit Thread class
    def __init__(self, ID, colony):
        Thread.__init__(self)
        self.ID = ID
        self.colony = colony
        self.graph = self.colony.graph
        self.node_start = colony.graph.node_index(colony.graph.start)
        self.node_end = colony.graph.node_index(colony.graph.end)

        self.node_curr = self.node_start
        self.path = [self.node_start]
        self.path_cost = 0

        self.nodes_to_visit = [0 for i in range(0, colony.graph.num_nodes)]
        self.nodes_to_visit[self.node_start] = 1

        self.q0 = 0.5

    #override run method in Thread
    def run(self):
        graph = self.colony.graph

        while not self.end():
            # we need exclusive access to the graph
            graph.lock.acquire()

            node_next = self.state_transition_rule(self.node_curr)
            self.nodes_to_visit[node_next] = 1
            self.path.append(node_next)
            #print self.path
            self.path_cost+=graph.edge(self.node_curr, node_next)
            self.local_updating_rule(self.node_curr, node_next)
            self.node_curr = node_next

            graph.lock.release()

        #send our results back to the colony
        self.update()

        #allow threads to be restarted (calls Thread.__init__)
        #self.__init__(ID=self.ID, colony=self.colony)

    def end(self):
        return (self.node_curr == self.node_end)

    #determine next node after current node
    def state_transition_rule(self, node_curr):
        graph = self.colony.graph
        q = random()
        alpha = 1
        beta = 2
        node_next = -1 #node with maximum pheromone value
        val_max = -1
        val_sum = 0
        diff_min = 10

        if q > self.q0:
            #print "Exploration"
            neighbors = graph.node_neighbors(node_curr)
            for node in neighbors:
                val_sum+=pow(graph.eta(node_curr, node), beta) * pow(graph.tau(node_curr, node), alpha)

            indicator = random()
            shuffle(neighbors)
            for node in neighbors:
                val = pow(graph.eta(node_curr, node), beta) * pow(graph.tau(node_curr, node), alpha)
                probability = val / val_sum
                diff = abs(indicator - probability)

                if diff < diff_min and self.nodes_to_visit[node] != 1:
                    diff_min = diff
                    node_next = node
            if node_next == -1:
                node_next = neighbors[0]

        else:
            #print "Exploitation"
            neighbors = graph.node_neighbors(node_curr)
            shuffle(neighbors)
            #print neighbors
            for node in neighbors:
                val = pow(graph.eta(node_curr, node), beta) * pow(graph.tau(node_curr, node), alpha)
                #print val
                if self.nodes_to_visit[node] == 1:
                    val = 0
                if val > val_max:
                    val_max = val
                    node_next = node

        return node_next

    #update pheromone when going through edges
    def local_updating_rule(self, node_curr, node_next):
        rho = self.colony.rho
        graph = self.colony.graph
        val = (1 - rho) * graph.tau(node_curr, node_next) + (rho * graph.tau0)
        graph.update_tau(node_curr, node_next, val)
        graph.update_tau(node_next, node_curr, val)

    def update(self):
        lock = Lock()
        lock.acquire()
        #print "Ant thread " + str(self.ID) + " terminating." + " Path: " + str(self.path) + " Cost: " + str(self.path_cost) + "\n"
        print "Ant thread " + str(self.ID) + " terminating." + " Cost: " + str(self.path_cost) + "\n"

        self.colony.ants_counter+=1

        if self.colony.best_path_cost > self.path_cost:
            self.colony.best_path_cost = self.path_cost
            self.colony.best_path = self.path

        if self.colony.ants_counter == len(self.colony.ants):
            self.colony.cv.acquire()
            self.colony.cv.notify()
            self.colony.cv.release()

        lock.release()
