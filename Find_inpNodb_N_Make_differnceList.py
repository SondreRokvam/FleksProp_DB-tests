# Os walk to get files, roots and
Inp_folders, inps = [], 0
INPfilS, ODBfilS = [], []
for root, dirs, files in os.walk(Source, topdown=False):
    for name in dirs:
        name = os.path.join(root, name)
        inp_files = [a for a in os.listdir(name) if a.endswith('.inp')]
        Odb_files = [a for a in os.listdir(name) if a.endswith('.odb')]
        if len(inp_files) > 0:
            Inp_folders.append(name.split('\n'))
            INPfilS.append(inp_files)
            inps = inps + len(inp_files)
            ODBfilS.append(Odb_files)
# Re
fuckedlist = []
for sets in INPfilS:
    odbss=ODBfilS[INPfilS.index(sets)]
    fold = Inp_folders[INPfilS.index(sets)]
    for sims in sets:
        if sims[:-4]+'.odb' not in odbss:
            fuckedlist.append([fold, sims])
print len(fuckedlist), ' unrun sims _in_ ',inps, ' sims and ', len(Inp_folders), '  sets'
