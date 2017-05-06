import numpy as np

class AntGrid:
    def __init__(self, file_name):
        fp = open(file_name, 'r')
        lines = fp.readlines()
        coordinate = lines[-1].split()
        coordinate = [int(i) for i in coordinate]

        #Size of map: self.size * self.size
        self.size = int(lines[0])
        #Bottom left of map is [0, 0], which needs to transform into python array index format
        self.start = [(self.size - 1) - coordinate[1], coordinate[0]]
        self.end = [(self.size - 1) - coordinate[3], coordinate[2]]

        heights = []
        for line in lines[1:len(lines)-1]:
            numbers = line.split()
            numbers = [int(number) for number in numbers]
            if len(numbers) != 0:
                heights.append(numbers)
        self.heights = heights

    def info(self):
        print "Grid Size: " + str(self.size) + " x " + str(self.size)
        print "Start Point: " + str(self.start) + " Height: " + str(self.heights[self.start[0]][self.start[1]])
        print "End Point:   " + str(self.end) + " Height: " + str(self.heights[self.end[0]][self.end[1]])
        print "Grid:"
        print np.array(self.heights)
