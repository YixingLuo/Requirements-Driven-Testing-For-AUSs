#!/bin/bash
#SBATCH -o UUV-test-adaptive.%j.out
#SBATCH -A hpc0006178148
#SBATCH -p C032M0128G
#SBATCH --qos=high
#SBATCH -J UUV-test-adaptive-Job
#SBATCH --nodes=1
#SBATCH --get-user-env
#SBATCH --ntasks-per-node=6
#SBATCH --time=120:00:00
#SBATCH --mail-type=end

module load matlab/R2020a
matlab -nodesktop -nosplash -r UUV_test_adaptive
