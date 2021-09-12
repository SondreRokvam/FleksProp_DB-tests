# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 14:40:07 2021

@author: Sondre
"""
#LEnodes
LE_nod=[]
TE_nod=[]
for line in range(400,1050,50):
     LE_nod.append([0.,-float(line)/1000,0.])
     TE_nod.append([0.98296,-float(line)/1000,0.])

from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math
import time
#Reset Abaqus, find Githhub
Mdb()
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\NACA0009\\'

# Os walk to get files, roots and
Inp_folders, inps = [], 0
INPfilS, ODBfilS = [], []
for root, dirs, files in os.walk(Source, topdown=False):
    for name in dirs:
        name = os.path.join(root, name)
        inp_files = [a for a in os.listdir(name) if a.endswith('.inp')]
        Odb_files = [a for a in os.listdir(name) if a.endswith('.odb')]
        if len(inp_files) > 0:
            Inp_folders.append(name.split('\n'))
            INPfilS.append(inp_files)
            inps = inps + len(inp_files)
            ODBfilS.append(Odb_files)
# Re
fuckedlist = []
for sets in INPfilS:
    odbss=ODBfilS[INPfilS.index(sets)]
    fold = Inp_folders[INPfilS.index(sets)]
    for sims in sets:
        if sims[:-4]+'.odb' not in odbss:
            fuckedlist.append([fold, sims])
print len(fuckedlist), ' unrun sims _in_ ',inps, ' sims and ', len(Inp_folders), '  sets'

if (inps-len(fuckedlist))>0:
    for gofor in Inp_folders:
        # Give odb_path
        odb_path = gofor[0]
        # create NPZ PATH
        npz_path = odb_path + '\\npz_files'
        try:
            os.mkdir(npz_path)  # Create target Directory
            #print("Directory ", npz_path, " Created ")
        except:
            #print("Directory ", npz_path, " already exists")
            pass

        # Hent resultatfiler i mappen
        odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb') and not "1000" in f.lower())]
        for i in odb_names:
             Mdb()

             odb = session.openOdb(name=odb_path + '\\' + i)
             Measurementnames= ['PROFILE-R_4', 'PROFILE-R_45',
                                   'PROFILE-R_5', 'PROFILE-R_55',
                                   'PROFILE-R_6', 'PROFILE-R_65',
                                   'PROFILE-R_7', 'PROFILE-R_75',
                                   'PROFILE-R_8', 'PROFILE-R_85',
                                   'PROFILE-R_9', 'PROFILE-R_95','PROFILE-R1']
             
             nodplace =odb.rootAssembly
             for profile in Measurementnames:
                    #print profile
                    dots_XY_langs_Z = []
                    dots_XY_langs_Zm = []
                    AllNodes= []
                    for nodes in nodplace.nodeSets[profile].nodes:
#                         print nodes
                         for node in nodes:
                              AllNodes.append(node)
                    Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                        region=nodplace.nodeSets[profile]).values
#                    print AllNodes
                    find_dis_trail_nodes = []
                    find_dis_lead_nodes = []

                    Acount= 0
                    for nod in AllNodes:
                
                        x = float(nod.coordinates[0])           #Initial position of node
                        y = float(nod.coordinates[1])
                        z = float(nod.coordinates[2])
                        xm = float(Disp[Acount].data[0])        #Displacement of node
                        ym= float(Disp[Acount].data[1])
                        zm= float(Disp[Acount].data[2])

                        dots_XY_langs_Z.append([x, y, z])
                        dots_XY_langs_Zm.append([x + xm, y + ym, z + zm])

                        # measure coordline nodes
                        trailpoint = TE_nod[Measurementnames.index(profile)]
                        leadpoint = LE_nod[Measurementnames.index(profile)]
                        find_dis_trail_nodes.append(round(math.sqrt((x - trailpoint[0]) ** 2 + (y - trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2),
                                  5))
                        find_dis_lead_nodes.append(
                            round(math.sqrt((x - leadpoint[0]) ** 2 + (y - leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2),
                                  5))

                        Acount = Acount + 1  # Manual counter

                    minTrail_dist = np.min(find_dis_trail_nodes)
                    minLead_dist = np.min(find_dis_lead_nodes)
                    index_minTrail = find_dis_trail_nodes.index(minTrail_dist)
                    index_minLead = find_dis_lead_nodes.index(minLead_dist)

                    undefCoordline = [dots_XY_langs_Z[index_minTrail], dots_XY_langs_Z[index_minLead]]
                    defCoordline = [dots_XY_langs_Zm[index_minTrail], dots_XY_langs_Zm[index_minLead]]
                    print(undefCoordline)
                    # Save for plotting
                    np.savez(npz_path + '\\Cartesian view of ' + Measurementnames[Measurementnames.index(profile)] + ' for ' + i[:-4],
                        profile_undeformed=np.array(dots_XY_langs_Z),
                        profile_deformed=np.array(dots_XY_langs_Zm),
                        profile_undefcoordline=undefCoordline,
                        profile_defcoordline=defCoordline)
                    
             print    '              Worked for :        ' + i[:-4] + '        in :        ', gofor, '\n\n'
             odb.close()

