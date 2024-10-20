#!/bin/bash

#SBATCH --job-name=mmidb_activity_high1.0_low4.0
#SBATCH --output=/home/s194101/TCAV-BENDR-own/experiment_logs/mmidb_activity-%J.out
#SBATCH --cpus-per-task=16
#SBATCH --mem=12gb
#SBATCH --gres=gpu:1
#SBATCH --mail-user=otto@skytop.dk
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=titans
#SBATCH --export=ALL
#SBATCH --time=04:00:00

## INFO

echo "Node: $(hostname)"
echo "Start: $(date +%F-%R:%S)"
echo -e "Working dir: $(pwd)\n"

source ~/.bashrc
source activate myenv
python src/source_localization/calculate_activity_parallel.py --high_pass 1.0 --low_pass 4.0

echo "Done: $(date +%F-%R:%S)"