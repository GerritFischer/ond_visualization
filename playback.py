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
    

    def __init__(self, button_play_pause, speedslider, timerslider, skip):
        self.button_play_pause = button_play_pause
        self.speedslider = speedslider
        self.timerslider = timerslider
        self.skip = skip

        super().__init__()
        super().addActor(CustomSlider(self.timerslider, xmin=0, xmax=3000, value=0, pos=[(0.25,0.09),(0.5, 0.09)], show_value=True, c=(1,1,1)))
        super().addActor(CustomSlider(self.skip, xmin=0, xmax=1, value=0, pos=[(0.25,0.03),(0.5, 0.03)], show_value=True, c=(1,1,1)))
        self.button = CustomButton(self.button_play_pause, states=[" ▶ "," ⏸ "], size=50, c=("white","white"), bc=("grey1","grey1"),pos=(0.21,0.09), font="Kanopus")
        super().addActor(self.button)
        super().addActor(CustomSlider(self.speedslider, xmin=0, xmax=2999, value=1000, pos=[(0.8,0.05),(0.98, 0.05)], title="Speed", show_value=False, c=(1,1,1)))
        super().addActor(CustomSlider(self.speedslider, xmin=0, xmax=2999, value=1000, pos=[(0.8,0.07),(0.98, 0.07)], title="", show_value=False, c=(0,0,0)))
        


    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))



def dummy_s(btn, event):
    print("hello")
    btn.switch()