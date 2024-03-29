import sys, os, io
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# MapMOS class has a static map given by MOS
class MapMOS:
    def __init__(self,mapfile):
        # initialize variables
        self.obstacleNames = []
        self.obstaclePos = {} # vertex_name: pos [x,y,z]
        self.readmapfile(mapfile)

    def readmapfile(self, mapfile):
        f = open(mapfile, 'r')
        lines = f.readlines()
        self.height = int(lines[1].split(' ')[1])
        self.width = int(lines[2].split(' ')[1])
        lnum = 4 # line number
        
        self.obstaclesNum = 0

        while lnum < len(lines):
            for i in range(self.width):
                if lines[lnum][i] == "@":
                    self.obstacleNames.append(self.obstaclesNum)
                    self.obstaclePos[self.obstaclesNum] = {"x":i,"y":self.height - (lnum-2)}
                    self.obstaclesNum += 1
            lnum += 1
        f.close()

    def draw_map(self):
        aspect = self.width / self.height
        self.fig = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0,right=1,bottom=0,top=1, wspace=None, hspace=None)
        xmin = 0
        ymin = 0
        xmax = self.width
        ymax = self.height

        # self.ax.relim()
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)

        for o in self.obstacleNames:
            self.ax.add_patch(Rectangle((self.obstaclePos[o]["x"], self.obstaclePos[o]["y"]+1), 1, 1, facecolor='red', edgecolor='red'))
        #plt.pause(100)


if __name__=="__main__":
    map = MapMOS("random-32-32-20.map")
    map.draw_map()


