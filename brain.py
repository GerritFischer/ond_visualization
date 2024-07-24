from actortemplate import *
from brainrender import Scene
class Brain(ActorTemplate):

    def __init__(self, session):
        self.session=session
        super().__init__()
        
        #get the Trial Data from the given session which is from library functions_cv6
        self.spikes=self.session.spikes
        self.clusters =self.session.cluster
        self.channels = self.session.channels
        self.end = self.spikes.times[-1]
        self.goCue, self.feedbackTime, self.feedbackType,self.stim, self.firstWheelMove, self.start = self.session.getTommyStuff()

        self.scene = Scene(atlas_name="allen_mouse_25um", title="") #load brain model
        self.scene.get_actors()[0].actor.GetProperty().SetColor(1,1,1)
        self.regionModels=self.getRegionModel(self.clusters,self.scene) #load brain regions
        super().setActors(self.scene.get_actors())   
        #setup mesh rendering
        for i in range(1, len(self.actors)):
            self.actors[i].actor.GetProperty().SetRepresentation(1) 
    
    def getRegionModel(self,clusters, scene):
        #return brain regions and acronyms, for color/opacity change
        regionModels = []
        for acro in list(set(clusters.acronym)):
            regionModels.append([acro, scene.add_brain_region(acro, alpha=0.5)])
        return regionModels
