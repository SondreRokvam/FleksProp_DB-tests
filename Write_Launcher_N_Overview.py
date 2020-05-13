if len(fuckedlist)>0:
    p = open(Source + '\\ReLauncher.bat', "w+")
    s = open(Source + '\\NotRun_possibleProblems.txt', "w+")
    a = 0  # Logic Flag
    for BAT in fuckedlist:
        if not BAT[0][0] == a:
            a = BAT[0][0]
            s.write(BAT[0][0] + ' \t ' + BAT[1] + '\n')
        else:
            s.write(' ' * len(BAT[0][0]) + ' \t ' + BAT[1] + '\n')
        p.write('chdir "' + BAT[0][0] + '"\n'+
                'call abq2017 job=' + BAT[1][:-4] + ' int\n')
    p.close()
    s.close()
    print 'wrote Relauncher and unRun List'
else:
    print 'No mishaps'
    p = open(Source + '\\ReLauncher.bat', "w+")
    s = open(Source + '\\NotRun_possibleProblems.txt', "w+")
    s.write('No problem')
    p.write('\n')
    p.close()
    s.close()