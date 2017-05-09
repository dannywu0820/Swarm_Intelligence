import sys
import numpy as np
from threading import Lock
from Ant_Grid import AntGrid


class AntGraph:
    def __init__(self, antgrid):
        self.start = antgrid.start
        self.end = antgrid.end
        self.size = antgrid.size
        self.num_nodes = antgrid.size * antgrid.size

        #adjacency matrix, which contains (height difference)^2
        self.adj_mat = [[sys.maxint for x in range(self.num_nodes)] for y in range(self.num_nodes)]
        #tau of edge i,j
        self.tau_mat = [[1 for x in range(self.num_nodes)] for y in range(self.num_nodes)]
        self.lock = Lock()

        for x in range(0, antgrid.size):
            for y in range(0, antgrid.size):
                node_index = x*antgrid.size + y #x = index/size, y = index%size
                if x != 0:
                    height_diff = antgrid.heights[x][y] - antgrid.heights[x-1][y]
                    edge = height_diff * height_diff
                    self.adj_mat[node_index][node_index-antgrid.size] = edge
                    self.adj_mat[node_index-antgrid.size][node_index] = edge
                elif x != antgrid.size-1:
                    height_diff = antgrid.heights[x][y] - antgrid.heights[x+1][y]
                    edge = height_diff * height_diff
                    self.adj_mat[node_index][node_index+antgrid.size] = edge
                    self.adj_mat[node_index+antgrid.size][node_index] = edge
                else:
                    pass

                if y != 0:
                    height_diff = antgrid.heights[x][y] - antgrid.heights[x][y-1]
                    edge = height_diff * height_diff
                    self.adj_mat[node_index][node_index-1] = edge
                    self.adj_mat[node_index-1][node_index] = edge
                elif y != antgrid.size-1:
                    height_diff = antgrid.heights[x][y] - antgrid.heights[x][y+1]
                    edge = height_diff * height_diff
                    self.adj_mat[node_index][node_index+1] = edge
                    self.adj_mat[node_index+1][node_index] = edge
                else:
                    pass

    def average(self, matrix):
        sum = 0
        for row in range(0, self.num_nodes):
            for col in range(0, self.num_nodes):
                sum += matrix[row][col]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

    def adj_info(self):
        print "Adjacency Matrix:"
        print np.array(self.adj_mat)

    def node_index(self, xy_coordinate):
        return xy_coordinate[0]*self.size + xy_coordinate[1]

    def node_position(self, node_index):
        return [node_index/self.size, node_index%self.size]

    def edge(self, node_curr, node_next):
        return self.adj_mat[node_curr][node_next]

    def average_edge(self):
        return self.average(self.adj_mat)

    def eta(self, node_curr, node_next):
        return 1.0 / (self.edge(node_curr, node_next)+1)

    def tau(self, node_curr, node_next):
        return self.tau_mat[node_curr][node_next]

    def reset_tau(self):
        lock = Lock()
        lock.acquire()
        avg = self.average_edge()

        # initial tau
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)

        print "Average = %s" % (avg,)
        print "Tau0 = %s" % (self.tau0)

        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0
        lock.release()

    def update_tau(self, node_curr, node_next, val):
        lock = Lock()
        lock.acquire()
        self.tau_mat[node_curr][node_next] = val
        self.tau_mat[node_next][node_curr] = val
        lock.release()

    def node_neighbors(self, node_curr):
        neighbors = []
        xy_curr = self.node_position(node_curr)

        if xy_curr[1] - 1 >= 0: #left
            neighbors.append(node_curr-1)
        if xy_curr[1] + 1 <= (self.size-1): #right
            neighbors.append(node_curr+1)
        if xy_curr[0] - 1 >= 0: #up
            neighbors.append(node_curr-self.size)
        if xy_curr[0] + 1 <= (self.size-1): #down
            neighbors.append(node_curr+self.size)

        return neighbors
