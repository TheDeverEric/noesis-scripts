#-------------------------------------------------------------------------------
# Name:        Davidson & Associates *.res
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
    handle = noesis.register("Davidson & Associates", ".res")
    noesis.setHandlerExtractArc(handle, resExtract)
    return 1

def resExtract(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:
        if justChecking:
            return 1
        verID = noeUnpack("<I", fs.read(4))[0]

        if verID == 2:
            fs.read(8) #null uint64
            TB1 = noeUnpack("<I", fs.read(4))[0] + 0x8
            TB1SZ = noeUnpack("<I", fs.read(4))[0] - 0x8
            TB2 = noeUnpack("<I", fs.read(4))[0] + 0x8
            TB2SZ = noeUnpack("<I", fs.read(4))[0] - 0x8
            endtb = TB1 + TB1SZ
            filenum = -1
            fs.seek(TB1, 0)

            while (TB1 != endtb):
                offset = noeUnpack("<I", fs.read(4))[0]
                size = noeUnpack("<I", fs.read(4))[0]
                TB1 = fs.tell()
                fs.seek(offset, 0)
                filenum += 1
                fileName = str(filenum) + ".dat"
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))
                fs.seek(TB1, 0)

            endtb = TB2 + TB2SZ
            fs.seek(TB2, 0)

            while (TB2 != endtb):
                offset = noeUnpack("<I", fs.read(4))[0]
                size = noeUnpack("<I", fs.read(4))[0]
                TB2 = fs.tell()
                fs.seek(offset, 0)
                filenum += 1
                fileName = str(filenum) + ".dat"
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))
                fs.seek(TB2, 0)

        elif verID == 3:
            while True:
                if(noeUnpack("<B", fs.read(1))[0]  != 0x0):
                    break

            fs.seek(-0x1, 1)
            TB_A = noeUnpack("<I", fs.read(4))[0] + 0x8
            TB_A_SZ = noeUnpack("<I", fs.read(4))[0] - 0x8
            while True:
                if(noeUnpack("<B", fs.read(1))[0]  != 0x0):
                    break


            fs.seek(-0x1, 1)
            TB_B = noeUnpack("<I", fs.read(4))[0]
            TB_B_SZ = noeUnpack("<I", fs.read(4))[0]
            fs.seek(TB_B, 0)
            FNTB = noeUnpack("<I", fs.read(4))[0]
            FNTB_SZ = noeUnpack("<I", fs.read(4))[0]
            endoftb = TB_A + TB_A_SZ

            while(TB_A != endoftb):
                fs.seek(TB_A, 0)
                offset = noeUnpack("<I", fs.read(4))[0]
                size = noeUnpack("<I", fs.read(4))[0]
                TB_A = fs.tell()
                fs.seek(FNTB)
                fs.read(4) #uint filenum
                fs.read(4) #uint fakesize
                fs.read(4) #float file date + time
                fs.read(4) #uint fileID
                fnsz = noeUnpack("<I", fs.read(4))[0]
                fileName = noeStrFromBytes(noeParseToZero(fs.read(fnsz)))
                FNTB = fs.tell()
                fs.seek(offset, 0)
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))

        elif verID == 4:
            fs.read(8)
            fs.read(4) #useless table offset
            fs.read(4) #useless table size
            TB = (noeUnpack("<I", fs.read(4))[0]) + 0x8
            TB_SZ = (noeUnpack("<I", fs.read(4))[0]) - 0x8
            TB_END = TB + TB_SZ

            i = -1
            while(TB != TB_END):
                fs.seek(TB)
                offset = noeUnpack("<I", fs.read(4))[0]
                size = noeUnpack("<I", fs.read(4))[0]
                TB = fs.tell()
                fs.seek(offset, 0)
                i += 1
                fileName = str(i) + ".dat"
                print("Writing", fileName)
                rapi.exportArchiveFile(fileName, fs.read(size))
    return 1
