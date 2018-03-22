from src import checkModuleWithDomains, util
import os
from cPickle import load
import configurations as conf

def main():
    inputFiles = os.listdir(conf.inputFolder)
    for inputFile in inputFiles:
        borderDict = load(open(os.path.join(conf.inputFolder, inputFile), "rb"))
        pfamDict = load(open(conf.PFamInfoDir, "rb"))
        pfamDict = checkModuleWithDomains.pfamDictToInt(pfamDict)
        # checkModuleWithDomains.checkModulesWithDomains(borderDict, pfamDict)

        detailedResults, singleContent, singleContentCount, multContentCount = \
            checkModuleWithDomains.checkDomainsWithModules(borderDict, pfamDict)

        # write results
        util.generateDirectories(conf.resultFolder)
        with open(os.path.join(conf.resultFolder, util.fileAppend(inputFile, "_detailedResults.txt")),"w") as f:
            f.write(detailedResults)
        with open(os.path.join(conf.resultFolder, util.fileAppend(inputFile, "_results.txt")),"w") as f:
            f.write("SingleCountentCount\t"+str(singleContentCount)+"\n")
            f.write("MultContentCount\t"+str(multContentCount)+"\n")
            f.write("\nSingleContent:\n")
            for c in singleContent.keys():
                f.write(str(c)+"\t"+str(singleContent[c])+"\n")


if __name__ == "__main__":
    main()
