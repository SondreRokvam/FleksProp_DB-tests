"""Plot/charts illustrationg deformation behaviour for fins like HW
Created on Feb-May 2020       @author: Sondre"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import os
from PlottingClass import plottts

#Directories#
gitHub = 'C:\\MultiScaleMethod\\Github\\FleksProp_DB-tests\\'
#Singles eller Mass Simulations?
HW = 'D:/PhD/Simuleringer/HW/'
gofor = HW
Inp_folders = []
for root, dirs, files in os.walk(gofor, topdown=False):
     for name in dirs:
          name = os.path.join(root, name)
          inp_files = [a for a in os.listdir(name) if a.endswith('.inp')]
          Odb_files = [a for a in os.listdir(name) if a.endswith('.odb')]
          if len(inp_files)>0:
              Inp_folders.append(name)
stuff = Inp_folders
print(len(stuff))
FuckedList=[]

for gofor in stuff:  # for many folder
    odb_path = gofor
    npz_path=odb_path+'\\npz_files' 
    plot_path= odb_path+'\\plots'
    plottts.new_folder(plot_path)
    
    # Hent data
    odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb'))]  # if not f.endswith('.inp')]
    npz_files = [f for f in os.listdir(npz_path) if (f.endswith('.npz'))]
    
    
    Para   =  np.load(gitHub+'parameters_for_plot.npz')
    Measurementes = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
    radius= 1
    Radi=Para['r_val']
    
    #Start loggin for comparison of concepts plotting
    spenn_delU, spenn_delA, spenn_delW=[],[],[]
    spenn_AfU,spenn_WfU =[],[]
    
    for u in odb_names:#[0:1]:
        try:
             # Logging deltas
             delta_U, delta_A, delta_W = [],[],[]
             A_for_U, W_for_U =[],[]
             # Start configuring plots
             fig, axs = plt.subplots(2,5,figsize = (20,8))
             fig.suptitle('Sim: '+u, fontsize=16)
             axs[0, 0].set_ylabel('Propeller longtudinal axis')
             s,j='gr', ['--','-'] #Farge og form for plottene
             ProfilePlots=[]
             # Data processing for each profile
             for maal in range(0,len(Measurementes)):
                 # Data pickup
                 Data   =  np.load( npz_path+'Cartesian view of '+Measurementes[maal]+' for '+u[:-4]+'.npz')
                 Coordline = [Data['profile_undefcoordline'],Data['profile_defcoordline']]
                 dotCyl,dotCylm = Data['profile_undeformed'],Data['profile_deformed']
                 
                 Inter=[[1,0],[7,6]] # The datacolumns in plotdata used for plotting
                 
                 
                 # Sort data
                 PlotData=plottts.sortProfile_points_for_plotting(dotCyl, dotCylm,'HW')
                 
                 #Same for Both HW and AZP
                 
                 # Logging lists of deformation behaviour for plotting on each profeil plot
                 CenterDeflection, Alphas, Coordlengths, = [],[],[]
                 Warping,WarpingT,WarpingB,blobbing= [],[],[],[]
                 
                 CurcentProfilePlots, FlatProfilePlots=[],[]                
                 CLplot = []
                 NCLplot = []
                 #Hvor langt extra den linja på CL?
                 Chordline_ext = 15.0
                 
                 CLcenterMark = []
                 WarpPointsPlotting=[]
                 #Prep profile plots
                 for p in Inter:
                     ProfXs = PlotData[:,p[0]]
                     ProfYs = PlotData[:,p[1]]
                     CurcentProfilePlots.append([ProfXs,ProfYs,s[Inter.index(p)]+j[Inter.index(p)]])
                     
                     #Linear regression for chordline
                     m,y = np.polyfit(np.array(Coordline[Inter.index(p)])[:,1],Coordline[Inter.index(p)][:,0],1)
                     
                     #Lag X-axis for choordline
                     xmin=np.min(Coordline[Inter.index(p)][:,1])
                     xmax=np.max(Coordline[Inter.index(p)][:,1])
                     
                     #Plot chordline with CenterMark
                     Xline=np.linspace(xmin-abs(Chordline_ext*(xmax-xmin)/100),xmax+abs(Chordline_ext*(xmax-xmin)/100),10)
                     CLx=(xmin+xmax)/2
                     CLy=m*(xmin+xmax)/2+y
                     CLcenterMark.append([CLx,CLy, 'bx'])
                     CLplot.append([Xline, m*Xline + y,':']) 
                     
                     #Save chordline angle, defelction and coordline change                    
                     Alphas.append(math.atan2(m,1)*180/math.pi)
                     CenterDeflection.append([np.average(PlotData[:,p[0]]),np.average(PlotData[:,p[1]])])
                     Choord_length= math.sqrt((Radi[maal]*radius*np.array(Coordline[Inter.index(p)])[1,0]-Radi[maal]*radius*np.array(Coordline[Inter.index(p)])[0,0])**2+(Coordline[Inter.index(p)][1,2]-Coordline[Inter.index(p)][0,2])**2)                    
                     Coordlengths.append(Choord_length)
                     
                     #Warp Calculation
                     #Find normal
                     
                     NM = -1/m
                     Ny = m*(xmin+xmax)/2+y-NM*(xmin+xmax)/2
                     NCLplot.append([Xline,NM*Xline+Ny,'-']) #    """LIST ADD - Normal too chordline"""
                     
                     #Orient data
                     WarpPoints = np.transpose([PlotData[:,p[0]],PlotData[:,p[1]]])
                     #Rotate pointcloud to flat
                     RWP =[]
                     for point in WarpPoints:
                          RWP.append(plottts.rotate([(xmin+xmax)/2,m*(xmin+xmax)/2+y], point, -math.atan2(m,1)))
                     #PICK RELEVASNT POINTS #Filter through tolerance
                     tol =5 #Ca half char element size
                     RelevantPoints=  []
                     for point in RWP:                     
                          Xref =(xmin+xmax)/2
                          if point[0] > Xref-tol:
                               if point[0] < Xref+tol:
                                    #print(RWP[RWP.index(point)][0])
                                    RelevantPoints.append([RWP[RWP.index(point)][0],RWP[RWP.index(point)][1]])
                     print('Filter = ',len(RelevantPoints), ' of ',len(RWP) )
                             
                     #Is in the top points or bottom?
                     CLdists =[]
                     for Coords in np.array(RelevantPoints)[:,0:2]:
                          CLdists.append(math.sqrt((Coords[0]-(xmin+xmax)/2)**2+ (Coords[1]-m*(xmin+xmax)/2+y)**2))
                     SnittDist = np.mean(CLdists)
     
                     Botpoints=[]
                     TopPoints=[]
     
                     for Coords in range(0,len(CLdists)):
                          if CLdists[Coords]<SnittDist:
                               Botpoints.append(RelevantPoints[Coords])
                          else:
                               TopPoints.append(RelevantPoints[Coords])
                     
                     
                     #Find Excact warppoints?
                     A = (CLx, CLy + 200)
                     B = (CLx, CLy- 200)
                     
                     for i in range(len(TopPoints)):
                         if len(TopPoints)==2:
                              E = (TopPoints[0][0], TopPoints[0][1])
                              F = (TopPoints[1][0], TopPoints[1][1])
                              warp_point_top = plottts.line_intersection((A, B), (E, F))
                         elif len(TopPoints)>2:
                              E = (TopPoints[0][0], TopPoints[0][1])
                              F = (TopPoints[1][0], TopPoints[1][1])
                              warp_point_top1 = plottts.line_intersection((A, B), (E, F))
                              E = (TopPoints[2][0], TopPoints[2][1])
                              F  = (TopPoints[1][0], TopPoints[1][1])
                              warp_point_top2 = plottts.line_intersection((A, B), (E, F))
                              if warp_point_top2 == 'lines do not intersect':
                                   warp_point_top = warp_point_top1
                              elif warp_point_top1 == 'lines do not intersect':
                                   warp_point_top = warp_point_top2
                              elif warp_point_top1 == 'lines do not intersect' and warp_point_top2 == 'lines do not intersect':
                                   print(warp_point_top1)
                              else:
                                   warp_point_top = warp_point_top1
                     
                     for i in range(len(Botpoints)):
                         if len(Botpoints)==2:
                              E = (Botpoints[0][0], Botpoints[0][1])
                              F = (Botpoints[1][0], Botpoints[1][1])
                              warp_point_bot = plottts.line_intersection((A, B), (E, F))
                         elif len(Botpoints)>2:
                              E = (Botpoints[0][0], Botpoints[0][1])
                              F = (Botpoints[1][0], Botpoints[1][1])
                              warp_point_bot1 = plottts.line_intersection((A, B), (E, F))
                              E = (Botpoints[2][0], Botpoints[2][1])
                              F = (Botpoints[1][0], Botpoints[1][1])
                              warp_point_bot2 = plottts.line_intersection((A, B), (E, F))
                              if warp_point_bot2 == 'lines do not intersect':
                                   warp_point_bot = warp_point_bot1
                              elif warp_point_bot1 == 'lines do not intersect':
                                   warp_point_bot = warp_point_bot2
                              elif warp_point_bot1 == 'lines do not intersect' and warp_point_bot2 == 'lines do not intersect':
                                   print(warp_point_bot1)
                              else:
                                   warp_point_bot = warp_point_bot1
                     
                     #Show WarpLine Points
                     #Translate/Roatae back to real posistoin
                     
                     warp_point_topPlots = plottts.rotate((CLx,CLy),(warp_point_top),math.atan2(m,1))
                     warp_point_botPlots = plottts.rotate((CLx,CLy),(warp_point_bot),math.atan2(m,1))
                     #print(warp_point_botPlots, warp_point_topPlots)
                     WarpPointsPlotting.append([[warp_point_botPlots[0],warp_point_topPlots[0]],[warp_point_botPlots[1],warp_point_topPlots[1]],'m*'])
                     #WarpPointsPlotting.append([[warp_point_top[0],warp_point_topPlots[0]],[warp_point_botPlots[1],warp_point_topPlots[1]],'m*'])
                     WarpTOP=warp_point_top[1]-CLy
                     WarpBOT=warp_point_bot[1]-CLy
                     Warp=(WarpTOP+WarpBOT)/2
                     Blob=warp_point_top[1]-warp_point_bot[1]
                     blobbing.append(warp_point_top[1]-warp_point_bot[1])
                     WarpingT.append(WarpTOP)
                     WarpingB.append(WarpBOT)
                     Warping.append(Warp)
                     #print('Warp',Warp,'blob',Blob)
                     #For å plotte profilene helt som flate plots av flat profil
                     
                     #RW=np.transpose(RWP)
                     #FlatProfilePlots.append([RW[0],RW[1],s[Inter.index(p)]+j[Inter.index(p)]])
                                               
                 #Find change  angle 
                 deltaDeflec= ((CenterDeflection[1][0]-CenterDeflection[0][0])**2+(CenterDeflection[1][1]-CenterDeflection[0][1])**2)**0.5
                 deltaAlfa= Alphas[1]-Alphas[0]
                 deltaCoordchange= Coordlengths[1]-Coordlengths[0]
                 deltaWarp= Warping[1]-Warping[0]
                 dekWarpingT= WarpingT[1]-WarpingT[0]
                 dekWarpingB= WarpingB[1]-WarpingB[0]
                 deltaBlob= blobbing[1]-blobbing[0]
                 delta_U.append(deltaDeflec)
                 delta_A.append(deltaAlfa)
                 A_for_U.append(deltaAlfa/deltaDeflec)
                 delta_W.append(deltaWarp)  
                 W_for_U.append(deltaWarp/deltaDeflec)
                 
                 #Plottinga av srofile Subplots 
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
                      axs[0, maal].plot(cl[0],cl[1],cl[2])
                      axs[0, maal].plot(ncl[0],ncl[1],ncl[2])
                      axs[0, maal].plot(clM[0],clM[1],clM[2])
                      axs[0, maal].plot(wpp[0],wpp[1],wpp[2])
                 axs[0, maal].set_xlim([-300, 250])
                 axs[0, maal].set_ylim([-225, 325])
                
                 # Preparere Legends
                 extraString = '\u0394' + '\u03B1' + ' = ' + str("%.4f" % deltaAlfa)
                 handles, labels = axs[0, maal].get_legend_handles_labels()
                 handles.append(mpatches.Patch(color='none', label=extraString))
                 extraStringss2 = '\u0394' + 'W' + ' = ' + str("%.4f" % deltaWarp)
                 handles.append(mpatches.Patch(color='none', label=extraStringss2))
                 extraStrings22 = '\u0394' + 'Wt,Wb' + ' = ' + str("%.4f" % dekWarpingT)+', '+str("%.4f" % dekWarpingB)
                 handles.append(mpatches.Patch(color='none', label=extraStrings22))
                 extraString2 = '\u0394' + 'CL' + ' = ' + str("%.4f" % deltaCoordchange)
                 handles.append(mpatches.Patch(color='none', label=extraString2))
                 extraString3 = '\u0394' + 'Blob' + ' = ' + str("%.4f" % deltaBlob)
                 handles.append(mpatches.Patch(color='none', label=extraString3))
                 # Plotte Legends
                 axs[0, maal].legend(handles=handles, loc='best', fontsize=9)
                 
             spenn_delU.append(delta_U)
             spenn_delA.append(delta_A)
             spenn_AfU.append(A_for_U)
             spenn_delW.append(delta_W)
             
             #Andre rad - Maa oppdateres med nye plot når warp er satt opp
             ploo=[delta_U,delta_A,A_for_U,delta_W,W_for_U]
             pli= ['\u0394_Deflection of center','\u0394_Alpha of coordline','\u0394_Alpha per \u0394_deflection',
                   '\u0394_Avg-Warp','\u0394_Avg-Warp per \u0394_deflection']
             #        Xlim         Ylims
             a = [([0,1]  , [-50, 50]),
                  ([0,1]  , [-10, 10]),
                  ([0,1]  , [-1, 1]),
                  ([0,1]  , [-10, 10]),
                  ([0,1]  , [-1, 1])]
                  
             for plo in range(0,5):
                 #Plot profile
                 axs[1, plo].plot(Radi,ploo[plo])  
                 axs[1, plo].set_xlabel('Radius length')
                 axs[1, plo].set_ylabel(pli[plo])
                 axs[1, plo].set_xlim(a[plo][0])
                 axs[1, plo].set_ylim(a[plo][1])
                 #Subplot title
                 axs[1, plo].title.set_text(pli[plo])
     
     
             fig.tight_layout()
             plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.91, wspace=None, hspace=0.3)  
             #plt.savefig(plot_path+u[:-4]+'.png')
             np.savez(plot_path,
                      spenn_delU=spenn_delU,
                      spenn_delA=spenn_delA,
                      spenn_delW =spenn_delW,
                      radz=Radi)
             plt.savefig('D:\\PhD\\Simuleringer\\HW_plots\\'+u[:-4]+'.png')
             plt.close()
        except:
             try:
                  plt.close()
             except:
                  pass
             FuckedList.append(u)
             pass
print(FuckedList)