from vedo import Plotter
from vedo import Text2D,Button
import math
from timeline import *
class actors:
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
    timer_id = -1
    skipped=False


    currentActionText=None
    trialCounterText=None
    rewardTypeText=None
    stimText =None
    skipCounterText=None
    timer=0
    plotter= Plotter()
    newTimes=0

    def __init__(self,spikes,goCue,feedbackTime,feedbackType,stim):
        self.spikes=spikes
        self.goCue=goCue
        self.feedbackTime=feedbackTime
        self.feedbackType=feedbackType
        self.stim=stim
        self.timeline = timeline(0.105, 0.71)
        self.addActors()
        self.createRightText()

    def addActors(self):
        self.button = self.plotter.add_button(self.button_play_pause, states=[" Play ","Pause"], size=40,pos=(0.9,0.1))
        #self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)

        self.plotter.add_button(self.skip,states=["Skip"],size=40,pos=(0.5,0.1))

        self.plotter.add_button(self.slowdecSkip,states=["-"],size=20,pos=(0.15,0.09))
        self.plotter.add_button(self.fastdecSkip,states=["--"],size=20,pos=(0.09,0.09))
        self.plotter.add_button(self.slowinSkip,states=["+"],size=20,pos=(0.27,0.09))
        self.plotter.add_button(self.fastinSkip,states=["++"],size=20,pos=(0.33,0.09))
        self.timeline.addToPlotter(self.plotter)

    def button_play_pause(self,obj, btn):
        self.plotter.timer_callback("destroy", self.timer_id)
        if "Play" in self.button.status():
            # instruct to call handle_timer() every 10 msec:
            self.timer_id = self.plotter.timer_callback("create", dt=1000)
        self.button.switch() 
    
    def slowdecSkip(self,obj,btn):
        self.skipCounter-=1
    def fastdecSkip(self,obj,btn):
        self.skipCounter-=10
    def fastinSkip(self,obj,btn):
        self.skipCounter+=10
    def slowinSkip(self,obj,btn):
        self.skipCounter+=1

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
                print("yeayyy")
                self.stimCounter+=1

        self.currentActionText.text("Order: "+self.currentAction)
        self.trialCounterText.text("Number of Trials: "+str(self.trialCounter))
        self.rewardTypeText.text("Reward Type: "+self.rewardType)
        self.stimText.text(self.stimAppear)

        self.skipCounterText.text(str(self.skipCounter))

    def numberOfBtn(self):
        counter=0
        for i in self.plotter.get_actors():
            if type(i)==Button:
                counter+=1
        print(counter)
        return len(self.plotter.get_actors())
    def createRightText(self):
        self.currentActionText=Text2D(" ",pos=(0.7,0.97),c=(1,1,1))
        self.trialCounterText=Text2D(" ",pos=(0.7,1),c=(1,1,1))
        self.rewardTypeText=Text2D(" ",pos=(0.7,0.94),c=(1,1,1))
        self.stimText = Text2D(" ",pos=(0.7,0.91),c=(1,1,1))
        self.skipCounterText= Text2D(str(self.skipCounter),pos=(0.2,0.1),c=(1,1,1),s=2.5)

        self.plotter.add(self.currentActionText)
        self.plotter.add(self.trialCounterText)
        self.plotter.add(self.rewardTypeText)
        self.plotter.add(self.stimText)
        self.plotter.add(self.skipCounterText)
    def getSkipCounter(self):
        return self.skipCounter
    def isSkipped(self):
        return self.skipped
    def setSkipped(self):
        self.skipped=False
    def getTimer(self):
        return self.timer
    #füge Skip function hinzu


    def skip(self,obj,btn):
        if self.skipCounter==0:
            return
        self.skipped=True
        if (self.goCueIndex+self.skipCounter<len(self.goCue)):
            if(self.goCueIndex+self.skipCounter>=0):
                print("yeep")
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
    def getPlotter(self):
        return self.plotter
    def getSpikeIndex(self):
        return self.newTimes