import re, string,os
from glob import glob as gb
import pandas as pd
from tqdm import tqdm
import subprocess


original_path = "/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original"
covid_subset_path = "/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/covid-subsets"

df_terms = pd.read_csv('/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/resources/keywords-corona-translation.csv')

def subset(lan):
    terms = [x.lower() for x in list(df_terms[df_terms['language'] == lan]["translation"])]
    print(terms)
    language_original_path = os.path.join(original_path,f"{lan}/{lan}-txt")
    language_pp_path = os.path.join(original_path,f"{lan}/{lan}-txt-preproc")
    list_files = [x for x in gb(language_original_path + "/*") if "meta" not in x and "READ" not in x]
    path = f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{lan}/{lan}-txt-preproc/*"
    grp = "egrep -iE '" + "|".join(terms) + "' " + path.replace('*',"*2020*")
    output = subprocess.check_output(grp,shell=True).decode('utf-8')
    output = [l.split('\t') for l in output.split('\n')]
    if len(output) > 0:
        output = pd.DataFrame(output)
    output.to_csv(os.path.join(covid_subset_path,f"{lan}-covid-subset.txt"),sep='\t',index=False)    

subset('si')