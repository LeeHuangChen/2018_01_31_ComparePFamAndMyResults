import re


def processPfamDict(pfamDict):
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