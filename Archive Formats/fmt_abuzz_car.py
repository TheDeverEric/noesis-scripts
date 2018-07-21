#-------------------------------------------------------------------------------
# Name:        Abuzz Games *.car
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
    handle = noesis.register("Abuzz Games", ".car")
    noesis.setHandlerExtractArc(handle, carExtract)
    return 1

def carExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        if justChecking:
            return 1
        magic = noeStrFromBytes(fs.read(3))
        if magic == "rac":
            fs.read(1) #1 byte
            fs.read(4) #uint 1
            fs.read(4) #header size
            fcount = int(noeUnpack("<I", fs.read(4))[0])
            for i in range(fcount):
                fs.read(4) #uint 1
                BASE_OFF = noeUnpack("<I", fs.read(4))[0]
                fnsz = noeUnpack("<I", fs.read(4))[0]
                fileName = noeStrFromBytes(fs.read(fnsz))
                while True:
                    if(noeUnpack("<B", fs.read(1))[0] != 0x0):
                        break
                fs.seek(-0x1, 1)
                tableoff = fs.tell()
                fs.seek(BASE_OFF, 0)
                fs.read(4) #uint 2
                fs.read(4) #uint null
                size = noeUnpack("<I", fs.read(4))[0]
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))
                fs.seek(tableoff, 0)
        else:
            print("Invalid archive!")
            return 0

    return 1
