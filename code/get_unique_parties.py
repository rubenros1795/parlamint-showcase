import os
import pandas
from functions import *
import sys

language = sys.argv[1]

data = data_loader.full(language)
data = utils.add_metadata(data,language)
unique_parties = list(zip(data["speaker_party_name"],data["speaker_party"]))
unique_parties = [" \t ".join([x[0],x[1]]) for x in unique_parties]
for u in set(unique_parties):
	print(u,"\n----------------------------------")
#print(data.columns)
