odb = session.openOdb(name='D:\PhD\Simuleringer\Modelling_LayUp_vs_DefBehaviour\AZP_Particular\Eiv5\ERV1_1-Blade-2.odb')
prifs= []
for a in range(0,len(odb.rootAssembly.nodeSets.items())):
    if 'profile' in odb.rootAssembly.nodeSets.items()[a][1].name.lower():
        prifs.append(odb.rootAssembly.nodeSets.items()[a][1].name)
prifs.sort()
print prifs