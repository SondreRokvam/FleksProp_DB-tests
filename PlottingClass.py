# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 13:21:24 2020

@author: sondreor
"""
import os
import numpy as np
import operator
import math

class plottts:
     def __init__(self):
          pass
    
     def Top_bottom_warpPoints(tolran,REL_Points_rotated,XMI,XMA,CooLiX,CooliY,mama,yaya):
          #print(len(REL_Points_rotated))
          RelevantPoints=  []
          Xref =(float(XMI+XMA)/2)
          
          for point in REL_Points_rotated:
               #print('is ', Xref+tolran,' < ',point[0],' > ', Xref-tolran)                      
               if point[0] > Xref-tolran:
                    if point[0] < Xref+tolran:
                         #print(REL_Points_rotated[REL_Points_rotated.index(point)][0])
                         RelevantPoints.append([REL_Points_rotated[REL_Points_rotated.index(point)][0],REL_Points_rotated[REL_Points_rotated.index(point)][1]])
          #print('Filter = ',len(RelevantPoints), ' of ',len(REL_Points_rotated) )
          #Is in the top points or bottom?
          CLdists =[]
          #print(np.array(RelevantPoints))
          for Coords in RelevantPoints:
               CLdists.append(math.sqrt((Coords[0]-(XMI+XMA)/2)**2+ (Coords[1]-mama*(XMI+XMA)/2+yaya)**2))
          SnittDist = np.mean(CLdists)
          
          Botpoints=[]
          TopPoints=[]
          for Coords in range(len(CLdists)):
               if CLdists[Coords]<SnittDist:
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
                    cool =pospoints[0:1]
                    for pop in pospoints[1:]:
                         if pop[0]<cool[0][0]:
                              cool=[pop]
                    pospoints=cool
               if len(negpoints)>1:
                    cool =negpoints[0:1]
                    for pop in negpoints[1:]:
                         if pop[0]>cool[0][0]:
                              cool=[pop]
                    negpoints=cool
               Botpoints=[negpoints[0],pospoints[0]]
          #print(Botpoints)
          if len(TopPoints)>2:
               relpoints=[]
               for poi in TopPoints:     
                    relpoints.append([poi[0] - Xref,poi[1]])
               pospoints= [sd for sd in relpoints if sd[0]>0]
               negpoints= [sd for sd in relpoints if sd not in pospoints]
               if len(pospoints)>1:
                    cool =pospoints[0:1]
                    for pop in pospoints[1:]:
                         if pop[0]<cool[0][0]:
                              cool=[pop]
                    pospoints=cool
               if len(negpoints)>1:
                    cool =negpoints[0:1]
                    for pop in negpoints[1:]:
                         if pop[0]>cool[0][0]:
                              cool=[pop]
                    negpoints=cool
               TopPoints=[negpoints[0],pospoints[0]]
          #print(TopPoints)
          
          
          #Find Excact warppoints?
          A = (CooLiX, CooliY + 200)
          B = (CooLiX, CooliY- 200)
          #print(len(TopPoints),len(Botpoints))
          for i in range(len(TopPoints)):
               if len(TopPoints)==2:
                    E = (TopPoints[0][0], TopPoints[0][1])
                    F = (TopPoints[1][0], TopPoints[1][1])
                    WAPOTO = plottts.line_intersection((A, B), (E, F))
               elif len(TopPoints)>2:
                    E = (TopPoints[0][0], TopPoints[0][1])
                    F = (TopPoints[1][0], TopPoints[1][1])
                    warp_point_top1 = plottts.line_intersection((A, B), (E, F))
                    E = (TopPoints[2][0], TopPoints[2][1])
                    F  = (TopPoints[1][0], TopPoints[1][1])
                    warp_point_top2 = plottts.line_intersection((A, B), (E, F))
                    if warp_point_top2 == 'lines do not intersect':
                         WAPOTO = warp_point_top1
                    elif warp_point_top1 == 'lines do not intersect':
                         WAPOTO = warp_point_top2
                    elif warp_point_top1 == 'lines do not intersect' and warp_point_top2 == 'lines do not intersect':
                         print(warp_point_top1)
                    else:
                         WAPOTO = warp_point_top1
           
          for i in range(len(Botpoints)):
               if len(Botpoints)==2:
                    E = (Botpoints[0][0], Botpoints[0][1])
                    F = (Botpoints[1][0], Botpoints[1][1])
                    
                    WAPOBO = plottts.line_intersection((A, B), (E, F))
               elif len(Botpoints)>2:
                    E = (Botpoints[0][0], Botpoints[0][1])
                    F = (Botpoints[1][0], Botpoints[1][1])
                    warp_point_bot1 = plottts.line_intersection((A, B), (E, F))
                    E = (Botpoints[2][0], Botpoints[2][1])
                    F = (Botpoints[1][0], Botpoints[1][1])
                    warp_point_bot2 = plottts.line_intersection((A, B), (E, F))
                    if warp_point_bot2 == 'lines do not intersect':
                         WAPOBO = warp_point_bot1
                    elif warp_point_bot1 == 'lines do not intersect':
                         WAPOBO = warp_point_bot2
                    elif warp_point_bot1 == 'lines do not intersect' and warp_point_bot2 == 'lines do not intersect':
                         print(warp_point_bot1)
                    else:
                         WAPOBO = warp_point_bot1     
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
               #print("Directory " , path ,  " already exists")
            
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