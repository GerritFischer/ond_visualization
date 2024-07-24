from brain import Brain
from timeline import Timeline
from background import Background
from playback import Playback
from info import Info
from vedo import Plotter
import colorsys
import numpy as np
import math
class Renderer:

    timer_id = -1
    goCueIndex=0
    trialCounter=0
    feedbackIndex=0
    stimAppear="Off"
    stimCounter=0
    #prev variable needed to get the timeline data
    prevFeedIn=0
    prevGoCueIn=0
    prevTrialIn=0
    prevWheelMoveCounter=0

    def __init__(self, session):
        self.session = session
        self.plotter = Plotter()
        self.brain = Brain(session)#session.getClusterAndSpikesOfSess()
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
        
        self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)
        self.playback.addToPlotter(self.plotter)
    def startRender(self):
        self.plotter.show(__doc__)

    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    
    def animation_tick(self, event):
        #everything that happens in one frame
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
        try:
            self.plotter.timer_callback("destroy", self.timer_id)
            self.timer_id = self.plotter.timer_callback("create", dt=math.ceil(3000-self.playback.speed_minus))
        except:
            pass
    
    def timerslider(self, widget, event):
        self.synchIndex(self.playback.timer,math.floor(widget.value*100) / 100)
        self.playback.timer = math.floor(widget.value*100) / 100
        self.updateSpikeIndex()
        
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
            #check if we are between the FeedbackTime and the new Trial 
            if (timelineTrial<len(self.brain.start)):
                if timer>=self.brain.feedbackTime[timelineTrial] and timer<=self.brain.start[timelineTrial]  :
                    #push the feedbackType into the Array to plot it in the histogram
                    if self.brain.feedbackType[timelineTrial]>0:
                        timeline.append("Feedback Time, Reward")
                    else:
                        timeline.append("Feedback Time, Error")
                    append=True
            #check if the first feedbackType is happening now
            if (timelineFeed<len(self.brain.feedbackTime)):
                if math.floor((timer+0.1)*100)/100>= self.brain.feedbackTime[timelineFeed]and timer<=self.brain.feedbackTime[timelineFeed]:
                    if self.brain.feedbackType[timelineFeed]>0:
                        #push the feedbackType into the Array to plot it in the histogram
                        timeline.append("Feedback Time, Reward")
                    else:
                        timeline.append("Feedback Time, Error")
                    append=True
                    timelineFeed+=1
            #check if the Go Cue starts at the moment 
            if (timelineGoCue<len(self.brain.goCue)):
                if math.floor((timer+0.1)*100)/100>=self.brain.goCue[timelineGoCue] and timer<=self.brain.goCue[timelineGoCue]:
                    #push it to array to plot it in the histogram
                    timeline.append("Go Cue")
                    append=True
                    timelineGoCue+=1
            #check if the First Movement starts
            if(timelineWheel<len(self.brain.firstWheelMove)):
                if math.floor((timer+0.1)*100)/100>=self.brain.firstWheelMove[timelineWheel] and timer <=self.brain.firstWheelMove[timelineWheel]:
                    #push it to the array to plot that inside the histogram
                    timeline.append("First Wheel Movement")
                    append=True
                    timelineWheel+=1
            #if nothing is pushed at that iteration empty String is pushed to show nothing happend
            if not append:
                timeline.append("")
            append=False
            if(timelineTrial<len(self.brain.start)):
                if math.floor((timer+0.1)*100)/100>=self.brain.start[timelineTrial] and timer<=self.brain.start[timelineTrial]:
                    timelineTrial+=1
            timer=math.floor((timer+0.1)*100)/100
        return timeline

    
    def updateTrialInfo(self):
        #if the timer is higher than the current Go Cue increase the index
        if self.goCueIndex< len(self.brain.goCue):
            if self.brain.goCue[self.goCueIndex]<=self.playback.timer:
                self.goCueIndex+=1
        #if the timer is higher than the current Feedback Time increase the index
        if self.feedbackIndex<len(self.brain.feedbackTime):
            if self.brain.feedbackTime[self.feedbackIndex]<=self.playback.timer:
                self.feedbackIndex+=1
       #if the timer is higher than the current Trialstart Time increase the index
        if self.trialCounter<len(self.brain.start):
            if self.brain.start[self.trialCounter]<=self.playback.timer:
                self.trialCounter+=1
        #if the timer is higher than the current Stim switch  increase the index
        if self.stimCounter< len(self.brain.stim):
            if self.brain.stim[self.stimCounter]<=self.playback.timer:
                self.stimCounter+=1
        #if the timer is higher than the previous Go Cue increase the index
        if self.prevGoCueIn<len(self.brain.goCue):
            if self.brain.goCue[self.prevGoCueIn]<=self.playback.timer-5:
                self.prevGoCueIn+=1
        #if the timer is higher than the previous Feedback Time increase the index
        if self.prevFeedIn< len(self.brain.feedbackTime):
            if self.brain.feedbackTime[self.prevFeedIn]<=self.playback.timer-5:
                self.prevFeedIn+=1
        #if the timer is higher than the previous Trialstart Time increase the index
        if self.prevTrialIn<len(self.brain.start):
            if self.brain.start[self.prevTrialIn]<=self.playback.timer-5:
                self.prevTrialIn+=1
        #set the text stim off/on according to the counter
        if self.stimCounter<len(self.brain.stim):
            if self.brain.stim[self.stimCounter]<=self.playback.timer:
                self.stimCounter+=1
        if self.stimCounter%2==0:
            self.stimAppear="Off"
        else:
            self.stimAppear="On"
        #if the timer is higher than the previous First Wheel Movement increase the index
        if self.prevWheelMoveCounter<len(self.brain.firstWheelMove):
            if self.brain.firstWheelMove[self.prevWheelMoveCounter]<=self.playback.timer-5 or np.isnan(self.brain.firstWheelMove[self.prevWheelMoveCounter]):
                self.prevWheelMoveCounter+=1


    #update the timer
    def getSkippedTimer(self,skip):
        if skip<=0:
            return 0
        if skip>=len(self.brain.goCue):
            #if the skip is higher or equal to the amount of trual set the time to the last trial
            timer= self.brain.feedbackTime[len(self.brain.feedbackTime)-2]# one time -1 to get be inside the list boundary and the other -1 to get the time of prev feedbackTime
            if self.brain.feedbackType[len(self.brain.feedbackType)-2]>0:
                timer+=1 #new trial time after reward
                timer= math.floor(timer*10)/10
            else:
                timer= math.floor((timer/10)+1)*10
                timer+=2 # new trial time after Fail
            return timer
        #set the timer to the skipped trial add 1 or 2 depending on error or reward
        timer=self.brain.feedbackTime[skip-1]
        if self.brain.feedbackType[skip-1]>0:
            timer+=1
            timer= math.floor(timer*10)/10
        else:
            timer+=2
            timer= math.floor(timer*10)/10
        return timer
    #this function update the index and time equivalent to the trial
    def skip(self, widget, event):
        trialNum = math.floor(widget.value)
        #if the trial number is resettet reset all indexes
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
        #update Indexes to the current trial
            self.goCueIndex=trialNum-1
            self.feedbackIndex=self.goCueIndex
            self.trialCounter=trialNum
            self.prevFeedIn=self.goCueIndex
            self.prevGoCueIn=self.goCueIndex
            self.playback.timer=self.getSkippedTimer(trialNum)
            self.prevWheelMoveCounter=self.goCueIndex
            self.prevTrialIn=self.goCueIndex
        #iterate to update the stim index
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
        #update Spike Index
        self.updateSpikeIndex()
    #update the indexes equivalent to the timer
    def synchIndex(self,oldTime,newTime):
        #check if the user skip back or forward
        if newTime<oldTime:
            #update goCue Index from 0
            goCueIndex=0
            while self.brain.goCue[goCueIndex]<=newTime:
                goCueIndex+=1
                if(goCueIndex>=len(self.brain.goCue)):break
            self.goCueIndex=goCueIndex
            #update help variable previous Go Cue from 0
            prevGoCue=0
            while self.brain.goCue[prevGoCue]<=newTime-5:
                prevGoCue+=1
                if(goCueIndex>=len(self.brain.goCue)):break
            self.prevGoCueIn=prevGoCue
            #update FeedBack Index from 0
            feedbackIndex=0
            while self.brain.feedbackTime[feedbackIndex]<=newTime:
                feedbackIndex+=1
                if(feedbackIndex>=len(self.brain.feedbackTime)):break
            self.feedbackIndex=feedbackIndex
            #update help variable previous Feedback Time from 0
            prevFeed=0
            while self.brain.feedbackTime[prevFeed]<=newTime-5:
                prevFeed+=1
                if(prevFeed>=len(self.brain.feedbackTime)):break
            self.prevFeedIn=prevFeed
            #update Trial Counter Index from 0
            trialCounter=0
            while(self.brain.start[trialCounter]<=newTime):
                trialCounter+=1
                if(trialCounter>= len(self.brain.start)):break
            self.trialCounter=trialCounter
            #update help variable previous trial Counter from 0
            prevTrialCounter=0
            while self.brain.start[prevTrialCounter]<=newTime-5:
                prevTrialCounter+=1
                if(prevTrialCounter>=len(self.brain.start)):break
            self.prevTrialIn=prevTrialCounter
            #update help variable previous first Wheel Move from 0
            prevWheelMove=0
            while self.brain.firstWheelMove[prevWheelMove]<=newTime-5 or np.isnan(self.brain.firstWheelMove[prevWheelMove]):
                prevWheelMove+=1
                if(prevWheelMove>=len(self.brain.firstWheelMove)):break
            self.prevWheelMoveCounter=prevWheelMove
            #update the Stim Index from 0
            stimCounter=0
            while self.brain.stim[stimCounter]<= newTime:
                stimCounter+=1
                if(stimCounter>=len(self.brain.stim)):break
        else:
            #update goCue Index from the current Index
            goCueIndex=self.goCueIndex
            if (goCueIndex<len(self.brain.goCue)):
                while(self.brain.goCue[goCueIndex]<=newTime):
                    goCueIndex+=1
                    if(goCueIndex>=len(self.brain.goCue)):break
            self.goCueIndex=goCueIndex
            #update help variable previous goCue Index from the current Index
            prevGoCue=self.prevGoCueIn
            if (prevGoCue<len(self.brain.goCue)):
                while(self.brain.goCue[prevGoCue]<=newTime-5):
                    prevGoCue+=1
                    if(prevGoCue>=len(self.brain.goCue)):break
            self.prevGoCueIn=prevGoCue
            #update Feedback Time Index from the current Index
            feedbackIndex=self.feedbackIndex
            if(feedbackIndex<len(self.brain.feedbackTime)):
                while(self.brain.feedbackTime[feedbackIndex]<=newTime):
                    feedbackIndex+=1
                    if(feedbackIndex>=len(self.brain.feedbackTime)):break
            self.feedbackIndex=feedbackIndex
            #update help variable previous Feedback Time Index from the current Index
            prevFeed=self.prevFeedIn
            if(prevFeed<len(self.brain.feedbackTime)):
                while(self.brain.feedbackTime[prevFeed]<=newTime-5):
                    prevFeed+=1
                    if(prevFeed>=len(self.brain.feedbackTime)):break
            self.prevFeedIn=prevFeed
            #update the Trial Counter from the current Index
            trialCounter=self.trialCounter
            if(trialCounter<len(self.brain.start)):
                while(self.brain.start[trialCounter]<=newTime):
                    trialCounter+=1
                    if(trialCounter>=len(self.brain.start)):break
            self.trialCounter=trialCounter
            #update help variable previous Trial Counter from the current Index
            prevTrialCounter=self.prevTrialIn
            if(prevTrialCounter<len(self.brain.start)):
                while(self.brain.start[prevTrialCounter]<=newTime-5):
                    prevTrialCounter+=1
                    if(prevTrialCounter>=len(self.brain.start)):break
            self.prevTrialIn=prevTrialCounter
            #update help variable previous First Wheel Movement from the current index
            prevWheelMove=self.prevWheelMoveCounter
            if(prevWheelMove<len(self.brain.firstWheelMove)):
                while(self.brain.firstWheelMove[prevWheelMove]<=newTime-5)or np.isnan(self.brain.firstWheelMove[prevWheelMove]):
                    prevWheelMove+=1
                    if(prevWheelMove>=len(self.brain.firstWheelMove)):break
            self.prevWheelMoveCounter=prevWheelMove
            #update the Stim Counter from the current Index
            stimCounter=self.stimCounter
            if(stimCounter<len(self.brain.stim)):
                while(self.brain.stim[stimCounter]<=newTime):
                    stimCounter+=1
                    if(stimCounter>=len(self.brain.stim)):break
            self.stimCounter=stimCounter