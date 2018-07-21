#-------------------------------------------------------------------------------
# Name:        Kim Possible: What's The Switch? *.A2M
# Purpose:     Extract Archive
#
# Author:      Eric Van Hoven
#
# Created:     04/09/2017
# Copyright:   (c) Eric Van Hoven 2017
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Kim Possible: What's the Switch?", ".A2M")
    noesis.setHandlerExtractArc(handle, arcExtract)
    return 1

def arcExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        if justChecking:
            return 1

        fs.seek(0x800, 0) #straight to first folder name
        extractFile(fs,"")


    return 1

def extractFile(fs , CurrPath):
    Name = ""
    CUR_OFF = fs.tell()
    fnsz = 0
    while True:
        if(noeUnpack("<B", fs.read(1))[0] == 0x0):
            break
        else:
            fnsz += 1

    fs.seek(CUR_OFF, 0)
    Name += noeStrFromBytes(fs.read(fnsz))
    fs.seek(CUR_OFF + 0x10, 0)
    flags = noeUnpack("<I", fs.read(4))[0]
    offset = noeUnpack("<I", fs.read(4))[0]
    length = noeUnpack("<I", fs.read(4))[0]

    IsFolder = (flags & 1) != 0

    CurrPath += Name
    if IsFolder:
        CurrPath += "\\"
        for i in range(length):
            fs.seek(0x800 + offset + i * 0x1c, 0)
            extractFile(fs, CurrPath)

    else:
        fs.seek(0x1000 + offset, 0)
        print("Writing", CurrPath)
        rapi.exportArchiveFile(CurrPath, fs.read(length))
        return 1









