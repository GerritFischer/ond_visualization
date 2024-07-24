from vedo import Text2D, Image
import matplotlib.pyplot as plt
import vtk
import numpy as np
import math
from actortemplate import *
class Timeline(ActorTemplate):
    def __init__(self,x, y):
        super().__init__()
        self.x = x
        self.y = y
        #self.generateOverlay("↓ - Go Cues")
        self.generateHistogram()
        self.data_names = []
        self.dataset = []
        for i in range(100):
            self.data_names.append("")
            self.dataset.append(i+1)
        

    def generateOverlay(self, headingString):
        heading = Text2D(headingString)
        heading.pos((self.x+0.1, self.y+0.1))
        super().addActor(heading)
    def generateHistogram(self):
        #generate histogram in matplotlib
        fig = plt.figure()
        fig.add_subplot(111)
        N, bins, patches = plt.hist(x=[1,40,100],bins=100, range=(1,100))
        fig.tight_layout(pad=1)
        fig.canvas.draw()

        #get image data from plot
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        #turn image data into image from vedo
        pic = Image(data)
        pic.resize([400,300])

        #map image to 2d actor
        mapper = vtk.vtkImageMapper()
        mapper.SetInputData(pic.dataset)
        mapper.SetColorWindow(255)
        mapper.SetColorLevel(127.5)
        actor2d = vtk.vtkActor2D()
        actor2d.SetMapper(mapper)
        actor2d.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        actor2d.SetPosition(self.x, self.y)
        actor2d.GetProperty().SetDisplayLocationToBackground()
        self.hist = actor2d      
        self.hist.SetVisibility(0)
        super().addActor(self.hist)
    def updateHistogram(self, plotter):
        #same as generate
        fig= plt.figure()
        ax = fig.add_subplot(111)
        fig.set_facecolor("black")
        ax.set_facecolor("black")

        N, bins, patches = plt.hist(self.dataset, bins=100, range=(1,100))
        for i, patch in enumerate(patches):
            if(self.data_names[i] == "Go Cue"):
                patch.set_facecolor((0,0,1))
            elif(self.data_names[i] == "Feedback Time, Reward"):
                patch.set_facecolor((0, 1, 0))
            elif(self.data_names[i] == "Feedback Time, Error"):
                patch.set_facecolor((1, 0, 0))
            elif(self.data_names[i] == "Feedback Time"): #for debug, delete later
                patch.set_facecolor((1, 0, 0))
            elif(self.data_names[i]=="First Wheel Movement"):
                patch.set_facecolor((1,1,0))
            else:
                patch.set_facecolor((0,0,0))
 
        patches[50].set_edgecolor((1,1,1))
        fig.tight_layout(pad=1)
        fig.canvas.draw()

        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        
        pic = Image(data)
        pic.resize([math.floor(plotter.window.GetActualSize()[0] * 0.15), math.floor(plotter.window.GetActualSize()[1] * 0.1)])
        pic.actor.SetPosition(0.3,0.3,0)


        mapper = vtk.vtkImageMapper()
        mapper.SetInputData(pic.dataset)
        mapper.SetColorWindow(255)
        mapper.SetColorLevel(127.5)
        self.hist.SetMapper(mapper)
        self.hist.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        self.hist.SetPosition(self.x, self.y)
        self.hist.GetProperty().SetDisplayLocationToBackground()
        self.hist.SetVisibility(1)
        #plt.close() maybe add this later

    def updateWholeDataSet(self, dataset):
        self.data_names = dataset
