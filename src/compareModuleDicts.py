import os
import configurations as conf
from cPickle import load, dump
from src import util
import re


def compareModuleDicts(myDict, PFamDict, threshold):
    numSimilar = 0
    totNumBorders = 0

    # logs the similar boarders as a list of pairs of lists
    # format:
    #    list:
    #      val: list in the form [[m, s, e], [m', s', e']]

    similarBorders = []

    for protein in myDict.keys():
        myBorders = myDict[protein]
        pBorders = PFamDict[protein]

        totNumBorders += len(myBorders)

        for myBorder in myBorders:
            for pBorder in pBorders:
                sm, em = myBorder[1], myBorder[2]
                sp, ep = int(re.sub('[a-zA-Z]', "", pBorder[1])), int(re.sub('[a-zA-Z]', "", pBorder[2]))
                diff = abs(sm - sp) + abs(em - ep)

                if diff < threshold:
                    numSimilar += 1
                    similarBorders.append([myBorder, pBorder])
                    break

    return numSimilar, totNumBorders, similarBorders


def compareInputDataUsingThreshold(threshold):
    inputFiles = os.listdir(conf.inputFolder)
    inputFiles.sort()

    totNumSimilar = 0
    totNumBorders = 0
    totSimilarBorders = []

    while len(inputFiles) > 0:
        inputFile = inputFiles[0]
        del inputFiles[0]

        if "myBorders" in inputFile:
            myDict = load(open(os.path.join(conf.inputFolder, inputFile)))
            for i in range(len(inputFiles)):
                if inputFiles[i].replace("pfamBorders", "myBorders") == inputFile:
                    PFamDict = load(open(os.path.join(conf.inputFolder, inputFiles[i])))
                    del inputFiles[i]
                    break
        elif "pfamBorders" in inputFile:
            PFamDict = load(open(os.path.join(conf.inputFolder, inputFile)))
            for i in range(len(inputFiles)):
                if inputFiles[i].replace("myBorders", "pfamBorders") == inputFile:
                    myDict = load(open(os.path.join(conf.inputFolder, inputFiles[i])))
                    del inputFiles[i]
                    break

        # analyize the two dicts and sum the results
        numSimilar, numBorders, similarBorders = compareModuleDicts(myDict, PFamDict, threshold)
        totNumSimilar += numSimilar
        totNumBorders += numBorders
        totSimilarBorders += similarBorders

    return totNumSimilar, totNumBorders, totSimilarBorders


def compareData():
    util.generateDirectories(conf.resultFolder)
    resultFile = os.path.join(conf.resultFolder, util.getDateSting() + "_" + conf.resultFile)
    with open(resultFile, "w") as f:
        f.write("Threshold\t#Sim\t#Borders\t%Sim\n")

    util.progressbarGuide(20)
    for threshold in range(conf.borderDifferenceStart, conf.borderDifferenceEnd+1, conf.borderDifferenceStep):
        # print progress
        progressIndex = threshold-conf.borderDifferenceStart
        progressEnd = conf.borderDifferenceEnd-conf.borderDifferenceStart
        util.progressbar(progressIndex, progressEnd, 20)

        numSimilar, numBorders, similarBorders = compareInputDataUsingThreshold(threshold)
        percentSim = int(float(numSimilar)/numBorders * 1000)/10
        with open(resultFile, "a") as f:
            f.write(str(threshold)+"\t"+str(numSimilar)+"\t"+str(numBorders)+"\t"+str(percentSim)+"\n")

        # dump the similar border pairs for future analysis
        util.generateDirectories(conf.simBorderFolder)
        outfilename = util.getDateSting() + "_" + str(threshold) + ".cpickle"
        dump(similarBorders, open(os.path.join(conf.simBorderFolder, outfilename), "wb"))

