#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gloname import *
from numpy import mean,var,std

def maxlike(num_reads, len_msi, len_ref, num_rpt, len_hook, delta):
    global COUNT
    global LEN_READS
    COUNT += 1
    cov = (num_reads * LEN_READS ) / (len_msi + 2 * len_ref)
    flag = 1
    try:
        le = (num_rpt * LEN_READS  + len_hook) / cov
    except ZeroDivisionError:
        print "Error:cov is zero!"
    while (flag == 1 and cov != 0):
        if (abs(le - len_msi) < le) or COUNT > 60:
            flag = 0
        else:
            len_msi = le 
            le = maxlike(num_reads,len_msi, len_ref, num_rpt, len_hook, delta)[0]
    return le, COUNT, cov

def cal_nor(bklist,posdic,lenhooklist,repetelist):
    print "Calculating_NormalParameter>>>>>>>>>>>>>>>>>>>>>>"
    keys = list(bklist.keys())
    ldic =  dict()
    rdic = dict()
    for key in keys:
        ldic[key]=[0]*ITIE_TIME  
        rdic[key]=[0]*3 
    num = len(keys)
    for key in keys:
        for i in range(ITIE_TIME):
            num_reads = posdic[bklist[key]][i] + repetelist[key]
            mlk =  maxlike(num_reads,MSI_INIT,REF_INIT,repetelist[key],lenhooklist[key],DELTA)
            ldic[key][i] = mlk[0]
    for key in keys:
        rdic[key][0]=mean(ldic[key])
        rdic[key][1]=round(var(ldic[key]))
        rdic[key][2]=round(std(ldic[key]))
    return rdic,ldic

def print_result(f_out,bklist,rdic,ldic):
    print "Wrinting_Result>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    keys = list(bklist.keys())
    print >>f_out,"UNIT","\t\t","BreakPoint","\t\t","NormalParameter","\t\t","Length"
    for key in keys:
        print >>f_out,key,"\t\t",bklist[key],"\t\t",rdic[key],"\t\t",ldic[key]
    return

