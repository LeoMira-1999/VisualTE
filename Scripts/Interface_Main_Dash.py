#!/usr/bin/python3
# -*- coding: utf-8 -*-
#author: Leonardo Mirandola

#importing neccessary packages
import os
import sys
import os.path

#Package to move / copy
import shutil

#packages to import with string and link paths
import importlib
import importlib.util

#packgae to unzip
import zipfile

#package for gunzip
import gzip

#dash packages
import dash
import dash_uploader as du
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#dash package to prevent updates
from dash.exceptions import PreventUpdate

#dash package that can be called if an output doesn't need to change
from dash import no_update

#import app
from app import app

#importing all necessary backend file management for Data processing
from . import Interface_DownloadGenomes
from . import dash_functions
from . import ReadInfos_TE
from . import ReadInfos_GeneOntology
from . import ReadInfos_WikiPathways
from . import Create_MainFile
from . import Create_Color
from . import Create_CommonDATA

#importing all necessary backend file management for TE processing
from . import Create_CommonDATA2
from . import Create_MainFile
from . import Create_SelectedAnnotations
from . import Create_Random_Sequences
from . import Create_Overlap_TFBS
from . import Create_Alignment_and_Tree

#importing all necessary backend dash app creation for TE processing
from . import MakeFunction_GenomeBrowser
from . import MakeFunction_ChromosomeDistribution
from . import MakeFunction_GeneralFeaturesDistribution
from . import MakeFunction_SimilarityOccurrences
from . import MakeFunction_TEEnvironment
from . import MakeFunction_DistanceNeighboringGene
from . import MakeFunction_NeighboringGeneFunctions
from . import MakeFunction_OverlappingTFBS
from . import MakeFunction_SummaryTable


#######################################################################
def Dash_CreateGenomeDATA():
    """
    Arguments: None

    Description: Called when the user uses the '-Dash' argument in the make_VisualTE3.py
                to launch the dash interface

    Return: None

    """
    #all necessary global variables to be used and modified upon call
    global pathVisual
    global pathVisualDATA
    global pathVisualDATA2
    global tab_status
    global enabling
    global Genome_Name
    global TE_method
    global fileTE
    global fileFNA
    global fileGFF
    global GO_basic_file
    global repbase
    global nbSeq_Assemble
    global nameOrganism
    global maxSize
    global taxon
    global dictionary_organ
    global dictionary_tissue
    global dataTE
    global pathVisualNEW
    global pathVisualFunctions
    global ListeCompleteTE
    global ListeFamilleTE
    global ListeSuperFamilyTE
    global list_selection_TE
    global indexTE
    global numberOFselection
    global ListeConsensus
    global moduleSelectTE
    global moduleCommonDATA
    global NameSeq
    global DEB
    global FIN
    global Sens
    global Size
    global Similarity
    global listGeneSelect5
    global listGeneSelect3
    global listGeneSelectInside
    global randomSeqDEB
    global randomSeqFIN
    global randomSeqCHR
    global tissue_dictionary_SelectedTE
    global organ_dictionary_SelectedTE
    global tissue_dictionary_Global
    global organ_dictionary_Global
    global tissue_dictionary_RandomSeq
    global organ_dictionary_RandomSeq
    global nbSeq_Assemble
    global numberTE
    global res

    if not os.path.exists("DB.txt"):
        with open("DB.txt" , "w") as file:
            file.write("")

    genome_dropdown = []

    with open("DB.txt" , "r") as file:
        lines = file.readlines()
        for line in lines:
            genome = line.split("\t")[2]
            genome_dropdown.append({"label":genome,"value":genome})

    #allows the upload of files bigger than 200 Mb in a Dash_upload directory
    du.configure_upload(app, "Dash_upload", use_upload_id=False)

    #creation of the app layout
    app.layout = html.Div([

        #Creating the main div
        html.Div(id = "main-all", children = [


        ##############################################################

        #creating a H1 main title centered
        html.H1(children='VisualTE V3', style = {'textAlign': 'center'}),

        #creating a Div for genome and method name input
        html.Div([

            html.H3(children = "Enter your genome name and method name", id = "main-text"),

            html.Div([

                dcc.Dropdown(
                    id='genome-dropdown',
                    placeholder = 'Enter your genome name',
                    style = {'margin':'2% 0% 2% 0%'},
                    options = genome_dropdown,
                    multi = False
                ),

                dcc.Dropdown(
                    id='TE-dropdown-selector',
                    placeholder = 'Enter your TE name',
                    style = {'margin':'2% 0% 2% 0%'},
                    disabled = True,
                    multi = False
                ),

                #genome name textbox
                dcc.Input(
                  id="genome-name-entry",
                  type="text",
                  placeholder="Enter your genome name here",
                  style={
                      'width': '20%'
                  }),

                #method name textbox
                dcc.Input(
                  id="method-name-entry",
                  type="text",
                  placeholder="Repet or RepeatMasker or Blast",
                  style={
                      'width': '21%',
                      'margin' : '20px'
                  }),

                #submit button
                html.Button('Initiate', id='initiation', n_clicks=0),
            ],id = "pre-processing", )

        ], style = {
            'width': '80%',
            'margin' : '10px 10%',
            'display' : 'block',
            'textAlign': 'center'
            }),

        #horizontal line
        html.Hr(id = "hr"),

        ###########################################################

        #creation of the tab section
        dcc.Tabs([

            #creating a tab
            dcc.Tab(label='Data Loading', children=[

                ##############################################################
                #TE file upload div
                html.Div([

                    html.H6("Upload your TE file"),

                    # file Uploading component
                    du.Upload(
                        id="upload-TE",
                        text = "Drag and drop or click to select file",
                        max_files=1,
                        max_file_size = 10240, # limited to 10 Gb
                        pause_button=True,
                        default_style = {
                            'width': '80%',
                            'height': '30%',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center'}
                    ),

                ], id = "TE-container",style = {
                    'float':'left',
                    'width' :'25%',
                    'height': '10%',
                    'margin' : '20px',
                    'display' : 'none'

                    }),

                ##############################################################

                #genome files div
                html.Div([

                    html.H6("Upload your genome files"),

                    #radiobutton div
                    html.Div([

                        #radiobuttons to select upload or download
                        dcc.RadioItems(
                            id = "genome-file-bool",
                            options=[
                                {'label': 'Local', 'value': 'yes'},
                                {'label': 'Download', 'value': 'no'},
                            ],
                            value = None,
                            labelStyle={'display': 'inline-block'}),

                    ]),

                #Upload genome files
                html.Div([
                          html.P("Upload your FNA file"),

                          #Uploading component
                          du.Upload(
                              id="upload-FNA",
                              text = "Drag and drop or click to select file",
                              max_files=1,
                              max_file_size = 10240, # Max 10 Gb upload
                              pause_button=True,
                              default_style = {
                                  'width': '80%',
                                  'height': '30%',
                                  'lineHeight': '60px',
                                  'borderWidth': '1px',
                                  'borderStyle': 'dashed',
                                  'borderRadius': '5px',
                                  'textAlign': 'center'}
                          ),


                          html.P("Upload your GFF file"),

                          #Uploading component
                          du.Upload(
                              id="upload-GFF",
                              text = "Drag and drop or click to select file",
                              max_files=1,
                              max_file_size = 10240, # Max 10 Gb upload
                              pause_button=True,
                              default_style = {
                                  'width': '80%',
                                  'height': '30%',
                                  'lineHeight': '60px',
                                  'borderWidth': '1px',
                                  'borderStyle': 'dashed',
                                  'borderRadius': '5px',
                                  'textAlign': 'center'}
                          ),

                      ], id = 'genome-container-yes'),

                # genome download files
                html.Div([

                        #textbox input genome name
                        dcc.Input(
                        id="genome-entry",
                        type="text",
                        placeholder="Enter your genome name",
                        style={
                            'width': '80%',
                            'margin' : '10px'
                        }),

                        # download button
                        html.Button('Download', id='submit-genome', n_clicks=0,
                            style={
                                'width': '80%',
                                'margin' : '10px'
                        }),

                        #loading icon
                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-output-genome", style={'margin':'20px'})
                            ),

                        #div used to display text when download completed
                        html.Div(id = "genome-download-output")

                    ], id = 'genome-container-no'),

                ], id = 'genome-container',style = {
                    'float':'left',
                    'width' :'25%',
                    'height': '10%',
                    'margin' : '20px',
                    'display' : 'none'
                    }),

                ##############################################################
                #GO files div
                html.Div([

                    html.H6("Upload your GO files"),

                    # GO radiobutton div
                    html.Div([

                        #radiobutton to select local or download
                        dcc.RadioItems(
                            id = "GO-file-bool",
                            options=[
                                {'label': 'Local', 'value': 'yes'},
                                {'label': 'Download', 'value': 'no'},
                            ],
                            value = None,
                            labelStyle={'display': 'inline-block'}),

                    ]),

                #GO upload div
                html.Div([
                          html.P("Upload your GO basic list file"),

                          #uploading component
                          du.Upload(
                              id="upload-GO",
                              text = "Drag and drop or click to select file",
                              max_files=1,
                              max_file_size = 10240, #max 10 Gb
                              pause_button=True,
                              default_style = {
                                  'width': '80%',
                                  'height': '30%',
                                  'lineHeight': '60px',
                                  'borderWidth': '1px',
                                  'borderStyle': 'dashed',
                                  'borderRadius': '5px',
                                  'textAlign': 'center'}
                          ),

                      ], id = 'GO-container-yes'),

                #GO download div
                html.Div([

                    #Breaking line
                    html.Br(),

                    #Download button
                    html.Button("Download GO files", id="GO-download", n_clicks = 0, style={
                        'width': '80%',
                        'margin' : '45px 20px 10px 20px'
                        }),

                    #loading circle
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="loading-output-GO", style={'margin':'20px'})
                        ),

                    #div to display download has been finished
                    html.Div(id = "GO-download-output")

                    ], id = 'GO-container-no'),

                ],id = 'GO-container',style = {
                    'float':'left',
                    'width' :'25%',
                    'height': '10%',
                    'margin' : '20px',
                    'display' : 'none'
                    }),

                ##############################################################

                #CHIP-Seq files Div
                html.Div([
                    html.H6("Upload your CHIP-Seq files"),

                    # radio button div
                    html.Div([

                        #radio button to select uplaod or download
                        dcc.RadioItems(
                            id = "CHIP-file-bool",
                            options=[
                                {'label': 'Local', 'value': 'yes'},
                                {'label': 'Download', 'value': 'no'},
                            ],
                            value = None,
                            labelStyle={'display': 'inline-block'}),

                    ]),

                #CHIP-Seq upload div
                html.Div([
                          html.P("Upload your CHIP-Seq file in zip format"),

                          #uploading component
                          du.Upload(
                              id="upload-CHIP",
                              text = "Drag and drop or click to select file",
                              max_file_size = 10240, #Max 10 Gb
                              max_files=1,
                              pause_button=True,
                              default_style = {
                                  'width': '80%',
                                  'height': '30%',
                                  'lineHeight': '60px',
                                  'borderWidth': '1px',
                                  'borderStyle': 'dashed',
                                  'borderRadius': '5px',
                                  'textAlign': 'center'}
                          ),

                      ], id = 'CHIP-container-yes'),

                # CHIP-Seq download div
                html.Div([

                    # textbox entry
                    dcc.Input(
                      id="CHIP-entry",
                      type="text",
                      placeholder="Enter your genome name",
                      style={
                          'width': '80%',
                          'margin' : '10px'
                      }),

                    #download button
                    html.Button("Download CHIP-Seq files", id="CHIP-download", n_clicks = 0, style={
                        'width': '80%',
                        'margin' : '10px',
                        }),

                    #loading circle
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="loading-output-CHIP", style={'margin':'20px'})
                        ),

                    #div used to display finished download
                    html.Div(id = "CHIP-download-output")

                    ], id = 'CHIP-container-no'),

                ],id = 'CHIP-container',style = {
                    'float':'left',
                    'width' :'25%',
                    'height': '10%',
                    'margin' : '20px',
                    'display' : 'none'
                    }),

                #Submit button
                html.Button("Submit", id = "submit-button", n_clicks = 0, style={
                    'width': '30%',
                    'margin' : '10px 35%',
                    'display' : 'none'
                    }),

                #loading circle
                dcc.Loading(
                    type="circle",
                    children=html.Div(id="loading-submit-button",style={'margin':'30px'})
                    ),

                #div used in case file missing
                html.Div(id = "submit-prompt", children = "Please check your content", style={
                    'width': '30%',
                    'margin' : '10px 35%',
                    'display' : 'none'
                    })

            ], value = "data-loading", id = "tab-data-loading"),

#########################################################################

            #data processing tab
            dcc.Tab(label='Data Processing', id = "tab-data-processing", value = "data-processing",disabled = True, children=[

                #main div of data processing
                html.Div([

                    # The following code will be displayed as such:
                    # 7 steps, each of them will have an attributed text and
                    # loading circle that will let the user know where the
                    # program is at
                    ################################################
                    html.Div([
                            "Extracting TE data from Repbase sequences"

                    ], id = "repbase", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        #loading circle
                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-repbase", style={'margin':'20px'})
                            ),


                    ], id = "container-repbase", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Extracting TE data from TE file"

                    ], id = "TE", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE", style={'margin':'20px'})
                            ),

                    ], id = "container-TE", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Extracting NCBI annotations from GFF file"

                    ], id = "GFF", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-GFF", style={'margin':'20px'})
                            ),

                    ], id = "container-GFF", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Extracting gene ontology from GO-basic file"

                    ], id = "GO", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-GO", style={'margin':'20px'})
                            ),

                    ], id = "container-GO", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Copying SVG files from wikipathways"

                    ], id = "wiki", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-wiki", style={'margin':'20px'})
                            ),

                    ], id = "container-wiki", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Transforming CHIP-Seq Data"

                    ], id = "CHIP", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-CHIP", style={'margin':'20px'})
                            ),

                    ], id = "container-CHIP", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Finalising files and results"

                    ], id = "final", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-final", style={'margin':'20px'})
                            ),

                    ], id = "container-final", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                ], style = {
                    'width': '80%',
                    'margin' : '10px 10%',
                    'display' : 'block',
                    })
            ]),
#########################################################################
            # TE selection tab
            dcc.Tab(label='TE Selection', id = "tab-TE-selection", value = "TE-selection",disabled = True,children=[

                #main div of TE selection tab
                html.Div(children = [

                    html.H6("Select your TE(s) from the dropdown list"),
                    html.P("Up to 3 families (same superfamily)"),

                    #dropdown menu
                    dcc.Dropdown(
                        id='TE-dropdown',
                        placeholder = 'Enter your TE(s) name',
                        style = {'margin':'2% 0% 2% 0%'}
                    ),

                    #div used to display selected item from dropdown menu
                    html.Div(id = "TE-selected", style = {'margin':'0% 0% 2% 0%'}),

                    #selection button
                    html.Button('Select TE', id='TE-select-button', n_clicks=0),

                    html.Div("Merge TE families:", style = {'margin':'2% 0% 0% 0%'}),

                    #radio button used to select merging
                    dcc.RadioItems(
                        options=[
                            {'label': 'Yes', 'value': 'yes'},
                            {'label': 'No', 'value': 'no'},
                        ],
                        id = "radio-TE",
                        value = "no",
                        labelStyle={'display': 'inline-block', 'margin':'20px'}
                    ),

                    #submit button
                    html.Button('Submit', id='TE-finish-button', n_clicks=0),

                    #loading circle
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="loading-TE-selection", style={'margin':'20px'})
                        ),

                ], style = {
                    'width': '80%',
                    'margin' : '10px 10%',
                    'display' : 'block',
                    'textAlign': 'center'
                    })
            ]),

#########################################################################

            #TE processing tab
            dcc.Tab(label='TE Processing', id = "tab-TE-processing", value = "TE-processing",disabled = True, children=[

                #main div of TE processing
                html.Div([

                    # The following code will be displayed as such:
                    # 18 steps, each of them will have an attributed text and
                    # loading circle that will let the user know where the
                    # program is at
                    ################################################

                    html.Div([
                            "Processing for the selected TE(s) and creating Selected TE File"

                    ], id = "proc-create-TE", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-proc-create-TE", style={'margin':'20px'})
                            ),


                    ], id = "container-proc-create-TE", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Loading TE File"

                    ], id = "TE-load", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-load", style={'margin':'20px'})
                            ),


                    ], id = "container-TE-load", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating Genic Environment File"

                    ], id = "gene-env", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-gene-env", style={'margin':'20px'})
                            ),


                    ], id = "container-gene-env", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Alignment and Phylogenetic Tree Files"

                    ], id = "TE-align-phylo", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-align-phylo", style={'margin':'20px'})
                            ),


                    ], id = "container-TE-align-phylo", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating Random Sequences and Their Genic Environment"

                    ], id = "random-seq", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-random-seq", style={'margin':'20px'})
                            ),


                    ], id = "container-random-seq", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Selecting Overlap TFBS for TE Sequences"

                    ], id = "TFBS-seq", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TFBS-seq", style={'margin':'20px'})
                            ),


                    ], id = "container-TFBS-seq", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Selecting Overlap TFBS for Random Sequences"

                    ], id = "TFBS-random", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TFBS-random", style={'margin':'20px'})
                            ),


                    ], id = "container-TFBS-random", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Printing Overlap TFBS for TE/Random Sequences"

                    ], id = "TFBS-random-print", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TFBS-random-print", style={'margin':'20px'})
                            ),


                    ], id = "container-TFBS-random-print", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating Main File (VisualTE3.py)"

                    ], id = "main-file", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-main-file", style={'margin':'20px'})
                            ),


                    ], id = "container-main-file", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Genome Browser File Function"

                    ], id = "TE-genome-browser", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-genome-browser", style={'margin':'20px'})
                            ),


                    ], id = "container-TE-genome-browser", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Chromosome Distribution File Function"

                    ], id = "TE-chrom-distrib", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px',
                        'background-color' : 'none'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-chrom-distrib", style={'margin':'20px'})
                            ),


                    ], id = "container-TE-chrom-distrib", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE General Features File Function"

                    ], id = "TE-general", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-general", style={'margin':'20px'})
                            ),

                    ], id = "container-TE-general", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Gene Distance file"

                    ], id = "TE-gene-distance", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-gene-distance", style={'margin':'20px'})
                            ),

                    ], id = "container-TE-gene-distance", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Genetic Functions File"

                    ], id = "TE-genic-func", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-genic-func", style={'margin':'20px'})
                            ),

                    ], id = "container-TE-genic-func", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Overlapping TFBS File Function"

                    ], id = "TE-TFBS", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-TFBS", style={'margin':'20px'})
                            ),

                    ], id = "container-TE-TFBS", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE Similarity Occurrences File Function"

                    ], id = "TE-sim-occ-func", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-sim-occ-func", style={'margin':'20px'})
                            ),

                    ], id = "container-TE-sim-occ-func", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating TE environment "

                    ], id = "TE-env", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-TE-env", style={'margin':'20px'})
                            ),

                    ], id = "container-TE-env", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                    ################################################
                    html.Div([
                            "Creating summary table"

                    ], id = "summary", style = {
                        'width': '80%',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),
                    html.Div([

                        dcc.Loading(
                            type="circle",
                            children=html.Div(id="loading-summary", style={'margin':'20px'})
                            ),

                    ], id = "container-summary", style = {
                        'width': '20%',
                        'textAlign' : 'right',
                        'font-size' : ' 24px',
                        'float':'left',
                        'display' : 'block',
                        'margin' : '2% 0px'

                    }),

                ], id = "TE-main-div", style = {
                    'width': '80%',
                    'margin' : '10px 10%',
                    'display' : 'block',
                    })

            ]),

        ],id = "main-tabs", style = {'display': 'none'}),

        ])
    ])

###############################################################################

# app callbacks are used to monitor the activity of the user via an
# Input ('id_name','component_to_listen_to')
    @app.callback(

        [Output("pre-processing", "style"),
        Output("main-text", "children"),
        Output("main-text", "style"),
        Output("TE-container", "style"),
        Output("hr", "style"),
        Output("main-tabs", "style")],
        Input("initiation", "n_clicks"),
        State("genome-dropdown", "value"),
        State("TE-dropdown-selector", "value"),
        State("genome-name-entry", "value"),
        State("method-name-entry", "value"),
        prevent_initial_call =True
    )

    def start(click, genome_dropdown, TE_dropdown,GenomeName, TEmethod):
        """
        Arguments: listen for a click, genome name textbox, method name textbox

        Description: when the user hits initiate, it will take the genome name
                    and methode name to display it and create the appropriate
                    directory

        Returns: changes the css style of genome name textbox, method name textbox
                initiation button, the main text with the new content, creates a
                horizontal line and displays the tabs

        """
        #global variables that will be modified and listened to
        global pathVisual
        global pathVisualDATA
        global pathVisualDATA2
        global Genome_Name
        global TE_method
        global tab_status
        global enabling

        Genome_Name = GenomeName
        TE_method = TEmethod

        #used in the return to hide the appropriate output
        selectors = {'display': 'none'}

        #used in the return to center the appropriate output
        main_text_style = {'textAlign': 'center'}

        #used in the return to style the appropriate output
        style = {
            'float':'left',
            'width' :'25%',
            'height': '10%',
            'margin' : '20px',
            'display' : 'block'

            }

        #used in the return to hide the appropriate output
        hr = {'display': 'none'}

        #used in the return to display the appropriate output
        main_tabs = {'display': 'block'}

        #when the user hits the initiate button and that both textboxes are not empty
        if click and GenomeName is not None and TEmethod is not None:

            #used in the return to show the appropriate output
            main_text = "Working on {} with {} method".format(GenomeName, TEmethod)

            #create the main pathway with genome name and method
            pathVisual = 'VisualTE3__' + str(GenomeName) + '__' + str(TEmethod)

            #create pathway if it doesn't exist
            if not os.path.exists(pathVisual):
                os.mkdir(pathVisual)

            #additional pathway
            pathVisualDATA = pathVisual + '/Downloaded'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualDATA):
                os.mkdir(pathVisualDATA)

            #additional pathway
            pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualDATA2):
                os.mkdir(pathVisualDATA2)

            # Create the (sub) directories for VisualTE3
            pathVisualCSS = pathVisual + '/css'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualCSS):
                   os.mkdir(pathVisualCSS)

            #additional pathway
            pathVisualCSS_file = pathVisualCSS + '/dash-wind-streaming.css'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualCSS_file):
                   shutil.copyfile('Scripts/dash-wind-streaming.css', pathVisualCSS_file)

            #additional pathway
            init = pathVisual + "/__init__.py"

            #create additional pathway if it doesn't exist
            if not os.path.exists(init):
                with open(init, "w") as file:
                    file.write("")

            #list containing the files pathVisualDATA
            files_downloaded = os.listdir(pathVisualDATA)

            #remove DS_Store if found
            if ".DS_Store" in files_downloaded:
                files_downloaded.remove(".DS_Store")

            #if the program already went through and finished data processing
            if len(files_downloaded) == 15 and not os.path.exists(pathVisual+"/second_half/VisualTE3.py"):

                #enable appropriate tab
                enabling = "tab-TE-selection"
                tab_status = "TE-selection"
                return selectors, main_text, main_text_style, style, hr, main_tabs

            #if the program already went finished entirely
            elif os.path.exists(pathVisual+"/second_half/VisualTE3.py"):

                #enable appropriate tab
                enabling = "tab-TE-processing"
                tab_status = "TE-processing"
                return selectors, main_text, main_text_style, style, hr, main_tabs

            #otherwise start from the beginning
            else:

                #enable appropriate tab
                enabling = "tab-data-loading"
                tab_status = "data-loading"
                return selectors, main_text, main_text_style, style, hr, main_tabs

        elif click and GenomeName is None and TEmethod is None:

            with open("DB.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    GenomeName = line.split("\t")[0]
                    TEmethod = line.split("\t")[1]

            #used in the return to show the appropriate output
            main_text = "Working on {} with {} method".format(GenomeName, TEmethod)

            #create the main pathway with genome name and method
            pathVisual = 'VisualTE3__' + str(GenomeName) + '__' + str(TEmethod)

            #create pathway if it doesn't exist
            if not os.path.exists(pathVisual):
                os.mkdir(pathVisual)

            #additional pathway
            pathVisualDATA = pathVisual + '/Downloaded'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualDATA):
                os.mkdir(pathVisualDATA)

            #additional pathway
            pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualDATA2):
                os.mkdir(pathVisualDATA2)

            # Create the (sub) directories for VisualTE3
            pathVisualCSS = pathVisual + '/css'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualCSS):
                   os.mkdir(pathVisualCSS)

            #additional pathway
            pathVisualCSS_file = pathVisualCSS + '/dash-wind-streaming.css'

            #create additional pathway if it doesn't exist
            if not os.path.exists(pathVisualCSS_file):
                   shutil.copyfile('Scripts/dash-wind-streaming.css', pathVisualCSS_file)


            if genome_dropdown is not None and TE_dropdown is None:

                #enable appropriate tab
                enabling = "tab-TE-selection"
                tab_status = "TE-selection"

                return selectors, main_text, main_text_style, style, hr, main_tabs

            elif genome_dropdown is not None and TE_dropdown is not None:

                #enable appropriate tab
                enabling = "tab-TE-processing"
                tab_status = "TE-processing"
                return selectors, main_text, main_text_style, style, hr, main_tabs


        #if there were no clicks
        else:

            #do nothing
            raise PreventUpdate
#############################################################################
    @app.callback(
    Output("TE-dropdown-selector", "options"),
    Output("TE-dropdown-selector", "disabled"),
    Output("genome-name-entry", "disabled"),
    Output("method-name-entry", "disabled"),
    Output("genome-dropdown", "disabled"),
    Input("genome-dropdown", "value"),
    Input("genome-name-entry", "value"),
    Input("method-name-entry", "value"),
    prevent_initial_call=True
    )
    def DB(dropdown_value, GenomeName, MethodName):
        #used to differentiate callbacks
        ctx = dash.callback_context

        #see which input triggered teh callback
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        TE_dropdown_selector = []
        if input_id == "genome-dropdown":
            with open("DB.txt" , "r") as file:
                lines = file.readlines()
                for line in lines:
                    if dropdown_value in line:
                        TE = line.split("\t")[3]
                        TE_dropdown_selector.append({"label":TE,"value":TE})
            return TE_dropdown_selector, False, True, True, no_update

        elif input_id == "genome-name-entry" or input_id == "method-name-entry":
            if MethodName is not None or GenomeName is not None:
                return no_update, True, False, False, True

        else:
            return no_update, True, False, False, False

#############################################################################

    @app.callback(
    [Output('genome-container', 'style'),
    Output('GO-container', 'style'),
    Output('CHIP-container', 'style'),
    Output("submit-button", "style")],
    [Input('upload-TE', 'isCompleted')],
    [State('upload-TE', 'fileNames')],
    prevent_initial_call=True
    )
    def callback_on_completion(iscompleted, filenames):
        """
        Arguments: boolean completion listening, fileNames

        Description: listens for the TE files that are being uploaded, once done,
                    it will move the files from the dash upload directory to the
                    appropriate user directory

        Returns: hide or show genome, GO, CHIP containers and submit button

        """

        # TE file location that will be used by other functions
        global fileTE

        #folder where dahs uploads its contents
        upload_folder = "Dash_upload/"

        #folder to move contents
        aim_folder = pathVisualDATA

        #if it is not finished
        if not iscompleted:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        #if file has a name
        if filenames is not None:

            #get its location
            fileTE = pathVisualDATA+"/"+filenames[0]

            #move it if not already done
            if not os.path.exists(fileTE):
                file_directory = upload_folder + filenames[0]
                shutil.move(file_directory, aim_folder)

            #all the css that is used to display outputs
            genome_container = {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}
            GO_container = {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}
            CHIP_container = {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}
            submit = {'width': '30%','margin' : '10px 35%'}

            return genome_container, GO_container, CHIP_container, submit

        #
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

#############################################################################
    @app.callback(
        [Output('genome-container-yes', 'style'), Output('genome-container-no', 'style')],
        Input('genome-file-bool','value')
        )
    def toggle_container(toggle_value):
        """
        Arguments: wait for a yes or a no when user clicks on radiobutton

        Description: asks user if he has the files, if yes then it will show a
                    a certain block and hide another one and vice versa if no

        Returns: display or hide the two different containers

        """

        #if no, show download
        if toggle_value == 'no':
            return [{'display': 'none'},{'display': 'block'}]
        #if yes, show upload
        elif toggle_value == 'yes':
            return [{'display': 'block'},{'display': 'none'}]
        #otherwise show none
        else:
            return [{'display': 'none'},{'display': 'none'}]

#############################################################################
    @app.callback(
        [Output("genome-download-output","children"), Output("loading-output-genome", "children")],
        Input("submit-genome", "n_clicks"),
        State('genome-entry','value')
        )

    def download_genome(submit, GenomeName):
        """
        Arguments: download click, genome name

        Description: downloads the genome that the user inputs once he hits download

        Returns: Display a message once finished, while downloading show a loading circle
        """

        #variables used by other functions
        global fileFNA
        global fileGFF

        #if file has no name do nothing
        if GenomeName is None:
            return None, None

        try:

            #used to download the genome
            FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress = Interface_DownloadGenomes.lanceTelechargement(GenomeName, pathVisualDATA)

            #create the path
            fileFNA = pathVisualDATA + '/' + FNAaTelecharger

            #generate url
            url = ftpAdress + FNAaTelecharger

            #download FNA file
            dash_functions.online_download(url, fileFNA)

            #gunzip, move and delete duplicate
            with gzip.open(fileFNA, 'rb') as f_in:
                with open(fileFNA[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(fileFNA)

            #create the path
            fileGFF = pathVisualDATA + '/' + GFFaTelecharger

            #generate url
            url = ftpAdress + GFFaTelecharger

            #download GFF file
            dash_functions.online_download(url, fileGFF)

            #gunzip, move and delete duplicate
            with gzip.open(fileGFF, 'rb') as f_in:
                with open(fileGFF[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(fileGFF)

            # return finished download and loading
            return "Downloaded {} FNA and GFF files".format(GenomeName), None

        #if not found then warn user
        except Exception:

            return "Couldn't find {} genome files".format(GenomeName), None

#############################################################################
    @app.callback(
        [Output('GO-container-yes', 'style'), Output('GO-container-no', 'style')],
        Input('GO-file-bool','value')
        )

    def toggle_container(toggle_value):
        """
        Arguments: wait for a yes or a no when user clicks on radiobutton

        Description: asks user if he has the files, if yes then it will show a
                    a certain block and hide another one and vice versa if no

        Returns: display or hide the two different containers
        """

        #if no, show download
        if toggle_value == 'no':
            return [{'display': 'none'},{'display': 'block'}]
        #if yes, show upload
        elif toggle_value == 'yes':
            return [{'display': 'block'},{'display': 'none'}]
        #otherwise show none
        else:
            return [{'display': 'none'},{'display': 'none'}]
#############################################################################
    @app.callback(
        [Output("GO-download-output", "children"), Output("loading-output-GO", "children")],
        Input("GO-download", "n_clicks")
        )

    def download_GO(click):
        """
        Arguments: listens for download click

        Description: download GO file if user clicks download button

        Returns: display download message and loading

        """

        #variable used by other functions
        global GO_basic_file

        #when the user hits download
        if click:

            #create pathway for file
            GO_basic_file = pathVisualDATA + '/go-basic.obo'

            url = 'http://purl.obolibrary.org/obo/go/go-basic.obo'

            #download file
            dash_functions.online_download(url, GO_basic_file)

            #download message and loading
            return "Downloaded all necessary GO files", None
        else:
            raise PreventUpdate

#############################################################################
    @app.callback(
        [Output('CHIP-container-yes', 'style'), Output('CHIP-container-no', 'style')],
        Input('CHIP-file-bool','value')
        )
    def toggle_container(toggle_value):
        """
        Arguments: wait for a yes or a no when user clicks on radiobutton

        Description: asks user if he has the files, if yes then it will show a
                    a certain block and hide another one and vice versa if no

        Returns: display or hide the two different containers
        """

        #if no, show download
        if toggle_value == 'no':
            return [{'display': 'none'},{'display': 'block'}]
        #if yes, show upload
        elif toggle_value == 'yes':
            return [{'display': 'block'},{'display': 'none'}]
        #otherwise show none
        else:
            return [{'display': 'none'},{'display': 'none'}]

#############################################################################
    @app.callback(
        [Output("CHIP-download-output","children"), Output("loading-output-CHIP", "children")],
        Input("CHIP-download", "n_clicks"),
        State('CHIP-entry','value'),
        )

    def download_genome_CHIP_SEQ(submit, GenomeName):
        """
        Arguments: download click, genome name, genome name main, method

        Description: dowload CHIP files

        Returns: display download message

        """

        #variable to be used by other functions
        global CHIP_files

        #if file has no name do nothing
        if GenomeName is None:
            return None, None
        try:

            #download chip files
            dash_functions.downloadENCODE(GenomeName, pathVisualDATA2)

            #attribute pathway
            CHIP_files = pathVisualDATA2

            #display message
            return "Downloaded {} CHIP-Seq files".format(GenomeName), None
        except Exception:
            return "Couldn't find {} CHIP-Seq files".format(GenomeName), None

#############################################################################
    @app.callback(
        Output("submit-prompt", "children"),
        Output("submit-prompt", "style"),
        Output("loading-submit-button", "children"),
        Input("submit-button", "n_clicks"),
        prevent_initial_call=True
        )

    def submit(click):
        """
        Arguments: listens for submit button press

        Description: Checks for the appropriate amount of files, moves certain files if required

        Returns: move to different page

        """

        #variable used by other functions
        global GO_basic_file
        global CHIP_files
        global fileGFF
        global fileFNA
        global tab_status
        global enabling

        #if the user hits submit
        if click:

            #define pathwyas
            upload_folder = "Dash_upload/"
            aim_folder = pathVisualDATA
            chip_folder = pathVisualDATA2

            #list the files in the upload folder
            files = os.listdir(upload_folder)

            #remove .DS_Store
            if ".DS_Store" in files:
                files.remove(".DS_Store")

            #if there are files present
            if len(files) >= 1:

                #for each file
                for file in files:

                    #if the file is zipped
                    if ".zip" in file:

                        #unzip the file, move it and  remove duplicate
                        with zipfile.ZipFile(upload_folder+file, 'r') as zip_ref:
                            zip_ref.extractall(chip_folder)
                        os.remove(upload_folder+file)

                        #update chip folder pathway
                        CHIP_files = pathVisualDATA2+file[:-4]


                    elif ".obo" in file:
                        GO_basic_file = aim_folder +"/"+file

                        if not os.path.exists(GO_basic_file):
                            file_directory = upload_folder + file
                            shutil.move(file_directory, aim_folder)

                    elif ".gff" in file:
                        fileGFF = aim_folder +"/"+file

                        if not os.path.exists(fileGFF):
                            file_directory = upload_folder + file
                            shutil.move(file_directory, aim_folder)

                    elif ".fna" in file:
                        fileFNA = aim_folder +"/"+file

                        if not os.path.exists(fileFNA):
                            file_directory = upload_folder + file
                            shutil.move(file_directory, aim_folder)

            #list files in the user created directory
            files = os.listdir(aim_folder)

            #remove .DS_Store
            if ".DS_Store" in files:
                files.remove(".DS_Store")

            #if there are 5 or more
            if len(files) >=5:

                #move to data processing tab
                tab_status = "data-processing"
                enabling= "tab-data-processing"

                return None, {'display' : 'none'},None

            #otherwise
            else:

                #move to data loading tab
                tab_status = "data-loading"
                enabling = "tab-data-loading"

                #stay on current tab and display error message
                return "Please control your files", {'width': '30%', 'margin' : '10px 35%', 'display' : 'block', 'textAlign': 'center'},None

        #if the user doesn't click
        else:

            #prevent it
            raise PreventUpdate

###############################################################################

    @app.callback(
        Output('main-tabs', 'value'),
        Output("tab-data-processing", "disabled"),
        Output("tab-data-loading", "disabled"),
        Output("tab-TE-selection", "disabled"),
        Output("tab-TE-processing", "disabled"),
        Input('initiation', 'n_clicks'),
        Input('submit-button', 'n_clicks'),
        Input("loading-submit-button", "children"),
        Input('loading-TE-selection', 'children' ),
        Input("main-text", "children"),
        Input('loading-final','children'),
        prevent_initial_call=True
    )
    def tab_controller(init, submit, submit_wait_loading, TE_loading_wait ,initiation_wait_time, data_final_wait_time):
        """
        Arguments: listen for initiation and submit button click, with also the
                    loading circles of main text, TE selection, submit, final

        Description: in charge of the tab enabling and desabling

        Returns: enables the correct tab while desabling all the others when
                a listened button is clicked

        """

        tab_data_processing = True
        tab_data_loading = True
        tab_TE_selection = True
        tab_TE_processing = True

        if enabling == "tab-data-processing":
            tab_data_processing = False
            tab_data_loading = True
            tab_TE_selection = True
            tab_TE_processing = True

        if enabling == "tab-data-loading":
            tab_data_processing = True
            tab_data_loading = False
            tab_TE_selection = True
            tab_TE_processing = True

        if enabling == "tab-TE-selection":
            tab_data_processing = True
            tab_data_loading = True
            tab_TE_selection = False
            tab_TE_processing = True

        if enabling == "tab-TE-processing":
            tab_data_processing = True
            tab_data_loading = True
            tab_TE_selection = True
            tab_TE_processing = False

        return tab_status, tab_data_processing, tab_data_loading, tab_TE_selection, tab_TE_processing


###############################################################################

    @app.callback(
        Output('loading-repbase','children'), Output('repbase','style'),
        Input("loading-submit-button", "children"),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: listen for the submit button click

        Description: launch data processing first step

        Returns: css and loading circle to show work step and completion

        """

        global repbase

        repbase = ReadInfos_TE.LireRepbase('Scripts/DATA/Repbase/Data_Repbase.txt')

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css

###############################################################################
    @app.callback(
        Output('loading-TE','children'), Output('TE','style'),
        Input('loading-repbase','children'),
        prevent_initial_call=True
    )

    def run_process(load):
        """
        Arguments: wait forloading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        dash_functions.ReadRepeatMasker(fileTE, repbase, pathVisualDATA)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css


###############################################################################
    @app.callback(
        Output('loading-GFF','children'), Output('GFF','style'),
        Input('loading-TE','children'),
        prevent_initial_call=True
    )

    def run_process(load):
        """
        Arguments: wait forloading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global nbSeq_Assemble
        global nameOrganism
        global maxSize
        global taxon


        files = os.listdir(pathVisualDATA)
        for file in files:
            if ".gff" in file:
                fileGFF = pathVisualDATA+"/"+file

        nbSeq_Assemble, nameOrganism, maxSize, taxon, dataFrame_Gene = dash_functions.ReadGFF(fileGFF, pathVisualDATA)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css

###############################################################################
    @app.callback(
        Output('loading-GO','children'), Output('GO','style'),
        Input('loading-GFF','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait forloading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        ReadInfos_GeneOntology.ParsingGeneOntologyDefinition(GO_basic_file, pathVisualDATA, 2)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css

###############################################################################
    @app.callback(
        Output('loading-wiki','children'), Output('wiki','style'),
        Input('loading-GO','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait forloading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        ReadInfos_WikiPathways.CopyPathWaysFile(pathVisualDATA)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css


###############################################################################
    @app.callback(
        Output('loading-CHIP','children'), Output('CHIP','style'),
        Input('loading-wiki','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait forloading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global dictionary_organ
        global dictionary_tissue

        dictionary_organ, dictionary_tissue = dash_functions.TransformChipSEQ(pathVisualDATA, CHIP_files)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css


###############################################################################
    @app.callback(
        Output('loading-final','children'), Output('final','style'),
        Input('loading-CHIP','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait forloading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global enabling
        global tab_status

        files = os.listdir(pathVisualDATA)
        for file in files:
            if ".fna" in file:
                fileFNA = pathVisualDATA+"/"+file

        Create_MainFile.EcrireApp(pathVisual)

        if not os.path.exists(pathVisual+"/"+"Functions"):
            os.mkdir(pathVisual+"/"+"Functions")

        Create_Color.PrepareListeColor(pathVisual)
        Create_CommonDATA.PrepareCommonDATA(pathVisual, nameOrganism, nbSeq_Assemble, maxSize, taxon, fileFNA, dictionary_organ, dictionary_tissue)

        with open("DB.txt", "r") as file:
            lines = file.readlines()
            if str(Genome_Name+"\t"+TE_method+"\t"+fileFNA.split("/")[-1]+"\t") not in lines:
                with open("DB.txt", "a") as file:
                    file.write(Genome_Name+"\t"+TE_method+"\t"+fileFNA.split("/")[-1]+"\t")

        enabling = "tab-TE-selection"
        tab_status = "TE-selection"

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',

        }

        return None, css

###############################################################################
    @app.callback(
        Output('TE-dropdown', 'options'),Output('TE-selected', 'children'),
        Input('loading-final','children'),
        Input('initiation', 'n_clicks'),
        Input("main-text", "children"),
        Input('TE-select-button', 'n_clicks'),
        State('TE-dropdown', 'value'),
        prevent_initial_call=True
    )

    def begin_TE_selection(loading_final, init_click,main, TE_select_click, value):
        """
        Arguments: listen for the ending of final loading, initiation button click,
                    main text, TE select button click, dropdown values of TE

        Description: initialise TE selection step by creating appropriate files,
                    folders and environement

        Returns: a dict of all the TE with families that are used by TE dropdown
        """

        #variables used by other functions
        global dataTE
        global pathVisualNEW
        global pathVisualFunctions
        global ListeCompleteTE
        global ListeFamilleTE
        global ListeSuperFamilyTE
        global list_selection_TE
        global indexTE
        global numberOFselection

        #used to differentiate callbacks
        ctx = dash.callback_context

        #see which input triggered teh callback
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        #if conditions are met from either tab selection (initiation) or loading steps
        if enabling == "tab-TE-selection" and input_id == "initiation" or input_id == "loading-final":

            #create file path for TE data
            dataTE = pathVisualDATA + '/DATA_List_TE_families.txt'

            #name of the TE selection and processing step
            folder = "second_half"

            #pathway of the TE selection and processing
            pathVisualNEW = pathVisual + '/' + folder

            #if pathway not already present, create it
            if not os.path.exists(pathVisualNEW):
                os.mkdir(pathVisualNEW)

            #
            pathVisualFunctions = pathVisualNEW + '/Functions'
            if not os.path.exists(pathVisualFunctions):
                os.mkdir(pathVisualFunctions)

            # Copy the app.py file
            originalFile = pathVisual + '/app.py'
            copyFile = pathVisualNEW + '/app.py'
            if not os.path.exists(copyFile):
                shutil.copyfile(originalFile, copyFile)

            # Copy the CommonDATA file
            originalFile = pathVisual + '/Functions/CommonDATA.py'
            copyFile = pathVisualNEW + '/Functions/CommonDATA.py'
            if not os.path.exists(copyFile):
                shutil.copyfile(originalFile, copyFile)

            # Copy the Couleur file
            originalFile = pathVisual + '/Functions/Couleur.py'
            copyFile = pathVisualNEW + '/Functions/Couleur.py'
            if not os.path.exists(copyFile):
                shutil.copyfile(originalFile, copyFile)

            #create __init files used by python for imports with importlib
            init = pathVisualNEW + "/__init__.py"
            if not os.path.exists(init):
                with open(init, "w") as file:
                    file.write("")

            #create __init files used by python for imports with importlib
            init = pathVisualFunctions + "/__init__.py"
            if not os.path.exists(init):
                with open(init, "w") as file:
                    file.write("")

            list_selection_TE = []
            numberOFselection = 0

            #read TE data
            ListeCompleteTE, ListeFamilleTE, ListeSuperFamilyTE, dict_dash_TE = dash_functions.getListeTE(dataTE)

            return dict_dash_TE, None

        #if the user presses the TE selection button
        elif input_id == "TE-select-button":
            dict_dash_TE = []

            ########Start Code of Sebastien Tempel############
            indexTE = ListeCompleteTE.index(value)

            selectedSuperfamily = ListeSuperFamilyTE[indexTE]
            selectedFamily = ListeFamilleTE[indexTE] + "\n"

            numberOFselection += 1
            if numberOFselection == 1 or numberOFselection == 2 :
                tempC = []
                tempF = []
                tempS = []
                for i in range(0, len(ListeCompleteTE), 1) :
                    if ListeSuperFamilyTE[i] == selectedSuperfamily and i != indexTE :
                        tempC.append(ListeCompleteTE[i])
                        tempF.append(ListeFamilleTE[i])
                        tempS.append(ListeSuperFamilyTE[i])
                ListeCompleteTE = tempC
                ListeFamilleTE = tempF
                ListeSuperFamilyTE = tempS

            if numberOFselection == 3 :
                ListeCompleteTE = []
                ListeFamilleTE = []
                ListeSuperFamilyTE = []

            if numberOFselection < 4:
                list_selection_TE.append(selectedFamily[:-1])
            ########End Code of Sebastien Tempel############

            #for each TE add them to the dict that will be used by the dropdown menu
            for TE in ListeCompleteTE:
                dict_dash_TE.append({"label":TE,"value":TE})

            #show which TE was selected
            res = "Selected : " +"".join([TE+' | ' for TE in list_selection_TE])

            return dict_dash_TE, res
        else:
            return None, None

###############################################################################
    @app.callback(
        Output("loading-TE-selection", "children"),
        Input('TE-finish-button', 'n_clicks'),
        prevent_initial_call=True
    )

    def run_TE_selection(click):
        """
        Arguments: Wait for the button TE submit button click

        Description: launch the TE processing step
        """

        global enabling
        global tab_status
        enabling = "tab-TE-processing"
        tab_status = "TE-processing"
        #HERE WILL BE ERROR MANAGEMENT OF TE SELECTION TAB
        return None

###############################################################################

    @app.callback(
        Output('loading-proc-create-TE','children'), Output('proc-create-TE','style'),
        Input("loading-TE-selection", "children"),
        State("radio-TE", "value"),
        prevent_initial_call=True
    )

    def run_process(click, radio_TE):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """
        global ListeConsensus


        OfficialName = ''
        if radio_TE == "yes" and len(list_selection_TE) > 1 :	# Merged the family
            OfficialName = 'Merged '
        for i in range(0, len(list_selection_TE), 1) :
            if i > 0 :
                OfficialName += ', '
            OfficialName += str(list_selection_TE[i])

        ListeConsensus = Create_CommonDATA2.writeSelectTE(pathVisual, pathVisualNEW, OfficialName, list_selection_TE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TE-load','children'), Output('TE-load','style'),
        Input("loading-proc-create-TE", "children"),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global moduleSelectTE
        global moduleCommonDATA

        # Import the recently created modules
        pathSelectTE = os.path.realpath(pathVisualNEW + '/Functions/CommonDATA_SelectTEs.py')
        loaderSelectTE = importlib.util.spec_from_file_location('CommonDATA_SelectTEs', pathSelectTE)
        moduleSelectTE = importlib.util.module_from_spec(loaderSelectTE)
        loaderSelectTE.loader.exec_module(moduleSelectTE)

        pathCommonDATA = os.path.realpath(pathVisualNEW + '/Functions/CommonDATA.py')
        loaderCommonDATA = importlib.util.spec_from_file_location('CommonDATA', pathCommonDATA)
        moduleCommonDATA = importlib.util.module_from_spec(loaderCommonDATA)
        loaderCommonDATA.loader.exec_module(moduleCommonDATA)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-gene-env','children'), Output('gene-env','style'),
        Input('loading-TE-load','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global NameSeq
        global DEB
        global FIN
        global Sens
        global Size
        global Similarity
        global listGeneSelect5
        global listGeneSelect3
        global listGeneSelectInside

        NameSeq, DEB, FIN, Sens, Size, Similarity, listGeneSelect5, listGeneSelect3, listGeneSelectInside = Create_SelectedAnnotations.SelectAnnotations(pathVisual, pathVisualNEW, moduleSelectTE, moduleCommonDATA, list_selection_TE, ListeConsensus)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TE-align-phylo','children'), Output('TE-align-phylo','style'),
        Input('loading-gene-env','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        Create_Alignment_and_Tree.AlignETPhylogeny(pathVisual, pathVisualNEW, moduleCommonDATA, moduleSelectTE, NameSeq, DEB, FIN, Sens, Size, Similarity)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-random-seq','children'), Output('random-seq','style'),
        Input('loading-TE-align-phylo','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global randomSeqDEB
        global randomSeqFIN
        global randomSeqCHR

        randomSeqDEB, randomSeqFIN, randomSeqCHR = Create_Random_Sequences.RandomSequences(pathVisual, pathVisualNEW, moduleSelectTE, NameSeq, DEB, FIN, list_selection_TE, listGeneSelect5, listGeneSelect3, listGeneSelectInside)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-TFBS-seq','children'), Output('TFBS-seq','style'),
        Input('loading-random-seq','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global tissue_dictionary_SelectedTE
        global organ_dictionary_SelectedTE
        global tissue_dictionary_Global
        global organ_dictionary_Global

        tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_Global, organ_dictionary_Global = Create_Overlap_TFBS.ExtractTFBS_forTE(pathVisual, pathVisualNEW, list_selection_TE, moduleCommonDATA, NameSeq, DEB, FIN, listGeneSelect5, listGeneSelect3)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TFBS-random','children'), Output('TFBS-random','style'),
        Input('loading-TFBS-seq','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global tissue_dictionary_RandomSeq
        global organ_dictionary_RandomSeq
        global tissue_dictionary_Global
        global organ_dictionary_Global

        tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq, tissue_dictionary_Global, organ_dictionary_Global = Create_Overlap_TFBS.ExtractTFBS_forRandom(pathVisual, pathVisualNEW, list_selection_TE, moduleCommonDATA, randomSeqCHR, randomSeqDEB, randomSeqFIN, tissue_dictionary_Global, organ_dictionary_Global)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-TFBS-random-print','children'), Output('TFBS-random-print','style'),
        Input('loading-TFBS-random','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        Create_Overlap_TFBS.PrintGlobalTFBS(pathVisualNEW, list_selection_TE, tissue_dictionary_Global, organ_dictionary_Global, tissue_dictionary_SelectedTE, organ_dictionary_SelectedTE, tissue_dictionary_RandomSeq, organ_dictionary_RandomSeq)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-main-file','children'), Output('main-file','style'),
        Input('loading-TFBS-random-print','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        global nbSeq_Assemble
        global numberTE

        # Create the function for the TE selected
        # Add few lines in the CommonDATA_SelectTEs file
        Create_CommonDATA2.AjoutAnnotations(pathVisualNEW)
        # Cree le fichier principal qui lance tous les autres
        nbSeq_Assemble, numberTE = Create_MainFile.EcrireVisualTE(pathVisual, pathVisualNEW, moduleSelectTE, moduleCommonDATA)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-TE-genome-browser','children'), Output('TE-genome-browser','style'),
        Input('loading-main-file','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_GenomeBrowser.GenomeBrowser(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-TE-chrom-distrib','children'), Output('TE-chrom-distrib','style'),
        Input('loading-TE-genome-browser','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_ChromosomeDistribution.ChromosomeDistribution(pathVisualNEW, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TE-general','children'), Output('TE-general','style'),
        Input('loading-TE-chrom-distrib','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_GeneralFeaturesDistribution.GeneralFeatures_layout(pathVisual, pathVisualNEW, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-TE-gene-distance','children'), Output('TE-gene-distance','style'),
        Input('loading-TE-general','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_DistanceNeighboringGene.DistanceNeighboringGene(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TE-genic-func','children'), Output('TE-genic-func','style'),
        Input('loading-TE-gene-distance','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_NeighboringGeneFunctions.NeighboringGeneFunctions(pathVisual, pathVisualNEW, nbSeq_Assemble, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TE-TFBS','children'), Output('TE-TFBS','style'),
        Input('loading-TE-genic-func','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_OverlappingTFBS.OverlappingTFBS(pathVisualNEW, nbSeq_Assemble, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('loading-TE-sim-occ-func','children'), Output('TE-sim-occ-func','style'),
        Input('loading-TE-TFBS','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_SimilarityOccurrences.SimilarityOccurrences(pathVisualNEW, nbSeq_Assemble, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-TE-env','children'), Output('TE-env','style'),
        Input('loading-TE-sim-occ-func','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_TEEnvironment.TEEnvironment(pathVisualNEW, nbSeq_Assemble, numberTE)

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css


###############################################################################

    @app.callback(
        Output('loading-summary','children'), Output('summary','style'),
        Input('loading-TE-env','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: wait for loading component of previous step to be finished

        Description: initiate next step

        Returns: css and loading circle to show work step and completion

        """

        MakeFunction_SummaryTable.SummaryTable(pathVisualNEW, nbSeq_Assemble, numberTE)

        with open("DB.txt", "r") as file:
            lines = file.readlines()
            if str("|".join(list_selection_TE)+"\n") not in lines:
                with open("DB.txt", "a") as file:
                    file.write("|".join(list_selection_TE)+"\n")

        css = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'#129dff',
        }

        return None, css

###############################################################################

    @app.callback(
        Output('TE-main-div','children'), Output('TE-main-div', 'style'),
        Input('loading-summary','children'),
        Input("initiation", "n_clicks"),
        Input("main-text", "children"),
        prevent_initial_call=True
    )

    def run_process(init, click, main_text_load):
        """
        Arguments: listen for initiation click or the final loading TE processing
                    step to be finished

        Description: Display the Visualise results button for the user

        Returns: display a button

        """

        #differentiate inputs
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        css = {'textAlign': 'center'}

        #differentiate inputs
        if input_id == "initiation" and tab_status == "TE-processing" and enabling == "tab-TE-processing":
            #dcc.Link('Visualise results', href='/Visualisation')

            #create button
            return html.Button('Visualise results', id = "visual", n_clicks = 0, style = {'margin':'10%', 'transform':'scale(1.5)'}), css

        elif input_id == "loading-summary":
            #dcc.Link('Visualise results', href='/Visualisation')
            #create button
            return html.Button('Visualise results', id = "visual", n_clicks = 0, style = {'margin':'10%', 'transform':'scale(1.5)'}), css
        else:

            #prevent update if conditions aren't met
            raise PreventUpdate


###############################################################################

    @app.callback(
        Output('main-all', 'children'),
        #Input('url', 'pathname'),
        Input("visual", "n_clicks"),
        prevent_initial_call=True
    )

    def run_process(click):
        """
        Arguments: listens for the visualisation button click

        Description: switch app layout to visualise results

        Returns: change the layout to

        """
        #print(url)

        #on click
        if click:
            # Contrived example of generating a module named as a string

            #create path
            full_module_name_raw = pathVisual+"/second_half/VisualTE3"

            #change the "/" with "." in the path
            full_module_name_processed = full_module_name_raw.replace("/",".")
            # The file gets executed upon import, as expected.

            #import the path automatically
            VisualTE = importlib.import_module(full_module_name_processed)

            #call the layout
            return VisualTE.visual_layout

        #if there are no clicks
        else:

            #don't update
            return no_update


    #run server
    app.run_server(debug=True)
