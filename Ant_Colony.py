import sys
from random import random
from threading import Lock, Condition
from Ant import Ant

class AntColony:
    def __init__(self, graph, num_ants, num_iterations):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.ants_counter = 0
        self.iter_counter = 0

        self.best_path_cost = sys.maxint
        self.best_path = []
        self.best_path_change = []

        self.cv = Condition() #condition variable object in threading
        self.rho = 0.5 #evaporation coefficient

    def ants_run(self):
        self.ants = self.create_ants()

        while self.iter_counter < self.num_iterations:
            #print "Round " + str(self.iter_counter)
            self.ants_run_one_iteration()
            self.cv.acquire()
            #in each iteration, wait until the last ant calls notify() so that updates can happen
            self.cv.wait()
            self.global_updating_rule()
            self.best_path_change.append(self.best_path_cost)
            self.cv.release()
            for ant in self.ants:
                ant.__init__(ID=ant.ID, colony=ant.colony)

        #self.graph.tau_info()
        print "Path: " + str(self.best_path) + " Cost: " + str(self.best_path_cost)
        print self.best_path_change

    def create_ants(self):
        ants = []
        for i in range(0, self.num_ants):
            ant = Ant(ID=i, colony=self)
            ants.append(ant)

        return ants

    def ants_run_one_iteration(self):
        self.ants_counter = 0
        self.iter_counter+=1
        for ant in self.ants:
            ant.start()

    def global_updating_rule(self):
        pheromone_evap = 0 #evaporation
        pheromone_depo = 0 #deposition

        for i in range(0, len(self.best_path)-1):
            node_curr = self.best_path[i]
            node_next = self.best_path[i+1]
            pheromone_evap = (1 - self.rho) * self.graph.tau(node_curr, node_next)
            pheromone_depo = self.rho * (100/self.best_path_cost)
            self.graph.update_tau(node_curr, node_next, pheromone_evap + pheromone_depo)
            self.graph.update_tau(node_next, node_curr, pheromone_evap + pheromone_depo)
