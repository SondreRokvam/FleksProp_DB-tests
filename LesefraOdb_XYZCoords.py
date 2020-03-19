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
print os.listdir(gofor)

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
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    for i in odb_names:
        print i
        odb = session.openOdb(name=odb_path+i)
        Measurementes = [nodeset.name for nodeset in odb.rootAssembly.nodeSets.values() if (nodeset.name.startswith('PROFILE-R'))]
        print(Measurementes)
        for profile in Measurementes:
            dots_XY_langs_Z = []
            dots_XY_langs_Zm =[]

            AllNodes = odb.rootAssembly.nodeSets[profile].nodes[0]
            Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region=odb.rootAssembly.nodeSets[profile]).values
            Disp = Disp.getSubset(

            )
            print len(Disp)
            del klil
            Acount= 0
            for nod in AllNodes:
                x = float(nod.coordinates[0])           #Initial position of node
                y = float(nod.coordinates[1])
                z = float(nod.coordinates[2])
                xm = float(Disp[Acount].data[0])        #Displacement of node
                ym= float(Disp[Acount].data[1])
                zm= float(Disp[Acount].data[2])
                Acount =Acount + 1  # Manual counter

                dots_XY_langs_Z.append([x, y , z ])

                dots_XY_langs_Zm.append([xm, ym,zm])


            #
            choordline=


            #Save for plotting
            np.savez(npz_path+'Cartesian view of '+profile+' for '+i[:-4],
                     profile_undeformed = np.array( dots_XY_langs_Z),
                     profile_deformed=np.array( dots_XY_langs_Zm) ,
                     profile__id=i)
        print('worked for '+i[:-4])
        odb.close()