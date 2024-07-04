from vedo import Button
class ActorTemplate:
    actors = []
    def setActors(self, actors):
        self.actors = actors
    def addActor(self, actor):
       
        self.actors.append(actor)
    def addToPlotter(self, plotter):
        for actor in self.actors:
            if(type(actor) == type(Button())):
                print(actor.GetPositionCoordinate().GetValue())
                plotter.add_button(actor.function, font="Kanopus", states=actor.states, size=20, pos=(actor.GetPositionCoordinate().GetValue()[0],actor.GetPositionCoordinate().GetValue()[1]))
            else:
                plotter.add(actor)