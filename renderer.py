from brain_new import *
from timeline import *
from background import Background
from playback import Playback
from info import Info
from vedo import Plotter
import colorsys
import vtk
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
    rewardType=""

    def __init__(self, session):
        self.session = session
        self.plotter = Plotter()
        self.brain = BrainNew(session.getClusterAndSpikesOfSess())
        self.timeline = Timeline(0, 0.35)
        self.background = Background()
        self.playback = Playback(self.button_play_pause, self.speedslider, self.timerslider, self.skip)
        self.end = self.brain.spikes.times[-1] #temp
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
            if timer>=self.brain.feedbackTime[timelineTrial] and timer<=self.brain.start[timelineTrial]  :
                timeline.append(self.rewardType)
                append=True
            if math.floor((timer+0.1)*100)/100>= self.brain.feedbackTime[timelineFeed]and timer<=self.brain.feedbackTime[timelineFeed]:
                if self.brain.feedbackType[timelineFeed]>0:
                    timeline.append("Feedback Time, Reward")
                    self.rewardType="Feedback Time, Reward"
                else:
                    timeline.append("Feedback Time, Error")
                    self.rewardType="Feedback Time, Error"
                append=True
                timelineFeed+=1
            if math.floor((timer+0.1)*100)/100>=self.brain.goCue[timelineGoCue] and timer<=self.brain.goCue[timelineGoCue]:
                timeline.append("Go Cue")
                append=True
                timelineGoCue+=1
            if math.floor((timer+0.1)*100)/100>=self.brain.firstWheelMove[timelineWheel] and timer <=self.brain.firstWheelMove[timelineWheel]:
                timeline.append("First Wheel Movement")
                append=True
                timelineWheel+=1
            if not append:
                timeline.append("")
            append=False
            if math.floor((timer+0.1)*100)/100>=self.brain.start[timelineTrial] and timer<=self.brain.start[timelineTrial]:
                timelineTrial+=1
            timer=math.floor((timer+0.1)*100)/100
        #print(timeline)
        return timeline

    
    def updateTrialInfo(self):
        if self.brain.goCue[self.goCueIndex]<=self.playback.timer:
            self.goCueIndex+=1
        if self.brain.feedbackTime[self.feedbackIndex]<=self.playback.timer:
            self.feedbackIndex+=1
        if self.brain.start[self.trialCounter]<=self.playback.timer:
            self.trialCounter+=1
        if self.brain.stim[self.stimCounter]<=self.playback.timer:
            self.stimCounter+=1
        if self.brain.goCue[self.prevGoCueIn]<=self.playback.timer-5:
            self.prevGoCueIn+=1
        if self.brain.feedbackTime[self.prevFeedIn]<=self.playback.timer-5:
            self.prevFeedIn+=1
        if self.brain.start[self.prevTrialIn]<=self.playback.timer-5:
            self.prevTrialIn+=1
        if self.brain.stim[self.stimCounter]<=self.playback.timer:
            self.stimCounter+=1
        if self.stimCounter%2==0:
            self.stimAppear="Off"
        else:
            self.stimAppear="On"
        if self.brain.firstWheelMove[self.prevWheelMoveCounter]<=self.playback.timer-5:
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
        if newTime<oldTime:
            goCueIndex=0
            while(self.brain.goCue[goCueIndex]<=newTime):
                goCueIndex+=1
            self.goCueIndex=goCueIndex
            feedbackIndex=0
            while(self.brain.feedbackTime[feedbackIndex]<=newTime):
                feedbackIndex+=1
            self.feedbackIndex=feedbackIndex
            prevGoCue=0
            while(self.brain.goCue[prevGoCue]<=newTime-5):
                prevGoCue+=1
            self.prevGoCueIn=prevGoCue
            wheelMove=0
            while(self.brain.firstWheelMove[wheelMove]<=newTime-5):
                wheelMove+=1
            self.prevWheelMoveCounter=wheelMove
            stimCounter=0
            while(self.brain.stim[stimCounter]<=newTime):
                stimCounter+=1
            self.stimCounter=stimCounter
            prevFeed=0
            while(self.brain.feedbackTime[prevFeed]<=newTime-5):
                prevFeed+=1
            self.prevFeedIn=prevFeed
            trialCounter=0
            while(self.brain.start[trialCounter]<=newTime):
                trialCounter+=1
            self.trialCounter=trialCounter
            prevTrial=0
            while(self.brain.start[prevTrial]<=newTime):
                prevTrial+=1
            self.prevTrialIn=prevTrial
        else:
            goCueIndex=self.goCueIndex
            while(self.brain.goCue[goCueIndex]<=newTime):
                goCueIndex+=1
            self.goCueIndex=goCueIndex
            feedbackIndex=self.feedbackIndex
            while(self.brain.feedbackTime[feedbackIndex]<=newTime):
                feedbackIndex+=1
            self.feedbackIndex=feedbackIndex
            prevGoCue=self.prevGoCueIn
            while(self.brain.goCue[prevGoCue]<=newTime-5):
                prevGoCue+=1
            self.prevGoCueIn=prevGoCue
            wheelMove=self.prevWheelMoveCounter
            while(self.brain.firstWheelMove[wheelMove]<=newTime-5):
                wheelMove+=1
            self.prevWheelMoveCounter=wheelMove
            stimCounter=self.stimCounter
            while(self.brain.stim[stimCounter]<=newTime):
                stimCounter+=1
            self.stimCounter=stimCounter
            prevFeed=self.prevFeedIn
            while(self.brain.feedbackTime[prevFeed]<=newTime-5):
                prevFeed+=1
            self.prevFeedIn=prevFeed
            trialCounter=self.trialCounter
            while(self.brain.start[trialCounter]<=newTime):
                trialCounter+=1
            self.trialCounter=trialCounter
            prevTrial=self.prevTrialIn
            while(self.brain.start[prevTrial]<=newTime-5):
                prevTrial+=1
            self.prevTrialIn=prevTrial