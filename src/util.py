import os
import datetime
import sys


# generate all the directories needed for the given path (helper function)
def generateDirectories(path):
    folders = path.split("/")
    curdir = ""
    prevFolder = ""
    for folder in folders:
        prevFolder = curdir
        curdir = os.path.join(curdir, folder)
        if not os.path.exists(curdir):
            # print curdir
            # os.chmod(prevFolder,stat.S_IWRITE)
            os.mkdir(curdir)


def getDateSting():
    return datetime.datetime.now().strftime("%Y%m%d_%I%p")


def progressbar(i, length, numberNotification):
    scale = length / numberNotification
    if scale > 0:
        if i % scale == 0:
            sys.stdout.write('*')
            if length - i < scale:
                sys.stdout.write('\n')
            sys.stdout.flush()


def progressbarGuide(length):
    sys.stdout.write('|')
    for i in range(0, length - 1):
        sys.stdout.write('-')
    sys.stdout.write('|\n')
    sys.stdout.flush()