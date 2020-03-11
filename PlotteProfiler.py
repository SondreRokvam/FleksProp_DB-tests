"""
Plot charts illustrationg deformation behaviour
Created on Wed Feb 19 02:36:36 2020

@author: Sondre
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import operator

def addcolum(li):
     #legg til rader 
     N=4
     cols=len(li[0])
     rows=len(li)
     Dots_data =  np.zeros((rows,cols+N))
     Dots_data[:,:-N] = li
     return Dots_data

def addrow(lo):
     N=1
     cols=len(lo[0])
     rows=len(lo)
     Dots_data =  np.zeros((rows+N,cols))
     Dots_data[:-N,:] = lo
     return Dots_data
     
def sortbyangle(dt):
     for i in range(0,len(dt)):
          dt[i][3]= dt[i][0]-np.average(dt[:,0])
          dt[i][4]= dt[i][2]-np.average(dt[:,2])
          
          ang = math.atan2(dt[i][4] , dt[i][3])
          dt[i][5]= ang
     dt =np.array(sorted(dt, key=operator.itemgetter(5)))
     dt= addrow(dt)  #Adds row to the array
     dt[-1]=dt[0]    #sets last row= first row for complete profile
     return dt

#ODB PATH
gitHub = 'C:/Users/sondreor/Documents/GitHub/FleksProp_DB-tests/'
Azp = 'C:/Users/sondreor/Desktop/Azp/'
odb_path = 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/2_Material-layup-check/0_InitialConstruct/'
"""
for g in os.listdir(Azp):
    odb_path = Azp
    odb_path =odb_path+g+'/'
    #NPZ PATH
"""
if True:
    npz_path=odb_path+'npz_files/'
            
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    npz_files = [f for f in os.listdir(npz_path) if (f.endswith('.npz'))]
    for i in odb_names:
        print( i)
        #Measurementes = [nodeset.name for nodeset in odb.rootAssembly.nodeSets.values() if (nodeset.name.startswith('PROFILE-R'))]
        #for profile in Measurementes:
    #Para   =  np.load(gitHub+'parameters_for_plot.npz')
    #print(Para.files)
    #Jobbs= ['Hollow_Thick', 'Hollow_Thin', 'Pressure_Thick', 'Pressure_Thin', 'Pressure_Thin-w-Ridge', 'Suction_Thick','Suction_Thin','Suction_Thin-w-Ridge','FEA One-by-one']
    Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9',
     'PROFILE-R_95']
    print (Measurementes)
    radius= 650
    Radi=Para['r_val']
    print (Radi)
    
    
    
    #Start plotting
    
    for i in range(0,len(Jobbs)-1):
         #Logging deltas
         delta_U=[]
         delta_A=[]
         delta_W=[]
         fig, axs = plt.subplots(2,6,figsize = (21,7))
         fig.suptitle('Simulation: '+Jobbs[i]+', Series: '+Jobbs[-1], fontsize=16)
         #fig, axs = plt.subplots(2,3,figsize = (14,8))
         axs[0, 0].set_ylabel('Propeller axis')
         for maal in range(0,len(Measurementes)):
              CylX   =  np.load('C:/temp/Profile_w '+Measurementes[maal]+Jobbs[i]+'_CylynderC_alongX.npz')
              CylX_m =  np.load('C:/temp/Profile_w '+Measurementes[maal]+Jobbs[i]+'_CylynderC_alongX_def.npz')
              dotCyl,dotCylm = CylX['arr_0'],CylX_m['arr_0']
              
              #Logging
              Centers= []
              Alphas= []
              Warping = []
              
              #Prepare for plotting                 """Plot Cylinder"""
              Plotting=[dotCyl,dotCylm]
              for plo in range(0,len(Plotting)):
                  Plotting[plo]= addcolum(Plotting[plo])
              for plo in range(0,len(Plotting)):
                   Plotting[plo]=sortbyangle(Plotting[plo])
              
              #Subplot title
              axs[0, maal].title.set_text(Measurementes[maal])
              #Plotting
              for plo in range(0,len(Plotting)):
                   #Plot profile
                   axs[0, maal].plot((Plotting[plo][:,0])*Radi[maal],Plotting[plo][:,2],'-')   
                   axs[0, maal].set_xlabel('Cylinder length')
                   
                   #Linear regression for chordline
                   m,y = np.polyfit(Plotting[plo][:,0]*Radi[maal],Plotting[plo][:,2],1)
                   
                   #2nd order regression for warp
                   a,b,c = np.polyfit(Plotting[plo][:,0]*Radi[maal],Plotting[plo][:,2],2)
                   #Lag X-axis for choordline
                   x= np.array([np.min(Plotting[plo][:,0]*Radi[maal])-0.1*abs(np.min(Plotting[plo][:,0]*Radi[maal])),np.max(Plotting[plo][:,0]*Radi[maal])+abs(0.1*np.min(Plotting[plo][:,0]*Radi[maal]))])
                   
                   
                   #Plot chordline
                   axs[0, maal].plot(x, m*x + y,'--') 
                   #axs[0, maal].plot(x, a*x**2 +b*x+c ,'--') 
                   #Save chordline angle
                   if m<0.0:
                        del koko
                   Alphas.append(math.atan2(m,1)*180/math.pi)
                   
                   Centers.append([np.average(Plotting[plo][:,0]),np.average(Plotting[plo][:,1])])
                   Warping.append(a)
              #Find angle change
              deltaDeflec= ((Centers[1][0]-Centers[0][0])**2+(Centers[1][1]-Centers[0][1])**2)**0.5
              deltaAlfa= Alphas[1]-Alphas[0]
              deltaWarp= Warping[1]-Warping[0]
              delta_U.append(deltaDeflec)
              delta_A.append(deltaAlfa)
              delta_W.append(deltaWarp)
         
         #Print data for dette designet
         print('\n\n', Jobbs[i],'\n')
         for maal in range(0,6):
             print('deltaDeflection \t',Measurementes[maal],'\t = ', delta_U[maal])
         for maal in range(0,6):
             print('deltaAlpha     \t',Measurementes[maal],'\t = ', delta_A[maal])
         for maal in range(0,6):
             print('deltaWarp      \t',Measurementes[maal],'\t = ', delta_W[maal])
             
         ploo=[delta_U,delta_A,delta_W]
         pli= ['deltaDeflection','deltaAlpha','deltaWarp']
         for plo in range(0,3):
              #Plot profile
              axs[1, plo].plot(Radi,ploo[plo])  
              axs[1, plo].set_xlabel('Radius length')
              axs[1, plo].set_ylabel(pli[plo])
              
              