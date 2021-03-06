# -*- coding: UTF-8 -*-
"""
module vinutils.py
-----------------------------------------------------------------------------

 Vinetto : a forensics tool to examine Thumbs.db files
 Copyright (C) 2005, 2006 by Michel Roukine
 
This file is part of Vinetto.
 
 Vinetto is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published
 by the Free Software Foundation; either version 2 of the License, or (at
 your option) any later version.
 
 Vinetto is distributed in the hope that it will be
 useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 
 You should have received a copy of the GNU General Public License along
 with the vinetto package; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 
-----------------------------------------------------------------------------
"""

__revision__ = "$Revision: 47 $"
__version__ = "0.01"
__author__ = 'Michel Roukine'

Catalog = {}
catIndxOutOfSeqFlag = False
iCatPrec = None

TNStreams = {}
tnStreamOutOfSeqFlag = False
iTnsPrec = None


def catIndxOutOfSeq():
    """Return catIndxOutOfSeqFlag value.  """
    return catIndxOutOfSeqFlag


def tnStreamOutOfSeq():
    """Return tnStreamOutOfSeqFlag value.  """
    return tnStreamOutOfSeqFlag


def addCatEntry (iCat, timestamp, TNname):
    """Add a new Catalog entry.  """ 
    global catIndxOutOfSeqFlag, iCatPrec
    if iCatPrec != None:
        if iCat != (iCatPrec + 1) :
            catIndxOutOfSeqFlag = True
            
    if Catalog.has_key(iCat):
        Catalog[iCat].append((timestamp, TNname))
    else:
        Catalog[iCat] = [(timestamp, TNname)]
        
    iCatPrec = iCat
    return


def addTNStream (iTN, vType, filename):
    """Add new thumbnail stream references.  """
    global tnStreamOutOfSeqFlag, iTnsPrec
    if iTnsPrec != None:
        if iTN != (iTnsPrec + 1) :
            tnStreamOutOfSeqFlag = True
            
    if TNStreams.has_key(iTN):
        TNStreams[iTN].append((vType, filename))
    else:
        TNStreams[iTN] = [(vType, filename)]
    
    iTnsPrec = iTN
    return


def nbCatEnt ():
    """Return number of Catalog entry.  """ 
    nb = 0
    for k in Catalog:
        nb += len(Catalog[k])
    return nb


def nbTNstr (*vt):
    """Return number of extracted/unextracted thumbnails.  """ 
    nb = 0
    if len(vt) == 0:
        for k in TNStreams:
            nb += len(TNStreams[k])
        return nb
    else :
        nb = 0
        for k in TNStreams:
            for (vType, filename) in TNStreams[k]:
                if vt[0] == vType :
                    nb += 1
        return nb


def extractStats(outputdir):
    """Return extraction statistics.  """
    extr = {"1":0, "2":0}
    unextr = {"1":0, "2":0}
    statstring = ""
    odstr = ""
    if outputdir != None:
        odstr = " to " + outputdir
    
    for k in TNStreams:
        for (vType, filename) in TNStreams[k]:
            if filename == "" :
                unextr[vType] += 1
            else:
                extr[vType] += 1
    
    for vt in extr:
        if extr[vt] > 0:
            statstring += str(extr[vt]) + " Type " + vt + \
                          " thumbnails extracted" + odstr + "\n"
    
    for vt in unextr:
        if unextr[vt] > 0:
            statstring += str(unextr[vt]) + " Type " + vt + \
                          " thumbnails unextracted" + odstr + "\n"
    return statstring


def getCatEntry(iCat):
    """Return iCat Catalog entry.  """ 
    if Catalog.has_key(iCat):
            return Catalog[iCat]
    return []


def fincrement (filename):
    """ Compute next "valid" filename for a given SID. """
    if filename.find("_") < 0:
        return filename + "_1"
    else:
        i = int(filename[filename.find('_') + 1:])
        return filename[:filename.find('_') + 1] + str(i + 1)
    

def TNfname(SIDstr, vType):
    """ Compute filenames for thumbnails.  """
    computedfn = SIDstr
    k = int(SIDstr)
    if TNStreams.has_key(k):
    # duplicate index numbers
        for (vtyp, filename) in TNStreams[k]:
            if computedfn == filename:
                computedfn = fincrement (filename)
    addTNStream(k, vType, computedfn)
    return computedfn
