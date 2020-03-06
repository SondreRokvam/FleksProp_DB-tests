def Layup(model, part_name, part_type):
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior

    ratio_list = [100, 75, 50, 25, 10, 1, 10, 25, 50, 75, 100]
    for i in range(len(ratio_list)):
        if i > 0:
            model.parts[part_name].compositeLayups['Layup-'+material_name].suppress()
        # --------------------Material--------------------
        ratio = ratio_list[i]
        if i <= (len(ratio_list)-1)/2:
            E1 = 140000
            E2 = E1 / ratio
            material_name = 'CF-R-E1_E2_' + str(ratio)
        elif i > (len(ratio_list)-1)/2:
            E2 = 140000
            E1 = E2 / ratio

            material_name = 'CF-R-E2_E1_' + str(ratio)

        model.Material(name=material_name)
        model.materials[material_name].Elastic(type=ENGINEERING_CONSTANTS,
                                         table=((E1, E2, 10000,      # E1, E2, E3
                                                 0.02, 0.3, 0.3,                 # v12, v13, v23
                                                 3500, 3300, 3300),))       # G12, G13, G23

        #-------------------------------LAYUP------------------------------------------------

        #---------------------Layup-------------------------
        layupOrientation= None
        p = model.parts[part_name]
        f = p.faces
        region1=regionToolset.Region(faces=f)

        p = model.parts[part_name]
        s = p.faces
        normalAxisRegion = p.Surface(side1Faces=s, name='Normal_Axis_Region')
        p = model.parts[part_name]
        e = p.edges
        edges = e.getSequenceFromMask(mask=('[#20 ]',), )
        primaryAxisRegion = p.Set(edges=edges, name='Primary_Axis_Region')
        compositeLayup = model.parts[part_name].CompositeLayup(name='Layup-'+material_name,
                                                               description='',
                                                               elementType=SHELL,
                                                               offsetType=TOP_SURFACE,
                                                               symmetric=False,
                                                               thicknessAssignment=FROM_SECTION)
        compositeLayup.Section(preIntegrate=OFF,
                               integrationRule=SIMPSON,
                               thicknessType=UNIFORM,
                               poissonDefinition=DEFAULT,
                               temperature=GRADIENT,
                               useDensity=OFF)

        compositeLayup.CompositePly(suppressed=False,
                                    plyName='Ply-1',
                                    region=region1,
                                    material=material_name,
                                    thicknessType=SPECIFY_THICKNESS,
                                    thickness=5.0,
                                    orientationType=SPECIFY_ORIENT,
                                    orientationValue=0.0,
                                    additionalRotationType=ROTATION_NONE,
                                    additionalRotationField='',
                                    axis=AXIS_3,
                                    angle=0.0,
                                    numIntPoints=3)
        compositeLayup.ReferenceOrientation(orientationType=DISCRETE,
                                            localCsys=None,
                                            additionalRotationType=ROTATION_NONE,
                                            angle=0.0,
                                            additionalRotationField='',
                                            axis=AXIS_3,
                                            stackDirection=STACK_3,
                                            normalAxisDefinition=SURFACE,
                                            normalAxisRegion=normalAxisRegion,
                                            normalAxisDirection=AXIS_3,
                                            flipNormalDirection=False,
                                            primaryAxisDefinition=EDGE,
                                            primaryAxisRegion=primaryAxisRegion,
                                            primaryAxisDirection=AXIS_1,
                                            flipPrimaryDirection=True)

        p = model.parts[part_name]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)

        # -----------------Load--------------------------------------
        model.loads['Load-1'].setValues(distributionType=FIELD)

        # ------------------JOB------------------------------------
        job = 'Job-' + material_name
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
            meshTechnique=OFF)

        mdb.Job(name=job,
                model='Model-1',
                description='',
                type=ANALYSIS,
                atTime=None,
                waitMinutes=0,
                waitHours=0,
                queue=None,
                memory=90,
                memoryUnits=PERCENTAGE,
                getMemoryFromAnalysis=True,
                explicitPrecision=SINGLE,
                nodalOutputPrecision=SINGLE,
                echoPrint=OFF,
                modelPrint=OFF,
                contactPrint=OFF,
                historyPrint=OFF,
                userSubroutine='',
                scratch='',
                resultsFormat=ODB,
                multiprocessingMode=DEFAULT,
                numCpus=1,
                numGPUs=0)
        mdb.jobs[job].submit(consistencyChecking=OFF)
        mdb.jobs[job].waitForCompletion()

Layup(model, part_name, part_type)