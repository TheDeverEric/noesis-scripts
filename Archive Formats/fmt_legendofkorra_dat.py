#-------------------------------------------------------------------------------
# Name:        The Legend of Korra *.dat
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
    handle = noesis.register("The Legend of Korra", ".dat")
    noesis.setHandlerExtractArc(handle, datExtract)
    return 1

def datExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:

        if justChecking:
            return 1

        magicword = noeStrFromBytes(fs.read(3))
        if magicword == "DAT":
            fs.read(1)
            fcount = noeUnpack("<I", fs.read(4))[0]


            offtable = noeUnpack("<I", fs.read(4))[0]
            typetable = noeUnpack("<I", fs.read(4))[0]
            fnametable = noeUnpack("<I", fs.read(4))[0]
            sizetable = noeUnpack("<I", fs.read(4))[0]
            fs.seek(fnametable, 0)
            fnsz = noeUnpack("<I", fs.read(4))[0]
            fnametable = fs.tell()

            for i in range(fcount):
                fs.seek(offtable, 0)
                offset = noeUnpack("<I", fs.read(4))[0]
                offtable = fs.tell()
                fs.seek(fnametable, 0)
                fileName = noeStrFromBytes(noeParseToZero(fs.read(fnsz)))
                fnametable = fs.tell()
                fs.seek(sizetable, 0)
                size = noeUnpack("<I", fs.read(4))[0]
                sizetable = fs.tell()
                fs.seek(offset, 0)
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))

        else:
            print("Invalid archive!!!")

    return 1


