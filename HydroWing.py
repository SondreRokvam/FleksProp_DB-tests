from abaqus import *
from abaqus import getInput
from abaqus import getInputs
from abaqusConstants import *
import __main__
import time
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
import os
import numpy as np

class HydroWing:
    def __init__(self, cae_file_path):
        self.cae_file_path = cae_file_path

    def all_over(self, angles, thickness, input_file_location):
        os.chdir(input_file_location)
        input_folder_name = getInput('Enter name for folder containing input files: ')
        if not os.path.exists(input_folder_name):
            os.mkdir(input_folder_name)
            print("Directory " , input_folder_name ,  " Created ")
            os.chdir(input_folder_name)
        else:
            print("Directory " , input_folder_name ,  " already exists")
            os.chdir(input_folder_name)
            return

        for angle in angles:
            try:
                openMdb(pathName=self.cae_file_path)
                p = mdb.models['Model-1'].parts['HW']

                #--------------- Materials -------------------------------------
                mdb.models['Model-1'].Material(name='CF')
                mdb.models['Model-1'].Material(name='Foam')
                mdb.models['Model-1'].materials['CF'].Elastic(type=ENGINEERING_CONSTANTS,
                        table=((130000.0, 10000.0, 10000.0, 0.2, 0.2, 0.4, 4000.0, 4000.0,
                        3000.0), ))
                mdb.models['Model-1'].materials['Foam'].Elastic(type=ISOTROPIC,
                        table=((300,0.3), ))


                #---------------- Section ----------------------------------------
                sectionLayer1 = section.SectionLayer(material='CF', thickness=thickness,
                    orientAngle=angle, numIntPts=3, plyName='')
                mdb.models['Model-1'].CompositeShellSection(name='CF', preIntegrate=OFF,
                    idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM,
                    poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                    useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

                mdb.models['Model-1'].HomogeneousSolidSection(name='Foam',
                    material='Foam', thickness=None)

                # --------------- Assignment ----------------------------------------
                cells = p.cells
                region = p.Set(cells=cells, name='Set-1')
                p.SectionAssignment(region=region, sectionName='Foam', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
                faces = p.faces
                p.Skin(faces=faces, name='Skin-1')
                region = p.Set(skinFaces=(('Skin-1', faces), ), name='Set-4')
                p.SectionAssignment(region=region, sectionName='CF', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)


                # ----------------- Orientation -------------------------------------
                s = p.faces
                edge = p.edges.getByBoundingBox(-1000,-1000,249,1000,1000,251)
                normalAxisRegion = p.Surface(side1Faces=s, name='Normal_Axis_Region')
                primaryAxisRegion = p.Set(edges=edge, name='Primary_Axis_Region')
                mdb.models['Model-1'].parts['HW'].MaterialOrientation(region=region,
                    orientationType=GLOBAL, axis=AXIS_1,
                    additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='')

                """
                mdb.models['Model-1'].parts['HW'].MaterialOrientation(region=region,
                    orientationType=DISCRETE, axis=AXIS_3, normalAxisDefinition=SURFACE,
                    normalAxisRegion=normalAxisRegion, flipNormalDirection=False,
                    normalAxisDirection=AXIS_3, primaryAxisDefinition=EDGE,
                    primaryAxisRegion=primaryAxisRegion, primaryAxisDirection=AXIS_2,
                    flipPrimaryDirection=False, additionalRotationType=ROTATION_NONE,
                    angle=0.0, additionalRotationField='')
                """

                # ----------------- Skin Mesh ----------------------------------------

                elemType1 = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)
                elemType2 = mesh.ElemType(elemCode=STRI65, elemLibrary=STANDARD)
                a = mdb.models['Model-1'].rootAssembly
                f1 = a.instances['HW-1'].faces
                pickedRegions = regionToolset.Region(skinFaces=(('Skin-1', f1), ))
                a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

                # ------------------ Job ----------------------------------------------
                name = 'HWAllOver_' + str(int(angle))
                print(name)
                mdb.Job(name=name, model='Model-1', description='', type=ANALYSIS,
                    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
                    numGPUs=0)
                mdb.jobs[name].writeInput(consistencyChecking=OFF)
                mdb.close()
            except:
                pass

