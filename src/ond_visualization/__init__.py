from vedo import Button
class ActorTemplate:
    def __init__(self):
        self.actors = []
    def setActors(self, actors):
        self.actors = actors
    def addActor(self, actor):
       
        self.actors.append(actor)
    def addToPlotter(self, plotter):
        for actor in self.actors:
            if(type(actor) == CustomButton):
                plotter.add_button(actor.function, font=actor.font_s, states=actor.states, size=actor.size_s, pos=(actor.GetPositionCoordinate().GetValue()[0],actor.GetPositionCoordinate().GetValue()[1]))
            elif(type(actor) == CustomSlider):
                #test = Slider2D()
                #print(actor.GetCommand(1))
                plotter.add_slider(actor.sliderfunc, xmin=actor.GetRepresentation().GetMinimumValue(),  xmax=actor.GetRepresentation().GetMaximumValue(), value=actor.value, pos=actor.pos, title=actor.title, show_value=actor.show_value, c=(1,1,1))
                #super().addActor(Slider2D(self.speedslider, xmin=0, xmax=2999, value=2000, pos=[(0.8,0.05),(0.98, 0.05)], title="", show_value=True, c=(1,1,1)))
            else:
                plotter.add(actor)

from vedo import Sphere, LegendBox, Text2D

class Background(ActorTemplate):
    def __init__(self):
        super().__init__()
        self.generateBackground()
    def generateBackground(self):
        #generate actor with empty legend as placeholder
        placeholderSphere = Sphere()
        placeholderSphere.legend(" ")
        test = Sphere()
        test.legend("test")
        #top side bar 
        lboxSidebarTop = LegendBox([placeholderSphere], width=0.15, height=0.55, c=(0,0,0), pos="top-left", alpha=1, padding=0)
        lboxSidebarTop.SetBackgroundColor(0.14,0.14,0.14)
        lboxSidebarTop.SetEntryColor(0, 0.14,0.14,0.14)
        lboxSidebarTop.BorderOff()
        super().addActor(lboxSidebarTop)
        #bottom side bar
        lboxSidebarBottom = LegendBox([placeholderSphere], width=0.15, height=0.35, c=(0,0,0), pos="bottom-left", alpha=1, padding=0)
        lboxSidebarBottom.SetBackgroundColor(0.14,0.14,0.14)
        lboxSidebarBottom.SetEntryColor(0,0.14,0.14,0.14)
        lboxSidebarBottom.BorderOff()
        super().addActor(lboxSidebarBottom)
        lboxBottomBar = LegendBox([placeholderSphere], width=0.85, height=0.15, c=(0,0,0), pos="bottom-left", alpha=1, padding=0)
        lboxBottomBar.SetBackgroundColor(0.14,0.14,0.14)
        lboxBottomBar.SetEntryColor(0, 0.14,0.14,0.14)
        lboxBottomBar.BorderOff()
        lboxBottomBar.GetPositionCoordinate().SetValue(0.15, 0)
        super().addActor(lboxBottomBar)
        
        lboxSidebarHeading = Text2D(" Info ", (0, 1), bg=(0.23,0.23,0.23), c=(1,1,1))
        super().addActor(lboxSidebarHeading)
        lboxBottombarHeading = Text2D(" Playback ", (0.15, 0.15), bg=(0.23,0.23,0.23), c=(1,1,1))
        super().addActor(lboxBottombarHeading)
        lboxSidebarBHeading = Text2D(" Spikes ", (0, 0.348),bg=(0.23,0.23,0.23), c=(1,1,1))
        super().addActor(lboxSidebarBHeading)

import numpy as np
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

from vedo import Slider2D, Button
#custom classes to save values while creating other objects
class CustomSlider(Slider2D):
    def __init__(self, sliderfunc, xmin, xmax, value=None, pos=4, title="", font="Calco", title_size=1, c="k", alpha=1, show_value=True, delayed=False, **options):
        self.sliderfunc = sliderfunc
        self.pos = pos
        self.value = value
        self.title=title
        self.show_value=show_value
        super().__init__(sliderfunc, xmin, xmax, value=value, pos=pos, title=title, font=font, title_size=title_size, c=c, alpha=alpha, show_value=show_value, delayed=delayed, **options)

class CustomButton(Button):
    def __init__(self, fnc=None, states='Button', c='white',	bc='green4',pos=(0.7, 0.1),	size=24, font='Courier', bold=True,	italic=False,	alpha=1, angle=0):
        self.font_s = font
        self.size_s = size
        super().__init__(fnc, states, c, bc, pos, size, font, bold, italic, alpha, angle)

#! pip install ONE-api
#! pip install ibllib
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import functions from the brainbox package for spike sorting and peri-event time histograms (PETHs)
from brainbox.io.one import SpikeSortingLoader
from brainbox.plot import peri_event_time_histogram
from brainbox.singlecell import calculate_peths

from pprint import pprint # function for pretty printing

# Import the ONE (Open Neurophysiology Environment) class from the ONE API package
from one.api import ONE
from iblatlas.atlas import AllenAtlas

# Create an instance of the ONE class, specifying the base URL of the server and a password for authentication
one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
ba = AllenAtlas()


class Session:
    #takes in session as well as PIDs and EIDs if possible, creates spikes and clusters on its own
    spikes = None 
    channels = None                                  
    def __init__(self, session, pid = None, eid=None, PrintOn = False):
        self.sess = session
        self.sessEID = eid
        self.sessEIDInfo = self.getEIDinfo()
        self.sessPID = pid
        self.PrintOn = PrintOn
        self.cluster = self.getClusterAndSpikesOfSess()
        self.trials = one.load_object(self.sessEID,"trials")

        
    #method of the class that has the function of being activated when a class object is created and updates the attributes in the class object itself with the data of the choosen session    
    def getClusterAndSpikesOfSess(self):
        if (self.sessPID == None):
            return None
        else:
            sl = SpikeSortingLoader(pid=self.sessPID, one=one, atlas=ba) # create instance of the SpikeSortingLoader
            spikes, clusters, channels = sl.load_spike_sorting() # load in spike sorted data
            cluster = sl.merge_clusters(spikes, clusters, channels) # merge cluster metrics
            if(self.PrintOn):
                print(f"Number of Spikes is {(len(spikes['clusters']))}")
                print(f"Number of Clusters is {len(clusters['channels'])}")
            self.spikes = spikes
            self.channel = channels
            return cluster
               
    def getEIDinfo(self):
        eidInfo = one.alyx.rest('sessions', 'list', id = self.sessEID)
        return eidInfo[0]
    
    def getMainInfo(self):
        return [self.sessEID, self.sessPID, self.sessEIDInfo["subject"], self.sessEIDInfo["lab"]]
        #return list with sessionInfo  = [unknown EID, PID, subject, lab]


    def getLineGraph(self, events1, Roi, figsize1 =(7,7), intervall1 = [0.2, 0.5], bin_size1= 0.025, smoothing1=0.025, as_rate1 = True, include_raster1=False, 
                            n_raster1= None, error_bars1='std', pethline_kwargs1 = {'color': 'blue', 'lw': 2}, errbar_kwargs1 = {'color': 'blue', 'alpha': 0.5}, 
                            eventline_kwargs1={'color': 'black', 'alpha': 0.5}, raster_kwargs1={'color': 'black', 'lw': 0.5}, xlab ="", ylab = "", pidnmb = 1):
        if(self.cluster != None):
            acronym = self.cluster["acronym"]
            ROI_neurons = [i for i, acronym in enumerate(self.cluster['acronym']) if Roi in acronym]
            trials = self.trials
            f, ax1 = plt.subplots(1, 1, figsize= figsize1)
            peri_event_time_histogram(spike_times = self.spikes.times, spike_clusters= self.spikes.clusters, events= trials[events1],
                                    cluster_id= ROI_neurons[pidnmb],  #ehemals ROI Neurons gibt einfach eine einzige Cluster ID an such dir die mal raus 
                                    t_before = intervall1[0], t_after=intervall1[1], bin_size= bin_size1, smoothing= smoothing1, as_rate=as_rate1,
                                    include_raster=include_raster1,n_rasters= n_raster1, error_bars = error_bars1, ax=ax1, #ax2 is a weird thing, understand it 
                                    pethline_kwargs=pethline_kwargs1,
                                    errbar_kwargs=errbar_kwargs1,
                                    eventline_kwargs=eventline_kwargs1,
                                    raster_kwargs=raster_kwargs1)
            ax1.set(ylabel=ylab, xlabel=xlab)
            plt.tight_layout() # maybe lieber return 
        else:
            Exception("No spikes and cluster there to create a Graph")

    def getAcronymInfo(self):
        finDic = {}
        copAcro = self.cluster['acronym'].copy()
        copAcro = set(copAcro)
        for i in copAcro:
            tempArr = []
            for j in range(0,len(self.cluster['acronym'])):
                if self.cluster['acronym'][j] == i:
                    tempArr.append(j)
            finDic[i] =tempArr
        
        return finDic


    
    def getSpecificTrials(self):
        return[self.trials['goCueTrigger_times'], self.trials['feedback_times'], self.trials['stimOff_times'],
                self.trials['stimOn_times'], self.trials['firstMovement_times'], self.trials['rewardVolume']]
        
    def getStimOnOff(self):
        conStims = []
        for i in range(0,len(self.trials["stimOn_times"])):
            conStims.append(self.trials['stimOn_times'][i])
            conStims.append(self.trials['stimOff_times'][i])
        return conStims
    
    def getTrialStart(self):
        fbTime = self.trials["feedback_times"]
        fbType = self.trials["feedbackType"]
        start = []
        for i in range(0,len(fbTime)):
            if fbType[i]>0:
                start.append(fbTime[i]+1)
            else:
                start.append(fbTime[i]+2)
        return start

    def getTommyStuff(self):
        trials = self.getSpecificTrials()
        stimOnOff = self.getStimOnOff()
        trialStart = self.getTrialStart()
        return [trials[0], trials[1], trials[5], stimOnOff, trials[4], trialStart] 
    #return [goCueTRigger, feebbackTimes, rewardVolumme, stimOn/Off times, firstMovment, trialstarts]



#takes in parameter and returns object of session probably takes longer when also inputtinga brain region
def createSess(Roi = "", pid = "", POn = False, sessNmb= 0, EID = "",lab ="", nmb = "", proj ="",starTime = "", subj="", taskProt = "" ):   #session search parameter
    if (Roi == "")and(pid == ""):         #case for no roi
        ses1 = one.alyx.rest('sessions', 'list', id = EID, lab = lab, number = nmb, projects = proj, start_time = starTime, subject=subj, task_protocol=taskProt )
        if POn:
                print(f'Found {len(ses1)} Sessions')   #print if POn = True
        if (sessNmb > len(ses1)):
            raise Exception("The session number of your choosing is bigger than the found sessions") #error check for bad unmatiching parameter
        else:
                ses11 = ses1[sessNmb]       #continue if sessNmb is fine    
                EID = ses11["id"]           #this 3 lines take 1 session, takes the EID and tries to find the PID with it
                PID = one.eid2pid(EID)[0]
                
                if (len(PID) == 0):
                    print("No PIDs found for this session ID, return Session object without it and without clsuters/spikes")    #PID is empty, so there is no PID
                    sessionwithoutPID = Session(ses11,eid = EID)
                    return sessionwithoutPID
                
                else:
                    sess11 = one.alyx.rest('insertions', 'list', id = PID[0])[0]    #PID found create session with PID
                    sessionwithPID = Session(sess11,PrintOn=POn, eid=EID)
                    return sessionwithPID
    else:
        finalPIDs = []                  #case if roi is searched
        ses2 = one.alyx.rest('insertions', 'list',atlas_acronym = Roi, id=pid)
        for i in ses2:
            if (EID != "")and(i["session_info"]["id"] != EID): continue
            if (lab != "")and(i["session_info"]["lab"] != lab): continue
            if (nmb != "")and(i["session_info"]["number"]!=nmb):continue
            if (subj != "")and(i["session_info"]["subject"] != subj):continue
            if (starTime != "")and (i["session_info"]["start_time"]!=starTime):continue
            if(taskProt != "")and(i["session_info"]["task_protocol"]==taskProt):continue
            finalPIDs.append(i)
        if POn:
            print(f'Found {len(finalPIDs)} Sessions')   #print if POn = True
        if (sessNmb > len(finalPIDs)):
            raise Exception("The session number of your choosing is bigger than the found sessions") #error check for bad unmatiching parameter
        if(len(finalPIDs) == 0):
            raise Exception("there where no sessions to your likeliness found")
        ses2 = finalPIDs[sessNmb]
        ses2EID = ses2["session_info"]
        EID = ses2EID["id"]
        session2 =Session(ses2,PrintOn=POn, pid=ses2["id"], eid=EID)
        return session2


#takes in cluster and returns cluster cords its not part of the class so that it can be used even if not using the Library object class
def getClusterPos(clusters):          
    clusterCords = []
    for clus in range(0,len(clusters["channels"])):
        tup = (clusters.x[clus],clusters.y[clus], clusters.z[clus])
        clusterCords.append(tup)
    return clusterCords
        

def pidsofSessions(roi = ""):
    ses = one.alyx.rest('insertions', 'list', atlas_acronym = roi)
    pids = [i['id'] for i in ses]
    return pids


#Some test cases can be completly ignored

""" #case 1
test1 = createSess(pid="5e8ac11b-959a-49ab-a6a3-8a3397e1df0e", POn=True)
Acros = test1.getAcronymInfo()
print(Acros)  
------------------------------
#case2
roi = "SNr" # Region Of Interest (acronym according to Allen Atlas)
test2= createSess(pid = '6a7544a8-d3d4-44a1-a9c6-7f4d460feaac', POn=True)
print(test2.getMainInfo())
test2.getLineGraph(events1='stimOn_times', Roi = roi, xlab="Time from Stimulus Onset (s)", ylab="spikes/s", intervall1=[0.5,2], error_bars1="sem",
                 pidnmb=2)
plt.show() 
------------------------------
#case3 
roi2 = "CP"
test3 = createSess(Roi= roi2, POn=True)
test3.getLineGraph(events1='stimOn_times', Roi = roi2, xlab="Time from Stimulus Onset (s)", ylab="spikes/s", intervall1=[0.5,2], include_raster1=True, error_bars1="sem",
                 pidnmb=2)
plt.show()"""

from vedo import Text2D

class Info(ActorTemplate):
    sessionInfo = []
    def __init__(self):
        super().__init__()
        self.createText()
        self.createRightText()
        self.createCurrentInfo()

    def createRightText(self):
        self.currentActionText=Text2D(" ",pos=(0.7,0.97),c=(1,1,1))
        self.trialCounterText=Text2D(" ",pos=(0.7,1),c=(1,1,1))
        self.rewardTypeText=Text2D(" ",pos=(0.7,0.94),c=(1,1,1))
        self.stimText = Text2D(" ",pos=(0.7,0.91),c=(1,1,1))
        self.skipCounterText= Text2D(" ",pos=(0.35,0.1),c=(1,1,1),s=2.5)

        super().addActor(self.currentActionText)
        super().addActor(self.trialCounterText)
        super().addActor(self.rewardTypeText)
        super().addActor(self.stimText)
        super().addActor(self.skipCounterText)
    def createText(self):
        for l in range(20):
            text_t = Text2D(" ")
            text_t.pos((0.005,l*0.03-0.26))
            text_t.properties.SetColor(1,1,1)
            super().addActor(text_t)
    def setSessionInfo(self, sessionInfo=["unknown-EID", "unknown-PID", "unknow-animal", "unknown-lab"]):
        self.sessionInfo = sessionInfo
        self.createSessionInfo()
    def createCurrentInfo(self):
        self.timerText = Text2D("Timer: 0", pos=(0.005, 0.51), c=(1,1,1))
        self.trialText = Text2D("Trial: 0", pos=(0.005, 0.48), c=(1,1,1))
        self.stimText = Text2D("Stim: Off", pos=(0.095, 0.48), c=(1,1,1))
        super().addActor(self.timerText)
        super().addActor(self.trialText)
        super().addActor(self.stimText)
    def createSessionInfo(self):
        self.headingSessionID = Text2D("Session-ID:", pos=(0.005, 0.96), c=(1,1,1))
        self.sessionID1 = Text2D(self.sessionInfo[0][:19], pos=(0.005, 0.93), c=(0.7,0.7,0.7))
        self.sessionID2 = Text2D(self.sessionInfo[0][19:], pos=(0.005, 0.90), c=(0.7,0.7,0.7))
        self.headingProbeID = Text2D("Probe-ID:", pos=(0.005, 0.87), c=(1,1,1))
        self.probeID1 = Text2D(self.sessionInfo[1][:19], pos=(0.005, 0.84), c=(0.7,0.7,0.7))
        self.probeID2 = Text2D(self.sessionInfo[1][19:], pos=(0.005, 0.81), c=(0.7,0.7,0.7))
        self.headingAnimal = Text2D("Animal:", pos=(0.005, 0.78), c=(1,1,1))
        self.animal = Text2D(self.sessionInfo[2], pos=(0.005, 0.75), c=(0.7,0.7,0.7))
        self.headingLab = Text2D("Lab:", pos=(0.005, 0.72), c=(1,1,1))
        self.lab = Text2D(self.sessionInfo[3], pos=(0.005, 0.69), c=(0.7,0.7,0.7))
        super().addActor(self.headingSessionID)
        super().addActor(self.sessionID1)
        super().addActor(self.sessionID2)
        super().addActor(self.headingProbeID)
        super().addActor(self.probeID1)
        super().addActor(self.probeID2)
        super().addActor(self.headingAnimal)
        super().addActor(self.animal)
        super().addActor(self.headingLab)
        super().addActor(self.lab)
        pass


        
''' 
    def updateTrialInfo(self,timer):
        self.timer=timer
        if(self.prevFeedIndex<len(self.feedbackTime)):
            if (self.timer-0.4>=self.feedbackTime[self.prevFeedIndex]):
                self.prevAction="Feedback Time"
                self.prevFeedIndex+=1
        if(self.prevFeedIndex<len(self.goCue)):
            if (self.timer-0.4>=self.goCue[self.prevGoCueIndex]):

                self.prevAction="Go Cue"
                self.prevGoCueIndex+=1

        if(self.feedbackTimeIndex<len(self.feedbackTime)):
            if (self.timer+0.1>=self.feedbackTime[self.feedbackTimeIndex]):
                    self.currentAction="Feedback Time"
                    self.feedbackTimeIndex+=1
        if(self.goCueIndex<len(self.goCue)):
            if (timer+0.1>=self.goCue[self.goCueIndex]):
                self.currentAction="Go Cue"
                self.goCueIndex+=1
                if self.feedbackType[self.trialCounter]>0:
                    self.rewardType="Reward"
                    self.trialCounter+=1
                else:
                    self.rewardType="Error"
                    self.trialCounter+=1
        if(self.stimCounter<len(self.stim)):
            if(timer +0.1 >=self.stim[self.stimCounter]):
                if(self.stimCounter%2==0):
                    self.stimAppear="Stim On"
                else:
                    self.stimAppear="Stim Off"
                self.stimCounter+=1

        self.currentActionText.text("Order: "+self.currentAction)
        self.trialCounterText.text("Number of Trials: "+str(self.trialCounter))
        self.rewardTypeText.text("Reward Type: "+self.rewardType)
        self.stimText.text(self.stimAppear)

        self.skipCounterText.text(str(self.skipCounter))
'''


from vedo import Button, Text2D
import math
import colorsys

class Playback(ActorTemplate):

    skipCounter=0
    prevFeedIndex=0
    prevGoCueIndex=0
    prevAction=""
    trialCounter=0
    currentAction=""
    rewardType=""
    goCueIndex=0
    feedbackTimeIndex=0
    stimCounter=0
    stimAppear="Stim Off"
    
    skipped=False

    timer=0
    i=0
    start=0
    
    currentActionText=None
    trialCounterText=None
    rewardTypeText=None
    stimText =None
    skipCounterText=None
    timer=0
    spikeIndex = 0
    newTimes=0
    speed_minus = 2000
    contrast = 1
    timestep = 0.1
    

    def __init__(self, button_play_pause, speedslider, timerslider, skip):
        self.button_play_pause = button_play_pause
        self.speedslider = speedslider
        self.timerslider = timerslider
        self.skip = skip

        super().__init__()
        super().addActor(CustomSlider(self.timerslider, xmin=0, xmax=3000, value=0, pos=[(0.3,0.09),(0.6, 0.09)], show_value=True, c=(1,1,1)))
        super().addActor(CustomSlider(self.skip, xmin=0, xmax=1, value=0, pos=[(0.3,0.03),(0.6, 0.03)], show_value=True, c=(1,1,1)))
        self.button = CustomButton(self.button_play_pause, states=[" ▶ "," ⏸ "], size=50, c=("white","white"), bc=("grey1","grey1"),pos=(0.21,0.09), font="Kanopus")
        super().addActor(self.button)
        super().addActor(CustomSlider(self.speedslider, xmin=0, xmax=2999, value=2000, pos=[(0.8,0.09),(0.98, 0.09)], title="", show_value=False, c=(1,1,1)))
        super().addActor(CustomSlider(self.contrastslider, xmin=0.01, xmax=5, value=1, pos=[(0.8,0.03),(0.98, 0.03)], title="", show_value=False, c=(0,0,0)))
        super().addActor(Text2D("Skip to \n Time", pos=(0.25, 0.12), c=(1,1,1)))
        super().addActor(Text2D("Skip to \n Trial", pos=(0.25, 0.06), c=(1,1,1)))
        super().addActor(Text2D("Speed", pos=(0.73,0.1), c=(1,1,1)))
        super().addActor(Text2D("Contrast", pos=(0.73,0.04), c=(1,1,1)))
        super().addActor(CustomButton(self.timestepButton, states=["0.1","0.01"], size=40, pos=(0.67, 0.08)))
        super().addActor(Text2D("Timestep", pos=(0.645, 0.11), c=(1,1,1,)))


    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    def contrastslider(self, widget, event):
        self.contrast = widget.value
    def timestepButton(self, btn, event):
        if self.timestep == 0.1: self.timestep = 0.01
        else: self.timestep = 0.1
        btn.switch()

from vedo import Plotter
import colorsys
import vtk
import numpy as np
class Renderer:

    timer_id = -1
    goCueIndex=0
    trialCounter=0
    feedbackIndex=0
    stimAppear="Off"
    stimCounter=0
    prevFeedIn=0
    prevGoCueIn=0
    prevTrialIn=0
    stillAppend=False
    prevWheelMoveCounter=0

    def __init__(self, session):
        self.session = session
        self.plotter = Plotter()
        self.brain = BrainNew(session)#session.getClusterAndSpikesOfSess()
        self.timeline = Timeline(0, 0.35)
        self.background = Background()
        self.playback = Playback(self.button_play_pause, self.speedslider, self.timerslider, self.skip)
        self.end = self.session.spikes.times[-1] #temp
        rep = self.playback.actors[0].GetSliderRepresentation()
        rep.SetMaximumValue(math.floor(self.end)) 
        self.playback.actors[0].SetRepresentation(rep)
        rep2 = self.playback.actors[1].GetSliderRepresentation()
        rep2.SetMaximumValue(len(self.brain.goCue)-1)
        self.playback.actors[1].SetRepresentation(rep2)



        self.info = Info()
        self.info.setSessionInfo(session.getMainInfo())
        self.background.addToPlotter(self.plotter)
        self.info.addToPlotter(self.plotter)  
        self.timeline.addToPlotter(self.plotter)
        self.brain.addToPlotter(self.plotter)
        
        self.plotter.roll(180)
        self.plotter.background((30,30,30))
        
        
        #wip


        self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)
        self.playback.addToPlotter(self.plotter)
    def startRender(self):
        self.plotter.show(__doc__)

    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    
    def animation_tick(self, event):
        if(self.playback.timer < self.end):
            self.updateTrialInfo()
            self.timeline.updateWholeDataSet(self.updateTimelineData())
            self.timeline.updateHistogram(self.plotter)
            currentSpikes = []
            elemStillIn = True         
            while(elemStillIn):
                if(self.playback.spikeIndex >= len(self.brain.spikes.times)):
                    break
                if(self.brain.spikes.times[self.playback.spikeIndex] > self.playback.timer and self.brain.spikes.times[self.playback.spikeIndex] < self.playback.timer + self.playback.timestep):
                    currentSpikes.append(self.playback.spikeIndex)   
                else:
                    elemStillIn = False
                self.playback.spikeIndex += 1
              
            self.info.actors[19].text("Total Spikes: " + str(len(currentSpikes)))
            for k,regionModel in enumerate(self.brain.regionModels):
                spikesInRegion = 0
                for j in currentSpikes:
                    if(self.brain.clusters.acronym[self.brain.spikes.clusters[j]] == regionModel[0]):
                        spikesInRegion += 1

                self.brain.actors[k+1].actor.GetProperty().SetOpacity(spikesInRegion * 0.01 * self.playback.contrast)
                

                color = self.hsv2rgb(k / len(self.brain.regionModels), 1,1)
                color255 = (color[0]/255, color[1]/255, color[2]/255)
            
            
                self.info.actors[18-k].text("Spikes in " + regionModel[0] + ": " + str(spikesInRegion))
                self.info.actors[18-k].properties.SetColor(color255)
                self.brain.actors[k+1].actor.GetProperty().SetColor(color255)

            #self.actors.updateTrialInfo(self.timer)


            self.info.timerText.text("Time: " + str(round(self.playback.timer,2)))
            self.info.trialText.text("Trial: " + str(self.goCueIndex))
            self.info.stimText.text("Stim: " + self.stimAppear)
            self.playback.timer = self.playback.timer + self.playback.timestep
        self.plotter.render()

    def button_play_pause(self, btn, obj):
        self.plotter.timer_callback("destroy", self.timer_id)
        if "▶" in btn.status():
            self.timer_id = self.plotter.timer_callback("create", dt=math.ceil(3000-self.playback.speed_minus))
        btn.switch()
    def speedslider(self, widget, event):
        self.playback.speed_minus = widget.value
        self.updateSpikeIndex()

        

        
        #TODO: needs fixing
        try:
            self.plotter.timer_callback("destroy", self.timer_id)
            self.timer_id = self.plotter.timer_callback("create", dt=math.ceil(3000-self.playback.speed_minus))
        except:
            pass
    
    def timerslider(self, widget, event):
        self.synchIndex(self.playback.timer,math.floor(widget.value*100) / 100)
        self.playback.timer = math.floor(widget.value*100) / 100
        self.updateSpikeIndex()

        

        #if "⏸" in self.playback.button.status():
    def updateSpikeIndex(self):
        newTimes=0
        while(self.brain.spikes.times[newTimes]<=self.playback.timer):#need to add spikes times
            newTimes+=1
            if(newTimes>=len(self.brain.spikes.times)):
                break
            # need to add spike index
        self.playback.spikeIndex = newTimes

    def updateTimelineData(self):
        timeline=[]
        timer=self.playback.timer-5
        timelineGoCue=self.prevGoCueIn
        timelineFeed=self.prevFeedIn
        timelineTrial= self.prevTrialIn
        timelineWheel=self.prevWheelMoveCounter
        append=False
        for time_e in range(100):
            if (timelineTrial<len(self.brain.start)):
                if timer>=self.brain.feedbackTime[timelineTrial] and timer<=self.brain.start[timelineTrial]  :
                    if self.brain.feedbackType[timelineTrial]>0:
                        timeline.append("Feedback Time, Reward")
                    else:
                        timeline.append("Feedback Time, Error")
                    append=True
            if (timelineFeed<len(self.brain.feedbackTime)):
                if math.floor((timer+0.1)*100)/100>= self.brain.feedbackTime[timelineFeed]and timer<=self.brain.feedbackTime[timelineFeed]:
                    if self.brain.feedbackType[timelineFeed]>0:
                        timeline.append("Feedback Time, Reward")
                    else:
                        timeline.append("Feedback Time, Error")
                    append=True
                    timelineFeed+=1
            if (timelineGoCue<len(self.brain.goCue)):
                if math.floor((timer+0.1)*100)/100>=self.brain.goCue[timelineGoCue] and timer<=self.brain.goCue[timelineGoCue]:
                    timeline.append("Go Cue")
                    append=True
                    timelineGoCue+=1
            if(timelineWheel<len(self.brain.firstWheelMove)):
                if math.floor((timer+0.1)*100)/100>=self.brain.firstWheelMove[timelineWheel] and timer <=self.brain.firstWheelMove[timelineWheel]:
                    timeline.append("First Wheel Movement")
                    append=True
                    timelineWheel+=1
            if not append:
                timeline.append("")
            append=False
            if(timelineTrial<len(self.brain.start)):
                if math.floor((timer+0.1)*100)/100>=self.brain.start[timelineTrial] and timer<=self.brain.start[timelineTrial]:
                    timelineTrial+=1
            timer=math.floor((timer+0.1)*100)/100
        return timeline

    
    def updateTrialInfo(self):
        if self.goCueIndex< len(self.brain.goCue):
            if self.brain.goCue[self.goCueIndex]<=self.playback.timer:
                self.goCueIndex+=1
        if self.feedbackIndex<len(self.brain.feedbackTime):
            if self.brain.feedbackTime[self.feedbackIndex]<=self.playback.timer:
                self.feedbackIndex+=1
        if self.trialCounter<len(self.brain.start):
            if self.brain.start[self.trialCounter]<=self.playback.timer:
                self.trialCounter+=1
        if self.stimCounter< len(self.brain.stim):
            if self.brain.stim[self.stimCounter]<=self.playback.timer:
                self.stimCounter+=1
        if self.prevGoCueIn<len(self.brain.goCue):
            if self.brain.goCue[self.prevGoCueIn]<=self.playback.timer-5:
                self.prevGoCueIn+=1
        if self.prevFeedIn< len(self.brain.feedbackTime):
            if self.brain.feedbackTime[self.prevFeedIn]<=self.playback.timer-5:
                self.prevFeedIn+=1
        if self.prevTrialIn<len(self.brain.start):
            if self.brain.start[self.prevTrialIn]<=self.playback.timer-5:
                self.prevTrialIn+=1
        if self.stimCounter<len(self.brain.stim):
            if self.brain.stim[self.stimCounter]<=self.playback.timer:
                self.stimCounter+=1
        if self.stimCounter%2==0:
            self.stimAppear="Off"
        else:
            self.stimAppear="On"
        if self.prevWheelMoveCounter<len(self.brain.firstWheelMove):
            if self.brain.firstWheelMove[self.prevWheelMoveCounter]<=self.playback.timer-5 or np.isnan(self.brain.firstWheelMove[self.prevWheelMoveCounter]):
                self.prevWheelMoveCounter+=1


    
    def getSkippedTimer(self,skip):
        if skip<=0:
            return 0
        if skip>=len(self.brain.goCue):
            timer= self.brain.feedbackTime[len(self.brain.feedbackTime)-2]# one time -1 to get be inside the list boundary and the other -1 to get the time of prev feedbackTime
            if self.brain.feedbackType[len(self.brain.feedbackType)-2]>0:
                timer+=1 #new trial time after reward
                timer= math.floor(timer*10)/10
            else:
                timer= math.floor((timer/10)+1)*10
                timer+=2 # new trial time after Fail
            return timer
        timer=self.brain.feedbackTime[skip-1]
        if self.brain.feedbackType[skip-1]>0:
            timer+=1
            timer= math.floor(timer*10)/10
        else:
            timer+=2
            timer= math.floor(timer*10)/10
        return timer
    
    def skip(self, widget, event):
        self.stillAppend=False
        trialNum = math.floor(widget.value)
        if trialNum==0:
            self.playback.timer=0
            self.goCueIndex=0
            self.feedbackIndex=0
            self.trialCounter=0
            self.prevFeedIn=0
            self.prevGoCueIn=0
            self.prevTrialIn=0
            self.prevWheelMoveCounter=0
        else:
            self.goCueIndex=trialNum-1
            self.feedbackIndex=self.goCueIndex
            self.trialCounter=trialNum
            self.prevFeedIn=self.goCueIndex
            self.prevGoCueIn=self.goCueIndex
            self.playback.timer=self.getSkippedTimer(trialNum)
            self.prevWheelMoveCounter=self.goCueIndex
            self.prevTrialIn=self.goCueIndex
        
        newStimCounter=0
        while(self.brain.stim[newStimCounter]<=self.playback.timer):
            newStimCounter+=1
            if(self.stimCounter>=len(self.brain.stim)):
                break
        self.stimCounter=newStimCounter
        if newStimCounter%2==0:
            self.stimAppear="Off"
        else:
            self.stimAppear="On"
        self.stimCounter=newStimCounter

        self.updateSpikeIndex()

    def synchIndex(self,oldTime,newTime):
        print(str(self.prevWheelMoveCounter)+"hihi")
        if newTime<oldTime:
            goCueIndex=0
            while self.brain.goCue[goCueIndex]<=newTime:
                goCueIndex+=1
                if(goCueIndex>=len(self.brain.goCue)):break
            self.goCueIndex=goCueIndex

            prevGoCue=0
            while self.brain.goCue[prevGoCue]<=newTime-5:
                prevGoCue+=1
                if(goCueIndex>=len(self.brain.goCue)):break
            self.prevGoCueIn=prevGoCue

            feedbackIndex=0
            while self.brain.feedbackTime[feedbackIndex]<=newTime:
                feedbackIndex+=1
                if(feedbackIndex>=len(self.brain.feedbackTime)):break
            self.feedbackIndex=feedbackIndex

            prevFeed=0
            while self.brain.feedbackTime[prevFeed]<=newTime-5:
                prevFeed+=1
                if(prevFeed>=len(self.brain.feedbackTime)):break
            self.prevFeedIn=prevFeed

            trialCounter=0
            while(self.brain.start[trialCounter]<=newTime):
                trialCounter+=1
                if(trialCounter>= len(self.brain.start)):break
            self.trialCounter=trialCounter

            prevTrialCounter=0
            while self.brain.start[prevTrialCounter]<=newTime-5:
                prevTrialCounter+=1
                if(prevTrialCounter>=len(self.brain.start)):break
            self.prevTrialIn=prevTrialCounter

            prevWheelMove=0
            while self.brain.firstWheelMove[prevWheelMove]<=newTime-5 or np.isnan(self.brain.firstWheelMove[prevWheelMove]):
                prevWheelMove+=1
                if(prevWheelMove>=len(self.brain.firstWheelMove)):break
            self.prevWheelMoveCounter=prevWheelMove

            stimCounter=0
            while self.brain.stim[stimCounter]<= newTime:
                stimCounter+=1
                if(stimCounter>=len(self.brain.stim)):break
        else:
            goCueIndex=self.goCueIndex
            if (goCueIndex<len(self.brain.goCue)):
                while(self.brain.goCue[goCueIndex]<=newTime):
                    goCueIndex+=1
                    if(goCueIndex>=len(self.brain.goCue)):break
            self.goCueIndex=goCueIndex

            prevGoCue=self.prevGoCueIn
            if (prevGoCue<len(self.brain.goCue)):
                while(self.brain.goCue[prevGoCue]<=newTime-5):
                    prevGoCue+=1
                    if(prevGoCue>=len(self.brain.goCue)):break
            self.prevGoCueIn=prevGoCue

            feedbackIndex=self.feedbackIndex
            if(feedbackIndex<len(self.brain.feedbackTime)):
                while(self.brain.feedbackTime[feedbackIndex]<=newTime):
                    feedbackIndex+=1
                    if(feedbackIndex>=len(self.brain.feedbackTime)):break
            self.feedbackIndex=feedbackIndex

            prevFeed=self.prevFeedIn
            if(prevFeed<len(self.brain.feedbackTime)):
                while(self.brain.feedbackTime[prevFeed]<=newTime-5):
                    prevFeed+=1
                    if(prevFeed>=len(self.brain.feedbackTime)):break
            self.prevFeedIn=prevFeed

            trialCounter=self.trialCounter
            if(trialCounter<len(self.brain.start)):
                while(self.brain.start[trialCounter]<=newTime):
                    trialCounter+=1
                    if(trialCounter>=len(self.brain.start)):break
            self.trialCounter=trialCounter

            prevTrialCounter=self.prevTrialIn
            if(prevTrialCounter<len(self.brain.start)):
                while(self.brain.start[prevTrialCounter]<=newTime-5):
                    prevTrialCounter+=1
                    if(prevTrialCounter>=len(self.brain.start)):break
            self.prevTrialIn=prevTrialCounter

            prevWheelMove=self.prevWheelMoveCounter
            if(prevWheelMove<len(self.brain.firstWheelMove)):
                while(self.brain.firstWheelMove[prevWheelMove]<=newTime-5)or np.isnan(self.brain.firstWheelMove[prevWheelMove]):
                    prevWheelMove+=1
                    if(prevWheelMove>=len(self.brain.firstWheelMove)):break
            self.prevWheelMoveCounter=prevWheelMove

            stimCounter=self.stimCounter
            if(stimCounter<len(self.brain.stim)):
                while(self.brain.stim[stimCounter]<=newTime):
                    stimCounter+=1
                    if(stimCounter>=len(self.brain.stim)):break
            self.stimCounter=stimCounter

        print(str(self.prevWheelMoveCounter)+"jo")

from vedo import Text2D, Image
import matplotlib.pyplot as plt
import vtk
import numpy as np
import math
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
        #actor2d.SetDisplayPosition(0,400)
        self.hist = actor2d      
        self.hist.SetVisibility(0)
        super().addActor(self.hist)
    def updateHistogram(self, plotter):
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
