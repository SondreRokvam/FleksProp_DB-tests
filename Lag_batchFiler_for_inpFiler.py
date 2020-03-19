"""
Created on Wed Mar 11 16:39:31 2020

@author: sondreor
"""
import os

os.chdir('C:\\Users\\Sondre\\Desktop\\HW\\')

current=os.getcwd()
print(current+'\\')
# Hent
for g in os.listdir(current):
    odb_names = [f for f in os.listdir(current+'\\'+g+'\\') if (f.endswith('.inp')) ]
    s=open(current+'\\'+g+'\\'+'run_inputs.bat',"w+")
    for od in odb_names:
        s.write('call abq2017 job='+od[:-4]+ ' int\n')
    s.close()