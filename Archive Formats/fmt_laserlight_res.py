#-------------------------------------------------------------------------------
# Name:        Laser Light *.RES
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
    handle = noesis.register("Laser Light (DOS)", ".res")
    noesis.setHandlerExtractArc(handle, resExtract)
    return 1

def resExtract(fileName, fileLen, justChecking):

    with open(fileName, "rb") as fs:
        if justChecking:
            return 1

        fcount = noeUnpack("<H", fs.read(2))[0]
        for i in range(fcount):
            fs.read(1) #fnsz
            fileName = noeStrFromBytes(noeParseToZero(fs.read(0xC)))
            offset = noeUnpack("<I", fs.read(4))[0]
            size = noeUnpack("<I", fs.read(4))[0]
            fs.read(1) #2 byte
            tablepos = fs.tell()
            fs.seek(offset, 0)
            print("Writing", fileName)
            rapi.exportArchiveFile(fileName, fs.read(size))
            fs.seek(tablepos, 0)
    return 1
