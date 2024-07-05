from actortemplate import ActorTemplate
from vedo import Button, Text2D
from custom_classes import CustomSlider, CustomButton
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
    

    def __init__(self, button_play_pause, speedslider, timerslider):
        self.button_play_pause = button_play_pause
        self.speedslider = speedslider
        self.timerslider = timerslider

        super().__init__()
        super().addActor(CustomSlider(self.timerslider, xmin=0, xmax=4000, value=2000, pos=[(0.25,0.09),(0.5, 0.09)], show_value=True, c=(1,1,1)))
        super().addActor(CustomSlider(self.skip, xmin=0, xmax=1, value=0, pos=[(0.25,0.03),(0.5, 0.03)], show_value=True, c=(1,1,1)))
        self.button = CustomButton(self.button_play_pause, states=[" ▶ "," ⏸ "], size=50, c=("white","white"), bc=("grey1","grey1"),pos=(0.21,0.09), font="Kanopus")
        print(type(self.button))
        super().addActor(self.button)
        super().addActor(CustomSlider(self.speedslider, xmin=0, xmax=2999, value=2000, pos=[(0.8,0.05),(0.98, 0.05)], title="", show_value=True, c=(1,1,1)))
        print(self.actors)


    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


 

    def skip(self,obj,btn):
        if self.skipCounter==0:
            return
        self.skipped=True
        if (self.goCueIndex+self.skipCounter<len(self.goCue)):
            if(self.goCueIndex+self.skipCounter>=0):
                self.goCueIndex+=self.skipCounter
                self.goCueIndex-=1
                self.trialCounter+=self.skipCounter
                self.trialCounter-=1
                if(self.feedbackTimeIndex!=0 and self.goCueIndex!=1):
                    self.feedbackTimeIndex=self.goCueIndex-1
                if(self.goCueIndex!=0):
                
                    self.prevGoCueIndex=self.goCueIndex-1
        
                self.timer=math.floor(self.goCue[self.goCueIndex]*10)/10
            else:
                self.goCueIndex=0
                self.trialCounter=0
                self.feedbackTimeIndex=0
                self.timer=0
                self.prevGoCueIndex=0
                self.prevFeedIndex=0
        else:
            self.goCueIndex=len(self.goCue)
            self.trialCounter=len(self.goCue)
            self.feedbackTimeIndex=self.goCueIndex-1
            self.timer=math.floor(self.goCue[self.goCueIndex]*10)/10
            self.prevGoCueIndex=self.goCueIndex-1
        index=0
        while(self.timer-0.5>=self.feedbackTime[index]):
            if(index>=len(self.feedbackTime)):
                break
            index+=1
        self.prevFeedIndex=index
        

        newStimCounter=0
        while(self.stim[newStimCounter]<=self.timer):
            newStimCounter+=1
            if(self.stimCounter>=len(self.stim)):
                break
        self.stimCounter=newStimCounter

        newTimes=0
        while(self.spikes.times[newTimes]<=self.timer):#need to add spikes times
            newTimes+=1
            if(newTimes>=len(self.spikes.times)):
                break
            # need to add spike index
            self.newTimes=newTimes
    
        if newStimCounter!=0:
            if newStimCounter!=self.stimCounter:
                if((newStimCounter-1)%2==0):
                    self.stimAppear="Stim On"
                else:
                    self.stimAppear="Stim Off"
        self.currentAction="Go Cue"
        if self.feedbackType[self.trialCounter]>0:
            rewardType="Reward"
        else:
            rewardType="Error"
        if self.timer!=0 and self.prevFeedIndex!=0 and self.prevGoCueIndex!=0:
            if self.feedbackTime[self.prevFeedIndex]>self.goCue[self.prevGoCueIndex]:
                self.prevAction="Feedback Time"
            else:
                self.prevAction="Go Cue"
        else:
            self.prevAction=""

    def getSkipCounter(self):
        return self.skipCounter
    def isSkipped(self):
        return self.skipped
    def setSkipped(self):
        self.skipped=False
    def getTimer(self):
        return self.timer
    def getSpikeIndex(self):
        return self.newTimes
def dummy_s(btn, event):
    print("hello")
    btn.switch()