# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 01:27:31 2020

@author: Sondre
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import os
#ODB PATH
gitHub = 'C:/Users/sondreor/Documents/GitHub/FleksProp_DB-tests/'
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
HW = 'C:/Users/sondre/Desktop/HW/'
Azp = 'C:/Users/sondre/Desktop/Azp/'
gofor = Azp

for g in os.listdir(gofor):#[0:1]:  #for many folders
    odb_path = gofor
    odb_path =odb_path+g+'/' #for many folders
    plot_path= odb_path+'plots/'
    
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    fig, axs = plt.subplots(1,3,figsize = (18,8))
    
    fig.suptitle('Simulations of series: '+g, fontsize=16)
    #Profile Subplot title
    #axs[0, maal].title.set_text(Measurementes[maal])
    CylX   =  np.load(plot_path+g+'.npz')
    deltas, Radi = [CylX['spenn_delU'],CylX['spenn_delA'],CylX['spenn_delW']],CylX['radz']
    #print (deltas[0][:])
    for uo in range(0,len(deltas[0])):
         ploo=deltas
         pli= ['\u0394_Deflection of center','\u0394_Alpha of coordline','\u0394_Alpha per \u0394_deflection']
         for plo in range(0,3):
               #Plot profile
               axs[plo].plot(Radi,np.array(ploo[:][plo][uo])  )
               axs[plo].set_xlabel('Radius length')
               axs[plo].set_ylabel(pli[plo])
               #Subplot title
               axs[plo].title.set_text(pli[plo])
     
    plt.savefig(gofor[:-1]+'_plots/AA'+g+'.png')
    plt.close()