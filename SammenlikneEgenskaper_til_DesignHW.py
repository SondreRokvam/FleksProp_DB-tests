"""Comparing Illustrations of deformation behaviour for HW propeller
@author: Sondre feb-may.2020"""

from PlottingClass import plottts
import matplotlib.pyplot as plt
import numpy as np
import math
import os

#Directories#
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
#Singles eller Mass Simulations?
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\HW' 

Inp_folders = plottts.FindInPFolders(Source)
#fig, axs = plt.subplots(1, 5, figsize=(12, 8))
#fig.suptitle('Sim: '+'all', fontsize=16)
    
#Starte datapreperation for simulation canvas
for fold in Inp_folders:#[0:1]:  # for many folder
    print(fold[0][55:])
    odb_path = fold[0]
    npz_path, plot_path=odb_path+'\\npz_files' , odb_path+'\\plots'
    
    # Hent
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    fig, axs = plt.subplots(1, 5, figsize=(17, 6))
    fig.suptitle('Sims: '+(fold[0][52:]), fontsize=16)

    for u in odb_names:
         # Profile Subplot title
         # axs[0, maal].title.set_text(Measurementes[maal])
         CylX = np.load(plot_path+'\\Comparison' + '.npz')
         deltas, Radi = [CylX['spenn_delU'], 
                        CylX['spenn_delAlp'], CylX['spenn_AfU'],
                        CylX['spenn_CMBR'], CylX['spenn_CMBRfU']],CylX['radz']
         
         
         pli= ['\u0394_Deflection of center',
             '\u0394_Alpha of coordline',
             '\u0394_Alpha per deflection',
             '\u0394_Chamber',
             '\u0394_Chamber per deflection']
         a = [([0.3,1]  , [-10, 150]),
               ([0.3,1]  , [-5, 10]),
               ([00.3,1]  , [-0.25, 0.25]),
               ([00.3,1]  , [-0.075, 0.01]),
               ([00.3,1]  , [-0.05, 0.001])]
         for uo in range(0, len(deltas[0])):
              
            for plo in range(0, 5):
                axs[plo].plot(Radi, deltas[plo][uo], label=odb_names[uo].rstrip('.odb'))
                # axs[plo].subplot2grid((0, 4), (0, plo))
                axs[plo].set_xlabel('Radius length')
                axs[plo].set_ylabel(pli[plo])
                axs[plo].set_xlim(a[plo][0])
                axs[plo].set_ylim(a[plo][1])
                # Subplot title
                axs[plo].title.set_text(pli[plo])
     
         # legend
         handles, labels = axs[4].get_legend_handles_labels()
         plt.legend(handles=handles[0:len(odb_names)], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=8)
         
         if 'hw' in Source.lower():    
             plt.savefig(Source +'_plots\\'+str(fold[0].split("\\")[6])+'\\!'+str(fold[0][63:]).replace("\\","-")+'.png')
             plt.savefig(Source +'_plots\\!'+str(fold[0][63:]).replace("\\","-")+'.png')
         #if 'azp' in Source.lower():    
         #    plt.savefig(Source +'_plots\\!'+str(fold[0][52:]).replace("\\","-")+'.png')
    fig.tight_layout()
    plt.subplots_adjust(left=None, bottom=0.1, right=0.7, top=0.91, wspace=None, hspace=0.3)  
    plt.close()
     
         