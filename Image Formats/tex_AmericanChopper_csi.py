#-------------------------------------------------------------------------------
# Name:        American Chopper *.CSI
# Purpose:     Import Image
#
# Author:      Eric Van Hoven
#
# Created:     07/07/2018
# Copyright:   (c) Eric Van Hoven 2018
# Licence:     <MIT License>
#-------------------------------------------------------------------------------

from inc_noesis import *

import noesis

def registerNoesisTypes():
    handle = noesis.register("American Chopper CSI Image", ".csi")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    id = bs.readBytes(4).decode("ASCII")
    if id != "MISC":
        return 0
    return 1

def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    bs.seek(0x8, 0)
    headln = bs.readUInt()
    dataStart = bs.readUInt()
    width = bs.readUInt()
    height = bs.readUInt()
    bs.seek(0x8, 1) #null uint32's
    codecidsz = bs.readUInt()
    codec = bs.readBytes(codecidsz).decode("ASCII")
    dataSize = (width * height) * codecidsz
    bs.seek(dataStart, 0)
    data = bs.readBytes(dataSize)

    if codec == "RGB":
        data = rapi.imageDecodeRaw(data, width, height, "r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGB24

    elif codec == "BGR":
        data = rapi.imageDecodeRaw(data, width, height, "b8 g8 r8")
        texFmt = noesis.NOESISTEX_RGB24

    else:
        data = rapi.imageDecodeRaw(data, width, height, "b8 g8 r8 a8")
        texFmt = noesis.NOESISTEX_RGBA32

    texFmt = noesis.NOESISTEX_RGBA32
    texList.append(NoeTexture(rapi.getInputName(), width, height, data, texFmt))
    return 1
