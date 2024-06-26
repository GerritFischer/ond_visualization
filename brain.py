import time
import numpy as np
from vedo import Plotter
from vedo.pyplot import plot
from vedo import Text2D, Latex, Mesh
from vedo import Ellipsoid, show, colors
import random
from brainrender import Scene
from brainrender.actors import Points
from brainbox.io.one import SpikeSortingLoader
from brainbox.plot import peri_event_time_histogram
from brainbox.singlecell import calculate_peths
from one.api import ONE
from ibllib.atlas import AllenAtlas
import math
from function import *
from actors import *
from timeline import *

class brain:
    timer_id=-1
    time_e = 0
    button=None
    timer=0
    i=0
    start=0
    brain_actors = []
    def __init__(self) :
        self.roi="SI"
        self.one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
        self.ba = AllenAtlas()

        self.ses=self.one.alyx.rest('insertions', 'list', atlas_acronym = self.roi) #loading recordings
        self.EID=self.ses[0]['session']

        self.spikes, self.clusters, self.channels = self.loadData()
        self.end = self.spikes.times[-1]
        self.goCue, self.feedbackTime, self.feedbackType,self.stim= self.loadTrials()

        self.actors= actors(self.spikes,self.goCue,self.feedbackTime,self.feedbackType,self.stim)
        self.plotter=self.actors.getPlotter()

        self.scene = Scene(atlas_name="allen_mouse_25um", title="")
        self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)

        self.plotter.roll(180)
        self.plotter.background("grey0")

        self.plotter, self.text_array= createText(self.plotter)
        self.regionModels=getRegionModel(self.clusters,self.scene)
        self.brain_actors = self.scene.get_actors()

    
        


        

    def startRender(self):
        self.plotter.show( __doc__, self.brain_actors)

    def loadData(self):
        print(f'Found {len(self.ses)} recordings')
        #isolating first session and probe ID
        PID = self.ses[0]['id']
        sl = SpikeSortingLoader(pid=PID, one=self.one, atlas=self.ba) # create instance of the SpikeSortingLoader
        spikes, clusters, channels = sl.load_spike_sorting() # load in spike sorted data
        clusters = sl.merge_clusters(spikes, clusters, channels) # merge cluster metrics
        return spikes, clusters, channels
    
    def loadTrials(self):
        trials = self.one.load_object(self.EID, 'trials')
        goCue= trials['goCueTrigger_times']
        feedbackTime=trials['feedback_times']
        feedbackType=trials['rewardVolume'] #Volume =0 error  >0 reward
        stimOff=trials['stimOff_times']
        stimOn=trials['stimOn_times']
        stim=concat(stimOn,stimOff)
        return goCue, feedbackTime, feedbackType, stim
    
    def animation_tick(self,event):
        print("TICK TACK")
        if self.actors.isSkipped():
            print("hey")
            self.actors.setSkipped()
            self.timer=self.actors.getTimer()
            self.i=self.actors.getSpikeIndex()
        self.brain_actors[0].actor.GetProperty().SetColor(1,1,1)
        if(self.timer < self.end):
            
            self.actors.timeline.updateHistogram(self.timer, self.actors.prevAction)
            currentSpikes = []
            elemStillIn = True
            
            while(elemStillIn):
                if(self.i >= len(self.spikes.times)):
                    print("BREAAAK") 
                    break
                if(self.spikes.times[self.i] > self.timer and self.spikes.times[self.i] < self.timer + 0.1):
                    currentSpikes.append(self.i)
            
                else:
                    elemStillIn = False
                self.i += 1
             

            
            self.text_array[19].text("Total Spikes: " + str(len(currentSpikes)))
            #outputString = "Total Spikes: " + str(len(currentSpikes)) + "\n"
            for k in range(len(self.regionModels)):
                spikesInRegion = 0
                for j in currentSpikes:
                    if(self.clusters.acronym[self.spikes.clusters[j]] == self.regionModels[k][0]):
                        spikesInRegion += 1
            #outputString += "Spikes in " + regionModels[k][0] + ": " + str(spikesInRegion) + "\n"
                self.brain_actors[k+1].actor.GetProperty().SetOpacity(spikesInRegion * 0.01)#überarbeite mit len (actors)
                o = Mesh()
                

                color = hsv2rgb(k / len(self.regionModels), 1,1)
                color255 = (color[0]/255, color[1]/255, color[2]/255)
            
            
                self.text_array[18-k].text("Spikes in " + self.regionModels[k][0] + ": " + str(spikesInRegion))
                self.text_array[18-k].properties.SetColor(color255)
                self.brain_actors[k+1].actor.GetProperty().SetColor(color255)#überarbeite mit len (actors)
                self.brain_actors[k+1].actor.GetProperty().SetRepresentation(1)#überarbeite mit len (actors)
            print("REACHED")
            #regionModels[i][1].SetAlpha(spikesInRegion * 0.01)
            #outputString += "Time: " + str(timer)
            self.actors.updateTrialInfo(self.timer)
            print("REACHED2")

            self.text_array[18-len(self.regionModels)].text("Time: " + str(self.timer))
            #text.text(outputString)
            print(self.timer)
            self.timer = math.floor((self.timer*10)+1)/10
        self.time_e += 0.1
        self.plotter.render()

    

    
