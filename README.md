# ELMSI
## Accurately estimating the length distributions of genomic micro-satellites by tumor purity deconvolution
We proposed a computational approach, named ELMSI, which detected MSI events based on the next generation sequencing technology. ELMSI can estimate the specific length distributions and states of micro-satellite regions from a mixed tumor sample paired with a control one. It first estimated the purity of the tumor sample based on the read counts of the filtered SNVs loci. Then, the algorithm identified the length distributions and the states of short micro-satellites by adding the Maximum Likelihood Estimation (MLE) step to the existing algorithm. After that, ELMSI continued to infer the length distributions of long micro-satellites by incorporating a simplified
Expectation Maximization (EM) algorithm with central limit theorem, and then used statistical tests to output the states of these micro-satellites. Based on our experimental results, ELMSI was able to handle micro-satellites with lengths ranging from shorter than one read length to 10kbps.

## input data<br>
-----
>inpos1-14.txt (1-7:normal 8-14:tumor)<br>

## distribution parameters estimation<br>
------
>runmsi_group.sh<br>

## MS state estimation<br>
-------
>short ms: z_test_short.m<br>
>long ms: z_test_long.m
