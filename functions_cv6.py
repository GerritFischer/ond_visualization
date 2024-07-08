#! pip install ONE-api
#! pip install ibllib
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import functions from the brainbox package for spike sorting and peri-event time histograms (PETHs)
from brainbox.io.one import SpikeSortingLoader
from brainbox.plot import peri_event_time_histogram
from brainbox.singlecell import calculate_peths

from pprint import pprint # function for pretty printing

# Import the ONE (Open Neurophysiology Environment) class from the ONE API package
from one.api import ONE
from iblatlas.atlas import AllenAtlas

# Create an instance of the ONE class, specifying the base URL of the server and a password for authentication
one = ONE(base_url='https://openalyx.internationalbrainlab.org', password='international', silent=True)
ba = AllenAtlas()


class Session:
    #takes in session as well as PIDs and EIDs if possible, creates spikes and clusters on its own
    spikes = None                                   
    def __init__(self, session, pid = None, eid=None, PrintOn = False):
        self.sess = session
        self.sessEID = eid
        self.sessEIDInfo = self.getEIDinfo()
        self.sessPID = pid
        self.PrintOn = PrintOn
        self.cluster = self.getClusterAndSpikesOfSess()
        self.trials = one.load_object(self.sessEID,"trials")
        
    #method of the class that has the function of being activated when a class object is created and updates the attributes in the class object itself with the data of the choosen session    
    def getClusterAndSpikesOfSess(self):
        if (self.sessPID == None):
            return None
        else:
            sl = SpikeSortingLoader(pid=self.sessPID, one=one, atlas=ba) # create instance of the SpikeSortingLoader
            spikes, clusters, channels = sl.load_spike_sorting() # load in spike sorted data
            cluster = sl.merge_clusters(spikes, clusters, channels) # merge cluster metrics
            if(self.PrintOn):
                print(f"Number of Spikes is {(len(spikes['clusters']))}")
                print(f"Number of Clusters is {len(clusters['channels'])}")
            self.spikes = spikes
            return cluster
               
    def getEIDinfo(self):
        eidInfo = one.alyx.rest('sessions', 'list', id = self.sessEID)
        return eidInfo[0]
    
    def getMainInfo(self):
        return [self.sessEID, self.sessPID, self.sessEIDInfo["subject"], self.sessEIDInfo["lab"]]
        #return list with sessionInfo  = [unknown EID, PID, subject, lab]


    #trials getten für response times und so co_cue times und so mit contrast left rights
    #in klasse noch als method umimplementieren (einfach paar wörter wechseln und umverlegen)
    def getLineGraph(self, events1, Roi, figsize1 =(7,7), t_before1 = 0.2, t_after1 = 0.5, bin_size1= 0.025, smoothing1=0.025, as_rate1 = True, include_raster1=False, 
                            n_raster1= None, error_bars1='std', pethline_kwargs1 = {'color': 'blue', 'lw': 2}, errbar_kwargs1 = {'color': 'blue', 'alpha': 0.5}, 
                            eventline_kwargs1={'color': 'black', 'alpha': 0.5}, raster_kwargs1={'color': 'black', 'lw': 0.5}, xlab ="", ylab = "", pidnmb = 1):
        if(self.cluster != None):
            acronym = self.cluster["acronym"]
            ROI_neurons = [i for i, acronym in enumerate(self.cluster['acronym']) if Roi in acronym]
            trials = self.trials
            f, ax1 = plt.subplots(1, 1, figsize= figsize1)
            peri_event_time_histogram(spike_times = self.spikes.times, spike_clusters= self.spikes.clusters, events= trials[events1],
                                    cluster_id= ROI_neurons[pidnmb],  #ehemals ROI Neurons gibt einfach eine einzige Cluster ID an such dir die mal raus 
                                    t_before = t_before1, t_after=t_after1, bin_size= bin_size1, smoothing= smoothing1, as_rate=as_rate1,
                                    include_raster=include_raster1,n_rasters= n_raster1, error_bars = error_bars1, ax=ax1, #ax2 is a weird thing, understand it 
                                    pethline_kwargs=pethline_kwargs1,
                                    errbar_kwargs=errbar_kwargs1,
                                    eventline_kwargs=eventline_kwargs1,
                                    raster_kwargs=raster_kwargs1)
            ax1.set(ylabel=ylab, xlabel=xlab)
            plt.tight_layout() # maybe lieber return 
        else:
            Exception("No spikes and cluster there to create a Graph")
        



#takes in parameter and returns object of session probably takes longer when also inputtinga brain region
def createSess(Roi = "", pid = "", POn = False, sessNmb= 0, EID = "",lab ="", nmb = "", proj ="",starTime = "", subj="", taskProt = "" ):   #session search parameter
    if (Roi == "")and(pid == ""):         #case for no roi
        ses1 = one.alyx.rest('sessions', 'list', id = EID, lab = lab, number = nmb, projects = proj, start_time = starTime, subject=subj, task_protocol=taskProt )
        if POn:
                print(f'Found {len(ses1)} Sessions')   #print if POn = True
        if (sessNmb > len(ses1)):
            raise Exception("The number of your choosing is bigger than the found sessions") #error check for bad unmatiching parameter
        else:
                ses11 = ses1[sessNmb]       #continue if sessNmb is fine    
                EID = ses11["id"]           #this 3 lines take 1 session, takes the EID and tries to find the PID with it
                PID = one.eid2pid(EID)[0]
                
                if (len(PID) == 0):
                    print("No PIDs found for this session ID, return Session object without it and without clsuters/spikes")    #PID is empty, so there is no PID
                    sessionwithoutPID = Session(ses11,eid = EID)
                    return sessionwithoutPID
                
                else:
                    sess11 = one.alyx.rest('insertions', 'list', id = PID[0])[0]    #PID found create session with PID
                    sessionwithPID = Session(sess11,PrintOn=POn, eid=EID)
                    return sessionwithPID
    else:
        finalPIDs = []                  #case if roi is searched
        ses2 = one.alyx.rest('insertions', 'list',atlas_acronym = Roi, id=pid)
        for i in ses2:
            if (EID != "")and(i["session_info"]["id"] != EID): continue
            if (lab != "")and(i["session_info"]["lab"] != lab): continue
            if (nmb != "")and(i["session_info"]["number"]!=nmb):continue
            if (subj != "")and(i["session_info"]["subject"] != subj):continue
            if (starTime != "")and (i["session_info"]["start_time"]!=starTime):continue
            if(taskProt != "")and(i["session_info"]["task_protocol"]==taskProt):continue
            finalPIDs.append(i)
        ses2 = finalPIDs[sessNmb]
        ses2EID = ses2["session_info"]
        EID = ses2EID["id"]
        session2 =Session(ses2,PrintOn=POn, pid=ses2["id"], eid=EID)
        return session2


#takes in cluster and returns cluster cords its not part of the class so that it can be used even if not using the Library object class
def getClusterPos(clusters):          
    clusterCords = []
    for clus in range(0,len(clusters["channels"])):
        tup = (clusters.x[clus],clusters.y[clus], clusters.z[clus])
        clusterCords.append(tup)
    return clusterCords
        

def pidsofSessions(roi = ""):
    ses = one.alyx.rest('insertions', 'list', atlas_acronym = roi)
    pids = [i['id'] for i in ses]
    return pids


