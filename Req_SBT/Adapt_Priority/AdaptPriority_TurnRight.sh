#!/bin/bash
#SBATCH -J adaptpriority_turnright
#SBATCH -o adaptpriority_turnright.%j.%N.out
#SBATCH --partition=C144M4096G
#SBATCH --qos=high
#SBATCH -A hpc0006178148
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=50
#SBATCH --mail-type=end
#SBATCH --mail-user=yixingluo@pku.edu.cn
#SBATCH --time=120:00:00

module load singularity/3.2.0
singularity run /gpfs/share/imgs/app/wine.sif
module load anaconda/3-4.4.0.1
conda info -e
source activate tensorflow-gpu
python Req_SBT_TurnRight.py


