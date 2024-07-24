# ond_visualization
A simple tool to visualize the IBL Dataset using the ONE API <br>
<br>
**Contributions**: <br>
Gerrit Fischer: Brain, Playback, Info, Background, Timeline, ActorTemplate <br>
Duc Cuong Tommy Tran: Timeline Data, Timeline, Skip Functions, Sync Functions <br>
Maximilian Wojak: Library for Data Access <br>
<br>
## How to use
### 1. Install pip package
```
pip install ond-visualization
```
### 2. Run example code
```py
import ond_visualization as ond

session = ond.createSess(Roi="SI")
renderer = ond.Renderer(session)
renderer.startRender()
```


## Citations  
Brainrender: <br>
Claudi, F., Tyson, A., Petrucco, L., Margrie, T. W., Portugues, R., & Branco, T. (2021). Visualizing anatomically registered data with brainrender. eLife, 10. https://doi.org/10.7554/eLife.65751 <br>
SimpleSessionEx: <br>
Wojak, M. https://github.com/Blumenfreund1337/SimpleSessionEx
