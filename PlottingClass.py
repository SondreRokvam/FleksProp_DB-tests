# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 13:21:24 2020

@author: sondreor
"""
import os
import numpy as np
import operator
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
            
    