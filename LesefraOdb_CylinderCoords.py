from abaqus import *
from abaqusConstants import *
from odbAccess import *
import numpy as np
import math
#ODB PATH
gitHub = 'C:/Users/sondreor/Documents/GitHub/FleksProp_DB-tests/'
Azp = 'C:/Users/sondreor/Desktop/Azp/'
odb_path = 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/2_Material-layup-check/0_InitialConstruct/'
for g in os.listdir(Azp):
    odb_path = Azp
    odb_path =odb_path+g+'/'
    #NPZ PATH
    npz_path=odb_path+'npz_files/'
        
    try:
        os.mkdir(npz_path) # Create target Directory
        print("Directory " , npz_path ,  " Created ") 
    except FileExistsError:
        print("Directory " , npz_path ,  " already exists")
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    for i in odb_names:
        print i
        odb = session.openOdb(name=odb_path+i)
        Measurementes = [nodeset.name for nodeset in odb.rootAssembly.nodeSets.values() if (nodeset.name.startswith('PROFILE-R'))]
        for profile in Measurementes:
            dots_cyl_langs_x = []
            dots_cyl_langs_xm =[]
    
            AllNodes = odb.rootAssembly.nodeSets[profile].nodes[0]
            Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region=odb.rootAssembly.nodeSets[profile]).values
    
            Acount= 0
            for nod in AllNodes:
                x = float(nod.coordinates[0])           #Initial position of node
                y = float(nod.coordinates[1])
                z = float(nod.coordinates[2])
                xm = float(Disp[Acount].data[0])        #Displacement of node
                ym= float(Disp[Acount].data[1])
                zm= float(Disp[Acount].data[2])
                Acount =Acount + 1  # Manual counter
    
                #Find angular value
                ang = math.atan2(y , z)
                angm = math.atan2((y+ym) , (z+zm))
    
                #                        Angle        radius        Cylinder height
                dots_cyl_langs_x.append([ang, ((y) ** 2 + (z) ** 2) ** 0.5, x ])
    
                dots_cyl_langs_xm.append([angm, ((y+ym)**2+(z+zm)**2)**0.5, x+xm])
    
            #Save for plotting
            np.savez(npz_path+'Cylinder view of '+profile+' for '+i[:-4],
                     profile_undeformed = np.array( dots_cyl_langs_x),
                     profile_deformed=np.array( dots_cyl_langs_xm) ,
                     profile__id=i)
        print('worked for '+i[:-4])
        odb.close()