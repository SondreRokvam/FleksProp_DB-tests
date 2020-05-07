"""
Created on Wed Mar 11 16:39:31 2020
@author: sondreor
"""
import os
Desk='C:/Users/Sondre/Desktop/'

#Set mappe directory

#Mass quantify Tests
#os.chdir('D:/PhD/Simuleringer/AzP')
os.chdir(Desk+'MassTests/Mass_Tests-HW')
os.chdir(Desk+'MassTests/Mass_Tests-AzP')

#Qualify Tests
os.chdir(Desk+'Single_Simulations/')
os.chdir(Desk+'Single_Simulations/Mecanical aspects/Force Scaling Azp')
current=os.getcwd()                                       

odb_names = [f for f in os.listdir(current) if (f.endswith('.inp')) ]
s=open(current+'\\run_inputs.bat',"w+")
for od in odb_names:
     s.write('call abq2017 job=\"'+od[:-4]+ '\" int\n')
s.close()
