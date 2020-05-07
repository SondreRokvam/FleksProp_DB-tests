from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import os
import math
Mdb()
# Hw chordline points
if 1:
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
#Directories
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'

Source = 'C:/Users/Sondre/Desktop/Single_Simulations/CFD-Dyn-Static_Tests'
Source = 'C:/Users/Sondre/Desktop/Single_Simulations/Shell-vs-Solid_Tests'
Source = 'C:/Users/Sondre/Desktop/Single_Simulations/Mecanical aspects'

gofor =  [b for b in os.listdir(Source) if 'HW' and not '.' in b]
print('filer',gofor)

# Hw choordline data



#Find ODB

for g in gofor: #for many folders

    odb_path =Source+'/'+g+'/' #for many folders
    npz_path=odb_path+'npz_files/'

    # Create npz Directory
    if 1:   # Create  Directory
        try:
            os.mkdir(npz_path)
            print("Directory ", npz_path, " Created ")
        except:
            print("Directory ", npz_path, " already exists")

    # Hent resultatfiler
    odb_names = [f for f in os.listdir(odb_path) if f.endswith('.odb') and 'HW' in f]
    print(odb_names)
    for i in odb_names:
        #try:
        print 'Extracting from: ', i
        odb = session.openOdb(name=odb_path+i)

        #Specify where to find sets
        Setnames = [nodeset.name for nodeset in odb.rootAssembly.instances['HYDROWINGTOPLEADING-1-1'].nodeSets.values() if ('R' in nodeset.name)]
        print(Setnames)
        del SJekker
        Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
        print 'Extracting at: ', Measurementes
        for profile in Measurementes:
                dots_XY_langs_Z = []
                dots_XY_langs_Zm =[]

                # AllNodes = odb.rootAssembly.nodeSets[Setnames[Measurementes.index(profile)]].nodes[0]
                AllNodes = odb.rootAssembly.instances['HYDROWINGTOPLEADING-1-1'].nodeSets[
                    Setnames[Measurementes.index(profile)]].nodes
                print(odb.steps.items())
                Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                    region=odb.rootAssembly.instances['HYDROWINGTOPLEADING-1-1'].nodeSets[
                        Setnames[Measurementes.index(profile)]]).values

                find_dis_trail_nodes = []
                find_dis_lead_nodes = []

                Acount= 0
                for nod in AllNodes:
                    x = float(nod.coordinates[0])           #Initial position of node
                    y = -float(nod.coordinates[1])
                    z = float(nod.coordinates[2])
                    xm = float(Disp[Acount].data[0])        #Displacement of node
                    ym= -float(Disp[Acount].data[1])
                    zm= float(Disp[Acount].data[2])

                    dots_XY_langs_Z.append([x, y , z ])
                    dots_XY_langs_Zm.append([x+xm, y+ym,z+zm])


                    #measure coordline nodes
                    trailpoint=Trailnodes[Measurementes.index(profile)]
                    leadpoint=Leadnodes[Measurementes.index(profile)]
                    find_dis_trail_nodes.append(round(math.sqrt( (x - trailpoint[0]) ** 2 + (y + trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2),5))
                    find_dis_lead_nodes.append(round(math.sqrt((x - leadpoint[0]) ** 2 + (y + leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2),5))

                    Acount =Acount + 1  # Manual counter


                #Identify coordline nodes
                minTrail_dist = np.min(find_dis_trail_nodes)
                minLead_dist = np.min(find_dis_lead_nodes)
                index_minTrail=find_dis_trail_nodes.index(minTrail_dist)
                index_minLead=find_dis_lead_nodes.index(minLead_dist)

                undefCoordline = [dots_XY_langs_Z[index_minTrail], dots_XY_langs_Z[index_minLead]]
                defCoordline = [dots_XY_langs_Zm[index_minTrail], dots_XY_langs_Zm[index_minLead]]



                #Save for plotting
                np.savez(npz_path+'Cartesian view of '+profile+' for '+i[:-4],
                         profile_undeformed = np.array( dots_XY_langs_Z),
                         profile_deformed=np.array( dots_XY_langs_Zm) ,
                         profile_undefcoordline=undefCoordline,
                         profile_defcoordline=defCoordline)
        print('worked for ' + i[:-4])
        odb.close()
        # except:
        # print(i, 'didnt work')
        # pass