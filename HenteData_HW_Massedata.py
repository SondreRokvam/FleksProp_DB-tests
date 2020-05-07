from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math

# Hw choordline punkts posisjon for tracing leading and trailing edge
if 1:  # Hw punkter
    Leadnodes = [[-921.988E-03, -188.362272, 250.],# r = 0.5
                 [-3.708949, -217.378003, 300.],
                 [-5.258573, -225.280987, 350.],# r = 0.7
                 [-4.852153, -202.093218, 400.],
                 [-1.732931, -130.598882, 450.]] # r = 0.9

    Trailnodes = [[-8.408669, 121.885101, 250.],
                  [-7.139085, 140.092972, 300.],
                  [-3.541321, 162.555817, 350.],
                  [3.404349, 191.702759, 400.],
                  [15.057261, 225.33374, 450.]]
Mdb()

# ODB PATH
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
HW = 'D:/PhD/Simuleringer/HW/'
gofor = HW


#stuff = [f for f in os.listdir(gofor) if not (f.endswith('.bat'))]
#Os walk to get files, roots and
Inp_folders = []
INPfilS = []
ODBfilS = []
for root, dirs, files in os.walk(gofor, topdown=False):
     for name in dirs:
          name = os.path.join(root, name)
          inp_files = [a for a in os.listdir(name) if a.endswith('.inp')]
          Odb_files = [a for a in os.listdir(name) if a.endswith('.odb')]
          if len(inp_files)>0:
              Inp_folders.append(name)
              INPfilS.append(inp_files)
              ODBfilS.append(Odb_files)
#Inp_folders = np.array(Inp_folders)
stuff = Inp_folders
fuckedlist = []
for gofor in stuff:  # for many folders
    print gofor
    odb_path = gofor

    # NPZ PATH
    npz_path = odb_path + '\\npz_files'
    try:
        os.mkdir(npz_path)  # Create target Directory
        print("Directory ", npz_path, " Created ")
    except:
        print("Directory ", npz_path, " already exists")

    # Hent resultatfiler
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]

    for i in odb_names:
        try:
            print
            'Extracting from: ', i
            odb = session.openOdb(name=odb_path + '/' + i)
            # Measurementes = [nodeset.name for nodeset in odb.rootAssembly.nodeSets.values() if (nodeset.name.startswith('PROFILE-R'))]
            Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
            print
            'Extracting at: ', Measurementes
            for profile in Measurementes:
                dots_XY_langs_Z = []
                dots_XY_langs_Zm = []

                AllNodes = odb.rootAssembly.nodeSets[profile].nodes[0]
                Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                    region=odb.rootAssembly.nodeSets[profile]).values

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

                    dots_XY_langs_Z.append([x, y, z])
                    dots_XY_langs_Zm.append([x + xm, y + ym, z + zm])

                    # measure coordline nodes
                    trailpoint = Trailnodes[Measurementes.index(profile)]
                    leadpoint = Leadnodes[Measurementes.index(profile)]
                    find_dis_trail_nodes.append(
                        round(math.sqrt((x - trailpoint[0]) ** 2 + (y - trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2),
                              5))
                    find_dis_lead_nodes.append(
                        round(math.sqrt((x - leadpoint[0]) ** 2 + (y - leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2),
                              5))

                    Acount = Acount + 1  # Manual counter

                # Identify coordline nodes
                minTrail_dist = np.min(find_dis_trail_nodes)
                minLead_dist = np.min(find_dis_lead_nodes)
                index_minTrail = find_dis_trail_nodes.index(minTrail_dist)
                index_minLead = find_dis_lead_nodes.index(minLead_dist)

                undefCoordline = [dots_XY_langs_Z[index_minTrail], dots_XY_langs_Z[index_minLead]]
                defCoordline = [dots_XY_langs_Zm[index_minTrail], dots_XY_langs_Zm[index_minLead]]

                # Save for plotting
                np.savez(npz_path + 'Cartesian view of ' + profile + ' for ' + i[:-4],
                         profile_undeformed=np.array(dots_XY_langs_Z),
                         profile_deformed=np.array(dots_XY_langs_Zm),
                         profile_undefcoordline=undefCoordline,
                         profile_defcoordline=defCoordline)
            print('worked for\t' + i[:-4] + '\tin :\t',gofor)
            odb.close()
        except:
            print(i,'\tin :\t',gofor, '\tdidnt work')
            fuckedlist.append(gofor+'\\'+i)
            pass
print fuckedlist