from vedo import Text2D, Image
import matplotlib.pyplot as plt
import vtk
import numpy as np
class timeline:
    actors = []
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.generateOverlay("↓ - Go Cues")
        self.generateHistogram()
        self.data_names = []
        self.dataset = []
        for i in range(100):
            self.data_names.append("")
            self.dataset.append(i+1)
        

    def generateOverlay(self, headingString):
        heading = Text2D(headingString)
        heading.pos((self.x+0.1, self.y+0.1))
        self.actors.append(heading)
    def generateHistogram(self):
        fig = plt.figure()
        fig.add_subplot(111)

        N, bins, patches = plt.hist(x=[1,40,100],bins=100, range=(1,100))
        fig.tight_layout(pad=1)
        fig.canvas.draw()

        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))


        pic = Image(data)
        pic.resize([400,300])


        mapper = vtk.vtkImageMapper()
        mapper.SetInputData(pic.dataset)
        mapper.SetColorWindow(255)
        mapper.SetColorLevel(127.5)
        actor2d = vtk.vtkActor2D()
        actor2d.SetMapper(mapper)
        actor2d.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        actor2d.SetPosition(self.x, self.y)
        actor2d.GetProperty().SetDisplayLocationToBackground()
        actor2d.SetDisplayPosition(0,400)
        self.hist = actor2d      
        self.actors.append(self.hist)
    def updateHistogram(self, timer, prevAction):
        fig= plt.figure()
        ax = fig.add_subplot(111)
        fig.set_facecolor("black")
        ax.set_facecolor("black")

        self.data_names[0] = prevAction  
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
            else:
                patch.set_facecolor((0,0,0))
        for i in range(0,99):
            self.data_names[98-i+1] = self.data_names[98-i] 
        
        print(self.data_names)

        fig.tight_layout(pad=1)
        fig.canvas.draw()

        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))


        pic = Image(data)
        pic.resize([400,300])


        mapper = vtk.vtkImageMapper()
        mapper.SetInputData(pic.dataset)
        mapper.SetColorWindow(255)
        mapper.SetColorLevel(127.5)
        self.hist.SetMapper(mapper)
        self.hist.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        self.hist.SetPosition(self.x, self.y)
        self.hist.GetProperty().SetDisplayLocationToBackground()
        self.hist.SetDisplayPosition(0, 400)
    def addToPlotter(self, plotter):
        for actor in self.actors:
            plotter.add(actor)
    def updateWholeDataSet(self, dataset):
        self.data_names = dataset
