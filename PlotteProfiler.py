"""
Plot charts illustrationg deformation behaviour
Created on Wed Feb 19 02:36:36 2020

@author: Sondre
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import operator
import os

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
ini_path = 'C:/Users/sondreor/Dropbox/!PhD!/Propeller Design and Production/LargeScale/2_Material-layup-check/0_InitialConstruct/'
gofor = Azp
for g in os.listdir(gofor): #for many folders
    #for g in [gofor]:
    odb_path = gofor
    odb_path =odb_path+g+'/' #for many folders
    print(odb_path)
    #NPZ PATH
    npz_path=odb_path+'npz_files/' 
           
    #Plot_Paths
    plot_path= odb_path+'plots/'
    try:
        os.mkdir(plot_path) # Create target Directory
        print("Directory " , plot_path ,  " Created ") 
    except:
        print("Directory " , plot_path ,  " already exists")
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    npz_files = [f for f in os.listdir(npz_path) if (f.endswith('.npz'))]
    Para   =  np.load(gitHub+'parameters_for_plot.npz')
    print(Para.files)
    Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
    print (Measurementes)
    radius= 650
    Radi=Para['r_val']
    print (Radi)
    
    #Start plotting
    
    for i in range(0,len(odb_names)):
        #Logging deltas
        delta_U=[]
        delta_A=[]
        delta_W=[]
        fig, axs = plt.subplots(2,5,figsize = (22,10))
        
        fig.suptitle('Simulation: '+odb_names[i]+', Series: '+g, fontsize=16)
        axs[0, 0].set_ylabel('Propeller axis')
        for maal in range(0,len(Measurementes)):
            CylX   =  np.load(npz_path+'Cylinder view of '+Measurementes[maal]+' for '+odb_names[i][:-4]+'.npz')
            dotCyl,dotCylm = CylX['profile_undeformed'],CylX['profile_deformed']
            
            #Logging
            Centers= []
            Alphas= []
            Warping = []
            
            #Prepare for plotting                 #Plot Cylinder
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
                axs[0, maal].plot((Plotting[plo][:,0])*Radi[maal]*radius,Plotting[plo][:,2],'x')   
                axs[0, maal].set_xlabel('Cylinder length')
                   
                #Linear regression for chordline
                m,y = np.polyfit(Plotting[plo][:,0]*Radi[maal]*radius,Plotting[plo][:,2],1)
                   
                #2nd order regression for warp
                a,b,c = np.polyfit(Plotting[plo][:,0]*Radi[maal]*radius,Plotting[plo][:,2],2)
                #Lag X-axis for choordline
                x= np.array([np.min(Plotting[plo][:,0]*Radi[maal])*radius-0.1*abs(np.min(Plotting[plo][:,0]*Radi[maal]*radius)),np.max(Plotting[plo][:,0]*Radi[maal]*radius)+abs(0.1*np.min(Plotting[plo][:,0]*Radi[maal]*radius))])
                   
                   
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
        print('\n\n', odb_names[i],'\n')
        for maal in range(0,5):
            print('deltaDeflection \t',Measurementes[maal],'\t = ', delta_U[maal])
        for maal in range(0,5):
            print('deltaAlpha     \t',Measurementes[maal],'\t = ', delta_A[maal])
        for maal in range(0,5  ):
            print('deltaWarp      \t',Measurementes[maal],'\t = ', delta_W[maal])
            
        ploo=[delta_U,delta_A,delta_W]
        pli= ['delta_Deflection of center','delta_Alpha of coordline','delta_Warp of propeller faces']
        for plo in range(0,3):
            #Plot profile
            axs[1, plo].plot(Radi,ploo[plo])  
            axs[1, plo].set_xlabel('Radius length')
            axs[1, plo].set_ylabel(pli[plo])
            #Subplot title
            axs[1, plo].title.set_text(pli[plo])
              
         
        fig.tight_layout()
        plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.91, wspace=None, hspace=0.3)  
        plt.savefig(plot_path+g+odb_names[i]+'.png')
        plt.close()
    #del tull