if 1: #AzP lead/trail punkter
    Leadnodes=[[88.140249,-198.797325,257.108194],
               [57.111528,-267.042178,284.233135],
               [26.214503,-343.738199,298.109126],
               [-6.368028,-429.953069,292.472833],
               [-46.696491,-530.173661,247.266837]]

    Trailnodes =[[-282.872286,-322.146479,-42.972622],
                [-291.328316,-382.15225,-77.843804],
                [-286.225663,-442.58725,-105.553427],
                [-270.14662,-504.497972,-126.022999],
                 [-236.240842,-571.887303,-123.166197] ]
execfile('C:/MultiScaleMethod/Github/FleksProp_DB-tests/Initiate.py')
# ODB PATH
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\AzP'       # Overmappe for massetestene
# Os walk to get files, roots and
execfile('C:/MultiScaleMethod/Github/FleksProp_DB-tests/Find_inpNodb_N_Make_differnceList.py')
# Extract from odb paths
if (inps-len(fuckedlist))>0:
    for gofor in Inp_folders:
        # Give odb_path
        odb_path = gofor[0]
        # create NPZ PATH
        npz_path = odb_path + '\\npz_files'
        try:
            os.mkdir(npz_path)  # Create target Directory
            #print("Directory ", npz_path, " Created ")
        except:
            #print("Directory ", npz_path, " already exists")
            pass

        # Hent resultatfiler i mappen
        odb_names = [f for f in os.listdir(odb_path) if (f.endswith('.odb') and not "1000" in f.lower())]
        for i in odb_names:
            Mdb()
            #try:
            if 1:
                print '\n              Attepting extraction from: ', odb_path + '\\' + i
                odb = session.openOdb(name=odb_path + '\\' + i)
                Measurementnames= ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
                #print i
                if not "CFD" in i:
                    Measurements = ['PROFILE-R_5', 'PROFILE-R_6', 'PROFILE-R_7', 'PROFILE-R_8', 'PROFILE-R_9']
                    nodplace =odb.rootAssembly
                else:
                    Measurements = ['R250', 'R300', 'R350', 'R400', 'R450']
                    nodplace =odb.rootAssembly.instances['HYDROWINGTOPLEADING-1-1']

                for profile in Measurements:
                    #print profile
                    dots_cyl_langs_x = []
                    dots_cyl_langs_xm =[]

                    if not "CFD" in i:
                        AllNodes = nodplace.nodeSets[profile].nodes[0]
                    else:
                        AllNodes = nodplace.nodeSets[profile].nodes
                    Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                        region=nodplace.nodeSets[profile]).values

                    find_dis_trail_nodes = []
                    find_dis_lead_nodes = []

                    Acount= 0
                    for nod in AllNodes:
                        x = float(nod.coordinates[0])           #Initial position of node
                        y = float(nod.coordinates[1])
                        z = float(nod.coordinates[2])
                        xm = float(Disp[Acount].data[0])        #Displacement of node
                        ym= float(Disp[Acount].data[1])
                        zm= float(Disp[Acount].data[2])

                        # measure coordline nodes
                        trailpoint = Trailnodes[Measurements.index(profile)]
                        leadpoint = Leadnodes[Measurements.index(profile)]
                        find_dis_trail_nodes.append(round(math.sqrt((x - trailpoint[0]) ** 2 + (y - trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2), 8))
                        find_dis_lead_nodes.append(round(math.sqrt((x - leadpoint[0]) ** 2 + (y - leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2), 8))


                        Acount = Acount + 1  # Manual counter

                        # Find angular value due to cylinder coordinates
                        ang = math.atan2(y , z)+math.pi
                        angm = math.atan2((y+ym) , (z+zm))+math.pi
                        AvgRad=((((y) ** 2 + (z) ** 2) ** 0.5)*(((y+ym)**2+(z+zm)**2)**0.5))/2.0
                        #                        Cylinder height   Angle width *Radius                      Radius
                        dots_cyl_langs_x.append( [x ,              ang*((y) ** 2 + (z) ** 2) ** 0.5,        ((y) ** 2 + (z) ** 2) ** 0.5])
                        dots_cyl_langs_xm.append([x+xm,            angm*((y+ym)**2+(z+zm)**2)**0.5,                             ((y+ym)**2+(z+zm)**2)**0.5])

                    #Identify coordline nodes
                    minTrail_dist = np.min(find_dis_trail_nodes)
                    minLead_dist = np.min(find_dis_lead_nodes)
                    index_minTrail = find_dis_trail_nodes.index(minTrail_dist)
                    index_minLead = find_dis_lead_nodes.index(minLead_dist)

                    undefCoordline = [dots_cyl_langs_x[index_minTrail], dots_cyl_langs_x[index_minLead]]
                    defCoordline = [dots_cyl_langs_xm[index_minTrail], dots_cyl_langs_xm[index_minLead]]

                    #Save for plotting
                    np.savez(npz_path+'\\Cylinder view of '+profile+' for '+i[:-4],
                             profile_undeformed = np.array( dots_cyl_langs_x),
                             profile_deformed=np.array( dots_cyl_langs_xm) ,
                             profile_undefcoordline=undefCoordline,
                             profile_defcoordline=defCoordline)
                print    '              Worked for :        ' + i[:-4] + '        in :        ', gofor, '\n\n'
                odb.close()
            #except:
            #    try:
            #        odb.close()
            #    except:
            #        pass
            #    print '              Didnt Work for :    ' + i[:-4] + '        in :        ', gofor, '\n\n'
            #    fuckedlist.append([gofor, i])
            #    print '          Added to redo-list\n\n'
            #    pass
execfile('C:/MultiScaleMethod/Github/FleksProp_DB-tests/Write_Launcher_N_Overview.py')