#-------------------------------------------------------------------------------
# Name:        KAO The Kangaroo *.pak
# Purpose:     Extract Archive
#
# Author:      Eric Van Hoven
#
# Created:     30/08/2017 
# Copyright:   (c) Eric Van Hoven 2017
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("KAO The Kangaroo", ".pak")
    noesis.setHandlerExtractArc(handle, pakExtractArc)
    return 1

def pakExtractArc(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:

        if justChecking:
            return 1

        fs.seek(-0xC, 2) #2 param = seek from end of file
        fcount = int(noeUnpack("<I", fs.read(4))[0])
        tablepos = noeUnpack("<I", fs.read(4))[0]
        fs.seek(tablepos, 0)

        for i in range(fcount):
            fileName = noeStrFromBytes(noeParseToZero(fs.read(0x50)))
            offset = noeUnpack("<I", fs.read(4))[0]
            size = noeUnpack("<I", fs.read(4))[0]
            tablepos = fs.tell()
            fs.seek(offset, 0)
            print("Writing", fileName)
            rapi.exportArchiveFile(fileName, fs.read(size))
            fs.seek(tablepos, 0)

    return 1
