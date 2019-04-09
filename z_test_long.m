clc;
clear all;
c=0.1;
% distribution parameters of normal sample
mu_nor=[86,425,46,43,89,71,56,76,45,100,78,221,78,40,58,90,77,70,89,146,213,134,185,105,167,205,120,90,56,355];
sigma_nor=2;
i=30
% the length data
L_MIX=...
[883.8774763181411, 805.6849918540241, 743.3179738463851, 691.7463253601903, 643.248501560874, 603.8210598290599, 569.4719576232151, 534.1067588292473, 505.6021347510479, 482.46775414634146, 460.36999441444794, 441.2289864382584, 425.54810085190604, 409.10774983454667, 391.9237977492471, 376.8992058532124, 362.8508680020544, 350.38220773699874, 338.4174693765825, 327.3728637627433, 316.7623930310018, 306.85619756763464,344.9130918057663, 291.6878119987167, 250.1901238304898,  298.0529459980713, 290.06360959587073, 281.3183047954946, 63.3450087089807, 61.204369572534496, 55.723885143417505, 54.108844254002264, 52.56958138190228]
L = (L_MIX-(1-c)*mu_nor(i))/c;
L=L';
[mu_tum, sigma_tum] = normfit(L);
H=ztest(L,mu_nor(i),sigma_nor);
if H == 0
    disp('stable')
else
    disp('unstable')
end