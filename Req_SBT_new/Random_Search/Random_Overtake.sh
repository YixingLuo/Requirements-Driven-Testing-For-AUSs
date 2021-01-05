#!/bin/bash
#SBATCH -J random_overtake
#SBATCH -o random_overtake.%j.%N.out
#SBATCH --partition=C032M0256G
#SBATCH --qos=high
#SBATCH -A hpc0006178148
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mail-type=end
#SBATCH --mail-user=yixingluo@pku.edu.cn
#SBATCH --time=120:00:00

module load singularity/3.2.0
singularity run /gpfs/share/imgs/app/wine.sif
module load anaconda/3-4.4.0.1
conda info -e
source activate tensorflow-gpu
python Random_Overtake.py

