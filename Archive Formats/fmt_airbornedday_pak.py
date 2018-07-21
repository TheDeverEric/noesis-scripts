#-------------------------------------------------------------------------------
# Name:        Airborne Troops- Countdown to D-Day *.PAK
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
    handle = noesis.register("Airborne Troops Count-Down to D-Day", ".PAK")
    noesis.setHandlerExtractArc(handle, pacExtract)
    return 1

def pacExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        if justChecking:
            return 1
        fs.read(8) #null uints
        tail = noeUnpack("<I", fs.read(4))[0]
        fcount = noeUnpack("<I", fs.read(4))[0]

        for i in range(fcount):
            fs.seek(tail, 0)
            fnsz = 0
            while True:
                if(noeUnpack("<b", fs.read(1))[0]== 0xA):
                    break
                else:
                    fnsz += 1

            fs.seek(tail, 0)
            fileName = noeStrFromBytes(fs.read(fnsz))
            fs.read(1) #0xA byte
            offset = noeUnpack("<I", fs.read(4))[0]
            size = noeUnpack("<I", fs.read(4))[0]
            tail = fs.tell()
            fs.seek(offset, 0)
            print("Writing", fileName)
            rapi.exportArchiveFile(fileName, fs.read(size))


    return 1




