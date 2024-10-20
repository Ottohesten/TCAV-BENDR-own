import os
from collections import defaultdict
# if os.getcwd().split("/")[-1] != 'BENDR-XAI': os.chdir("../")

import mne
import numpy as np
import matplotlib.pyplot as plt
from utils import *

from matplotlib import animation
import matplotlib.cm as cm
import sys
from tqdm import tqdm
from pathlib import Path

subjects_dir, subject, trans, src_path, bem_path = get_fsaverage()

random_edf_file_path = 'notebooks/S001R03.edf' 
# mmidb_path = Path(r"/home/s194260/BENDR-XAI/data/eegmmidb/files")
mmidb_path = Path(r"C:\Users\Otto\OneDrive - Danmarks Tekniske Universitet\DTU\Kurser\Bachelors\data\mmidb\files")
parcellation_name = "aparc.a2009s"
snr = 1.0

info = get_raw(random_edf_file_path, filter=True).info # Just need one raw to get info
src = get_src(src_path)
fwd = get_fwd(info, trans, src_path, bem_path)

labels = get_labels(subjects_dir, parcellation_name = parcellation_name)

def calculate_activity_per_label(annotation_dict, labels, compute_inverse):
    activity = {}

    for anno in annotation_dict.keys():
        activity[anno] = np.empty((len(annotation_dict[anno]), sum(len(hemi) for hemi in labels)))
        for i, window in enumerate(annotation_dict[anno]):
            stc = compute_inverse(window)
            activity[anno][i] = np.concatenate(get_power_per_label(stc, labels, standardize=False))

    return activity

dataset_activity = defaultdict(lambda: {})

pbar = tqdm()

for (dirpath, _, filenames) in os.walk(mmidb_path):
    for filename in filenames:
        if filename.endswith(".edf"):
            filepath = Path(dirpath) / filename       
            raw = get_raw(filepath, filter=True, resample=160)
            annotations = get_annotations(filepath)
            annotation_dict = get_window_dict(raw, annotations)

            cov = get_cov(raw)
            compute_inverse = make_fast_inverse_operator(raw.info, fwd, cov, snr=snr)

            activity = calculate_activity_per_label(annotation_dict, labels, compute_inverse)
            dataset_activity[dirpath.split('/')[-1]][filename[:-4]] = activity

            pbar.update(1)
            pbar.set_description(filename[:-4])

pbar.close()

dataset_activity = dict(dataset_activity)

np.save("mmidb_{}_{}_new".format(parcellation_name, str(round(snr, 1))), dataset_activity, allow_pickle=True)