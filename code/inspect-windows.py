import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from parser import *

list_xml = [x for x in gb("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/ParlaMint-PL-txt/*.txt") if "meta" not in x and "2020" in x]

fn = [x for x in list_xml if "2020-04-16" in x][0]
parse_object = DebateParser(fn=fn)
debate = parse_object.debates()
metadata = parse_object.metadata()
preprocessed = parse_object.preprocessed()

for k,v in preprocessed.items():
    if "koronawirusem" in v:
        indices = [c for c,i in enumerate(v) if i == "koronawirusem"]
        for ind_ in indices:
            left = ind_-5
            right = ind_ + 5
            if left < 0:
                left = 0
            if right > len(v):
                right = len(v)
            print(" ".join(v[left:right]),'\n')