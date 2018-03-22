import re


def pfamDictToInt(pfamDict):
    for protein in pfamDict.keys():
        borders = pfamDict[protein]
        for border in borders:
            s = border[1]
            e = border[2]
            sf = re.search("\d+", s).group(0)
            ef = re.search("\d+", e).group(0)

            border[1] = int(sf)
            border[2] = int(ef)
    return pfamDict


def freqDictToString(freqDict):
    keys = freqDict.keys()
    keys.sort()
    outstring = "{"
    for i, key in enumerate(keys):
        outstring += str(key)+": " + str(freqDict[key])
        if i != len(keys)-1:
            outstring += ", "
    outstring += "}"

    return outstring


def checkModulesWithDomains(borderDict, pfamDict):
    # A dictionary showing which domains each modules was observed nested in
        # key: module numbers
        # val: a list of domain numbers
    moduleToDomainDict = {}
    detailedOutput = ""

    proteins = borderDict.keys()
    for protein in proteins:
        for moduleBorder in borderDict[protein]:
            for domainBorder in pfamDict[protein]:
                m = moduleBorder[0]
                ms = moduleBorder[1]
                me = moduleBorder[2]

                d = domainBorder[0]
                ds = domainBorder[1]
                de = domainBorder[2]

                # If the domain boundary covers the module boundary
                if ds <= ms and de >= me:
                    if m in moduleToDomainDict.keys():
                        # addToCountDict(moduleToDomainDict[m], d)
                        if d in moduleToDomainDict[m]:
                            moduleToDomainDict[m][d] += 1
                        else:
                            moduleToDomainDict[m][d] = 1
                    else:
                        moduleToDomainDict[m] = {d: 1}

    inSingleDomain = 0
    inMultDomain = 0

    modules = moduleToDomainDict.keys()
    modules.sort()

    for m in modules:
        freqDict = moduleToDomainDict[m]
        if len(freqDict.keys()) == 1:
            if freqDict[freqDict.keys()[0]] != 1:
                inSingleDomain += 1
                detailedOutput += str(m) + ": " + freqDictToString(freqDict) + "\n"
        else:
            inMultDomain += 1
            detailedOutput += str(m) + ": " + freqDictToString(freqDict) + "\n"

    print detailedOutput
    print "inSingleDomain:", inSingleDomain
    print "inMultDomain:", inMultDomain


def checkDomainsWithModules(borderDict, pfamDict, nestedLeeway = 10):
    # A dictionary detailing which module combinations each domain has
    domainToModuleDict = {}

    totNumBorders = 0
    totNestBorders = 0

    proteins = borderDict.keys()
    for protein in proteins:
        # a temporary dict to keep track of the module contents inside each domain for this protein
            # key: domain number
            # val: a sorted list of modules numbers
        domainContentDict = {}
        moduleBorders = borderDict[protein]
        totNumBorders += len(moduleBorders)

        # checking for all borders in this protein and populate the domainContentDict
        for domainBorder in pfamDict[protein]:
            nestedborders = []
            for moduleBorder in moduleBorders:
                ms = moduleBorder[1]
                me = moduleBorder[2]

                d = domainBorder[0]
                ds = domainBorder[1]
                de = domainBorder[2]

                # If the domain boundary covers the module boundary

                #if ds <= ms and de >= me:
                if ms - ds > -nestedLeeway and de - me > -nestedLeeway:
                    if moduleBorder not in nestedborders:
                        nestedborders.append(moduleBorder)

            totNestBorders += len(nestedborders)
            for moduleBorder in nestedborders:
                m = moduleBorder[0]
                if d in domainContentDict.keys():
                    domainContentDict[d].append(m)
                else:
                    domainContentDict[d] = [m]

        for d in domainContentDict.keys():
            domainContentDict[d] = list(set(domainContentDict[d]))
            domainContentDict[d].sort()

        # add the content of the domainContentDict to domainToModuleDict

        for d in domainContentDict.keys():
            moduleContent = tuple(domainContentDict[d])

            if d in domainToModuleDict.keys():
                mcFreqDict = domainToModuleDict[d]
                if moduleContent in mcFreqDict.keys():
                    mcFreqDict[moduleContent] += 1
                else:
                    mcFreqDict[moduleContent] = 1
            else:
                mcFreqDict = {moduleContent: 1}
                domainToModuleDict[d] = mcFreqDict

    # print out the results
    detailedResults = ""
    domains = domainToModuleDict.keys()
    domains.sort()

    singleContent = {}
    singleContentCount = 0
    multContentCount = 0
    for d in domains:
        if len(domainToModuleDict[d].keys()) == 1:
            count = domainToModuleDict[d][domainToModuleDict[d].keys()[0]]
            if count > 1:
                singleContentCount += 1
                if count in singleContent:
                    singleContent[count] += 1
                else:
                    singleContent[count] = 1

                detailedResults += str(d) + ": " + str(domainToModuleDict[d]) + "\n"

        else:
            detailedResults += str(d) + ": " + str(domainToModuleDict[d]) + "\n"
            multContentCount += 1

    # print detailedResults
    # print "SingleContent:"
    # print singleContent
    # print "singleContentCount: ", singleContentCount
    # print "multContentCount: ", multContentCount

    return detailedResults, singleContent, singleContentCount, multContentCount, totNestBorders, totNumBorders




