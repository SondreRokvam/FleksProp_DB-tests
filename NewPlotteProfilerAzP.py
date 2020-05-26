# -*- coding: utf-8 -*-
"""Illustrationg deformation behaviour for AzP propeller
@author: Sondre feb-may.2020"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import os
from PlottingClass import plottts
a = [([0.3,1]   , [-5, 140]),
     ([0.3,1]   , [-4, 1.5]),
     ([0.3,1]   , [-0.25, 0.15]),
     ([0.3,1]   , [-0.01, 0.15]),
     ([0.3,1]   , [-0, 0.003])]

b = [([0.3,1]   , [-0, 5]),
     ([0.3,1]   , [-0, 0.075]),
     ([0.3,1]   , [-0, 0.1]),
     ([0.3,1]   , [-0, 0.0015]),
     ([0.3,1]   , [-0, 0.004])]
#Directories#
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
#Singles eller Mass Simulations?
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\AZP' 
#Source = 'D:\\PhD\\Simuleringer\\Mecanical aspects\\Periodic Force Variations'

Inp_folders = plottts.FindInPFolders(Source)

#Starte datapreperation for simulation canvas
for fold in Inp_folders:#[:1]:  # for many folder
     print('\n\nFolder :',fold[0].split("\\")[-4:-1],'\n')
     odb_path = fold[0]
     npz_path, plot_path=odb_path+'\\npz_files' , odb_path+'\\plots'
     plottts.new_folder(plot_path)
     #plottts.new_folder('D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp_plots\\'+str(fold[0].split("\\")[6])+'\\')
     
     # Hent data
     odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb') and not '100'in f)]
     npz_files = [f for f in os.listdir(npz_path) if (f.endswith('.npz') and not '100 ' in f)]
          
     #Hente faste variabler for plotting
     Para   =  np.load(gitHub+'parameters_for_plot.npz')
     Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
     Radi=Para['r_val']

     #Make lists for holding KPI for comparison of concepts in folder plotting
     spenn_delU, spenn_delAlp, spenn_CMBR=[],[],[]
     spenn_AfU,spenn_CMBRfU =[],[]
     
     for Sim in odb_names:#[:3]:
          print(Sim)
          #KPIs
          delta_U, delta_A, delta_CMBR = [],[],[]
          A_for_U, CMBR_for_U =[],[]
          
          # Start configuring plots
          fig, axs = plt.subplots(2,5,figsize = (19,9))
          fig.suptitle('Sim: '+Sim, fontsize=16)
          axs[0, 0].set_ylabel('Propeller longtudinal axis')
          s,j='gr', ['--','-'] #Farge og form for Display profil plottene
                
          ProfilePlots=[]
          for maal in range(0,len(Measurementes)):
               Data   =  np.load(npz_path+'\\Cylinder view of '+Measurementes[maal]+' for '+Sim[:-4]+'.npz')
               Coordline = [Data['profile_undefcoordline'],Data['profile_defcoordline']]
               dotCyl,dotCylm = Data['profile_undeformed'],Data['profile_deformed']
               Inter=[[1,0],[7,6]] # The datacolumns in plotdata used for plotting in current tests
                    
               # Sort data - Rotational from center
               PlotData=plottts.sortProfile_points_for_plotting(dotCyl, dotCylm,'HW')
               # Sort data - ADD ARCLENGHT SORT

               #Make lists for holding KPI for comparison of concepts in folder plotting
               CenterDeflection, Alphas, Warp = [],[],[]
               Coordlengths, Thicknesses= [],[]

               CurcentProfilePlots, FlatProfilePlots=[],[]                
               CLplot, NCLplot= [],[]

               CLcenterMark = []
               WarpPointsPlotting=[]

               #Prep profile plots
               for p in Inter:
                    #Make X - Y data
                    ProfXs, ProfYs = PlotData[:,p[0]], PlotData[:,p[1]]
                     
                    #Lag X-axis for choordline
                    xmin=np.min(Coordline[Inter.index(p)][:,1])
                    xmax=np.max(Coordline[Inter.index(p)][:,1])
                     
                    #Linear regression for coordline
                    m,y = np.polyfit(np.array(Coordline[Inter.index(p)])[:,1],Coordline[Inter.index(p)][:,0],1)
                    Xline=np.linspace(xmin-50.0,xmax+50.0,10)
                    CLx, CLy =(xmin+xmax)/2,m*(xmin+xmax)/2+y
                     
                    #Find normal to coordline
                    NM = -1/m
                    Ny = m*(xmin+xmax)/2+y-NM*(xmin+xmax)/2
                                          
                    # KPI management: Alfa, deflection and coordlength change                    
                    Alphas.append(math.atan2(m,1)*180/math.pi)
                    CenterDeflection.append([np.average(PlotData[:,p[0]]),np.average(PlotData[:,p[1]])])
                    Coordlengths.append(math.sqrt((np.array(Coordline[Inter.index(p)])[1,0]-np.array(Coordline[Inter.index(p)])[0,0])**2+(Coordline[Inter.index(p)][1,1]-Coordline[Inter.index(p)][0,1])**2))
                    
                    #Sort and rotate data for Warp Calculation
                    WarpPoints = np.transpose([PlotData[:,p[0]],PlotData[:,p[1]]])
                    RWP =[]
                    for point in WarpPoints:
                         RWP.append(plottts.rotate([(xmin+xmax)/2,m*(xmin+xmax)/2+y], point, -math.atan2(m,1)))
                         
                    #Find Warp Points
                    warp_point_top,warp_point_bot=plottts.Top_bottom_warpPoints(40,RWP,xmin,xmax,CLx,CLy,m,y)
     
                    # KPI management
                    Thickness=(warp_point_top[1]-warp_point_bot[1])
                    Thicknesses.append(Thickness)
                    Warp.append((warp_point_top[1]+warp_point_bot[1])/2-CLy)
                    
                     
                    #Translate/Roatae back to real pos for plotting
                    warp_point_topPlots = plottts.rotate((CLx,CLy),(warp_point_top),math.atan2(m,1))
                    warp_point_botPlots = plottts.rotate((CLx,CLy),(warp_point_bot),math.atan2(m,1))
                    WarpPointsPlotting.append([[(warp_point_botPlots[0]+warp_point_topPlots[0])/2],[(warp_point_botPlots[1]+warp_point_topPlots[1])/2],'m*'])
                    #Plot coordlne and Normal with CenterMark
                    CLcenterMark.append([CLx,CLy, 'k.'])
                    CLplot.append([Xline, m*Xline + y,'--']) 
                    XlineMob=np.linspace(xmin+50.0,xmax-50.0,2)
                    
                    NCLplot.append([XlineMob,NM*XlineMob+Ny,':']) 
                    
                    #Plotting profile plots
                    CurcentProfilePlots.append([ProfXs,ProfYs,s[Inter.index(p)]+j[Inter.index(p)]])
                    
                    #Plotting flat profil plots
                    RW=np.transpose(RWP)
                    FlatProfilePlots.append([RW[0],RW[1],s[Inter.index(p)]+j[Inter.index(p)]])                 
                    
               #Find change  angle 
               deltaDeflec= ((CenterDeflection[1][0]-CenterDeflection[0][0])**2+(CenterDeflection[1][1]-CenterDeflection[0][1])**2)**0.5
               deltaAlfa= Alphas[1]-Alphas[0]
               deltaCoordchange= Coordlengths[1]-Coordlengths[0]
               deltaWarp= Warp[1]-Warp[0]
               deltaThick= Thicknesses[1]-Thicknesses[0]
               deltaCAMBER= deltaWarp/Coordlengths[0]
               delta_U.append(deltaDeflec)
               delta_A.append(deltaAlfa)
               A_for_U.append((deltaAlfa/deltaDeflec))
               delta_CMBR.append(deltaCAMBER)  
               CMBR_for_U.append(deltaCAMBER/deltaAlfa)
               
               #Plottinga av profile Subplots 
               axs[0, maal].title.set_text(Measurementes[maal])#Label Title in the subplot
               axs[0, maal].set_xlabel('Cylinder length')      #Label x-axis in the subplot
               handle = ['Undef.', 'Loaded'] # For legends
               for p in Inter:
                    cp =CurcentProfilePlots[Inter.index(p)]
                    #fp =FlatProfilePlots[Inter.index(p)]
                    cl =CLplot[Inter.index(p)]
                    ncl =NCLplot[Inter.index(p)]
                    clM = CLcenterMark[Inter.index(p)]
                    wpp =WarpPointsPlotting[Inter.index(p)]
                    axs[0, maal].plot(cp[0],cp[1],cp[2],label=handle[Inter.index(p)])
                    #axs[0, maal].plot(fp[0],fp[1],fp[2])
                    axs[0, maal].plot(cl[0],cl[1],cl[2],s[Inter.index(p)]+':')
                    axs[0, maal].plot(ncl[0],ncl[1],ncl[2])
                    axs[0, maal].plot(clM[0],clM[1],clM[2])
                    axs[0, maal].plot(wpp[0],wpp[1],wpp[2])
               axs[0, maal].set_xlim([375,1225])
               axs[0, maal].set_ylim([-400, 600])
                
               # Preparere Legends
               handles, labels = axs[0, maal].get_legend_handles_labels()
               
               AlfaLabl = '\u03B1, \u0394' + '\u03B1 = '+ str("%.2f" % Alphas[0])+ ', '+str("%.2f" % deltaAlfa) + ' °'
               CMBRLabl = 'CL, \u0394' + 'CL' + ' = '+ str("%.3f" % float(Warp[0]/Coordlengths[0]))+ ', '+str("%.1f" % (float(deltaCAMBER/(Warp[0]/Coordlengths[0]))*100.0))+'%'
               CoorlineLabl = 'Coordlen.' + ' = ' + str("%.1f" % (float(Coordlengths[0]))) + ', ' + str("%.1f" % (float(deltaCoordchange/Coordlengths[0])*100.0))+'%'
               ThicknessLabl ='Thickness' + ' = ' + str("%.1f" % (float(Thicknesses[0] ))) + ', '+ str("%.1f" % (float(deltaThick/Thicknesses[0])*100.0))+'%'

               handles.append(mpatches.Patch(color='none', label=AlfaLabl))
               handles.append(mpatches.Patch(color='none', label=CMBRLabl))
               handles.append(mpatches.Patch(color='none', label=CoorlineLabl))
               handles.append(mpatches.Patch(color='none', label=ThicknessLabl))
               # Plotte Legends
               axs[0, maal].legend(handles=handles, loc='best', fontsize=8)
               
          spenn_delU.append(delta_U)
          spenn_delAlp.append(delta_A)
          spenn_AfU.append(A_for_U)
          spenn_CMBR.append(delta_CMBR)
          spenn_CMBRfU.append(CMBR_for_U)
             
          #Andre rad - Maa oppdateres med nye plot når warp er satt opp
          ploo=[delta_U,delta_A,A_for_U,delta_CMBR,CMBR_for_U]
          KPItitles = ['Bend ', 'Twist', 'BendTwist (Twist per Bend)','Camber','Camber per Twist' ]
          pli= ['Deflection [mm]','\u0394 \u03B1 of coordline [°]','\u0394 \u03B1 / deflection [°/mm] ',
                '\u0394 Camber','\u0394 Camber / \u03B1 [1/°]']
          #        Xlim         Ylims

          for plo in range(0,5):
               #Plot profile
               axs[1, plo].plot(Radi,ploo[plo])
               axs[1, plo].set_xlabel('Radius length')
               axs[1, plo].set_ylabel(pli[plo])
               axs[1, plo].set_xlim(a[plo][0])
               #axs[1, plo].set_ylim(a[plo][1])
               #Subplot title
               axs[1, plo].title.set_text(KPItitles[plo])
          plt.subplots_adjust(left=0.075, bottom=0.075, right=0.975, top=0.9, wspace=0.35, hspace=0.3)  
          np.savez(plot_path+'\\Comparison',
                   spenn_delU=spenn_delU,
                   spenn_delAlp=spenn_delAlp,
                   spenn_AfU=spenn_AfU,
                   spenn_CMBR =spenn_CMBR,
                   spenn_CMBRfU = spenn_CMBRfU,
                   radz=Radi)
          
          plottts.new_folder('D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp_plots\\'+str(fold[0].split("\\")[6]))
          plt.savefig('D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\Azp_plots\\'+str(fold[0].split("\\")[6])+'\\'+Sim[:-4]+'.png')
          #plt.savefig(Source+'\\'+Sim[:-4]+'.png')
          plt.close()

             
