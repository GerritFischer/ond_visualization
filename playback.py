from actortemplate import ActorTemplate
from vedo import Button, Text2D
from custom_classes import CustomSlider
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
    newTimes=0
    speed_minus = 2000
    



    def __init__(self, button_play_pause):
        self.button_play_pause = button_play_pause
        super().__init__()
        self.button = Button(self.button_play_pause, states=[" ▶ "," ⏸ "], size=20,pos=(0.2,0.1), font="Kanopus")
        print(type(self.button))
        super().addActor(self.button)

        super().addActor(Button(self.skip,states=["Skip"],size=40,pos=(0.7,0.1)))

        super().addActor(Button(self.slowdecSkip,states=["-"],size=20,pos=(0.3,0.1)))
        super().addActor(Button(self.fastdecSkip,states=["--"],size=20,pos=(0.25,0.1)))
        super().addActor(Button(self.slowinSkip,states=["+"],size=20,pos=(0.45,0.1)))
        super().addActor(Button(self.fastinSkip,states=["++"],size=20,pos=(0.5,0.1)))
        super().addActor(CustomSlider(self.speedslider, xmin=0, xmax=2999, value=2000, pos=[(0.8,0.05),(0.98, 0.05)], title="", show_value=True, c=(1,1,1)))
        print(self.actors)
        #self.timeslider = Slider2D(self.timerslider, xmin=0, xmax=5000, value=0, pos=[(0.8,0.15),(0.98, 0.15)], show_value=True, c=(1,1,1))                                                           #xmax=self.spikes.times[-1]
        #super().addActor(self.timeslider)

    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    
    def timerslider(self, widget, event):
        self.timer = widget.value
    def slowdecSkip(self,obj,btn):
        self.skipCounter-=1
    def fastdecSkip(self,obj,btn):
        self.skipCounter-=10
    def fastinSkip(self,obj,btn):
        self.skipCounter+=10
    def slowinSkip(self,obj,btn):
        self.skipCounter+=1
    def speedslider(self, widget, event):
        self.speed_minus = widget.value
        if "⏸" in self.button.status():
            self.plotter.timer_callback("destroy", self.timer_id)
            self.timer_id = self.plotter.timer_callback("create", dt=math.ceil(3000-self.speed_minus))

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