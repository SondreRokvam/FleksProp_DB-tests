# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 01:27:31 2020

@author: Sondre
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import os

# ODB PATH
# gitHub = 'C:/Users/sondreor/Documents/GitHub/FleksProp_DB-tests/'
# gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
gitHUB = 'C:/Users/lmark/Documents/GitHub/FleksProp_DB-tests/'
# HW = 'C:/Users/sondre/Desktop/HW/'
# Azp = 'C:/Users/sondre/Desktop/Azp/'
Azp = 'D:/PhD/Simuleringer/AZP/'
HW = 'D:/PhD/Simuleringer/HW/'
gofor = Azp
stuff= [f for f in os.listdir(gofor) if not (f.endswith('.bat'))]
print(stuff)
for g in stuff:  # for many folders
    try:
        odb_path = gofor
        odb_path = odb_path + g + '/'  # for many folders
        plot_path = odb_path + 'plots/'

        # Hent
        odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
        fig, axs = plt.subplots(1, 3, figsize=(18, 8))
        fig.suptitle('Simulations of series: ' + g, fontsize=16)
        # Profile Subplot title
        # axs[0, maal].title.set_text(Measurementes[maal])
        CylX = np.load(plot_path + g + '.npz')
        deltas, Radi = [CylX['spenn_delU'], CylX['spenn_delA'], CylX['spenn_delW']], CylX['radz']
        for uo in range(0, len(deltas[0])):
            ploo = deltas
            pli = ['\u0394_Deflection of center', '\u0394_Alpha of coordline', '\u0394_Alpha per \u0394_deflection']
            for plo in range(0, 3):
                # Plot profile
                axs[plo].plot(Radi, np.array(ploo[:][plo][uo]), label=odb_names[uo].rstrip('.odb'))
                # axs[plo].subplot2grid((0, 4), (0, plo))
                axs[plo].set_xlabel('Radius length')
                axs[plo].set_ylabel(pli[plo])
                # Subplot title
                axs[plo].title.set_text(pli[plo])

        # legend
        handles, labels = axs[plo].get_legend_handles_labels()
        axs[plo].legend(handles=handles, loc='upper center', bbox_to_anchor=(1.45, 0.8), borderaxespad=0., fontsize=10)
        # plt.tight_layout()
        if gofor.endswith('HW/'):    
             plt.savefig('D:/PhD/Simuleringer/HW_plots/AA' + g + '.png', bbox_inches='tight')
        if gofor.endswith('AZP/'): 
             plt.savefig('D:/PhD/Simuleringer/Azp_plots/AA' + g + '.png', bbox_inches='tight')
        plt.close()
    except:
        print('not', g)
        pass
    