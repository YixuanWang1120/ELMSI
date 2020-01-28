# -*- coding: utf-8 -*-


 
import scipy
from scipy.stats import f
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
# additional packages
from statsmodels.stats.diagnostic import lillifors
 
group1=[2,3,7,2,6]
group2=[10,8,7,5,10]
group3=[10,13,14,13,15]
list_groups=[group1,group2,group3]
list_total=group1+group2+group3
 
 
#正态分布测试
def check_normality(testData):
    #20<样本数<50用normal test算法检验正态分布性
    if 20<len(testData) <50:
       p_value= stats.normaltest(testData)[1]
       if p_value<0.05:
           print"use normaltest"
           print "data are not normal distributed"
           return  False
       else:
           print"use normaltest"
           print "data are normal distributed"
           return True
     
    #样本数小于50用Shapiro-Wilk算法检验正态分布性
    if len(testData) <50:
       p_value= stats.shapiro(testData)[1]
       if p_value<0.05:
           print "use shapiro:"
           print "data are not normal distributed"
           return  False
       else:
           print "use shapiro:"
           print "data are normal distributed"
           return True
       
    if 300>=len(testData) >=50:
       p_value= lillifors(testData)[1]
       if p_value<0.05:
           print "use lillifors:"
           print "data are not normal distributed"
           return  False
       else:
           print "use lillifors:"
           print "data are normal distributed"
           return True
     
    if len(testData) >300: 
       p_value= stats.kstest(testData,'norm')[1]
       if p_value<0.05:
           print "use kstest:"
           print "data are not normal distributed"
           return  False
       else:
           print "use kstest:"
           print "data are normal distributed"
           return True
 
 
#对所有样本组进行正态性检验
def NormalTest(list_groups):
    for group in list_groups:
        #正态性检验
        status=check_normality(group1)
        if status==False :
            return False
             
     
#对所有样本组进行正态性检验   
NormalTest(list_groups)