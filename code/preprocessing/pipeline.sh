#!/bin/sh

python3 "preprocess.py $1"
python3 "generate_flat_lemmatized_data.py $1"
python3 "generate_metadata.py $1"
python3 "generate_totals.py $1"