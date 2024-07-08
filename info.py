from actortemplate import ActorTemplate
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