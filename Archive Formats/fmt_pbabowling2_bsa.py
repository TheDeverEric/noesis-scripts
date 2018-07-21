#-------------------------------------------------------------------------------
# Name:        PBA Bowling 2 *.BSA
# Purpose:     Extract Archive
#
# Author:      Eric Van Hoven
#
# Created:     01/09/2017
# Copyright:   (c) Eric Van Hoven 2017
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("PBA Bowling 2", ".bsa")
    noesis.setHandlerExtractArc(handle, bsaExtract)
    return 1

def bsaExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        if justChecking:
            return 1
        fileoffset = noeUnpack("<I", fs.read(4))[0]
        fcount = int(noeUnpack("<I", fs.read(4))[0])
        BASE_OFF = fs.tell()
        fileoffset += BASE_OFF

        for i in range(fcount):
            fnoff = noeUnpack("<I", fs.read(4))[0] + BASE_OFF
            size = noeUnpack("<I", fs.read(4))[0]
            fs.read(4) #null uint
            filetable = fs.tell()
            fs.seek(fnoff, 0)
            fnsz = 0
            while True:
                if(noeUnpack("<b", fs.read(1))[0] == 0x0):
                    fnsz += 1
                    break
                else:
                    fnsz += 1

            fs.seek(fnoff, 0)
            fileName = noeStrFromBytes(noeParseToZero(fs.read(fnsz)))
            fs.seek(fileoffset, 0)
            print("Writing", fileName)
            rapi.exportArchiveFile(fileName, fs.read(size))
            fileoffset += size
            fs.seek(filetable, 0)

    return 1









