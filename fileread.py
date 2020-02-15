#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read import *
from cluster import *
from samfunction import *
from maxlike import *

path = "C:/Users/Administrator/Desktop/inpostxt/MSI_4/RealData/"
class fileRead:
    def __init__(self):
        self.counter = 0
        self.doubleset = dict()
        self.oneset = dict()
        self.twoset = dict()
        self.bklist = dict()
        self.unitdic = None
        self.bk = None
        self.repetelist = dict()
        self.lenhooklist = dict()
        self.snplist= dict()

    def classifyMSI(self, filename):
        filename.seek(0)
        unit = []
        while True:
            line1 = filename.readline()
            if not line1: break
            line2 = filename.readline().strip()  #strip
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if pairedread.read1.isRepete() and pairedread.read2.isRepete():
                r = pairedread.read1.isRepete()
                unit.append(r[1])
        msilist = [unit[0]]
        for i in range(1, len(unit)):
            if unitindex(unit[i], msilist) is False:
                msilist.append(unit[i])
        return msilist

    def countMSI(self, filename):
        filename.seek(0)
        counter1 = 0
        while True:
            line = filename.readline()
            if not line: break
            line_list = line.split('\t')
            readseq = line_list[9].upper()
            read = Read(line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5],
                        line_list[6], line_list[7], line_list[8], readseq)
            if read.isRepete():
                self.counter += 1
                continue
            else:
                counter1 += 1
                continue
        return self.counter, counter1

    def countdoubleMSI(self, filename): 
        filename.seek(0)
        counter0 = counter1 = counter2 = counter3 = 0
        while True:
            line1 = filename.readline()
            if not line1: break
            line2 = filename.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if int(pairedread.classify()) == 3:  
                counter3 += 1
                continue
            if int(pairedread.classify()) == 2: 
                counter2 += 1
                continue
            if int(pairedread.classify()) == 1:  
                counter1 += 1
                continue
            if int(pairedread.classify()) == 0:  
                counter0 += 1
                continue
        return counter3, counter2, counter1, counter0

    def countrpt(self, filename):
        num1, num2, num3, num4 = self.countdoubleMSI(filename)
        return num1 * 2 + num2 + num3

    def countsum(self, filename):
        filename.seek(0)
        num1, num2, num3, num4 = self.countdoubleMSI(filename)
        return (num1 + num2 + num3 + num4) * 2

    def getset(self):
        return self.doubleset, self.oneset, self.twoset

    def getalnone(self, file_in, file_out, file_out1):
        file_in.seek(0)
        counter1 = counter2 = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (str(pairedread.read1.CIGAR) == '100M' and str(pairedread.read2.CIGAR) != '100M' and str(
                    pairedread.read2.CIGAR) != '*') \
                    or (str(pairedread.read1.CIGAR) != '100M' and str(pairedread.read1.CIGAR) != '*' and str(
                        pairedread.read2.CIGAR) == '100M'):
                print >> file_out, pairedread.printinf()
                counter1 += 1
            if (str(pairedread.read1.CIGAR) == '100M' and str(pairedread.read2.CIGAR) == '*') or \
                    (str(pairedread.read1.CIGAR) == '*' and str(pairedread.read2.CIGAR) == '100M'):
                print >> file_out1, '*', pairedread.printinf()
                counter2 += 1
        return counter1, counter2

    def getdoublealn(self, file_in, file_out):
        file_in.seek(0)
        counter = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (str(pairedread.read1.CIGAR) == str(pairedread.read2.CIGAR) == '100M'):
                print >> file_out, pairedread.printinf()
                counter += 1
        return counter

    def searchBK(self, file_in, lmsi):
        file_in.seek(0)
        candidate = []
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (pairedread.read1.CIGAR == '100M' and pairedread.read2.CIGAR != '100M' and pairedread.read2.isRepete() is False
                and (int(pairedread.read1.POS) < int(pairedread.read2.POS))):
                bkun = pairedread.read2.getbkunit()
                if bkun[0] and bkun[1]:
                    candidate.append(bkun)
        cpos = cluster(candidate, 100, 0)
        print len(cpos)
        pos = []
        for i in range(len(cpos)):
            pos.append(cpos[i][0])
        return pos

    def searchHook(self, file_in):
        file_in.seek(0)
        len_hook = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            if len(line1_list) > 10 and len(line2_list) > 10:
                readseq1 = line1_list[9].upper()
                readseq2 = line2_list[9].upper()
                pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
                if (pairedread.read1.CIGAR == '100M' and pairedread.read2.CIGAR != '100M' and not pairedread.read2.isRepete()): 
                    len_hook += pairedread.read2.getlefthook()
                    continue
                if (pairedread.read1.CIGAR != '100M' and not pairedread.read1.isRepete() and pairedread.read2.CIGAR == '100M'): 
                    len_hook += pairedread.read1.getlefthook()
                    continue
        return len_hook

    def searchHook1(self, file_in):
        file_in.seek(0)
        len_hook1 = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (pairedread.read1.isRepete() and pairedread.read2.CIGAR != '100M' and not pairedread.read2.isRepete()): 
                len_hook1 += pairedread.read2.getlefthook()
                continue
            elif (pairedread.read1.CIGAR != '100M' and not pairedread.read1.isRepete() and pairedread.read2.isRepete()): 
                len_hook1 += pairedread.read1.getlefthook()
                continue
        return len_hook1

    def searchHook2(self, file_in):
        file_in.seek(0)
        len_hook2 = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (pairedread.read1.CIGAR != '100M' and pairedread.read2.CIGAR != '100M'):
                len_hook2 += pairedread.read1.getlefthook()
                len_hook2 += pairedread.read2.getlefthook()
                continue
        return len_hook2

    def getlenhook(self, file_in):
        le1 = self.searchHook(file_in)
        le2 = self.searchHook1(file_in)
        le3 = self.searchHook2(file_in)
        return le1 + le2 + le3

    def countreads(self, file_in):
        file_in.seek(0)
        counter = 0
        for line in file_in:
            counter += 1
        return counter

    def searchHook3(self, file_in):
        file_in.seek(0)
        len_hook = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (pairedread.read1.CIGAR == '100M' and pairedread.read2.CIGAR != '100M' and not pairedread.read2.isRepete()):
                len_hook = pairedread.read2.getlefthook()
                break
            if (pairedread.read1.CIGAR != '100M' and not pairedread.read1.isRepete() and pairedread.read2.CIGAR == '100M'):
                len_hook = pairedread.read1.getlefthook()
                break
        return len_hook

    def searchHook4(self, file_in):
        file_in.seek(0)
        len_hook1 = 0
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if (pairedread.read1.isRepete() and pairedread.read2.CIGAR != '100M' and not pairedread.read2.isRepete()):
                len_hook1 = pairedread.read2.getlefthook()
                break
            if (pairedread.read1.CIGAR != '100M' and not pairedread.read1.isRepete() and pairedread.read2.isRepete()):
                len_hook1 = pairedread.read1.getlefthook()
                break
        return len_hook1

    def getlenhook1(self, file_in):
        le1 = self.searchHook3(file_in)
        le2 = self.searchHook4(file_in)
        return le1 + le2

    def countCS(self, filename, msi_list):
        # c = self.classifyMSI(filename)
        filename.seek(0)
        msl = [[] for i in range(len(msi_list))]
        for i in range(len(msi_list)):
            msl[i].append(msi_list[i])
            msl[i].append(0)
        while True:
            line1 = filename.readline()
            if not line1: break
            line2 = filename.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if pairedread.read1.isRepete() and pairedread.read2.isRepete():
                ms = pairedread.read1.isRepete()[1]
                id = unitindex(ms, msi_list)
                if type(id) is int:
                    msl[id][1] += 2
            elif pairedread.read1.isRepete():
                ms = pairedread.read1.isRepete()[1]
                id = unitindex(ms, msi_list)
                if type(id) is int:
                    msl[id][1] += 1
            elif pairedread.read2.isRepete():
                ms = pairedread.read2.isRepete()[1]
                id = unitindex(ms, msi_list)
                if type(id) is int:
                    msl[id][1] += 1
            else:
                continue
        return msl  

    def ratioMS(self, filename, msi_list):
        l = self.countCS(filename, msi_list)
        print l
        nl = []
        for i in range(len(l)):
            nl.append(l[i][1])
        s = float(min(nl))
        sl = []
        for i in range(len(nl)):
            sl.append(nl[i] / s)
        rl = []
        for i in range(len(l)):
            rl.append((l[i][0], sl[i]))
        return rl  

    def printrpt_read(self,file_in):
        file_in.seek(0)
        f_out = open("C:\\Users\\Administrator\\Desktop\\rpt1.txt",'w')
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if int(pairedread.classify()) == 2:
                print >>f_out,pairedread.read1.FLAG,':',pairedread.read1.SEQ,'\n',pairedread.read2.FLAG,':',pairedread.read2.SEQ,'\n','!!!!!!!!'
        f_out.close()

    def bk_unit(self,file_in):
	print "Geting_breakpoint&unit>>>>>>>>>>>>>>>>>>>>>>>"
        file_in.seek(0)
        bklist = []
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            '''readlen1 = len(pairedread.read1.SEQ)
            readlen2 = len(pairedread.read2.SEQ)
            if pairedread.read1.CIGAR == str(readlen1) + "M" and pairedread.read2.CIGAR != str(readlen2) + "M" and \
                            pairedread.read2.CIGAR != "*" and int(pairedread.read1.POS) < int(pairedread.read2.POS):
                # if pairedread.read1.verify(ref) and pairedread.read2.getmsiunit():
                if pairedread.read2.getmsiunit()[0]:
                    bkun = pairedread.read2.getbkunit()  
                    bklist.append(bkun)
            elif pairedread.read2.CIGAR == str(readlen2) + "M" and pairedread.read1.CIGAR != str(readlen1) + "M" and \
                            pairedread.read1.CIGAR != "*" and int(pairedread.read2.POS) < int(pairedread.read1.POS):
                # if pairedread.read2.verify(ref) and pairedread.read1.getmsiunit():
                if pairedread.read1.getmsiunit()[0]:
                    bkun = pairedread.read1.getbkunit()  
                    bklist.append(bkun)
            else:
                continue'''
            if pairedread.read1.isMap() and not pairedread.read2.isMap() and  pairedread.read2.CIGAR != "*" and \
                int(pairedread.read1.POS) < int(pairedread.read2.POS) and pairedread.read2.getmsiunit()[0]:
                bkun = pairedread.read2.getbkunit() 
                bklist.append(bkun)
            elif not pairedread.read1.isMap() and pairedread.read1.CIGAR != "*"and pairedread.read2.isMap() and \
                int(pairedread.read2.POS) < int(pairedread.read1.POS) and pairedread.read1.getmsiunit()[0]:
                bkun = pairedread.read1.getbkunit()  
                bklist.append(bkun)
            else:
                continue
        rebu = cluster(bklist,30,1,alpha=0.1)
        keys = []
        bklist =[]
        for r in rebu:
            bklist.append(r[0])
        self.bklist = dict(bklist)
        self.unitdic = list(self.bklist.keys())
        return self.bklist,self.unitdic

    def get_hook(self,file_in):    
        file_in.seek(0)
        lenhooklist = {}
        repetelist = {}
        SNPlist = {}
        unitlist = []
        if self.unitdic is None:
            unitlist = self.bk_unit(file_in)[1]
        elif self.unitdic == []:
            return
        else:
            unitlist = self.unitdic
        #print unitlist
        lenhooklist = lenhooklist.fromkeys(unitlist,0)
        repetelist = repetelist.fromkeys(unitlist,0)
        SNPlist = SNPlist.fromkeys(unitlist,'')
        while True:
            line1 = file_in.readline()
            if not line1: break
            line2 = file_in.readline().strip()
            line1_list = line1.split('\t')
            line2_list = line2.split('\t')
            readseq1 = line1_list[9].upper()
            readseq2 = line2_list[9].upper()
            pairedread = pairedRead(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                                    line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1, \
                                    line2_list[0], line2_list[1], line2_list[2], line2_list[3], line2_list[4],
                                    line2_list[5], line2_list[6], line2_list[7], line2_list[8], readseq2)
            if not pairedread.read1.isMap():
                unit , flag = pairedread.read1.getmsiunit()
                if  unit and flag != 0 and pairedread.read1.isRepete(unit,flag):
                    key = unitfromlist(unit,unitlist)
                    if key:
                        repetelist[key] += 1
                        SNP=findSNP(unit,readseq1)
                        if SNP and not SNPlist[key]:
                            SNPlist[key]=SNP
                if unit and flag != 0 and not pairedread.read1.isRepete(unit,flag):
                    key = unitfromlist(unit, unitlist)
                    if key:
                        lenhook = pairedread.read1.getlefthook(unit, flag)
                        lenhooklist[key] += lenhook
                        SNP=findSNP(unit,readseq1[len(readseq1)-lenhook+len(unit):len(readseq1)])
                        if SNP and not SNPlist[key]:
                            SNPlist[key]=SNP
            if not pairedread.read2.isMap():
                unit , flag = pairedread.read2.getmsiunit()
                if unit and flag != 0 and pairedread.read2.isRepete(unit,flag):
                    key = unitfromlist(unit,unitlist)
                    if key:
                        repetelist[key] += 1
                        SNP=findSNP(unit,readseq2)
                        if SNP and not SNPlist[key]:
                            SNPlist[key]=SNP
                if unit and flag != 0 and not pairedread.read2.isRepete(unit,flag):
                    key = unitfromlist(unit, unitlist)
                    if key:
                        lenhook = pairedread.read2.getlefthook(unit, flag)
                        lenhooklist[key] += lenhook
                        SNP=findSNP(unit,readseq2[len(readseq2)-lenhook+len(unit):len(readseq2)])
                        if SNP and not SNPlist[key]:
                            SNPlist[key]=SNP
        assert (len(lenhooklist) == len(repetelist))
        delkey = []
        for key in lenhooklist:
            if lenhooklist[key] == 0 and repetelist[key] == 0:
                delkey.append(key)
        for key in delkey:
            del lenhooklist[key]
            del repetelist[key]
            del SNPlist[key]
            del self.bklist[key]
        self.lenhooklist = lenhooklist
        self.repetelist = repetelist
        self.SNPlist=SNPlist
        self.bk = self.bklist.values()
        return self.lenhooklist,self.repetelist,self.bk,self.SNPlist

    def read_count(self,file_in, poslist):
        posdic = dict()
        for key in poslist:
            posdic[key] = [0]*ITIE_TIME
        length = REF_INIT
        for i in range(ITIE_TIME):
            file_in.seek(0)
            while True:
                line = file_in.readline()
                if not line: break
                line_list = line.split('\t')
                readseq = line_list[9].upper()
                read = Read(line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5],line_list[6],
                        line_list[7], line_list[8], readseq)
                readlen  = len(readseq)
                pos = int(read.getpos())
                for p in poslist:
                    if (p- length / 2 - readlen) < pos < (p + length / 2 - readlen):
                        posdic[p][i] +=1
            length = length + REF_PLUS
        return posdic

if __name__ == "__main__":
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    #f = open(path +raw_input("Enter the filename:") , 'rU')
    f = open(path+file1,'rU')
    f_out = open(path+file2,'w')
    fr = fileRead()
    #fr.printrpt_read(f)
    bklist,unitlist=fr.bk_unit(f)
    lenhooklist,repetelist,bk=fr.get_hook(f)
    #f_out = open(path +raw_input("Enter the out filename:"), 'w')
    print len(bklist)
    print >>f_out,'bklist:',bklist
    print len(unitlist)
    print >>f_out,'unitlist:',unitlist
    print >>f_out,"lenhooklist:",lenhooklist
    print len(lenhooklist)
    print >>f_out,"repetelist:",repetelist
    print len(repetelist)
    print len(bk)
    f_out.close()
    posdic = fr.read_count(f,bk)
    rdic = cal_nor(bklist,posdic,lenhooklist,repetelist)
    print >> f_out, "rdic", rdic
    f_out.close()
    f.close()
    print "OK"
