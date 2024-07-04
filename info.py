from actortemplate import ActorTemplate
from vedo import Text2D

class Info(ActorTemplate):
    def __init__(self):
        super().__init__()
        self.createText()
        self.createRightText()

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
            text_t.pos((0.005,l*0.03+0.4295))
            text_t.properties.SetColor(1,1,1)
            super().addActor(text_t)
        
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