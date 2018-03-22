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
        with open(conf.resultFile, "w") as wf:
            wf.write("leeway\ttotNumModuleBorders\ttotNumNested\tSingleCountentCount\tMultContentCount\ts_mult_ratio\n")
            for leeway in range(0, 20, 1):
                detailedResults, singleContent, singleContentCount, multContentCount, totNestBorders, totNumBorders = \
                    checkModuleWithDomains.checkDomainsWithModules(borderDict, pfamDict, leeway)

                # write results
                util.generateDirectories(conf.singleFolder)
                util.generateDirectories(conf.detailFolder)

                with open(os.path.join(conf.detailFolder, util.fileAppend(inputFile, str(leeway)+".txt")), "w") as f:
                    f.write(detailedResults)
                with open(os.path.join(conf.singleFolder, util.fileAppend(inputFile, str(leeway)+".txt")), "w") as f:
                    f.write("\nSingleContent:\n")
                    for c in singleContent.keys():
                        f.write(str(c)+"\t"+str(singleContent[c])+"\n")
                wf.write(str(leeway)+"\t")
                wf.write(str(totNumBorders) + "\t")
                wf.write(str(totNestBorders) + "\t")
                wf.write(str(singleContentCount) + "\t")
                wf.write(str(multContentCount) + "\t")
                wf.write(str(float(singleContentCount)/multContentCount) + "\n")


if __name__ == "__main__":
    main()
