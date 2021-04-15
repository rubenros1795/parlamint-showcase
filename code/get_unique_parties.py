import os
import pandas
from functions import *
import sys

language = sys.argv[1]

data = data_loader.full(language)
data = utils.add_metadata(data,language)
unique_parties = list(zip(data["speaker_party_name"],data["speaker_party"]))
unique_parties = pandas.DataFrame(unique_parties,columns=["speaker_party_name","speaker_party"]).groupby(["speaker_party_name","speaker_party"]).sum().reset_index()

print(unique_parties[["speaker_party","speaker_party_name"]])
