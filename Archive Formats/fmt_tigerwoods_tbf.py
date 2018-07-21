#-------------------------------------------------------------------------------
# Name:        Tiger Woods PGA Tour *.tbf 
# Purpose:     Extract Archive
#
# Author:      Eric Van Hoven
#
# Created:     06/07/2018
# Copyright:   (c) Eric Van Hoven 2018
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Tiger Woods PGA Tour TBF", ".tbf")
    noesis.setHandlerExtractArc(handle, tbfParse)
    return 1

def tbfParse(fileName, fileLen, justChecking):
    with open(fileName, "rb") as fs:

        if justChecking:
            return 1

        files = noeUnpack("<I", fs.read(4))[0]
        tableoff = fs.tell()
        for i in range(files):
            fs.seek(tableoff, 0)
            fnln = noeUnpack("<I", fs.read(4))[0]
            name = fs.read(fnln).decode("ASCII").rstrip("\0")
            offset = noeUnpack("<I", fs.read(4))[0]
            size = noeUnpack("<I", fs.read(4))[0]
            tableoff = fs.tell()
            fs.seek(offset, 0)
            print("Writing", name)
            rapi.exportArchiveFile(name, fs.read(size))

    return 1
