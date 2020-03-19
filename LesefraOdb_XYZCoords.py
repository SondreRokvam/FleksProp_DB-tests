from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math
Mdb()
#ODB PATH
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
HW = 'C:/Users/Sondre/Desktop/HW/'
gofor = HW
# Hw choordline
if 1:  # Hw
    Leadnodes = [[-921.988E-03, -188.362272, 250.],
                 [-3.708949, -217.378003, 300.],
                 [-5.258573, -225.280987, 350.],
                 [-4.852153, -202.093218, 400.],
                 [-1.732931, -130.598882, 450.]]

    Trailnodes = [[-8.408669, 121.885101, 250.],
                  [-7.139085, 140.092972, 300.],
                  [-3.541321, 162.555817, 350.],
                  [3.404349, 191.702759, 400.],
                  [15.057261, 225.33374, 450.]]

for g in os.listdir(gofor): #for many folders
    odb_path = gofor
    odb_path =odb_path+g+'/' #for many folders
    
    #NPZ PATH
    npz_path=odb_path+'npz_files/'
    try:
        os.mkdir(npz_path)  # Create target Directory
        print("Directory ", npz_path, " Created ")
    except:
        print("Directory ", npz_path, " already exists")

    # Hent resultatfiler
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]

    for i in odb_names:
        print 'Extracting from: ', i
        odb = session.openOdb(name=odb_path+i)
        Measurementes = [nodeset.name for nodeset in odb.rootAssembly.nodeSets.values() if (nodeset.name.startswith('PROFILE-R'))]
        print('Extracting at: ',Measurementes)

        for profile in Measurementes:
            dots_XY_langs_Z = []
            dots_XY_langs_Zm =[]

            AllNodes = odb.rootAssembly.nodeSets[profile].nodes[0]
            Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region=odb.rootAssembly.nodeSets[profile]).values


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
                trailpoint=Trailnodes[Measurementes.index(profile)]
                leadpoint=Leadnodes[Measurementes.index(profile)]
                find_dis_trail_nodes.append(round(math.sqrt( (x - trailpoint[0]) ** 2 + (y - trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2),5))
                find_dis_lead_nodes.append(round(math.sqrt((x - leadpoint[0]) ** 2 + (y - leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2),5))

                Acount =Acount + 1  # Manual counter
                dots_XY_langs_Z.append([x, y , z ])

                dots_XY_langs_Zm.append([xm, ym,zm])
            minTrail_dist = np.min(find_dis_trail_nodes)
            minLead_dist = np.min(find_dis_lead_nodes)
            index_minTrail=find_dis_trail_nodes.index(minTrail_dist)
            index_minLead=find_dis_lead_nodes.index(minLead_dist)

            print index_minLead

            undefCoordline = [dots_XY_langs_Z[index_minTrail], dots_XY_langs_Z[index_minLead]]
            defCoordline = [dots_XY_langs_Zm[index_minTrail], dots_XY_langs_Zm[index_minLead]]



            #Save for plotting
            np.savez(npz_path+'Cartesian view of '+profile+' for '+i[:-4],
                     profile_undeformed = np.array( dots_XY_langs_Z),
                     profile_deformed=np.array( dots_XY_langs_Zm) ,
                     profile_undefcoordline=undefCoordline,
                     profile_defcoordline=defCoordline)
        print('worked for '+i[:-4])
        odb.close()