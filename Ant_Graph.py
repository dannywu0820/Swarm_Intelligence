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
        self.adj_mat = [[1000 for x in range(self.num_nodes)] for y in range(self.num_nodes)]
        self.tau_mat = [] #tau of edge i,j
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

    def adj_info(self):
        print "Adjacency Matrix:"
        print np.array(self.adj_mat)

    def node_index(self, xy_coordinate):
        return xy_coordinate[0]*self.size + xy_coordinate[1]
