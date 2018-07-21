#-------------------------------------------------------------------------------
# Name:        Hannah Montana: Spotlight World Tour *.hog
# Purpose:     Extract Archive
#
# Author:      Eric Van Hoven
#
# Created:     05/09/2017
# Copyright:   (c) Eric Van Hoven 2017
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Hannah Montana: Spotlight World Tour", ".hog")
    noesis.setHandlerExtractArc(handle, hogExtract)
    return 1

def hogExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        if justChecking:
            return 1
        fs.read(4)
        TB = noeUnpack("<I", fs.read(4))[0]
        fs.read(4) #uint 0
        fs.read(4) #float?
        fcount = noeUnpack("<I", fs.read(4))[0]
        fs.seek(TB)
        for i in range(fcount):
            fnoff = noeUnpack("<I", fs.read(4))[0]
            offset = noeUnpack("<I", fs.read(4))[0]
            size = noeUnpack("<I", fs.read(4))[0]
            fs.read(4) #null float?
            TB = fs.tell()
            fs.seek(fnoff, 0)
            fnsz = 0
            while True:
                if(noeUnpack("<B", fs.read(1))[0] == 0x0):
                    break
                else:
                    fnsz += 1

            fs.seek(fnoff, 0)
            fileName = noeStrFromBytes(fs.read(fnsz))
            fs.seek(offset, 0)
            print("Writing", fileName)
            rapi.exportArchiveFile(fileName, fs.read(size))
            fs.seek(TB, 0)

    return 1

