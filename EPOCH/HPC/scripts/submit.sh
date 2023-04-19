#!/bin/sh
#PBS -N twoD0.4
#PBS -P physics
#PBS -q low
#PBS -m bea
#PBS -M $USER@iitd.ac.in
###################Edit_accordingly######################
#PBS -l select=10:ncpus=4:mpiprocs=6
#PBS -l place=scatter
#PBS -l walltime=00:07:00
#PBS -o stdout_file
#PBS -e stderr_file
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
export directories="7run 8run 9run"
## The input files must be in the directory

module load apps/epoch/4.9.0/intel2015

bash run.sh > output
##time -p mpirun -n $PBS_NTASKS epoch2d > output
##time echo $PBS_O_WORKDIR | mpirun -np $PBS_NTASKS epoch2d
##time echo $PBS_O_WORKDIR | mpirun -np $PBS_NTASKS epoch3d
