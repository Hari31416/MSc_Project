#!/bin/sh
#PBS -N twoD3.3
#PBS -P ecrt.std
#PBS -q standard
#PBS -m bea
#PBS -M $USER@iitd.ac.in
###################Edit_accordingly######################
#PBS -l select=15:ncpus=6:mpiprocs=6
#PBS -l place=scatter
#PBS -l walltime=03:00:00
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
export directories="8run"
## The input files must be in the directory

module load apps/epoch/4.17.10/intel2019 && module load apps/anaconda/3

bash run.sh > output
bash run_plots.sh > output_plots
##time -p mpirun -n $PBS_NTASKS epoch2d > output
##time echo $PBS_O_WORKDIR | mpirun -np $PBS_NTASKS epoch2d
##time echo $PBS_O_WORKDIR | mpirun -np $PBS_NTASKS epoch3d
