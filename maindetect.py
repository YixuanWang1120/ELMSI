#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read import *
from cluster import *
from samfunction import *
from fileread import *
from gloname import *
from maxlike import *
from numpy import mean,var,std
import sys
import time

#path = "/home/xjd/Public/1000genomes_2/NA19240/"
if __name__ == "__main__":
    start = time.clock()
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    #f = open(path +raw_input("Enter the filename:") , 'rU')
    f = open(file1,'rU')
    f_out = open(file2,'w')
    fr = fileRead()
    bklist,unitlist=fr.bk_unit(f)
    lenhooklist,repetelist,bk,SNPlist=fr.get_hook(f)
    posdic = fr.read_count(f,bk)
    rdic,ldic= cal_nor(bklist,posdic,lenhooklist,repetelist)     #计算长度分布参数
    end = time.clock()
    print >>f_out,"****************Number of MSI*****************"
    print >>f_out,len(bklist)
    print >>f_out,"****************BreakPoint List of MSI*****************"
    print >>f_out,bklist                            #保存unit:断点的字典
    '''print >>f_out,"****************Unit List of MSI*****************"
    print >>f_out,unitlist
    print >>f_out,"****************LenHook List of MSI*****************"
    print >>f_out,lenhooklist
    print >>f_out,"****************Repete List of MSI*****************"
    print >>f_out,repetelist'''
    print >>f_out,"****************Normal parameter List of MSI*****************"
    print >>f_out, rdic
    print_result(f_out,bklist,rdic,ldic)
    print >>f_out,"****************Running Time*****************"
    print >>f_out,"Running Time:%f s" %(end - start)
    f_out.close()
    f.close()
    print "OK"
