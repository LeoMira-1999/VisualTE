# VisualTE 3 Web App

## About / Synopsis

VisualTE lets users visualize transposable elements (TE) in a specific genome, neighboring genes, TE/genes copies distribution, Gene ontology of your selected TE, all other TEs, and the genes. The third version of VisualTE is a web based app, a web deployment of the first standalone version.

## Installation

- Install all required packages:
```
pip install dash
pip install dash-uploader
pip install dash-bio
pip install pandas
pip install importlib
```
 - [Clustal Omega download](http://www.clustal.org/omega/)
 - [FastTree download](http://www.microbesonline.org/fasttree/#Install)
- Download the VisualTE 3 repository
- Download [Data zip file](https://unice-my.sharepoint.com/:u:/g/personal/leonardo_mirandola_etu_unice_fr/EVb_WSZpbmBBg-TJD1YrnJ0B8FqhabPsarhJ8Kt7awUevg?e=REHNn4)
- Extract zip file
- Move DATA folder to VisualTE/Scripts/
- On your terminal navigate to the downloaded repo folder
- Using python 3 `python3 make_VisualTE3.py -Dash`

## Authors and acknowledgements

VisualTE project idea and development by Sebastien Tempel who also created the background data processing and final visualisation result web page. Web based pre-data selection, data and transposable elements loading page app developed by Leonardo Mirandola and coordinated by Sebastien Tempel.

## Modifications from previous VisualTE 3 build

- Added a dash_uploader folder
- modified Make_visualTE3.py
- In Scripts folder:
 - Modified all make_functions imports
 - Created Interface_Main_Dash.py and dash_functions.py files

dash_functions.py file contains Sebastien Tempel's functions but without the incorporated view components (tkinter)
