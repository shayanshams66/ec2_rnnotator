module load gcc/4.9.0
module load perl/5.16.3/INTEL-14.0.2
module load blat/0.35/INTEL-14.0.2
echo starting assembly ; /work/sshams2/Rnnotator-3.4.0/scripts/rnnotator.pl -strP 225 CIZB_HEAD10.fastq -a Ray -n 16  
echo checking imp file
