import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import concurrent.futures
from lxml import etree
import sys

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--language', dest="language", required=True)
args = parser.parse_args()

base_path = "/media/ruben/Elements/ParlaMint"


############
def rt(fn):
    with open(fn,'r') as f:
        c = f.read()
    return bs(c)

###########
def parse(fn):
    tree = etree.parse(fn)
    root = tree.getroot()
    namespaces = {}
    for k,v in root.nsmap.items():
        if not k:
            namespaces['ns'] = v

    d = {}
    for speech in root.findall('.//ns:u', namespaces):
        
        id_ = speech.attrib['{http://www.w3.org/XML/1998/namespace}id']
        speech_text = []
        for sentence in speech.findall('.//ns:s', namespaces):
            sentence_text = []
            for word in sentence.findall('.//ns:w', namespaces):
                if 'lemma' in word.attrib.keys():
                    lemma = word.attrib['lemma']
                sentence_text.append(lemma)
            speech_text.append(" ".join(sentence_text))
        d.update({id_:". ".join(speech_text)})
    d = pd.DataFrame(list(d.items()))
    ofn = fn.replace('-ana-xml','-ana-txt').replace('.xml','.txt')
    d.to_csv(ofn,sep='\t',index=False)

##########

if __name__ == "__main__":
    lan = args.language
    list_ = gb(f'{base_path}/{lan}/{lan}-ana-xml/*ana.xml*')
    if os.path.exists(f'{base_path}/{lan}/{lan}-ana-txt/') == False:
        os.mkdir(f'{base_path}/{lan}/{lan}-ana-txt/')
    print("transforming items:",len(list_))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as e:
        for u in list_:
            e.submit(parse, u)
