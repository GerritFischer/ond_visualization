from actortemplate import *
from vedo import Sphere, LegendBox

class Background(ActorTemplate):
    def __init__(self):
        super().__init__()
        self.generateBackground()
    def generateBackground(self):
        print("generated background")
        #generate actor with empty legend as placeholder
        placeholderSphere = Sphere()
        placeholderSphere.legend(" ")
        #top side bar 
        lboxSidebarTop = LegendBox([placeholderSphere], width=0.15, height=0.6, c=(0,0,0), pos="top-left", alpha=1, padding=0)
        lboxSidebarTop.SetBackgroundColor(0.14,0.14,0.14)
        lboxSidebarTop.SetEntryColor(0, 0.14,0.14,0.14)
        lboxSidebarTop.BorderOff()
        super().addActor(lboxSidebarTop)
        #bottom side bar
        lboxSidebarBottom = LegendBox([placeholderSphere], width=0.15, height=0.3, c=(0,0,0), pos="bottom-left", alpha=1, padding=0)
        lboxSidebarBottom.SetBackgroundColor(0.14,0.14,0.14)
        lboxSidebarBottom.SetEntryColor(0,0.14,0.14,0.14)
        lboxSidebarBottom.BorderOff()
        super().addActor(lboxSidebarBottom)
        lboxBottomBar = LegendBox([placeholderSphere], width=0.85, height=0.15, c=(0,0,0), pos="bottom-left", alpha=1, padding=0)
        lboxBottomBar.SetBackgroundColor(0.14,0.14,0.14)
        lboxBottomBar.SetEntryColor(0, 0.14,0.14,0.14)
        lboxBottomBar.BorderOff()
        lboxBottomBar.GetPositionCoordinate().SetValue(0.15, 0)

        super().addActor(lboxBottomBar)
