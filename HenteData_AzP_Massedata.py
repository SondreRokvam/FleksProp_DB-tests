print 'HenteData'
if 1: #AzP lead/trail punkter
    Leadnodes=  [[88.140251,-198.797333,257.108185],
               	 [72.609589,-231.798492,272.168518],
               	 [57.111526,-267.042175,284.233124],
               	 [41.653526,-304.398315,292.998169],
               	 [26.214502,-343.73819,298.109131],
               	 [10.324939,-385.480377,298.431122],
               	 [-6.368028,-429.953064,292.472839],
               	 [-24.538908,-477.645782,277.688263],
               	 [-46.696491,-530.173645,247.26683],
               	 [-76.464775,-587.882629,188.94519],
               	 [-132.20723,-647.919617,48.496048]]

    Trailnodes =[[-282.872284,-322.146484,-42.972622],
                    [-289.217621,-352.204224,-61.306122],
                    [-291.328308,-382.152252,-77.843803],
                    [-290.203033,-412.236786,-92.558594],
                    [-286.225677,-442.58725,-105.553429],
                    [-279.586548,-473.282013,-116.87767],
                    [-270.146667,-504.497986,-126.02298],
                    [-256.404358,-536.900452,-130.361664],
                    [-236.24086,-571.887329,-123.166191],
                    [-206.038391,-610.488525,-92.790321],
                    [-146.371887,-649.578003,14.1441]]
execfile('C:/MultiScaleMethod/Github/FleksProp_DB-tests/Initiate.py')
# ODB PATH
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\AzP_Particular'       # Overmappe for massetestene
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
#                print '\n              Attepting extraction from: ', odb_path + '\\' + i
                odb = session.openOdb(name=odb_path + '\\' + i)
                Measurementnames= ['PROFILE-R_5', 'PROFILE-R_55', 'PROFILE-R_6', 'PROFILE-R_65', 'PROFILE-R_7', 'PROFILE-R_75', 'PROFILE-R_8', 'PROFILE-R_85', 'PROFILE-R_9', 'PROFILE-R_95','PROFILE-R1']
                #print i
                if not "CFD" in i:
                    Measurements = ['PROFILE-R_5', 'PROFILE-R_55', 'PROFILE-R_6', 'PROFILE-R_65', 'PROFILE-R_7', 'PROFILE-R_75', 'PROFILE-R_8', 'PROFILE-R_85', 'PROFILE-R_9', 'PROFILE-R_95','PROFILE-R1']
                    nodplace =odb.rootAssembly
                else:
                    Measurements = ['R250', 'R300', 'R350', 'R400', 'R450']
                    nodplace =odb.rootAssembly.instances['HYDROWINGTOPLEADING-1-1']

                for profile in Measurements:
                    #print profile
                    dots_cyl_langs_x = []
                    dots_cyl_langs_xm =[]
                    AllNodes= []
                    for nodes in nodplace.nodeSets[profile].nodes:
#                         print nodes
                         for node in nodes:
                              AllNodes.append(node)
                    Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                        region=nodplace.nodeSets[profile]).values
#                    print AllNodes
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