import time
import numpy as np
from vedo import Plotter
from vedo.pyplot import plot
from vedo import Text2D, Latex, Picture, Sphere, Image
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
import matplotlib.pyplot as plt
import colorsys
import vtk
one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
ba = AllenAtlas()


def get_n_random_points_in_region(region, N):
    """
    Gets N random points inside (or on the surface) of a mesh
    """
    region_bounds = region.mesh.bounds()
    X = np.random.randint(region_bounds[0], region_bounds[1], size=10000)
    Y = np.random.randint(region_bounds[2], region_bounds[3], size=10000)
    Z = np.random.randint(region_bounds[4], region_bounds[5], size=10000)
    #print("Region Bound X:" + str(region_bounds[0]) + " " + str(region_bounds[1]))
    X = [math.floor(clusters.x[2] * 2500000), math.floor(clusters.x[3] * 2500000)]
    Y = [math.floor(clusters.y[2] * 2500000), math.floor(clusters.y[3] * 2500000)]
    Z = [math.floor(clusters.z[2] * 2500000), math.floor(clusters.z[3] * 2500000)]
    #print(str(X) + " " + str(Y) + " " + str(Z))
    pts = [[x, y, z] for x, y, z in zip(X, Y, Z)]

    ipts = region.mesh.inside_points(pts).coordinates
    print(np.vstack((X,Y,Z)))
    return np.vstack((X,Y,Z))



def loadData():

    roi = "SI" # Region Of Interest (acronym according to Allen Atlas)
    ses = one.alyx.rest('insertions', 'list', atlas_acronym = roi) #loading recordings
    #print(f'Found {len(ses)} recordings')
    #isolating first session and probe ID
    EID = ses[0]['session']
    PID = ses[0]['id']
    sl = SpikeSortingLoader(pid=PID, one=one, atlas=ba) # create instance of the SpikeSortingLoader
    spikes, clusters, channels = sl.load_spike_sorting() # load in spike sorted data
    clusters = sl.merge_clusters(spikes, clusters, channels) # merge cluster metrics
    return spikes, clusters, channels


def loadTrials():
    roi="SI"
    ses = one.alyx.rest('insertions', 'list', atlas_acronym = roi)
    EID= ses[0]['session']
    trials = one.load_object(EID, 'trials')
    goCue= trials['goCueTrigger_times']
    feedbackTime=trials['feedback_times']
    feedbackType=trials['rewardVolume'] #Volume =0 error  >0 reward
    stimOff=trials['stimOff_times']
    stimOn=trials['stimOn_times']
    stim=concat(stimOn,stimOff)
    return goCue, feedbackTime, feedbackType, stim

def concat(on,off):
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




def button_play_pause(obj, btn):
    global timer_id
    plotter.timer_callback("destroy", timer_id)
    if "Play" in button.status():
        # instruct to call handle_timer() every 10 msec:
        timer_id = plotter.timer_callback("create", dt=10)
    button.switch() 

def skip(obj,btn):
    global timer_id
    global timer
    global skipCounter
    global goCueIndex
    global goCue
    global trialCounter
    global feedbackTimeIndex

    global prevAction
    global prevGoCueIndex
    global prevFeedIndex
    #timer=math.floor(goCue[goCueIndex+skipCounter-1]*10)/10
    if (goCueIndex+skipCounter<len(goCue)):
        if(goCueIndex+skipCounter>=0):
            goCueIndex+=skipCounter
            goCueIndex-=1
            trialCounter+=skipCounter
            trialCounter-=1
            if(feedbackTimeIndex!=0 and goCueIndex!=1):
                feedbackTimeIndex=goCueIndex-1
            if(goCueIndex!=0):
                print("yo")
                prevGoCueIndex=goCueIndex-1
                prevFeedIndex=goCueIndex-1
            timer=math.floor(goCue[goCueIndex]*10)/10
        else:
            goCueIndex=0
            trialCounter=0
            feedbackTimeIndex=0
            timer=0
    else:
        goCueIndex=len(goCue)
        trialCounter=len(goCue)
        feedbackTimeIndex=goCueIndex-1
        timer=math.floor(goCue[goCueIndex]*10)/10

   
    global stim
    global stimCounter
    newStimCounter=0
    while(stim[newStimCounter]<= timer):
        newStimCounter+=1
        if(stimCounter>=len(stim)):
            break
    if newStimCounter!=0:
        newStimCounter-=1
    stimCounter=newStimCounter
    global i
    newTimes=0
    global spikes
    while(spikes.times[newTimes]<=timer):
        newTimes+=1
        if(newTimes>=len(spikes.times)):
            break
    i=newTimes
    
    global currentAction
    global rewardType
    global feedbackType
    global stimAppear
    if newStimCounter!=stimCounter:
        if(newStimCounter%2==0):
            stimAppear="Stim On"
        else:
            stimAppear="Stim Off"
    currentAction="Go Cue"
    if feedbackType[trialCounter]>0:
        rewardType="Reward"
    else:
        rewardType="Error"

def updateTrialInfo():
    global feedbackTime
    global feedbackTimeIndex
    global currentAction
    global goCue
    global goCueIndex
    global currentAction
    global rewardType
    global trialCounter

    global stimCounter
    global stimAppear

    global prevAction
    global prevGoCueIndex
    global prevFeedIndex

    if(prevFeedIndex<=len(feedbackTime)):
        if (timer-0.4>=feedbackTime[prevFeedIndex]):
            prevAction="Feedback Time"
            prevFeedIndex+=1
    if(prevFeedIndex<=len(goCue)):
        if (timer-0.4>=goCue[prevGoCueIndex]):
            prevAction="Go Cue"
            prevGoCueIndex+=1

    if(feedbackTimeIndex<=len(feedbackTime)):
        if (timer+0.1>=feedbackTime[feedbackTimeIndex]):
                currentAction="Feedback Time"
                print(feedbackTimeIndex)
                feedbackTimeIndex+=1
    if(goCueIndex<=len(goCue)):
        if (timer+0.1>=goCue[goCueIndex]):
            currentAction="Go Cue"
            goCueIndex+=1
            if feedbackType[trialCounter]>0:
                rewardType="Reward"
                trialCounter+=1
            else:
                rewardType="Error"
                trialCounter+=1
    if(stimCounter<=len(stim)):
        if(timer +0.1 >=stim[stimCounter]):
            if(stimCounter%2==0):
                stimAppear="Stim On"
            else:
                stimAppear="Stim Off"
            stimCounter+=1

    global currentActionText
    global trialCounterText
    global rewardTypeText
    global stimText
    currentActionText.text("Order: "+currentAction)
    trialCounterText.text("Number of Trials: "+str(trialCounter))
    rewardTypeText.text("Reward Type: "+rewardType)
    stimText.text(stimAppear)


def generateTimeline():
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
    actor2d.SetPosition(0.2, 0.1)
    actor2d.GetProperty().SetDisplayLocationToBackground()
    actor2d.SetDisplayPosition(0, 400)
    return actor2d, []
def updateTimeline(actor2d, dataSet):
    global timer
    fig= plt.figure()
    ax = fig.add_subplot(111)
    fig.set_facecolor("black")
    ax.set_facecolor("black")

    number = random.randint(1,100)
    dataSet = [x + 1 for x in dataSet if x <= 100]

    print(dataSet)
    global prevAction
    if(prevAction == "Go Cue"):
        dataSet.append(1)
    N, bins, patches = plt.hist(dataSet, bins=100, range=(1,100))
    #patches[number-1].set_facecolor((random.random(), random.random(), random.random()))
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
    actor2d.SetMapper(mapper)
    actor2d.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
    actor2d.SetPosition(0.2, 0.1)
    actor2d.GetProperty().SetDisplayLocationToBackground()
    actor2d.SetDisplayPosition(0, 400)
    return actor2d, dataSet



scene = Scene(atlas_name="allen_mouse_25um", title="")
spikes, clusters, channels = loadData()

regionModels = []
for acro in list(set(clusters.acronym)):
    regionModels.append([acro, scene.add_brain_region(acro, alpha=0.5)])


start = 0
end = spikes.times[-1]
timer = 0
i = 0

prevFeedIndex=0
prevGoCueIndex=0
prevAction=""
goCue , feedbackTime, feedbackType, stim=loadTrials()
trialCounter=0
currentAction=""
rewardType=""
goCueIndex=0
feedbackTimeIndex=0
stimCounter=0
stimAppear="Stim Off"
skipCounter=1


def slowdecSkip(obj,btn):
    global skipCounter
    skipCounter-=1
def fastdecSkip(obj,btn):
    global skipCounter
    skipCounter-=10
def fastinSkip(obj,btn):
    global skipCounter
    skipCounter+=10
def slowinSkip(obj,btn):
    global skipCounter
    skipCounter+=1

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
 
def animation_tick(event): 
    global regionModels
    global timer
    global end
    global i
    global actor2d
    global dataSet
    actor2d, dataSet = updateTimeline(actor2d, dataSet)


    plotter.get_actors()[1].GetProperty().SetColor(1,1,1)
    if(timer < end):
        currentSpikes = []
        elemStillIn = True
        while(elemStillIn):
            if(i >= len(spikes.times)): break
            if(spikes.times[i] > timer and spikes.times[i] < timer + 0.1):
                currentSpikes.append(i)
            
            else:
                elemStillIn = False
            i += 1
             

            
        text_array[19].text("Total Spikes: " + str(len(currentSpikes)))
        #outputString = "Total Spikes: " + str(len(currentSpikes)) + "\n"
        for k in range(len(regionModels)):
            spikesInRegion = 0
            for j in currentSpikes:
                if(clusters.acronym[spikes.clusters[j]] == regionModels[k][0]):
                    spikesInRegion += 1
            #outputString += "Spikes in " + regionModels[k][0] + ": " + str(spikesInRegion) + "\n"
            plotter.get_actors()[k+7].GetProperty().SetOpacity(spikesInRegion * 0.02)
            color = hsv2rgb(k / len(regionModels), 1,1)
            color255 = (color[0]/255, color[1]/255, color[2]/255)
            
            
            text_array[18-k].text("Spikes in " + regionModels[k][0] + ": " + str(spikesInRegion))
            text_array[18-k].properties.SetColor(color255)
            plotter.get_actors()[k+7].GetProperty().SetColor(color)
            plotter.get_actors()[k+7].GetProperty().SetRepresentation(1)
            plotter.get_actors()[k]
            
            #regionModels[i][1].SetAlpha(spikesInRegion * 0.01)
        #outputString += "Time: " + str(timer)
        updateTrialInfo()
        global skipCounterText
        global skipCounter
        skipCounterText.text(str(skipCounter))

        text_array[18-len(regionModels)].text("Time: " + str(timer))
        #text.text(outputString)
        timer = math.floor((timer*10)+1)/10

    global time_e  
    #boop = plotter.get_actors()[2]
    #boop.SetVisibility(not boop.GetVisibility())
    time_e += 0.1

    plotter.render()


#Notes
#shorten time frame
#move time frame slowly
#try to divide brain region into smaller parts as "neurons"
#indicate current event (stimOn, response etc)
#fix linux problems (maybe), color problems, divByZero prob

print(stim)
time_e = 0
timer_id = -1
#t0 = time.time()

plotter= Plotter()

currentActionText=Text2D(" ",pos=(0.7,0.97),c=(1,1,1))
trialCounterText=Text2D(" ",pos=(0.7,1),c=(1,1,1))
rewardTypeText=Text2D(" ",pos=(0.7,0.94),c=(1,1,1))
stimText = Text2D(" ",pos=(0.7,0.91),c=(1,1,1))
skipCounterText= Text2D(str(skipCounter),pos=(0.2,0.1),c=(1,1,1),s=2.5)
plotter.add(currentActionText)
plotter.add(trialCounterText)
plotter.add(rewardTypeText)
plotter.add(stimText)
plotter.add(skipCounterText)


button = plotter.add_button(button_play_pause, states=[" Play ","Pause"], size=40)
evntid = plotter.add_callback("timer", animation_tick, enable_picking=False)

skipBtn=plotter.add_button(skip,states=["Skip"],size=40,pos=(0.5,0.1))

decSBtn= plotter.add_button(slowdecSkip,states=["-"],size=20,pos=(0.15,0.09))
decFBtn=plotter.add_button(fastdecSkip,states=["--"],size=20,pos=(0.09,0.09))
inSBtn= plotter.add_button(slowinSkip,states=["+"],size=20,pos=(0.27,0.09))
inFBtn=plotter.add_button(fastinSkip,states=["++"],size=20,pos=(0.33,0.09))



plotter.roll(180)
plotter.background("grey0")
text_array = []
for l in range(20):
    text_t = Text2D(" ")
    text_t.pos((0.005,l*0.03+0.4295))
    text_array.append(text_t)
    plotter.add(text_t)

#---------------------------

textCurrentPointer = Text2D("↓ - Go Cues")
textCurrentPointer.pos((0.105, 0.71))
plotter.add(textCurrentPointer)
actor2d, dataSet = generateTimeline()

plotter.show( __doc__, scene.get_actors(), actor2d)


