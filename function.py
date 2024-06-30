import colorsys
from vedo import Text2D
from vedo import Plotter
from brainbox.io.one import SpikeSortingLoader
def concat(on,off):
    onIndex=0
    offIndex=0
    counter=0
    stim=[]
    while(True):
        if(onIndex==len(on) and offIndex==len(off)):
            break
        else:
            if(counter%2==0):
                stim.append(on[onIndex])
                onIndex+=1
            else:
                stim.append(off[offIndex])
                offIndex+=1
            
        counter+=1
    return stim
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def createText(plotter):
    text_array = []
    for l in range(20):
        text_t = Text2D(" ")
        text_t.pos((0.005,l*0.03+0.4295))
        text_array.append(text_t)
        plotter.add(text_t)
    return plotter,text_array


def getRegionModel(clusters, scene):
    regionModels = []
    for acro in list(set(clusters.acronym)):
        regionModels.append([acro, scene.add_brain_region(acro, alpha=0.5)])
    return regionModels

