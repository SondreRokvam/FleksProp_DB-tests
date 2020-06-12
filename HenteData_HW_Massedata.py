if 1:  # Hw punkter
    Leadnodes = [[-921.988E-03, -188.362272, 250.],  # r = 0.5
                 [-3.708949, -217.378003, 300.],
                 [-5.258573, -225.280987, 350.],  # r = 0.7
                 [-4.852153, -202.093218, 400.],
                 [-1.732931, -130.598882, 450.]]  # r = 0.9

    Trailnodes = [[-8.408669, 121.885101, 250.],
                  [-7.139085, 140.092972, 300.],
                  [-3.541321, 162.555817, 350.],
                  [3.404349, 191.702759, 400.],
                  [15.057261, 225.33374, 450.]]
execfile('C:/MultiScaleMethod/Github/FleksProp_DB-tests/Initiate.py')
# ODB PATH
Source = 'D:\\PhD\\Simuleringer\\Modelling_LayUp_vs_DefBehaviour\\HW_Particular'       # Overmappe for massetestene
# Os walk to get files, roots and
execfile('C:/MultiScaleMethod/Github/FleksProp_DB-tests/Find_inpNodb_N_Make_differnceList.py')
# Extract from odb path
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
            try:
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
                    dots_XY_langs_Z = []
                    dots_XY_langs_Zm = []
                    if not "CFD" in i:
                        AllNodes = nodplace.nodeSets[profile].nodes[0]
                    else:
                        AllNodes = nodplace.nodeSets[profile].nodes
                    Disp = odb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(
                        region=nodplace.nodeSets[profile]).values

                    find_dis_trail_nodes = []
                    find_dis_lead_nodes = []

                    Acount = 0
                    for nod in AllNodes:
                        x = float(nod.coordinates[0])  # Initial position of node
                        y = -float(nod.coordinates[1])
                        z = float(nod.coordinates[2])
                        xm = float(Disp[Acount].data[0])  # Displacement of node
                        ym = float(Disp[Acount].data[1])
                        zm = float(Disp[Acount].data[2])

                        dots_XY_langs_Z.append([x, y, z])
                        dots_XY_langs_Zm.append([x + xm, y + ym, z + zm])

                        # measure coordline nodes
                        trailpoint = Trailnodes[Measurements.index(profile)]
                        leadpoint = Leadnodes[Measurements.index(profile)]
                        find_dis_trail_nodes.append(
                            round(math.sqrt((x - trailpoint[0]) ** 2 + (y - trailpoint[1]) ** 2 + (z - trailpoint[2]) ** 2),
                                  5))
                        find_dis_lead_nodes.append(
                            round(math.sqrt((x - leadpoint[0]) ** 2 + (y - leadpoint[1]) ** 2 + (z - leadpoint[2]) ** 2),
                                  5))

                        Acount = Acount + 1  # Manual counter

                    # Identify coordline nodes
                    minTrail_dist = np.min(find_dis_trail_nodes)
                    minLead_dist = np.min(find_dis_lead_nodes)
                    index_minTrail = find_dis_trail_nodes.index(minTrail_dist)
                    index_minLead = find_dis_lead_nodes.index(minLead_dist)

                    undefCoordline = [dots_XY_langs_Z[index_minTrail], dots_XY_langs_Z[index_minLead]]
                    defCoordline = [dots_XY_langs_Zm[index_minTrail], dots_XY_langs_Zm[index_minLead]]

                    # Save for plotting
                    np.savez(npz_path + '\\Cartesian view of ' + Measurementnames[Measurements.index(profile)] + ' for ' + i[:-4],
                             profile_undeformed=np.array(dots_XY_langs_Z),
                             profile_deformed=np.array(dots_XY_langs_Zm),
                             profile_undefcoordline=undefCoordline,
                             profile_defcoordline=defCoordline)
                print '              Worked for :        ' + i[:-4] + '        in :        ',gofor,'\n\n'
                odb.close()
            except:
                try:
                    odb.close()
                except:
                    pass
                print '              Didnt Work for :    ' + i[:-4]+ '        in :        ',gofor,'\n\n'
                fuckedlist.append([gofor,i])
                print '          Added to redo-list\n\n'
                pass
execfile('C:\MultiScaleMethod\Github\FleksProp_DB-tests\Write_Launcher.py')