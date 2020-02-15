#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _pyio import __metaclass__
__metaclass__ = type

from samfunction import *
import re

class Read:
    def __init__(self, *args):
        self.QNAME = args[0]
        self.FLAG = args[1]
        self.RNAME = args[2]
        self.POS = args[3]
        self.MAPQ = args[4]
        self.CIGAR = args[5]
        self.RNEXT = args[6]
        self.PNEXT = args[7]
        self.TLEN = args[8]
        self.SEQ = args[9]

    def __getitem__(self):
        return self.QNAME, self.FLAG, self.RNAME, self.POS, self.MAPQ, \
               self.CIGAR, self.RNEXT, self.PNEXT, self.TLEN, self.SEQ

    def __setitem__(self, lst):
        self.QNAME = lst[0]
        self.FLAG = lst[1]
        self.RNAME = lst[2]
        self.POS = lst[3]
        self.MAPQ = lst[4]
        self.CIGAR = lst[5]
        self.RNEXT = lst[6]
        self.PNEXT = lst[7]
        self.TLEN = lst[8]
        self.SEQ = lst[9]

    def length(self):
        str = self.CIGAR
        mode = re.compile(r'\d+')
        l = mode.findall(str)
        le =0
        for i in l:
            le += int(i)
        return le

    def isMap(self):
        readlen = len(self.SEQ)
        ml = re.findall(r'[0-9]{1,}M',self.CIGAR)
        mode = re.compile(r'\d+')
        num_M =0
        for m in ml:
            num_M += int(mode.findall(m)[0])
        if num_M >= readlen*0.98:
            return True
        else:
            return False

    '''def isRepete(self):
        unit,flag = self.getmsiunit()
        reSEQ = self.SEQ[-1::-1]
        if unit and reSEQ.upper().count(unit) >= (len(reSEQ) / len(unit) - 2):
            return True, unit
        else:
            return False'''

    def isRepete(self,unit,flag):
        #unit,flag = self.getmsiunit()
        if flag == 1 :
            reSEQ = self.SEQ
        if flag == 2:
            reSEQ = self.SEQ[-1::-1]
        if reSEQ.upper().count(unit) >= (len(reSEQ) / len(unit) - 2):
            return True
        else:
            return False

    def verify(self, ref):
        readlen = len(self.SEQ)
        if str(self.CIGAR) == str(readlen)+'M':
            alnpos = int(self.POS)
            alnstr = self.SEQ.upper()
            refstr = ref[alnpos - 1:alnpos + readlen-1].upper()
            if alnstr == refstr:
                return True
            else:
                return False

    def getpos(self):
        return self.POS

    def getunit(self):
        for i in range(1, 7):
            unitlist = []
            for j in range(-1, -7, -1):
                unitlist.append(self.SEQ[j:j - i:-1])
            unit = unitissame(unitlist)
            if unit is False:
                continue
            else:
                return unit

    def getlefthook(self,unit,flag):
        #unit,flag = self.getmsiunit()
        lenhook = 0
        if flag == 1:
            seq = self.SEQ
            if unit:
                for i in range(0, len(seq), len(unit)):
                    if issame(seq[i:i + len(unit)], unit):
                        lenhook += len(unit)
                    else:
                        break
        if flag == 2:
            seq = self.SEQ[-1::-1]
            if unit:
                for i in range(0, len(seq), len(unit)):
                    if issame(seq[i:i + len(unit)], unit):
                        lenhook += len(unit)
                    else:
                        break
        return lenhook

    def getbkunit(self):
        unit,flag = self.getmsiunit()
        lenhook = self.getlefthook(unit,flag)
        assert (int(self.POS) > 0)
        bk = int(self.POS) + (len(self.SEQ) - lenhook)
        return (unit,bk)

    def getmsiunit(self):
        seq = self.SEQ
        unitwin = seq[0:6]
        unit = []
        flag = 0
        for i in range(6):
            unit.append(seq[i+6])
            slidewin = seq[i+1:i+7]
            if slidewin != unitwin:
                continue
            else:
                flag = 1  
                return ''.join(unit),flag
        revseq = self.SEQ[-1::-1]
        revunitwin = revseq[0:6]
        revunit = []
        for i in range(6):
            revunit.append(revseq[i + 6])
            slidewin = revseq[i + 1:i + 7]
            if slidewin != revunitwin:
                continue
            else:
                flag =2   
                return ''.join(revunit),flag
        return  False , flag

class pairedRead:
    def __init__(self, *args):
        self.read1 = Read(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
        self.read2 = Read(args[10], args[11], args[12], args[13], args[14], args[15], args[16], args[17], args[18],args[19])
        self.msset = []

    def __getitem__(self):
        return self.read1.__getitem__(), self.read2.__getitem__()

    def classify(self):
        if self.read1.isRepete() and self.read2.isRepete():
            return 3  
        elif self.read1.isRepete():
            return 2  
        elif self.read2.isRepete():
            return 1 
        else:
            return 0  
    def getms(self):
        return self.msset

    def printinf(self):
        return self.__getitem__()

if __name__ == "__main__":
    l = "chr19_112721_113237_113138_1_1_0:0:0_0:0:0_57	83	chr19	113138	60	100M	=	112721	-517	AAAATTACTCAAAATTATTGTCCTCATTTCATCGTCTTCAGGACATCAAACTTAGTG".split()
    read1 = Read(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9])
    u, f = read1.getmsiunit()
    print read1.getlefthook(u,f)
    print f == 0
    print u,f
