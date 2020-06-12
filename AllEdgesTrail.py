# AzP65C - coordinates
if 1: #AzP lead/trail punkter
    Leadnodes=[[88.140249,-198.797325,257.108194],
               [72.609588,-231.798489,272.168533],
               [57.111528,-267.042178,284.233135],
               [41.653526,-304.398309,292.998156],
               [26.214503,-343.738199,298.109126],
               [10.324939,-385.480371,298.431121],
               [-6.368028,-429.953069,292.472833],
               [-24.538908,-477.645768,277.688261],
               [-76.464772,-587.88261,188.945196],
               [-46.696491,-530.173661,247.266837]]
    Trailnodes=[[-282.872286,-322.146479,-42.972622],
               [-289.21762,-352.204216,-61.306121],
               [-291.328316,-382.15225,-77.843804],
               [-290.203022,-412.236773,-92.558592],
               [-286.225663,-442.58725,-105.553427],
               [-279.586559,-473.282009,-116.877673],
               [-270.14662,-504.497972,-126.022999],
               [-206.038365,-610.488496,-92.790333],
               [-256.404372,-536.900446,-130.361654],
               [-236.240842,-571.887303,-123.166197]]



from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math
import time

#Reset Abaqus, find Githhub
Mdb()
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'#brukes denne?

Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\AzP_Particular'       # Overmappe for testmapper

# Os walk to get inp and odb overviews

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
    for gofor in Inp_folders[:]:
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
        for i in odb_names[:]:
            measures = []
            Mdb()
            print '\n              Attepting extraction from: ', odb_path + '\\' + i
            odb = session.openOdb(name=odb_path + '\\' + i)
            #prifs= []
            #for a in range(0,len(odb.rootAssembly.nodeSets.items())):
            #    if 'profile' in odb.rootAssembly.nodeSets.items()[a][1].name.lower():
            #        prifs.append(odb.rootAssembly.nodeSets.items()[a][1].name)
            #prifs.sort()
            prifs = ['PROFILE-R_5', 'PROFILE-R_55', 'PROFILE-R_6', 'PROFILE-R_65', 'PROFILE-R_7', 'PROFILE-R_75', 'PROFILE-R_8', 'PROFILE-R_85', 'PROFILE-R_9', 'PROFILE-R_95']
            #    print 'adsasdas', i
            #Measurementnames = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
            nodplace = odb.rootAssembly

            for profile in prifs[:]:
                print profile
                dots_cyl_langs_x = []
                dots_cyl_langs_xm = []

                AllNodes = nodplace.nodeSets[profile].nodes[0]


                Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                    region=nodplace.nodeSets[profile]).values

                find_dis_trail_nodes = []
                find_dis_lead_nodes = []

                Acount = 0
                for nod in AllNodes:
                    x = float(nod.coordinates[0])  # Initial position of node
                    y = float(nod.coordinates[1])
                    z = float(nod.coordinates[2])
                    xm = float(Disp[Acount].data[0])  # Displacement of node
                    ym = float(Disp[Acount].data[1])
                    zm = float(Disp[Acount].data[2])

                    # measure coordline nodes
                    trailpoint = Trailnodes[prifs.index(profile)]
                    leadpoint = Leadnodes[prifs.index(profile)]
                    find_dis_trail_nodes.append(
                        round(math.sqrt((x - trailpoint[0]) ** 2 + (y - trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2),
                              8))
                    find_dis_lead_nodes.append(
                        round(math.sqrt((x - leadpoint[0]) ** 2 + (y - leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2),
                              8))

                    Acount = Acount + 1  # Manual counter

                    # Find angular value due to cylinder coordinates
                    ang = math.atan2(y, z) + math.pi
                    angm = math.atan2((y + ym), (z + zm)) + math.pi
                    AvgRad = ((((y) ** 2 + (z) ** 2) ** 0.5) * (((y + ym) ** 2 + (z + zm) ** 2) ** 0.5)) / 2.0
                    #                        Cylinder height   Angle width *Radius                      Radius
                    dots_cyl_langs_x.append([x, ang * ((y) ** 2 + (z) ** 2) ** 0.5, ((y) ** 2 + (z) ** 2) ** 0.5])
                    dots_cyl_langs_xm.append([x + xm, angm * ((y + ym) ** 2 + (z + zm) ** 2) ** 0.5, ((y + ym) ** 2 + (z + zm) ** 2) ** 0.5])

                # Identify coordline nodes
                minTrail_dist = np.min(find_dis_trail_nodes)
                minLead_dist = np.min(find_dis_lead_nodes)
                index_minTrail = find_dis_trail_nodes.index(minTrail_dist)
                index_minLead = find_dis_lead_nodes.index(minLead_dist)

                undefCoordline = [dots_cyl_langs_x[index_minTrail], dots_cyl_langs_x[index_minLead]]
                defCoordline = [dots_cyl_langs_xm[index_minTrail], dots_cyl_langs_xm[index_minLead]]

                # Save for plotting
                np.savez(npz_path + '\\Cylinder view of ' + profile + ' for ' + i[:-4],
                         profile_undeformed=np.array(dots_cyl_langs_x),
                         profile_deformed=np.array(dots_cyl_langs_xm),
                         profile_undefcoordline=undefCoordline,
                         profile_defcoordline=defCoordline)
            print  '              Worked for :        ' + i[:-4] + '        in :        ', gofor, '\n\n'
            odb.close()
