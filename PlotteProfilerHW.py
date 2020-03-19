"""
Plot/charts illustrationg deformation behaviour
Created on Wed Feb 19 02:36:36 2020

@author: Sondre
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from PlottingClass import plottts

print (plottts)

#ODB PATH
gitHub = 'C:/Users/sondreor/Documents/GitHub/FleksProp_DB-tests/'
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
HW = 'C:/Users/sondre/Desktop/HW/'
gofor = HW   
print (os.listdir(gofor))                                     # folder of folders of ODBs
for g in os.listdir(gofor):#[0:1]: #for many folders
    odb_path = gofor
    odb_path =odb_path+g+'/' #for many folders
    
    #NPZ PATH #Plot_Paths
    npz_path=odb_path+'npz_files/' 
    plot_path= odb_path+'plots/'
    plottts.new_folder(plot_path)
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    npz_files = [f for f in os.listdir(npz_path) if (f.endswith('.npz'))]
    Para   =  np.load(gitHub+'parameters_for_plot.npz')
    Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
    radius= 1
    Radi=Para['r_val']
    print (Radi)
    #Start plotting
    spenn_delU=[]
    spenn_delA=[]
    spenn_delW=[]
    for u in odb_names:#[0:1]:
        #Logging deltas
        delta_U=[]
        delta_A=[]
        delta_W=[]
        
        
        fig, axs = plt.subplots(2,5,figsize = (18,8))
        
        fig.suptitle('Simulation: '+u+', Series: '+g, fontsize=16)
        axs[0, 0].set_ylabel('Propeller axis')
       
        
        for maal in range(0,len(Measurementes)):
            CylX   =  np.load( npz_path+'Cartesian view of '+Measurementes[maal]+' for '+u[:-4]+'.npz')
            
            Coordline = [CylX['profile_undefcoordline'],CylX['profile_defcoordline']]
            dotCyl,dotCylm = CylX['profile_undeformed'],CylX['profile_deformed']
            
            
            # Sort stuff
            Plotting=np.zeros((12, len(dotCyl)))
            Plotting[0:3]=np.transpose(np.array(dotCyl))
            Plotting[6:9]=np.transpose(np.array(dotCylm))
            for i in range(0,len(Plotting[0])):
                Plotting[3][i]= Plotting[1][i]-np.average(Plotting[1,:])
                Plotting[4][i]= Plotting[0][i]-np.average(Plotting[0,:])
                ang = math.atan2(Plotting[4][i] , Plotting[3][i])
                Plotting[5][i]= ang
                Plotting[9][i]= Plotting[7][i]-np.average(Plotting[7,:])
                Plotting[10][i]= Plotting[6][i]-np.average(Plotting[6,:])
                ang = math.atan2(Plotting[10][i] , Plotting[9][i])
                Plotting[11][i]= ang
            Plotting=plottts.sortbyangle(np.transpose(Plotting))
            
            #ProfileLogging
            Centers= []
            Alphas= []
            Warping = []
            
            #Profile Subplot title
            axs[0, maal].title.set_text(Measurementes[maal])
            Inter=[[0,1],[6,7]]
            s='gr'
            #Plot profile
            axs[0, maal].set_xlabel('coordlength')
            for p in Inter:
                axs[0, maal].plot((Plotting[:,p[1]]),Plotting[:,p[0]],s[Inter.index(p)]+'-')   
                
                #Linear regression for chordline
                m,y = np.polyfit(np.array(Coordline[Inter.index(p)])[:,1],Coordline[Inter.index(p)][:,0],1)
                
                #2nd order regression for warp
                #a,b,c = np.polyfit(Plotting[:,p[0]]*Radi[maal]*radius,Plotting[:,1],2)
            
                #Lag X-axis for choordline
                xmin=np.min(Coordline[Inter.index(p)][:,1])
                xmax=np.max(Coordline[Inter.index(p)][:,1])
                ext = 5
                x= np.linspace(xmin-abs(ext/100)*xmin,xmax+abs(ext/100)*xmax)
                #Plot chordline
                axs[0, maal].plot(x, m*x + y,'--') 
                #Save chordline angle
                #if m<0.0:
                #    del koko
                Alphas.append(math.atan2(m,1)*180/math.pi)
                Centers.append([np.average(Plotting[:,p[1]]),np.average(Plotting[:,p[0]])])
                Warping.append(1)
            #axs[0, maal].set_xlim([-250, 250])
            #axs[0, maal].set_ylim([-25, 50])
            #Find angle change
            deltaDeflec= ((Centers[1][0]-Centers[0][0])**2+(Centers[1][1]-Centers[0][1])**2)**0.5
            deltaAlfa= Alphas[1]-Alphas[0]
            deltaWarp= deltaAlfa/deltaDeflec
            delta_U.append(deltaDeflec)
            delta_A.append(deltaAlfa)
            delta_W.append(deltaWarp)
        spenn_delU.append(delta_U)
        spenn_delA.append(delta_A)
        spenn_delW.append(delta_W)
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
        plt.savefig('C:/Users/sondre/Desktop/HW_plots/'+u[:-4]+'.png')
        plt.close()
