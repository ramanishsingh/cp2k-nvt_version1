cd /panfs/roc/groups/12/siepmann/singh891/projects/signac/cp2k/iodine
#PBS -N 409wP48a1000tc
#PBS -M singh891@umn.edu
#PBS -m abe
#PBS -l walltime=00:10:00,mem=300gb,nodes=1:ppn=10

module load mkl
module load fftw
module load intel/cluster/2018
module load python
/panfs/roc/msisoft/anaconda/anaconda3-2018.12/bin/python project.py exec run_config 4a54cb77289f361a77be93e891eda4d4
/panfs/roc/msisoft/anaconda/anaconda3-2018.12/bin/python project.py exec run_config 0154c40573aade595a99b583a90d3945

