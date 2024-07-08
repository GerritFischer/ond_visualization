from vedo import Button#
from custom_classes import CustomSlider, CustomButton
class ActorTemplate:
    def __init__(self):
        self.actors = []
    def setActors(self, actors):
        self.actors = actors
    def addActor(self, actor):
       
        self.actors.append(actor)
    def addToPlotter(self, plotter):
        for actor in self.actors:
            if(type(actor) == CustomButton):
                plotter.add_button(actor.function, font=actor.font_s, states=actor.states, size=actor.size_s, pos=(actor.GetPositionCoordinate().GetValue()[0],actor.GetPositionCoordinate().GetValue()[1]))
            elif(type(actor) == CustomSlider):
                #test = Slider2D()
                #print(actor.GetCommand(1))
                plotter.add_slider(actor.sliderfunc, xmin=actor.GetRepresentation().GetMinimumValue(),  xmax=actor.GetRepresentation().GetMaximumValue(), value=actor.value, pos=actor.pos, title=actor.title, show_value=actor.show_value, c=(1,1,1))
                #super().addActor(Slider2D(self.speedslider, xmin=0, xmax=2999, value=2000, pos=[(0.8,0.05),(0.98, 0.05)], title="", show_value=True, c=(1,1,1)))
            else:
                plotter.add(actor)