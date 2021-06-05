from pylab import *

X=linspace(-3,3,20)
Y=linspace(-2,3,12)
X,Y=meshgrid(X, Y)


def E(x,y):
    r = 1#sqrt(x**6 + y**6)
    return (x/r,y/r)

def E_dir(x,y):
    #direction field
    print(E(x,y))
    Ex,Ey=E(x,y)
    n=1#sqrt(Ex**2+Ey**2)
    return [Ex/n, Ey/n]

Ex,Ey = E(X,Y)
#Exdir,Eydir = E_dir(X,Y)
EE=10#sqrt(Ex**2+Ex**2)
E
Q  = quiver(X,Y,1,0,EE,cmap='autumn')
#Q  = quiver(X,Y,Exdir,Eydir,EE,cmap='autumn')
show()# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:07:51 2021

@author: Sondre
"""

