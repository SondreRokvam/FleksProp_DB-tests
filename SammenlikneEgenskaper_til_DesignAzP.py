"""Comparing Illustrations of deformation behaviour for AZP propeller
@author: Sondre feb-may.2020"""

from PlottingClass import plottts
import matplotlib.pyplot as plt
import numpy as np
import math
import os

#Declare Directories
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp' 

#Hente folder directories
Inp_folders = plottts.FindInPFolders(Source)

#Plotting starte
Figurines= 'ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>ovsP*XD<>'
mirker=0

KPItitles = ['Bending', 'Twisting', 'BendTwist, BT - (Twist per Bend)','Camber','Camber per Bend' ]
pli= ['\u0394_Deflection of center','\u0394_Alpha of coordline','\u0394_Alpha per deflection',
          '\u0394_Camber','\u0394_Camber per deflection']

a = [([0.3,1]   , [10, 110]),
     ([0.3,1]   , [-4, 0.4]),
     ([0.3,1]   , [-0.065, 0.02]),
     ([0.3,1]   , [0, 0.160]),
     ([0.3,1]   , [0.00125, 0.003])]

fog, asas = plt.subplots(1, 5, figsize=(20, 8))
fog.suptitle('Sim: '+'all'+ Source.split("\\")[-1], fontsize=16)
#Starte datapreperation for simulation canvas
for fold in Inp_folders:#[0:1]:  # for many folder
    print(fold[0][55:],'\n')
    odb_path = fold[0]
    npz_path, plot_path=odb_path+'\\npz_files' , odb_path+'\\plots'
    
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    #fig, axs = plt.subplots(1, 5, figsize=(17, 6))
    #fig.suptitle('Sims: '+(fold[0][52:]), fontsize=16)
    try:
         for u in odb_names:
              # Profile Subplot title
              # axs[0, maal].title.set_text(Measurementes[maal])
              CylX = np.load(plot_path+'\\Comparison' + '.npz')
              deltas, Radi = [CylX['spenn_delU'], 
                             CylX['spenn_delAlp'], CylX['spenn_AfU'],
                             CylX['spenn_CMBR'], CylX['spenn_CMBRfU']],CylX['radz']
              
              
              KPItitles = ['Bending', 'Twisting', 'BendTwist, BT - (Twist per Bend)','Camber','Camber per Bend' ]
              pli= ['\u0394_Deflection of center','\u0394_Alpha of coordline','\u0394_Alpha per deflection',
                   '\u0394_Camber','\u0394_Camber per deflection']

              for uo in range(0, len(deltas[0])):
                   
                 for plo in range(0, 5):
                     mirker = mirker +1
                     axs[plo].plot(Radi, deltas[plo][uo], ,marker = Figurines[mirker],label=odb_names[uo].rstrip('.odb')[3:])
                     # axs[plo].subplot2grid((0, 4), (0, plo))
                     axs[plo].set_xlabel('Radius length')
                     axs[plo].set_ylabel(pli[plo])
                     axs[plo].set_xlim(a[plo][0])
                     axs[plo].set_ylim(a[plo][1]) 
                     # Subplot title
                     axs[plo].title.set_text(KPItitles[plo])
    except:
         pass
    # legend
    #handles, labels = axs[4].get_legend_handles_labels()
    #plt.legend(handles=handles[0:len(odb_names)], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=8)
    #plt.subplots_adjust(left=None, bottom=0.05, right=0.825, top=0.87, wspace=0.5, hspace=None)  
         
if 'hw' in Source.lower():    
    plt.savefig(Source +'_plots\\'+str(fold[0].split("\\")[6])+'\\!'+str(fold[0][55:]).replace("\\","-")+'.png')
    plt.savefig(Source +'_plots\\!'+str(fold[0][55:]).replace("\\","-")+'.png')
    #if 'azp' in Source.lower():    
    #    plt.savefig(Source +'_plots\\!'+str(fold[0][52:]).replace("\\","-")+'.png')
    #plt.close()
    #except:
    #     try:
    #          plt.close()
    #     except:
    #          pass
    #     print ( ' Did\'nt work \n')
             
              