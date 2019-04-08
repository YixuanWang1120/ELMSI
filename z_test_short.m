clc;
clear all;
% get the read count distribution from the MSIsensor results
N_rc=[
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 45 6 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
];
TM_rc=[
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 42 8 2 2 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
];
L=[];
for i=1:100
    if 	TM_rc(i)~=0
    L=[L,ones(1,TM_rc(i))*i];
    end   
end
d=L;
mu_nor=22;
sigma_nor=1;
% the likelihood function
pdf = @(d,mu,sigma) 0.9*(1./(sqrt(2*pi)*sigma_nor))*exp(-((d-mu_nor).^2)./2)+0.1*(1./(sqrt(2*pi)*sigma))*exp(-((d-mu).^2)./(2*sigma.^2));
phat = mle(d,'pdf',pdf,'start',[10,1])
L_N=[];
for i=1:100
    if 	N_rc(i)~=0
    L_N=[L_N,ones(1,N_rc(i))*i];
    end   
end
A = L_N';
H=ztest(A,phat(1),phat(2))
if H == 0
disp('stable')
else
disp('unstable')
end