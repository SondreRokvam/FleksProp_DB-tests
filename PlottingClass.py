"""  Created on Thu Mar 12 13:21:24 2020
@author: sondreor """

import matplotlib.pyplot as plt
import numpy as np
import operator
import math
import os

class plottts:
     
     def __init__(self):
          pass
    
     def Top_bottom_warpPoints(tolran,REL_Points_rotated,XMI,XMA,CooLiX,CooliY,mama,yaya):
          #print(len(REL_Points_rotated))
          RelevantPoints=  []
          Xref =(float(XMI+XMA)/2)
          for point in REL_Points_rotated:
#               print('is ', Xref+tolran,' < ',point[0],' > ', Xref-tolran)                      
               if point[0] > Xref-tolran:
                    if point[0] < Xref+tolran:
                         #print(REL_Points_rotated[REL_Points_rotated.index(point)][0])
                         RelevantPoints.append([REL_Points_rotated[REL_Points_rotated.index(point)][0],REL_Points_rotated[REL_Points_rotated.index(point)][1]])
          #print('Filter = ',len(RelevantPoints), ' of ',len(REL_Points_rotated) )
          
          #print(np.array(RelevantPoints))
          Snitt = np.mean(np.array(RelevantPoints)[:,1])
          
          Botpoints=[]
          TopPoints=[]
          for Coords in range(len(RelevantPoints)):
               if RelevantPoints[Coords][1]<Snitt:
                    Botpoints.append(RelevantPoints[Coords])
               else:
                    TopPoints.append(RelevantPoints[Coords])
          
          #print(len(Botpoints))
          if len(Botpoints)>2:
               relpoints=[]
               for poi in Botpoints:     
                    relpoints.append([poi[0] - Xref,poi[1]])
               pospoints= [sd for sd in relpoints if sd[0]>0]
               negpoints= [sd for sd in relpoints if sd not in pospoints]
               if len(pospoints)>1:
                    cool =pospoints[0]
                    for pop in pospoints:
                         if pop[0]<cool[0]:
                              cool=pop
                    pospoints=cool
               if len(negpoints)>1:
                    cool =negpoints[0]
                    for pop in negpoints:
                         if pop[0]>cool[0]:
                              cool=pop
                    negpoints=cool
               Botpoints=[negpoints,pospoints]
          #print('\n\nBOT',Botpoints)
          if len(TopPoints)>2:
               relpoints=[]
               for poi in TopPoints:     
                    relpoints.append([poi[0] - Xref,poi[1]])
               pospoints= [sd for sd in relpoints if sd[0]>0]
               negpoints= [sd for sd in relpoints if sd not in pospoints]
               if len(pospoints)>1:
                    cool =pospoints[0]
                    for pop in pospoints[1:]:
                         if pop[0]<cool[0]:
                              cool=pop
                    pospoints=cool
               if len(negpoints)>1:
                    cool =negpoints[0]
                    for pop in negpoints[1:]:
                         if pop[0]>cool[0]:
                              cool=pop
                    negpoints=cool
               TopPoints=[negpoints,pospoints]
          #print('\n\n',TopPoints,'\n\n',Botpoints)
#          print ('lil',TopPoints)
          ere,y = np.polyfit(np.array(TopPoints)[:,0],np.array(TopPoints)[:,1],1)
          WAPOTO=(Xref, y)
          ere,y = np.polyfit(np.array(Botpoints)[:,0],np.array(Botpoints)[:,1],1)
#          else:
#               print( 'its Aokay')
          WAPOBO=(Xref, y)
          return WAPOTO, WAPOBO
     
     def FindInPFolders(Soe):
          Inpfodes=[]
          for root, dirs, files in os.walk(Soe, topdown=False):
               for name in dirs:
                    name = os.path.join(root, name)
                    inp_files = [a for a in os.listdir(name) if a.endswith('.inp')]
                    if len(inp_files)>0:
                        Inpfodes.append(name.split('\n'))
          return Inpfodes
    
     def addrow(lo):
          N=1
          cols=len(lo[0])
          rows=len(lo)
          Dots_data =  np.zeros((rows+N,cols))
          Dots_data[:-N,:] = lo
          return Dots_data
         
     def sortbyangle(dt):
          dt =np.array(sorted(dt, key=operator.itemgetter(5)))
          dt= plottts.addrow(dt)  #Adds row to the array
          dt[-1]=dt[0]    #sets last row= first row for complete profile
          return dt
    
     def new_folder(path):
          try:
               os.mkdir(path) # Create target Directory
               #print("Directory " , path ,  " Created ") 
          except:
               pass
               print("Directory " , path ,  " already exists")
            
     def sortProfile_points_for_plotting(PointCloud, PointCloudm,mark):
          PD=np.zeros((12, len(PointCloud)))
          PD[0:3]=np.transpose(np.array(PointCloud))
          PD[6:9]=np.transpose(np.array(PointCloudm))
          for i in range(0,len(PD[0])):
               if mark=='HW':
                    PD[3][i]= PD[1][i]-np.average(PD[1,:])
                    PD[4][i]= PD[0][i]-np.average(PD[0,:])
               else:    
                    PD[3][i]= PD[0][i]-np.average(PD[0,:])
                    PD[4][i]= PD[2][i]-np.average(PD[2,:])
               ang = math.atan2(PD[4][i] , PD[3][i])
               PD[5][i]= ang
               PD[9][i]= PD[6][i]-np.average(PD[6,:])
               PD[10][i]= PD[8][i]-np.average(PD[8,:])
               ang = math.atan2(PD[10][i] , PD[9][i])
               PD[11][i]= ang
          PD=plottts.sortbyangle(np.transpose(PD))
          return PD
    
     def rotate(origin, point, angle):
          ox, oy = origin
          px, py = point
     
          qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
          qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
          return qx, qy
       
     def line_intersection(line1, line2):
          xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
          ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
     
          def det(a, b):
               return a[0] * b[1] - a[1] * b[0]
          
          div = det(xdiff, ydiff)
          if div == 0:
               return('lines do not intersect')
          else:
               d = (det(*line1), det(*line2))
               x = det(d, xdiff) / div
               y = det(d, ydiff) / div
               return x, y
          
     def ScriptForSimuleringsSammenligningMasse(Source,Inp_folders, ALL,a):
          Figurines= 'ovsP*XD<>'
          KPItitles = ['Bend ', 'Twist', 'BendTwist (Twist per Bend)','Camber','Camber per Twist' ]
          pli= ['Deflection [mm]','\u0394 \u03B1 of coordline [°]','\u0394 \u03B1 / deflection [°/mm] ',
                '\u0394 Camber','\u0394 Camber / Twist [1/°]']
          #        Xlim         Ylims
          if ALL:
               print('All testing')
               fig, axs = plt.subplots(1, 5, figsize=(19, 9))
               fig.suptitle('Sim: '+'All '+ Source.split("\\")[-1]+' simulations', fontsize=16)
          #try:
          if 1:
               for fold in Inp_folders:  # for many folder
                    
                    #print(fold[0],'\n')
                    odb_path = fold[0]
                    plot_path= odb_path+'\\plots'
                    
                    # Hent
                    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb') and not ('20' in f or '100' in f))]#print(odb_names)
                    if not ALL:
                         fig, axs = plt.subplots(1, 4, figsize=(19, 10))
                         fig.suptitle('Comparison: '+(fold[0][52:-8])+' Baseline models', fontsize=20)
                         
                    #Sette alle filene i denne mappen i ett plott
                    #print(odb_names)
                    #print(len(odb_names))
                    
                    CylX = np.load(plot_path+'\\Comparison' + '.npz')
                    deltas, Radi = [CylX['spenn_delU'], 
                                       CylX['spenn_delAlp'], CylX['spenn_AfU'],
                                       CylX['spenn_CMBR'], CylX['spenn_CMBRfT']],CylX['radz']
                    
                    
                    for u in odb_names:
                         #print ('hjkhkhk',u)
                         
                         # Profile Subplot title
     
                         #(deltas[0])
                         for plo in range(0, 4):
                              if ALL:
                                   axs[plo].plot(Radi, deltas[plo].tolist()[u][:],linewidth=1.0)
                              if not ALL:
                                   axs[plo].plot(Radi, deltas[plo].tolist()[u][:],markersize=10,linewidth=2.0,marker=Figurines[odb_names.index(u)%len(Figurines)] ,label=odb_names[odb_names.index(u)].rstrip('.odb')[0:])
                              axs[plo].set_xlabel('Radius length', fontsize=18)
                              axs[plo].set_ylabel(pli[plo], fontsize=18)
                              axs[plo].set_xlim(a[plo][0])
                              
                              axs[plo].tick_params(labelsize=16)
                              axs[plo].grid(True)
#                              if not ALL:
#                                  axs[plo].set_ylim(a[plo][1]) 
                              
                              # Subplot title
                              axs[plo].set_title(KPItitles[plo], fontsize=18)
          
                    if not ALL:
                         handles, labels = axs[0].get_legend_handles_labels()
                         plt.legend(handles=handles[0:len(odb_names)], bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
                         fig.tight_layout()
                         plt.subplots_adjust(left=0.05, bottom=0.075 ,top=0.9 )  
                         
#                         plt.savefig(Source +'_plots\\'+fold[0].split("\\")[-1]+'\\!-'+fold[0].split("\\")[-1]+'_Compare.png')
#                         plt.savefig(Source +'_plots\\!-'+fold[0].split("\\")[-1]+'_Compare.png')
#                         plt.close()
                                       
               if ALL:
                    fig.tight_layout()
                    plt.subplots_adjust(left=0.075, bottom=0.075 ,top=0.9 )  
                    plt.savefig(Source +'_plots\\- !All.png')
                    
                    #plt.savefig(Source +'_plots\\- !All.png')
          #except:
          #     print pass