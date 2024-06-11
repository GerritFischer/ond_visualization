import time
import numpy as np
from vedo import Plotter
from vedo.pyplot import plot
from vedo import Text2D, Latex
from vedo import Ellipsoid, show, colors
import random
from brainrender import Scene
from brainrender.actors import Points
from brainbox.io.one import SpikeSortingLoader
from brainbox.plot import peri_event_time_histogram
from brainbox.singlecell import calculate_peths
from one.api import ONE
from ibllib.atlas import AllenAtlas
import math
import colorsys
one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
ba = AllenAtlas()


def get_n_random_points_in_region(region, N):
    """
    Gets N random points inside (or on the surface) of a mesh
    """
    region_bounds = region.mesh.bounds()
    X = np.random.randint(region_bounds[0], region_bounds[1], size=10000)
    Y = np.random.randint(region_bounds[2], region_bounds[3], size=10000)
    Z = np.random.randint(region_bounds[4], region_bounds[5], size=10000)
    print("Region Bound X:" + str(region_bounds[0]) + " " + str(region_bounds[1]))
    X = [math.floor(clusters.x[2] * 2500000), math.floor(clusters.x[3] * 2500000)]
    Y = [math.floor(clusters.y[2] * 2500000), math.floor(clusters.y[3] * 2500000)]
    Z = [math.floor(clusters.z[2] * 2500000), math.floor(clusters.z[3] * 2500000)]
    print(str(X) + " " + str(Y) + " " + str(Z))
    pts = [[x, y, z] for x, y, z in zip(X, Y, Z)]

    ipts = region.mesh.inside_points(pts).coordinates
    print(np.vstack((X,Y,Z)))
    return np.vstack((X,Y,Z))



def loadData():
    roi = "SI" # Region Of Interest (acronym according to Allen Atlas)
    ses = one.alyx.rest('insertions', 'list', atlas_acronym = roi) #loading recordings
    print(f'Found {len(ses)} recordings')
    #isolating first session and probe ID
    EID = ses[0]['session']
    PID = ses[0]['id']
    sl = SpikeSortingLoader(pid=PID, one=one, atlas=ba) # create instance of the SpikeSortingLoader
    spikes, clusters, channels = sl.load_spike_sorting() # load in spike sorted data
    clusters = sl.merge_clusters(spikes, clusters, channels) # merge cluster metrics
    return spikes, clusters, channels



def button_play_pause(obj, btn):
    global timer_id
    plotter.timer_callback("destroy", timer_id)
    if "Play" in button.status():
        # instruct to call handle_timer() every 10 msec:
        timer_id = plotter.timer_callback("create", dt=1000)
    button.switch() 



scene = Scene(atlas_name="allen_mouse_25um", title="OND-Visualization")
spikes, clusters, channels = loadData()

regionModels = []
for acro in list(set(clusters.acronym)):
    regionModels.append([acro, scene.add_brain_region(acro, alpha=0.5)])


start = 0
end = spikes.times[-1]
timer = 0
i = 0

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def animation_tick(event): 
    global regionModels
    global timer
    global end
    global i
    global text
    plotter.get_actors()[1].GetProperty().SetColor(1,1,1)
    if(timer < end):
        currentSpikes = []
        elemStillIn = True
        while(elemStillIn):
            if(i >= len(spikes.times)): break
            if(spikes.times[i] > timer and spikes.times[i] < timer + 1):
                currentSpikes.append(i)
            
            else:
                elemStillIn = False
            i += 1
        text_array[19].text("Total Spikes: " + str(len(currentSpikes)))
        #outputString = "Total Spikes: " + str(len(currentSpikes)) + "\n"
        #print(spikes.clusters.keys())
        for k in range(len(regionModels)):
            spikesInRegion = 0
            for j in currentSpikes:
                if(clusters.acronym[spikes.clusters[j]] == regionModels[k][0]):
                    spikesInRegion += 1
            #outputString += "Spikes in " + regionModels[k][0] + ": " + str(spikesInRegion) + "\n"
            plotter.get_actors()[k+2].GetProperty().SetOpacity(spikesInRegion * 0.001)
            color = hsv2rgb(k / len(regionModels), 1,1)
            color255 = (color[0]/255, color[1]/255, color[2]/255)
            
            
            text_array[18-k].text("Spikes in " + regionModels[k][0] + ": " + str(spikesInRegion))
            text_array[18-k].properties.SetColor(color255)
            plotter.get_actors()[k+2].GetProperty().SetColor(color)
            plotter.get_actors()[k+2].GetProperty().SetRepresentation(1)
            plotter.get_actors()[k]
            
            print(spikesInRegion)
            #regionModels[i][1].SetAlpha(spikesInRegion * 0.01)
        #outputString += "Time: " + str(timer)
        text_array[18-len(regionModels)].text("Time: " + str(timer))
        #text.text(outputString)
        timer += 1 
    global time_e  
    print(plotter.get_actors())
    #boop = plotter.get_actors()[2]
    #boop.SetVisibility(not boop.GetVisibility())
    time_e += 1
    plotter.render()


#Notes
#shorten time frame
#move time frame slowly
#try to divide brain region into smaller parts as "neurons"
#indicate current event (stimOn, response etc)
#fix linux problems (maybe), color problems, divByZero prob


time_e = 0
timer_id = -1
t0 = time.time()

plotter= Plotter()


button = plotter.add_button(button_play_pause, states=[" Play ","Pause"], size=40)
evntid = plotter.add_callback("timer", animation_tick, enable_picking=False)
#text = Text2D("Test")
#text.color("white")
#plotter.add(text)
plotter.roll(180)
plotter.background("grey0")
text_array = []
for l in range(20):
    text_t = Text2D(" ")
    text_t.pos((0.005,l*0.03+0.4295))
    text_array.append(text_t)
    plotter.add(text_t)
plotter.show( __doc__, scene.get_actors())