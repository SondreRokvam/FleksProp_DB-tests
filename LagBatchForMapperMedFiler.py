"""
Created on Wed Mar 11 16:39:31 2020
@author: sondreor
"""
import os
def delBatchs(folder):
     Bat_file = [b for b in os.listdir(folder) if not b.endswith('.inp') ]
     for f in Bat_file:
          try:
             os.remove(os.path.join(folder, f))
          except:
             pass

def createBATforINPs(path):
     inp_names = [f for f in os.listdir(path) if (f.endswith('.inp')) ]
     indBATs=[]
     for od in inp_names:
          inpbatch = path+'\\'+'BAT'+od[:-4]+ '.bat'
          s=open(inpbatch,"w+")
          indBATs.append(inpbatch)
          s.write('call abq2017 job=\"'+od[:-4]+ '\" int\n')
          s.close()
     folderlauncher=path+'\\'+'BATs.bat'
     p=open(folderlauncher,"w+")
     for BAT in indBATs:
          p.write('call "'+BAT+'"\n')
     p.close()
     return folderlauncher


#Set mappe directory
Desk='C:/Users/Sondre/Desktop/'
os.chdir(Desk+'MassTests/Mass_HW_7degs')
#os.chdir(Desk+'Single_Simulations/Mecanical aspects')
current=os.getcwd() 
Bat_file = [b for b in os.listdir(current) if b.endswith('.bat') ]
for f in Bat_file:
     try:
        os.remove(os.path.join(current, f))
     except:
        pass
#Mass quantify - Parento tests
#Os walk to get files, roots and 
BAtfiles=[]
for root, dirs, files in os.walk(current, topdown=False):
     for name in dirs:
          name = os.path.join(root, name)
          delBatchs(name) 
          inplist= [a for a in os.listdir(name) if a.endswith('.inp')]
          if len(inplist)>0:
               BAtfiles.append([name,createBATforINPs(name)])

p=open(current+'\\Launcher.bat',"w+")
for BAT in BAtfiles:
     print ('chdir "'+BAT[0]+'"\ncall "'+BAT[1]+'"\n')
     p.write('chdir "'+BAT[0]+'"\nTIMEOUT /T 1\ncall "'+BAT[1]+'"\nTIMEOUT /T 1\n')
p.close()            
                         
                         
                    
                    
               