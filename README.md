# ond_visualization
A simple tool to visualize the IBL Dataset using the ONE API <br>
<br>
## Contributions
Gerrit Fischer: Brain, Playback, Info, Background, Timeline, ActorTemplate <br>
Duc Cuong Tommy Tran: Timeline Data, Timeline, Skip Functions, Sync Functions <br>
Maximilian Wojak: Library for Data Access <br>
<br>
## Important information
This software has been developed and tested on Windows systems. <br>
At the moment only a few tests have been done on Linux and MacOS with mixed results. <br>
We highly recommend using a Windows system. <br>
Also Python 3.12 is currently not working because of different dependencies. <br>
We recommend Python 3.11 <br>
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
### Alternative
Clone the whole repository and run the main.py file. <br>
For that ```pip install brainrender``` has to be run first <br>

## Known errors
ImportError: DLL load failed while importing _cext:
This error can be resolved by installing another package
``` pip install msvc-runtime ```

## Citations  
Brainrender: <br>
Claudi, F., Tyson, A., Petrucco, L., Margrie, T. W., Portugues, R., & Branco, T. (2021). Visualizing anatomically registered data with brainrender. eLife, 10. https://doi.org/10.7554/eLife.65751 <br>
SimpleSessionEx: <br>
Wojak, M. https://github.com/Blumenfreund1337/SimpleSessionEx <br>
Vedo: <br>
https://github.com/marcomusy/vedo
