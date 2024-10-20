#!/bin/bash

#SBATCH --job-name=mmidb_activity_high1.0_low4.0_4
#SBATCH --output=/home/s194101/TCAV-BENDR-own/mmidb_activity_4-%J.out
#SBATCH --cpus-per-task=30
#SBATCH --mem=120gb
#SBATCH --gres=gpu:1
#SBATCH --mail-user=otto@skytop.dk
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=titans
#SBATCH --export=ALL
#SBATCH --time=08:00:00

## INFO

echo "Node: $(hostname)"
echo "Start: $(date +%F-%R:%S)"
echo -e "Working dir: $(pwd)\n"

source ~/.bashrc
source activate myenv
python src/source_localization/calculate_activity_parallel.py --high_pass 1.0 --low_pass 4.0

echo "Done: $(date +%F-%R:%S)"