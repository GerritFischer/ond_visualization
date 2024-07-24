from actortemplate import *
from vedo import Sphere, LegendBox, Text2D

class Background(ActorTemplate):
    def __init__(self):
        super().__init__()
        self.generateBackground()
    def generateBackground(self):
        #generate actor with empty legend as placeholder
        placeholderSphere = Sphere()
        placeholderSphere.legend(" ")
        #top side bar 
        lboxSidebarTop = LegendBox([placeholderSphere], width=0.15, height=0.55, c=(0,0,0), pos="top-left", alpha=1, padding=0)
        lboxSidebarTop.SetBackgroundColor(0.14,0.14,0.14)
        lboxSidebarTop.SetEntryColor(0, 0.14,0.14,0.14)
        lboxSidebarTop.BorderOff()
        super().addActor(lboxSidebarTop)
        #bottom side bar
        lboxSidebarBottom = LegendBox([placeholderSphere], width=0.15, height=0.35, c=(0,0,0), pos="bottom-left", alpha=1, padding=0)
        lboxSidebarBottom.SetBackgroundColor(0.14,0.14,0.14)
        lboxSidebarBottom.SetEntryColor(0,0.14,0.14,0.14)
        lboxSidebarBottom.BorderOff()
        super().addActor(lboxSidebarBottom)
        #bottom bar
        lboxBottomBar = LegendBox([placeholderSphere], width=0.85, height=0.15, c=(0,0,0), pos="bottom-left", alpha=1, padding=0)
        lboxBottomBar.SetBackgroundColor(0.14,0.14,0.14)
        lboxBottomBar.SetEntryColor(0, 0.14,0.14,0.14)
        lboxBottomBar.BorderOff()
        lboxBottomBar.GetPositionCoordinate().SetValue(0.15, 0)
        super().addActor(lboxBottomBar)
        
        #headings
        lboxSidebarHeading = Text2D(" Info ", (0, 1), bg=(0.23,0.23,0.23), c=(1,1,1))
        super().addActor(lboxSidebarHeading)
        lboxBottombarHeading = Text2D(" Playback ", (0.15, 0.15), bg=(0.23,0.23,0.23), c=(1,1,1))
        super().addActor(lboxBottombarHeading)
        lboxSidebarBHeading = Text2D(" Spikes ", (0, 0.348),bg=(0.23,0.23,0.23), c=(1,1,1))
        super().addActor(lboxSidebarBHeading)

