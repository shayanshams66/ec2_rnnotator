kmer_length=$1
cat > pbs.script.ray.$kmer_length << EOF
#!/bin/bash
# ----------------QSUB Parameters----------------- #
#PBS -l  nodes=1:ppn=20,walltime=00:10:00
#PBS -N ray$kmer_length
#PBS -e /home/sshams2/error.txt
#PBS -o /home/sshams2/output.txt
# ----------------Load Modules-------------------- #
#module load rnnotator/3.4.0
module load gcc/4.9.0
module load perl/5.16.3/INTEL-14.0.2
module load blat/0.35/INTEL-14.0.2
module load ray/2.3.1/INTEL-140-MVAPICH2-2.0
# ----------------Your Commands------------------- #
cd $PBS_O_WORKDIR
Ray -k $kmer_length -i input.fastq -o outputRay$kmer_length
touch $kmer_length.imp
mv outputRay$kmer_length/* output0/rnnotator_run/Ray/ak$kmer_length
exit 0;
EOF
qsub pbs.script.ray.$kmer_length
cat >> kmer.txt <<EOF
$kmer_length
EOF
