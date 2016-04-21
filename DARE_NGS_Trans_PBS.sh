OUTPUT="$(cat $1 | wc -l)"
input=$1
echo "${OUTPUT}"
cs=2
z=$((OUTPUT/cs))
echo $z
mkdir tmp
#split -l $z $1 segment
echo splitting file into $cs parts;split -a $cs -d -l $z $1 tmp/segment
for (( i=0; i<$cs ; i++ ))
do
    cat > tmp/pbs.script.$i << EOF
#!/bin/bash
# ----------------QSUB Parameters----------------- #
#PBS -l  nodes=1:ppn=20,walltime=00:10:00
#PBS -N rnnotators$i
# ----------------Load Modules-------------------- #
#module load rnnotator/3.4.0
module load gcc/4.9.0
module load perl/5.16.3/INTEL-14.0.2
module load blat/0.35/INTEL-14.0.2
# ----------------Your Commands------------------- #
cd $PBS_O_WORKDIR
rnnotator.pl -strP 225 tmp/segment*$i -a Ray -n 16 -o output$i
touch tmp/$i.txt
exit 0;
 
EOF
pidarray[$i]=rnnotators$i
chmod u+x tmp/pbs.script.$i
qsub tmp/pbs.script.$i &
echo submit job no:$i
ARRAY[$i]=$!
echo sleeping 10;sleep 10
done
#for (( c=0; c<$cs ; c++ ))
#do
#	echo ${ARRAY[$c]}
#	qsub -hold_jidrnnotators$i
#done
#wait
#for pid in ${ARRAY[*]}; do wait $pid; done;
#for pid in ${ARRAY[*]}; do
#       while kill -0 "$pid"; do
#            sleep 0.5
#        done
#	echo $pid
#    done
#for pid in ${pidarray[*]}; do
#qsub -hold_jid rnnotators0
for (( c=0; c<$cs ; c++ ))
do
	while [ ! -f tmp/$c.txt ] 
		do
			sleep 1
		done
done
#c=1
#while (( $c+1<$cs ))
#do
#	echo merging; cat output$c/rnnotator_run/all_strP_1.dereplicated.fastq output$(c+1)/rnnotator_run/all_strP_1.dereplicated.fastq>temp.fastq
#	c++
#done
#if [  -f temp.fastq ];then 
#	cat output0/rnnotator_run/all_strP_1.dereplicated.fastq temp.fastq > temp1.fastq
#	mv temp1.fastq output0/rnnotator_run/all_strP_1.dereplicated.fastq 
#else
#   	cat output0/rnnotator_run/all_strP_1.dereplicated.fastq output1/rnnotator_run/all_strP_1.dereplicated.fastq >temp.fastq
#	mv temp.fastq output0/rnnotator_run/all_strP_1.dereplicated.fastq
#fi
echo merging; cat output*/rnnotator_run/all_strP_1.dereplicated.fastq > input.fastq

echo preprocess jobs are done
module load gcc/4.9.0
module load perl/5.16.3/INTEL-14.0.2
module load blat/0.35/INTEL-14.0.2
echo starting assembly ; rnnotator.pl -strP 225 tmp/segment*0 -a Ray -n 16 -o output0 &
wait
sleep 30 ;echo checking imp file
IFS=$'\r\n' GLOBIGNORE='*' command eval 'XYZ=($(cat kmer.txt))'
for kmer in ${XYZ[*]}
do	
	while [ ! -f $kmer.imp ]
                do
                        sleep 1
                done
done
touch assem.finish
qsuab last.pbs
