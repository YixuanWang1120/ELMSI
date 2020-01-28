#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from read import *
def read_len(file_in):
    file_in.seek(0)
    len = 0
    while True:
        line1 = file_in.readline()
        if not line1: break
        line1_list = line1.split('\t')
        readseq1 = line1_list[9].upper()
        read1 = Read(line1_list[0], line1_list[1], line1_list[2], line1_list[3], line1_list[4],
                     line1_list[5], line1_list[6], line1_list[7], line1_list[8], readseq1)
        len = read1.length()
        break
    return len

#path = "/home/xjd/Public/1000genomes_2/NA19240/"
filename = sys.argv[1]
COUNT = 0
LEN_READS= read_len(open(filename,'rb'))
print LEN_READS
REF_INIT = 5000
REF_PLUS = 1000
ITIE_TIME = 30
MSI_INIT = 1.0
DELTA = 10

