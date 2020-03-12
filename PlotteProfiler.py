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

def addrow(lo):
    N=1
    cols=len(lo[0])
    rows=len(lo)
    Dots_data =  np.zeros((rows+N,cols))
    Dots_data[:-N,:] = lo
    return Dots_data
     
def sortbyangle(dt):
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
    Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
    radius= 650
    Radi=Para['r_val']
    print (Radi)
    
    #Start plotting
    
    for u in odb_names:
        #Logging deltas
        delta_U=[]
        delta_A=[]
        delta_W=[]
        pl3D = []
        fig, axs = plt.subplots(2,5,figsize = (22,10))
        
        fig.suptitle('Simulation: '+u+', Series: '+g, fontsize=16)
        axs[0, 0].set_ylabel('Propeller axis')
        for maal in range(0,len(Measurementes)):
            CylX   =  np.load(npz_path+'Cylinder view of '+Measurementes[maal]+' for '+u[:-4]+'.npz')
            dotCyl,dotCylm = CylX['profile_undeformed'],CylX['profile_deformed']
            
            #Logging
            Centers= []
            Alphas= []
            Warping = []
            
            Plotting=np.zeros((12, len(dotCyl)))
            Plotting[0:3]=np.transpose(np.array(dotCyl))
            Plotting[6:9]=np.transpose(np.array(dotCylm))
            for i in range(0,len(Plotting[0])):
                Plotting[3][i]= Plotting[0][i]-np.average(Plotting[0,:])
                Plotting[4][i]= Plotting[2][i]-np.average(Plotting[2,:])
                ang = math.atan2(Plotting[4][i] , Plotting[3][i])
                Plotting[5][i]= ang
                Plotting[9][i]= Plotting[6][i]-np.average(Plotting[6,:])
                Plotting[10][i]= Plotting[8][i]-np.average(Plotting[8,:])
                ang = math.atan2(Plotting[10][i] , Plotting[9][i])
                Plotting[11][i]= ang
            Plotting=sortbyangle(np.transpose(Plotting))
            pl3D.append([Plotting[:][0:3],Plotting[:][6:9]])
            #Subplot title
            axs[0, maal].title.set_text(Measurementes[maal])
            Inter=[[0,2],[6,8]]
            #Plot profile
            axs[0, maal].set_xlabel('Cylinder length')
            for p in Inter:
                axs[0, maal].plot((Plotting[:,p[0]])*Radi[maal]*radius,Plotting[:,p[1]],'r-')   
               
                #Linear regression for chordline
                m,y = np.polyfit(Plotting[:,p[0]]*Radi[maal]*radius,Plotting[:,p[1]],1)
                   
                #2nd order regression for warp
                a,b,c = np.polyfit(Plotting[:,p[0]]*Radi[maal]*radius,Plotting[:,1],2)
            
                #Lag X-axis for choordline
                x= np.array([np.min(Plotting[:,p[0]]*Radi[maal])*radius-0.05*abs(np.min(Plotting[:,p[0]]*Radi[maal]*radius)),np.max(Plotting[:,p[0]]*Radi[maal]*radius)+abs(0.05*np.min(Plotting[:,p[0]]*Radi[maal]*radius))])
                   
                #Plot chordline
                axs[0, maal].plot(x, m*x + y,'--') 
                #Save chordline angle
                if m<0.0:
                    del koko
                Alphas.append(math.atan2(m,1)*180/math.pi)
                Centers.append([np.average(Plotting[:,p[0]]),np.average(Plotting[:,p[1]])])
                Warping.append(a)
            #Find angle change
            deltaDeflec= ((Centers[1][0]-Centers[0][0])**2+(Centers[1][1]-Centers[0][1])**2)**0.5
            deltaAlfa= Alphas[1]-Alphas[0]
            deltaWarp= Warping[1]-Warping[0]
            delta_U.append(deltaDeflec)
            delta_A.append(deltaAlfa)
            delta_W.append(deltaWarp)
        #Print data for dette designet
        print('\n\n', u,'\n')
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
        #print(pl3D[0][:])
        #axs[1,4].scatter(pl3D[0])
        #axs[1,4].scatter(pl3D[1])
        fig.tight_layout()
        plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.91, wspace=None, hspace=0.3)  
        plt.savefig(plot_path+g+u+'.png')
        plt.savefig('C:/Users/sondreor/Desktop/Azp_plots/'+g+u+'.png')
        plt.close()
    #del tull