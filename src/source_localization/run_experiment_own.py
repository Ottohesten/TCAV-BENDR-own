import os, time
# os.chdir('/zhome/33/6/147533/XAI/BENDR-XAI')


for high, low in zip([1.0, 4.0, 8.0, 12.0, 30.0], [4.0, 8.0, 12.0, 30.0, 70.0]):
    name = f"mmidb_activity_{high}_{low}_aparc"

    job = f"""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --output=/home/s194101/TCAV-BENDR-own/{name}-%J.out
#SBATCH --cpus-per-task=30
#SBATCH --mem=120gb
#SBATCH --gres=gpu:1
#SBATCH --mail-user=otto@skytop.dk
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=titans
#SBATCH --export=ALL
#SBATCH --time=08:00:00
## INFO

echo 'Node: $(hostname)'
echo 'Start: $(date +%F-%R:%S)'
echo -e 'Working dir: $(pwd)\n'

source ~/.bashrc
source activate myenv
python src/source_localization/calculate_activity_parallel.py --high_pass {high} --low_pass {low}

echo 'Done: $(date +%F-%R:%S)'"""

    with open('temp_submit.sh', 'w') as file:
        file.write(job)

    os.system('sbatch temp_submit.sh')
    time.sleep(0.5)
    os.remove('temp_submit.sh')
