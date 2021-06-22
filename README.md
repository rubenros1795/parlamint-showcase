# ParlaMint Showcase - Contested Expertise in COVID-19 Parliamentary Debates

This repository contains the code and planning for the ParlaMint showcase. This is a case study related to the [ParlaMint project](https://www.clarin.eu/content/parlamint-towards-comparable-parliamentary-corpora). The case focuses on the role of knowledge and expertise in parliamentary debates during the COVID-19 pandemic.

## Research
The case takes a three-step approach of:
1. aggregating references to scientific knowledge and expertise;
2. mapping the contestation of scientific knowledge and expertise;
3. mapping the differences between their employment across parties and individuals.

By taking this approach we aim to answer the following questions:
1. How and by whom is scientific knowledge employed in parliamentary debates?
2. How and by whom is scientific knowledge contested in parliamentary debates?
3. To what extent do we see changes in the politicality of scientific knowledge as measured through the interaction between employment and contestation?

## Methods
The text analysis is done in Python. In the ```code``` folder, all the scripts can be found. The case is based primarily on established text analysis methods such as frequency analysis, sentiment analysis and word association measures.

## Data
The original data can be downloaded [here](https://www.clarin.si/repository/xmlui/handle/11356/1431). Please cite:

```
 @misc{11356/1431,
 title = {Linguistically annotated multilingual comparable corpora of parliamentary debates {ParlaMint}.ana 2.1},
 author = {Erjavec, Toma{\v z} and Ogrodniczuk, Maciej and Osenova, Petya and Ljube{\v s}i{\'c}, Nikola and Simov, Kiril and Grigorova, Vladislava and Rudolf, Micha{\l} and Pan{\v c}ur, Andrej and Kopp, Maty{\'a}{\v s} and Barkarson, Starkaður and Steingr{\'{\i}}msson, Stein{\t h}{\'o}r and van der Pol, Henk and Depoorter, Griet and de Does, Jesse and Jongejan, Bart and Haltrup Hansen, Dorte and Navarretta, Costanza and Calzada P{\'e}rez, Mar{\'{\i}}a and de Macedo, Luciana D. and van Heusden, Ruben and Marx, Maarten and {\c C}{\"o}ltekin, {\c C}a{\u g}r{\i} and Coole, Matthew and Agnoloni, Tommaso and Frontini, Francesca and Montemagni, Simonetta and Quochi, Valeria and Venturi, Giulia and Ruisi, Manuela and Marchetti, Carlo and Battistoni, Roberto and Seb{\H o}k, Mikl{\'o}s and Ring, Orsolya and Darģis, Roberts and Utka, Andrius and Petkevi{\v c}ius, Mindaugas and Briedien{\.e}, Monika and Krilavi{\v c}ius, Tomas and Morkevi{\v c}ius, Vaidas and Bartolini, Roberto and Cimino, Andrea and Diwersy, Sascha and Luxardo, Giancarlo and Rayson, Paul},
 url = {http://hdl.handle.net/11356/1431},
 note = {Slovenian language resource repository {CLARIN}.{SI}},
 copyright = {Creative Commons - Attribution 4.0 International ({CC} {BY} 4.0)},
 year = {2021} }
```

## Code

The ```preprocessing``` folder contains the ```transform.ipynb``` notebook that takes the original data and transforms it to ```.tsv``` files ordered per month.

The ```code``` folder contains notebooks for several methods:

```closereading.ipynb```: a notebook for inspecting individual speeches based on keywords or metadata.

```collocations.ipynb```: a notebook for collocation analysis using ```nltk```.

```embeddings.ipynb```: a notebook for inspecting the semantics of keywords using ```word2vec``` models trained in ```train-w2v.py```.

```metadata.ipynb```: a notebook for visualising metadata (number of speakers per session, number of characters etc.).

```tfidf.ipynb```: a notebook for inspecting most relevant terms using Term Frequency - Inverse Document Frequency.

The ```functions.py``` file contains helper functions for data loading and the extraction of frequency distributions. 

The ```old``` folder contains other experiments that didn't make it to the final report.
