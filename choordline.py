# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 23:18:19 2020

@author: sondreor
"""
import numpy as np
Measurementes = [s for s in np.array(mdb.models['Model-1'].rootAssembly.sets.items())[:,0] if (s.startswith('PROFILE-R'))]
#Profile names
if 0:#AzP
    Leadnodes=[[-46.696491,-530.173661,247.266837],
               [-6.368028,-429.953069,292.472833],
               [26.214503,-343.738199,298.109126],
               [57.111528,-267.042178,284.233135],
               [88.140249,-198.797325,257.108194]]

    Trailnodes =[[-236.240842,-571.887303,-123.166197],
                [-270.14662,-504.497972,-126.022999],
                [-286.225663,-442.58725,-105.553427],
                [-291.328316,-382.15225,-77.843804],
                [-282.872286,-322.146479,-42.972622]]
if 1:#Hw
    Leadnodes = [[-921.988E-03, -188.362272, 250.],
                [-3.708949, -217.378003, 300.],
                [-5.258573, -225.280987, 350.],
                [-4.852153, -202.093218, 400.],
                [-1.732931, -130.598882, 450.]]

    Trailnodes = [[-8.408669,121.885101,250.],
               [-7.139085,140.092972,300.],
               [-3.541321,162.555817,350.],
               [3.404349,191.702759,400.],
               [15.057261,225.33374,450.]]

for nod in range(0, 5):
    nid =mdb.models['Model-1'].rootAssembly.instances['HydroWingTopLeading-1'].nodes.getByBoundingSphere(center=(Trailnodes[nod][0],Trailnodes[nod][1],Trailnodes[nod][2],),radius=1.0)
    mdb.models['Model-1'].rootAssembly.Set(name=Measurementes[nod]+'_trailing_point', nodes=nid)
    nid =mdb.models['Model-1'].rootAssembly.instances['HydroWingTopLeading-1'].nodes.getByBoundingSphere(center=(Leadnodes[nod][0],Leadnodes[nod][1],Leadnodes[nod][2],),radius=1.0)
    mdb.models['Model-1'].rootAssembly.Set(name=Measurementes[nod]+'_leading_point', nodes=nid)
    