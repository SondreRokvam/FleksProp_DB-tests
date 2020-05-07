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
            print("Directory " , path ,  " Created ") 
        except:
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