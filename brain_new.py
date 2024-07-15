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
        self.session=session
        super().__init__()
        self.roi="SI"
        self.one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
        self.ba = AllenAtlas()
        
        self.ses=self.one.alyx.rest('insertions', 'list', atlas_acronym = self.roi) #loading recordings
        self.EID=self.ses[0]['session']
        

        self.spikes=self.session.spikes
        self.clusters =self.session.cluster
        self.channels = self.session.channels
        self.end = self.spikes.times[-1]
        self.goCue, self.feedbackTime, self.feedbackType,self.stim, self.firstWheelMove, self.start = self.session.getTommyStuff()

        self.scene = Scene(atlas_name="allen_mouse_25um", title="")
        #self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)

        #self.plotter.roll(180)
        #self.plotter.background((30,30,30))
        self.scene.get_actors()[0].actor.GetProperty().SetColor(1,1,1)
        self.regionModels=self.getRegionModel(self.clusters,self.scene)
        super().setActors(self.scene.get_actors())   
        for i in range(1, len(self.actors)):
            self.actors[i].actor.GetProperty().SetRepresentation(1) 
    
    def addToPlotter(self, plotter):
        return super().addToPlotter(plotter)
   
    def getRegionModel(self,clusters, scene):
        regionModels = []
        for acro in list(set(clusters.acronym)):
            regionModels.append([acro, scene.add_brain_region(acro, alpha=0.5)])
        return regionModels
