# Steps for Preprocessing

The data needs several preprocessing steps before it can be used for analysis. This subfolder includes scripts for preprocessing and enriching the data. 

## Reformatting the data
The data is downloaded as a compressed archive with several folders. For the analysis, we use the plain text version and the annotated version. Extract both sets and place them in the folder structure printed below. To indicate the different languages ISO 639-1 codes are used (See [Wiki](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)).

````
├── original
└───── bg
       ├── bg-txt
       └── bg-txt-preproc
       └── bg-xml
       └── bg-ana-xml
       └── bg-ana-txt
       └── metadata
└───── fr
       ├── ...
└───── bg
       ├── ...
````

````/bg-txt```` contains text files (separated by ````tab````) with ````id```` and ````text````. Metadata text files are in the same folder. The script ````generate_metadata.py```` transforms these metadata text files to one ````.json```` file and removes the metadata text files. The new metadata file is placed in the ````/metadata```` subfolder.

````/bg-txt-preproc```` contains preprocessed text files, still matchable with the metadata file. To preprocess, simply run ````preprocess.py```` with the options of tokenizing, removing punctuation and lowercasing.

````/bg-xml```` contains the original xml files from the dump. 

````/bg-ana-xml```` contains the original xml data from the annotated dump. This data stems from the ````ParlaMint-....TEI.ana```` subfolder in this dump.

````/bg-ana-txt```` contains "flattened" text files that contain the lemmatized text found in the annotated files. To flatten the annotated xml data, run ````generate_flat_lemmatized_data.py````
