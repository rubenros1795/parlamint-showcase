# Script for transforming separate metadata .txt files to one metadata.json file for efficiency.

import json
import enum
import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from datetime import datetime, timedelta, date
from collections import OrderedDict
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
import math

base_path = "/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase"


def generate_metadata_json(language):
    metadata_files = os.path.join(base_path + "/data/original",f"{language}/{language}-txt/*")
    metadata_files = [x for x in gb(metadata_files) if "meta" in x]
    data = pd.DataFrame()
    for f in metadata_files:
        tdf = pd.read_csv(f,sep='\t')
        data = data.append(tdf)

    dict_ = {}
    for i,row in data.iterrows():
        key = row[0]
        td = {list(data.columns)[c+1].lower():i for c,i in enumerate(row[1:])}
        dict_.update({key:td})

    if os.path.exists(f"{base_path}/data/original/{language}/metadata") == False:
        os.mkdir(f"{base_path}/data/original/{language}/metadata")
    
    with open(f"{base_path}/data/original/{language}/metadata/metadata.json",'w',encoding='utf-8') as f:
        json.dump(dict_,f)

    [os.remove(x) for x in metadata_files]

for l in ['si','bg','pl']:
    generate_metadata_json(l)