#-------------------------------------------------------------------------------
# Name:        Jimmy Neutron Attack of the Twonkies *.PAK
# Purpose:     Extract Archive
#
# Author:      Eric Van Hoven
#
# Created:     31/08/2017
# Copyright:   (c) Eric Van Hoven 2017
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Jimmy Neutron Attack of the Twonkies", ".PAK")
    noesis.setHandlerExtractArc(handle, pakExtract)
    return 1

def pakExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        magic = noeStrFromBytes(fs.read(4))
        if magic == "kcap":
            fs.read(4) #uint 0x1
            fs.read(4) #uint header size
            fs.read(4) #uint archive size
            fntb = noeUnpack("<I", fs.read(4))[0]
            fcount = noeUnpack("<I", fs.read(4))[0]
            fs.read(4) #uint 0x0
            tbpos = fs.tell()
            for i in range(fcount):
                fs.seek(fntb, 0)
                fnsz = 0
                while True:
                    if(noeUnpack("<b", fs.read(1))[0] == 0x0):
                        fnsz += 1
                        break
                    else:
                        fnsz += 1

                fs.seek(fntb, 0)
                fileName = noeStrFromBytes(noeParseToZero(fs.read(fnsz)))
                fntb = fs.tell()
                fs.seek(tbpos, 0)
                offset = noeUnpack("<I", fs.read(4))[0]
                size = noeUnpack("<I", fs.read(4))[0]
                fs.read(4) #uint null
                tbpos = fs.tell()
                fs.seek(offset, 0)
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))

    return 1


