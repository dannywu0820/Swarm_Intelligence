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
            #self.global_updating_rule()
            self.cv.release()
            for ant in self.ants:
                ant.__init__(ID=ant.ID, colony=ant.colony)

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

    def update(self, ant):
        lock = Lock()
        lock.acquire()
        print "Ant thread " + str(ant.ID) + " terminating." + " Path: " + str(ant.path)

        self.ants_counter+=1

        if self.ants_counter == len(self.ants):
            self.cv.acquire()
            self.cv.notify()
            self.cv.release()

        lock.release()
