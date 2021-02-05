import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from parser import *

# Functions
def count_unigrams(text):
    counts = dict(Counter(text))
    return counts


list_xml_total = [x for x in gb("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/ParlaMint-PL-txt/*.txt") if "meta" not in x]


years = list(set([os.path.split(x)[-1][13:20] for x in list_xml_total]))

for year in years:
    ngram_filename = f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/ngrams/ngrams-pl-{year}.txt"
    print(ngram_filename)
    open(ngram_filename,'w',encoding='utf-8').close()
    with open(ngram_filename, "a") as f:
        f.write("\t".join("id unigram count term session sitting date subcorpus speaker_id speaker_name speaker_role speaker_type speaker_party speaker_party_name speaker_gender speaker_birth total_tokens_speech_preprocessed".split(' ')) + '\n')

    with open(ngram_filename, "a") as f:
        for fn in tqdm([f for f in list_xml_total if year in f]):
            parse_object = DebateParser(fn=fn)
            metadata = parse_object.metadata()
            debates_or = parse_object.debates()
            debates = parse_object.preprocessed()

            for id_,speech in debates.items():
                unigrams = count_unigrams(speech)

                for unigram,count in (unigrams).items():
                    t = [id_,unigram,count,metadata[id_]["term"],metadata[id_]["session"],metadata[id_]["sitting"],metadata[id_]["date"],metadata[id_]["subcorpus"],metadata[id_]["speaker_id"],metadata[id_]["speaker_name"],metadata[id_]["speaker_role"],metadata[id_]["speaker_type"],metadata[id_]["speaker_party"],metadata[id_]["speaker_party_name"],metadata[id_]["speaker_gender"],metadata[id_]["speaker_birth"],len(debates)]
                    t = "\t".join([str(x) for x in t])
                    f.write(t + '\n')
