from brain_new import *
from timeline import *
from background import Background
from playback import Playback
from info import Info
from vedo import Plotter
import colorsys
class Renderer:

    timer_id = -1
    def __init__(self):
        self.plotter = Plotter()
        self.brain = BrainNew()
        self.timeline = Timeline(0, 0.3)
        self.background = Background()
        self.playback = Playback(self.button_play_pause, self.speedslider, self.timerslider)
        self.info = Info()
        self.info.setSessionInfo()
        self.background.addToPlotter(self.plotter)
        self.info.addToPlotter(self.plotter)  
        self.timeline.addToPlotter(self.plotter)
        self.brain.addToPlotter(self.plotter)
        self.playback.addToPlotter(self.plotter)
        

        self.plotter.roll(180)
        self.plotter.background((30,30,30))
        
        self.end = self.brain.spikes.times[-1] #temp
        #wip
        rep = self.playback.actors[0].GetSliderRepresentation()
        print(rep.GetMaximumValue())
        rep.SetMaximumValue(math.floor(self.end))
        
        self.playback.actors[0].SetRepresentation(rep)

        self.plotter.add_callback("timer", self.animation_tick, enable_picking=False)
    def startRender(self):
        print(self.plotter.get_actors())
        self.plotter.show(__doc__)

    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    
    def animation_tick(self, event):
        if self.playback.isSkipped():
            self.playback.setSkipped()
            self.playback.spikeIndex =self.playback.getSpikeIndex()
        if(self.playback.timer < self.end):
            
            self.playback.actors[0].GetSliderRepresentation().SetValue(self.playback.timer)
            print(self.playback.speed_minus)
            self.timeline.updateHistogram(self.playback.timer, self.playback.prevAction, self.plotter)
            currentSpikes = []
            elemStillIn = True         
            while(elemStillIn):
                if(self.playback.spikeIndex >= len(self.brain.spikes.times)):
                    break
                if(self.brain.spikes.times[self.playback.spikeIndex] > self.playback.timer and self.brain.spikes.times[self.playback.spikeIndex] < self.playback.timer + 0.1):
                    currentSpikes.append(self.playback.spikeIndex)  
                    print("addedSpike") 
                else:
                    elemStillIn = False
                self.playback.spikeIndex += 1
             

            
            self.info.actors[19].text("Total Spikes: " + str(len(currentSpikes)))
            for k in range(len(self.brain.regionModels)):
                spikesInRegion = 0
                for j in currentSpikes:
                    if(self.brain.clusters.acronym[self.brain.spikes.clusters[j]] == self.brain.regionModels[k][0]):
                        spikesInRegion += 1

                self.brain.actors[k+1].actor.GetProperty().SetOpacity(spikesInRegion * 0.01)
                

                color = self.hsv2rgb(k / len(self.brain.regionModels), 1,1)
                color255 = (color[0]/255, color[1]/255, color[2]/255)
            
            
                self.info.actors[18-k].text("Spikes in " + self.brain.regionModels[k][0] + ": " + str(spikesInRegion))
                self.info.actors[18-k].properties.SetColor(color255)
                self.brain.actors[k+1].actor.GetProperty().SetColor(color255)
                self.brain.actors[k+1].actor.GetProperty().SetRepresentation(1)

            #self.actors.updateTrialInfo(self.timer)


            self.info.actors[18-len(self.brain.regionModels)].text("Time: " + str(self.playback.timer))
            self.info.actors[18-len(self.brain.regionModels)].properties.SetColor(1,1,1)
            self.playback.timer = math.floor((self.playback.timer*10)+1)/10
        print(self.playback.spikeIndex)
        self.plotter.render()

    def button_play_pause(self, btn, obj):
        self.plotter.timer_callback("destroy", self.timer_id)
        if "▶" in btn.status():
            self.timer_id = self.plotter.timer_callback("create", dt=math.ceil(3000-self.playback.speed_minus))
        btn.switch()
    def speedslider(self, widget, event):
        self.playback.speed_minus = widget.value
        self.updateSpikeIndex()
        
        #TODO: needs fixing
        try:
            print("ARGHT")
            self.plotter.timer_callback("destroy", self.timer_id)
            self.timer_id = self.plotter.timer_callback("create", dt=math.ceil(3000-self.playback.speed_minus))
        except:
            pass
    
    def timerslider(self, widget, event):
        self.playback.timer = math.floor(widget.value*100) / 100
        self.updateSpikeIndex()
        

        #if "⏸" in self.playback.button.status():
    def updateSpikeIndex(self):
        newTimes=0
        while(self.brain.spikes.times[newTimes]<=self.playback.timer):#need to add spikes times
            newTimes+=1
            if(newTimes>=len(self.brain.spikes.times)):
                break
            # need to add spike index
        self.playback.spikeIndex = newTimes

    
