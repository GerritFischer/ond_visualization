import numpy as np
from actortemplate import *
from brainrender import Scene
from brainbox.io.one import SpikeSortingLoader
from brainbox.plot import peri_event_time_histogram
from brainbox.singlecell import calculate_peths
from one.api import ONE
from ibllib.atlas import AllenAtlas
import math
class BrainNew(ActorTemplate):
    goCueIndex=0
    trialCounter=0
    feedbackIndex=0
    stimAppear=""
    stimCounter=0
    prevFeedIn=0
    prevGoCueIn=0
    prevTrialIn=0
    firstWheelMove=0

    def __init__(self, session):
        print("here")
        super().__init__()
        self.roi="SI"
        self.one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
        self.ba = AllenAtlas()
        
        self.ses=self.one.alyx.rest('insertions', 'list', atlas_acronym = self.roi) #loading recordings
        self.EID=self.ses[0]['session']
        

        self.spikes, self.clusters, self.channels = self.loadData()
        self.end = self.spikes.times[-1]
        self.goCue, self.feedbackTime, self.feedbackType,self.stim, self.firstWheelMove = self.loadTrials()

        self.scene = Scene(atlas_name="allen_mouse_25um", title="")
        #self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)

        #self.plotter.roll(180)
        #self.plotter.background((30,30,30))
        self.start = self.trialStart()
        self.scene.get_actors()[0].actor.GetProperty().SetColor(1,1,1)
        self.regionModels=self.getRegionModel(self.clusters,self.scene)
        super().setActors(self.scene.get_actors())    
    
    def addToPlotter(self, plotter):
        return super().addToPlotter(plotter)
    def loadData(self):       
        print(f'Found {len(self.ses)} recordings')
        #isolating first session and probe ID
        PID = self.ses[0]['id']
        sl = SpikeSortingLoader(pid=PID, one=self.one, atlas=self.ba) # create instance of the SpikeSortingLoader
        spikes, clusters, channels = sl.load_spike_sorting() # load in spike sorted data
        clusters = sl.merge_clusters(spikes, clusters, channels) # merge cluster metrics
        return spikes, clusters, channels
    def getRegionModel(self,clusters, scene):
        regionModels = []
        for acro in list(set(clusters.acronym)):
            regionModels.append([acro, scene.add_brain_region(acro, alpha=0.5)])
        return regionModels
    def loadTrials(self):
            trials = self.one.load_object(self.EID, 'trials')
            goCue= trials['goCueTrigger_times']
            feedbackTime=trials['feedback_times']
            feedbackType=trials['rewardVolume'] #Volume =0 error  >0 reward
            stimOff=trials['stimOff_times']
            stimOn=trials['stimOn_times']
            firstWheelMove=trials['firstMovement_times']
            stim=self.concat(stimOn,stimOff)
            return goCue, feedbackTime, feedbackType, stim, firstWheelMove
    def concat(self,on,off):
        onIndex=0
        offIndex=0
        counter=0
        stim=[]
        while(True):
            if(onIndex==len(on) and offIndex==len(off)):
                break
            else:
                if(counter%2==0):
                    stim.append(on[onIndex])
                    onIndex+=1
                else:
                    stim.append(off[offIndex])
                    offIndex+=1
                
            counter+=1
        return stim
    def trialStart(self):
        counter=0
        start=[]
        for time in self.feedbackTime:
            if self.feedbackType[counter]>0:
                start.append(time+1)
            else:
                start.append(time+2)
        return start