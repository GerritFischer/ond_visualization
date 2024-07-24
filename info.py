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