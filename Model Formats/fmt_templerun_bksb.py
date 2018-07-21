#-------------------------------------------------------------------------------
# Name:        Temple Run *.BKSB
# Purpose:     Import Mesh
#
# Author:      Eric Van Hoven
#
# Created:     29/07/2017
# Copyright:   (c) Eric Van Hoven 2017
# Licence:     MIT License
#-------------------------------------------------------------------------------
from inc_noesis import *

import noesis

import rapi

import struct

def registerNoesisTypes():
    handle = noesis.register("Temple Run" , ".bksb")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    return 1

def noepyCheckType(data):
    return 1

def noepyLoadModel(data, mdlList):
    ctx = rapi.rpgCreateContext()
    bs = NoeBitStream(data)
    
    MagicNumber = int(bs.readUInt())
    bs.seek(5, NOESEEK_ABS)
    VertHeader = int(bs.readUInt() * 16 + 9)
    VertBuffer = VertHeader + 0x2f
    
    if MagicNumber == 0x476:
        VertBuffer += 0x13
    
    bs.seek(VertHeader + 4, NOESEEK_ABS)
    VertCount  = int(bs.readUInt())
    VertStride = int(bs.readUInt())
    
    vertArray = [ NoeVec3() ] * VertCount
    uvArray   = [ NoeVec3() ] * VertCount

    for i in range(VertCount):
        bs.seek(VertBuffer + i * VertStride, NOESEEK_ABS)
        vertArray[i] = NoeVec3((bs.readFloat() , bs.readFloat() , bs.readFloat()))
        uvArray[i]   = NoeVec3((bs.readFloat() , bs.readFloat() , 0.0))

    bs.seek(VertBuffer + VertCount * VertStride, NOESEEK_ABS)
    
    IdxCount = bs.readUInt()
    
    bs.seek(0xc, NOESEEK_REL)

    faceArray = []

    for i in range(IdxCount):
        faceArray.append(bs.readUShort())

    meshes = []
    msh = NoeMesh(faceArray, vertArray)
    msh.setUVs(uvArray)
    meshes.append(msh)
    mdlList.append(NoeModel(meshes))

    return 1
