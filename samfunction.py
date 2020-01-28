#!/usr/bin/env python
# -*- coding: utf-8 -*-

def comple(base): #取某个碱基的互补碱基
    if base == 'A' or base == 'a':
        return 'T'
    if base == 'T' or base == 't':
        return 'A'
    if base == 'C' or base == 'c':
        return 'G'
    if base == 'G' or base == 'g':
        return 'C'

def revunit(unit): #将unit逆序
    return unit[::-1]

def compleunit(unit): #取unit的互补链
    # reu = unit[::-1]
    uc = ''
    for i in range(len(unit)):
        uc += str(comple(unit[i]))
    return uc

def revcompleunit(unit): #取unit的反向互补链
    # reu = unit[::-1]
    uc = ''
    for i in range(len(unit)):
        uc += str(comple(unit[i]))
    return uc[::-1]
    #return  uc

def issame(u1, u2):
    l = [] #例如：unit="ATG",L中保存['ATG', 'CAT', 'TGA', 'TCA', 'GAT', 'ATC']
    l1 = len(u1)
    l2 = len(u2)
    if l1 != l2:
        return False
    for i in range(l1):
        x = u1[i:] + u1[0:i]
        cx = compleunit(x)
        rcx = revcompleunit(x)
        l.append(x)
        l.append(cx)
        l.append(rcx)
    return u2 in l

def unitindex(u, ulist): #取某一unit在MSIlist中的索引位置
    for i in range(len(ulist)):
        if issame(u, ulist[i]):
            return i
    return False

def unitfromlist(u,ulist):
    for i in ulist:
        if issame(u,i):
            return i
    return False

def unitissame(unitlist): #k-mer+滑动窗口识别unit
    assert(len(unitlist)==6)
    if issame(unitlist[0],unitlist[1]) and issame(unitlist[1],unitlist[2]) and issame(unitlist[2],unitlist[3]) and issame(unitlist[3],unitlist[4]) and issame(unitlist[4], unitlist[5]):
        return unitlist[0]
    else:
        return False



def  findSNP(unit,seq):
    start=seq.find(unit)
    SNP=[]
    for i in range(start, len(seq)-start, len(unit)):
        if seq[i:i + len(unit)] != unit:
            tem=seq[i:i + len(unit)+1]
            if  len(tem) >= len(unit):
                for j in range(len(unit)):
                    if tem[j] != unit[j]:
                       SNP=[comple(tem),tem[j],i]
                       break
                break
    return SNP



if __name__ == "__main__":
    lt = ['AAGAA', 'AAGAA', 'CTCGCA', 'GGA', 'AGG', 'GTG', 'TAC', 'CAT', 'ATACA', 'TG', 'ACC', 'AAGT', 'C', 'C', 'AGGCTT', 'TCTG', 'TGTC', 'GCCT', 'CTGG', 'CGGT', 'TTCTG', 'CTGTT', 'ATTTTC', 'CCCTGG', 'GGTCCC', 'CTCTGA', 'CTCAGT', 'TCT', 'CATCG', 'GACCA', 'AGTTAT', 'TGATAT', 'CCATAA', 'TTA', 'ATT', 'TCCTT', 'TAT', 'TTGTT', 'ATCGC', 'AGTTC', 'TGGGAG', 'GAGGGT', 'CTCG', 'TG', 'CTT', 'AT', 'AACCGC', 'AACGCC', 'AT', 'TCCTTC', 'TCCTCT', 'GCGGT', 'GCA', 'GCT', 'CGT', 'TTGA', 'AGTT', 'TTAG', 'TGG', 'GTG', 'AGACAG', 'GA', 'AGCAC', 'TAA', 'CCCAA', 'AGCA', 'GAAC', 'ACGA', 'GGTCTG', 'TCTGGG', 'TGGTT', 'AGGGT', 'GAA', 'TTAAGG', 'AATTGG', 'TCTGGA', 'GACA', 'GGCG', 'AC', 'TAACGA', 'TTAT', 'GT', 'GT', 'TG', 'TTAGC', 'GATTC', 'TTCGA', 'CGATCC', 'CT', 'TCGT', 'TA', 'ATT', 'TAT', 'GAGGAC', 'GCGGG', 'CT', 'CT', 'G', 'CAG', 'GGAGAC', 'AGAT', 'AGAT', 'TTCGAC', 'GCTCG', 'GCTCG', 'TTGTCA', 'GC', 'CTTC', 'ACTTG', 'CGCTCC', 'GAGCC', 'TGGA', 'GGATA', 'GGTCC', 'GTA', 'AATCA', 'GCTGG', 'CGGGT', 'TGA', 'A', 'ACT', 'ATAATG', 'ACA', 'TCTAC', 'TGTT', 'TCAT', 'GGTTGA', 'GTTGGA', 'TTGGAG', 'GGTC', 'CA', 'CA', 'T']
    for i in lt:
        if len(i) == 6:
            print i
    print unitfromlist("AACCAT",lt)
    print unitfromlist("TGGTAT", lt)
    #print unitfromlist("")
    print unitfromlist("ATG",["TGA","A","ATG"])
