from actortemplate import ActorTemplate
from vedo import Text2D
from custom_classes import CustomSlider, CustomButton
import colorsys

class Playback(ActorTemplate):
    
    timer=0
    spikeIndex = 0

    speed_minus = 2000
    contrast = 1
    timestep = 0.1
    

    def __init__(self, button_play_pause, speedslider, timerslider, skip):
        self.button_play_pause = button_play_pause
        self.speedslider = speedslider
        self.timerslider = timerslider
        self.skip = skip

        super().__init__()
        #create control elements with functions defined in renderer
        super().addActor(CustomSlider(self.timerslider, xmin=0, xmax=3000, value=0, pos=[(0.3,0.09),(0.6, 0.09)], show_value=True, c=(1,1,1)))
        super().addActor(CustomSlider(self.skip, xmin=0, xmax=1, value=0, pos=[(0.3,0.03),(0.6, 0.03)], show_value=True, c=(1,1,1)))
        self.button = CustomButton(self.button_play_pause, states=[" ▶ "," ⏸ "], size=50, c=("white","white"), bc=("grey1","grey1"),pos=(0.21,0.09), font="Kanopus")
        super().addActor(self.button)
        super().addActor(CustomSlider(self.speedslider, xmin=0, xmax=2999, value=2000, pos=[(0.8,0.09),(0.98, 0.09)], title="", show_value=False, c=(1,1,1)))
        super().addActor(CustomSlider(self.contrastslider, xmin=0.01, xmax=5, value=1, pos=[(0.8,0.03),(0.98, 0.03)], title="", show_value=False, c=(0,0,0)))
        super().addActor(Text2D("Skip to \n Time", pos=(0.25, 0.12), c=(1,1,1)))
        super().addActor(Text2D("Skip to \n Trial", pos=(0.25, 0.06), c=(1,1,1)))
        super().addActor(Text2D("Speed", pos=(0.73,0.1), c=(1,1,1)))
        super().addActor(Text2D("Contrast", pos=(0.73,0.04), c=(1,1,1)))
        super().addActor(CustomButton(self.timestepButton, states=["0.1","0.01"], size=40, pos=(0.67, 0.08)))
        super().addActor(Text2D("Timestep", pos=(0.645, 0.11), c=(1,1,1,)))


    def hsv2rgb(h,s,v):
        #color calculation
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    def contrastslider(self, widget, event):
        self.contrast = widget.value
    def timestepButton(self, btn, event):
        if self.timestep == 0.1: self.timestep = 0.01
        else: self.timestep = 0.1
        btn.switch()
        