#!/usr/bin/env python
# -*- coding: utf-8 -*-

def cluster(lis_ins,epsilon,ind,alpha = 0.9):
    lis_sorted = sorted(lis_ins,key = lambda tu:tu[ind])
    len_lis = len(lis_ins)
    result = [[]]
    if len_lis == 0 :
        return result
    num_cluster = 0
    xt = lis_sorted[0][ind]
    st = xt
    result[0].append(lis_sorted[0])
    print len_lis
    for i in range(1,len_lis):
        xt = lis_sorted[i][ind]
        st = alpha * xt + (1 - alpha) *st
        if abs(st - xt) <= epsilon:
            result[num_cluster].append(lis_sorted[i])
        else:
            st = xt
            result.append([])
            num_cluster += 1
            result[num_cluster].append(lis_sorted[i])
    return result
