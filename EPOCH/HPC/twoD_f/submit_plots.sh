#!/bin/sh
#PBS -N twoDViz3.5
#PBS -P ecrt.std
#PBS -q standard
#PBS -m bea
#PBS -M $USER@iitd.ac.in
###################Edit_accordingly######################
#PBS -l select=10:ncpus=4:mpiprocs=6
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -o stdout_file_plots
#PBS -e stderr_file_plots
#PBS -r n
#########################################################
export OMP_NUM_THREADS=1

# Environment
echo "==============================="
echo $PBS_JOBID
echo $PBS_NTASKS
cat $PBS_NODEFILE
echo "==============================="
cd $PBS_O_WORKDIR
## The input files must be in the directory

module load apps/epoch/4.17.10/intel2019 && module load apps/anaconda/3

bash run_plots.sh > output_plots
