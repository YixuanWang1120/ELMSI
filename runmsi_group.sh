#! /bin/bash

coverage=(1 6 24 38 24 6 1)
nor=(0.1 0.3 0.4 0.7 0.9)
tur=(0.9 0.7 0.5 0.3 0.1)
cvg=100
mkdir -p group/snp 
for((num =1;num<2;num++));
do
for((i = 1;i < 2;i++));
do
echo ${nor[$i-1]}
echo ${tur[$i-1]}
	for((j = 1;j < 8;j++));
	do
	s[j-1]=$(echo " ${nor[$i-1]}*${coverage[$j-1]} "|bc -l)
	done
	for((j = 8;j < 15;j++));
	do
	s[j-1]=$(echo " ${tur[$i-1]}*${coverage[$j-8]} "|bc -l)
	done
	for((j = 1;j < 15;j++));
	do
	echo coverage，${s[$j-1]}
	./norsim -r 0 -X 0 -D 0 -B 0  -I ./inpos$j.txt ref.fa n0.sim
	./readgen -d 500 -c  ${s[$j-1]} -l 200 -r 200 -I n0.sim.idx ref.fa n0.sim l$j.fq r$j.fq
	done
cat l*.fq > l.fq
cat r*.fq > r.fq
read -p "Press any key to continue."
 bwa index -a is ref.fa
 bwa aln ref.fa l.fq>l.sai
 bwa aln ref.fa r.fq>r.sai
 bwa sampe -f ./group/snp/tum_tur${tur[$i-1]}.sam ref.fa l.sai r.sai l.fq r.fq
 sed -i '1d' ./group/snp/tum_tur${tur[$i-1]}.sam
 sed -i '1d' ./group/snp/tum_tur${tur[$i-1]}.sam
 echo "*******start processing "$i"file********"
read -p "Press any key to continue."
 python /home/wyx/sim/LMSI/fileclass/maindetect.py  group/snp/tum_tur${tur[$i-1]}.sam  group/snp/tum_tur${tur[$i-1]}.txt
 echo "************"$i"file finished********"
read -p "Press any key to continue."
done
done
