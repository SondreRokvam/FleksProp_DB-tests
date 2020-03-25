"""
Created on Wed Mar 11 16:39:31 2020

@author: sondreor
"""
import os

os.chdir('C:\\Users\\Sondre\\Desktop\\azp\\')

current=os.getcwd()
print(current+'\\')
# Hent
Batpaths =[]
for g in [f for f in os.listdir(current) if not f.endswith('.bat')]:
    odb_names = [f for f in os.listdir(current+'\\'+g+'\\') if (f.endswith('.inp')) ]
    s=open(current+'\\'+g+'\\'+'run_inputs.bat',"w+")
    Batpaths.append(current+'\\'+g+'\\'+'run_inputs.bat')
    for od in odb_names:
        s.write('call abq2017 job='+od[:-4]+ ' int\n')
    s.close()
"""
p=open(current+'\\batch.bat',"w+")
for bat in Batpaths:
    p.write('call '+bat+'\n')
p.close()"""