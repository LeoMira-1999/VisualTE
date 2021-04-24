#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import os.path
import base64
import requests, json
import shutil
import time
import dash
import zipfile
import gzip
import dash_uploader as du
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from . import Interface_DownloadGenomes
from . import dash_functions
from . import ReadInfos_TE
from . import ReadInfos_GeneOntology
from . import ReadInfos_WikiPathways
from . import Create_MainFile
from . import Create_Color
from . import Create_CommonDATA

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#######################################################################
def Dash_CreateGenomeDATA():

    global pathVisual
    global pathVisualDATA
    global pathVisualDATA2
    global tab_status
    global enabling
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

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    du.configure_upload(app, "Dash_upload", use_upload_id=False)

    app.layout = html.Div([

        ##############################################################
        html.H1(children='VisualTE V3', style = {'textAlign': 'center'}),

        html.Div([
            html.H3(children = "Enter your genome name and method name", id = "main-text"),
            dcc.Input(
              id="genome-name-entry",
              type="text",
              placeholder="Enter your genome name here",
              style={
                  'width': '20%'
              }),

            dcc.Input(
              id="method-name-entry",
              type="text",
              placeholder="Repet or RepeatMasker or Blast",
              style={
                  'width': '20%',
                  'margin' : '20px'
              }),

            html.Button('Initiate', id='initiatition', n_clicks=0),

        ]),

        html.Hr(id = "hr"),

        ###########################################################
        dcc.Tabs([
            dcc.Tab(label='Data Loading', children=[

                ##############################################################
                html.Div([

                    html.H6("Upload your TE file"),
                    du.Upload(
                        id="upload-TE",
                        text = "Drag and drop or click to select file",
                        max_files=1,
                        max_file_size = 10240,
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
                html.Div([

                    html.H6("Upload your genome files"),

                    html.Div([

                        dcc.RadioItems(
                            id = "genome-file-bool",
                            options=[
                                {'label': 'Local', 'value': 'yes'},
                                {'label': 'Download', 'value': 'no'},
                            ],
                            value = None,
                            labelStyle={'display': 'inline-block'}),

                    ]),
                html.Div([
                          html.P("Upload your FNA file"),
                          du.Upload(
                              id="upload-FNA",
                              text = "Drag and drop or click to select file",
                              max_files=1,
                              max_file_size = 10240,
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
                          du.Upload(
                              id="upload-GFF",
                              text = "Drag and drop or click to select file",
                              max_files=1,
                              max_file_size = 10240,
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

                html.Div([
                          dcc.Input(
                            id="genome-entry",
                            type="text",
                            placeholder="Enter your genome name",
                            style={
                                'width': '80%',
                                'margin' : '10px'
                            }),

                            html.Button('Download', id='submit-genome', n_clicks=0,
                                style={
                                    'width': '80%',
                                    'margin' : '10px'
                            }),

                            dcc.Loading(
                                type="circle",
                                children=html.Div(id="loading-output-genome", style={'margin':'20px'})
                                ),

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
                html.Div([

                    html.H6("Upload your GO files"),

                    html.Div([

                        dcc.RadioItems(
                            id = "GO-file-bool",
                            options=[
                                {'label': 'Local', 'value': 'yes'},
                                {'label': 'Download', 'value': 'no'},
                            ],
                            value = None,
                            labelStyle={'display': 'inline-block'}),

                    ]),
                html.Div([
                          html.P("Upload your GO basic list file"),
                          du.Upload(
                              id="upload-GO",
                              text = "Drag and drop or click to select file",
                              max_files=1,
                              max_file_size = 10240,
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

                html.Div([

                    html.Br(),

                    html.Button("Download GO files", id="GO-download", n_clicks = 0, style={
                        'width': '80%',
                        'margin' : '45px 20px 10px 20px'
                        }),

                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="loading-output-GO", style={'margin':'20px'})
                        ),

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
                html.Div([
                    html.H6("Upload your CHIP-Seq files"),

                    html.Div([

                        dcc.RadioItems(
                            id = "CHIP-file-bool",
                            options=[
                                {'label': 'Local', 'value': 'yes'},
                                {'label': 'Download', 'value': 'no'},
                            ],
                            value = None,
                            labelStyle={'display': 'inline-block'}),

                    ]),
                html.Div([
                          html.P("Upload your CHIP-Seq file(s) in zip format (.gz)"),
                          du.Upload(
                              id="upload-CHIP",
                              text = "Drag and drop or click to select file",
                              max_file_size = 10240,
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

                html.Div([

                    dcc.Input(
                      id="CHIP-entry",
                      type="text",
                      placeholder="Enter your genome name",
                      style={
                          'width': '80%',
                          'margin' : '10px'
                      }),

                    html.Button("Download CHIP-Seq files", id="CHIP-download", n_clicks = 0, style={
                        'width': '80%',
                        'margin' : '10px',
                        }),

                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="loading-output-CHIP", style={'margin':'20px'})
                        ),

                    html.Div(id = "CHIP-download-output")

                    ], id = 'CHIP-container-no'),

                ],id = 'CHIP-container',style = {
                    'float':'left',
                    'width' :'25%',
                    'height': '10%',
                    'margin' : '20px',
                    'display' : 'none'
                    }),

                html.Button("Submit", id = "submit-button", n_clicks = 0, style={
                    'width': '30%',
                    'margin' : '10px 35%',
                    'display' : 'none' #A CHANGER UNE FOIS QUE LE DATA PROCESSING FINI !!!!!
                    }),

                dcc.Loading(
                    type="circle",
                    children=html.Div(id="loading-submit-button",style={'margin':'30px'})
                    ),

                html.Div(id = "submit-prompt", children = "Please check your content", style={
                    'width': '30%',
                    'margin' : '10px 35%',
                    'display' : 'none'
                    })

            ], value = "data-loading", id = "tab-data-loading"),

#########################################################################
            dcc.Tab(label='Data Processing', id = "tab-data-processing", value = "data-processing",disabled = True, children=[

                html.Div([

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



                ], id = "", style = {
                    'width': '80%',
                    'margin' : '10px 10%',
                    'display' : 'block',
                    })
            ]),

            dcc.Tab(label='TE Selection', id = "tab-TE-selection", value = "TE-selection",disabled = True,children=[

            ]),

            dcc.Tab(label='TE Processing', id = "tab-TE-processing", value = "TE-processing",disabled = True, children=[

            ]),

        ],id = "main-tabs", style = {'display': 'none'}),
    ])

###############################################################################
    @app.callback(
        [Output("genome-name-entry", "style"), Output("method-name-entry", "style"), Output("initiatition", "style"), Output("main-text", "children"), Output("main-text", "style"), Output("TE-container", "style"), Output("hr", "style"), Output("main-tabs", "style")],
        Input("initiatition", "n_clicks"),
        State("genome-name-entry", "value"),
        State("method-name-entry", "value"),
        prevent_initial_call =True
    )

    def start(click, GenomeName, TEmethod):

        global pathVisual
        global pathVisualDATA
        global pathVisualDATA2
        global tab_status
        global enabling


        if click and GenomeName is not None and TEmethod is not None:

            pathVisual = 'VisualTE3__' + str(GenomeName) + '__' + str(TEmethod)

            if not os.path.exists(pathVisual):
                os.mkdir(pathVisual)

            pathVisualDATA = pathVisual + '/Downloaded'

            if not os.path.exists(pathVisualDATA):
                os.mkdir(pathVisualDATA)

            pathVisualDATA2 = pathVisualDATA + '/ChipSeq/'

            if not os.path.exists(pathVisualDATA2):
                os.mkdir(pathVisualDATA2)

            genome_name_entry = {'display': 'none'}

            genome_name_entry = {'display': 'none'}

            init_button = {'display': 'none'}

            main_text = "Working on {} with {} method".format(GenomeName, TEmethod)

            main_text_style = {'textAlign': 'center'}

            style = {
                'float':'left',
                'width' :'25%',
                'height': '10%',
                'margin' : '20px',
                'display' : 'block'

                }
            hr = {'display': 'none'}

            main_tabs = {'display': 'block'}

            files_downloaded = os.listdir(pathVisualDATA)

            if ".DS_Store" in files_downloaded:
                files_downloaded.remove(".DS_Store")

            print(len(files_downloaded))
            if len(files_downloaded) == 15:
                print("there1")
                enabling = "tab-TE-selection"
                tab_status = "TE-selection"
                return genome_name_entry, genome_name_entry, init_button, main_text, main_text_style, style, hr, main_tabs
            else:
                print("there2")
                enabling = "tab-data-loading"
                tab_status = "data-loading"
                return genome_name_entry, genome_name_entry, init_button, main_text, main_text_style, style, hr, main_tabs
        else:
            style = {
                'float':'left',
                'width' :'25%',
                'height': '10%',
                'display' : 'none'

                }
            print("there2")
            enabling = "tab-data-loading"
            tab_status = "data-loading"
            return {'display': 'inline', 'width': '20%'}, {'display': 'inline', 'width': '20%','margin' : '20px'}, {'display': 'inline'}, "Enter your genome name and method name" , None, style, None, {'display': 'none'}

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
        global fileTE

        upload_folder = "Dash_upload/"
        aim_folder = pathVisualDATA

        if not iscompleted:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

        if filenames is not None:

            fileTE = pathVisualDATA+"/"+filenames[0]

            if not os.path.exists(fileTE):
                file_directory = upload_folder + filenames[0]
                shutil.move(file_directory, aim_folder)

            return {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}, {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}, {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}, {'width': '30%','margin' : '10px 35%'}

        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

#############################################################################
    @app.callback(
        [Output('genome-container-yes', 'style'), Output('genome-container-no', 'style')],
        Input('genome-file-bool','value')
        )
    def toggle_container(toggle_value):

        if toggle_value == 'no':
            return [{'display': 'none'},{'display': 'block'}]
        elif toggle_value == 'yes':
            return [{'display': 'block'},{'display': 'none'}]
        else:
            return [{'display': 'none'},{'display': 'none'}]

#############################################################################
    @app.callback(
        [Output("genome-download-output","children"), Output("loading-output-genome", "children")],
        Input("submit-genome", "n_clicks"),
        State('genome-entry','value')
        )

    def download_genome(submit, GenomeName):
        global fileFNA
        global fileGFF

        if GenomeName is None:
            return None, None
        try:
            FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress = Interface_DownloadGenomes.lanceTelechargement(GenomeName, pathVisualDATA)

            fileFNA = pathVisualDATA + '/' + FNAaTelecharger
            url = ftpAdress + FNAaTelecharger
            dash_functions.online_download(url, fileFNA)

            with gzip.open(fileFNA, 'rb') as f_in:
                with open(fileFNA[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(fileFNA)

            fileGFF = pathVisualDATA + '/' + GFFaTelecharger
            url = ftpAdress + GFFaTelecharger
            dash_functions.online_download(url, fileGFF)

            with gzip.open(fileGFF, 'rb') as f_in:
                with open(fileGFF[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(fileGFF)

            return "Downloaded {} FNA and GFF files".format(GenomeName), None
        except Exception:

            return "Couldn't find {} genome files".format(GenomeName), None

#############################################################################
    @app.callback(
        [Output('GO-container-yes', 'style'), Output('GO-container-no', 'style')],
        Input('GO-file-bool','value')
        )

    def toggle_container(toggle_value):

        if toggle_value == 'no':
            return [{'display': 'none'},{'display': 'block'}]
        elif toggle_value == 'yes':
            return [{'display': 'block'},{'display': 'none'}]
        else:
            return [{'display': 'none'},{'display': 'none'}]

#############################################################################
    @app.callback(
        [Output("GO-download-output", "children"), Output("loading-output-GO", "children")],
        Input("GO-download", "n_clicks")
        )

    def download_GO(click):
        global GO_basic_file

        if click:
            GO_basic_file = pathVisualDATA + '/go-basic.obo'
            url = 'http://purl.obolibrary.org/obo/go/go-basic.obo'
            dash_functions.online_download(url, GO_basic_file)

            return "Downloaded all necessary GO files", None
        else:
            return None, None

#############################################################################
    @app.callback(
        [Output('CHIP-container-yes', 'style'), Output('CHIP-container-no', 'style')],
        Input('CHIP-file-bool','value')
        )
    def toggle_container(toggle_value):

        if toggle_value == 'no':
            return [{'display': 'none'},{'display': 'block'}]
        elif toggle_value == 'yes':
            return [{'display': 'block'},{'display': 'none'}]
        else:
            return [{'display': 'none'},{'display': 'none'}]

#############################################################################
    @app.callback(
        [Output("CHIP-download-output","children"), Output("loading-output-CHIP", "children")],
        Input("CHIP-download", "n_clicks"),
        State('CHIP-entry','value'),
        State("genome-name-entry", "value"),
        State("method-name-entry", "value"),
        )

    def download_genome_CHIP_SEQ(submit, GenomeName, GenomeNameMain, TEmethod):
        global CHIP_files

        if GenomeName is None:
            return None, None
        try:
            dash_functions.downloadENCODE(GenomeName, pathVisualDATA2)

            CHIP_files = pathVisualDATA2

            return "Downloaded {} CHIP-Seq files".format(GenomeName), None
        except Exception as e:
            print(e)
            return "Couldn't find {} CHIP-Seq files".format(GenomeName), None

#############################################################################
    @app.callback(Output("submit-prompt", "children"), Output("submit-prompt", "style"), Output("loading-submit-button", "children"),
        Input("submit-button", "n_clicks"),
        prevent_initial_call=True
        )

    def submit(click):
        global GO_basic_file
        global CHIP_files
        global tab_status
        global enabling

        if click:
            upload_folder = "Dash_upload/"
            aim_folder = pathVisualDATA
            chip_folder = pathVisualDATA2

            files = os.listdir(upload_folder)

            if ".DS_Store" in files:
                files.remove(".DS_Store")

            if len(files) >= 1:

                for file in files:
                    print(file)

                    if ".zip" in file:

                        with zipfile.ZipFile(upload_folder+file, 'r') as zip_ref:
                            zip_ref.extractall(chip_folder)
                        os.remove(upload_folder+file)

                        CHIP_files = pathVisualDATA2+file[:-4]

                    else:

                        if ".obo" in file:
                            GO_basic_file = aim_folder +"/"+file

                        if not os.path.exists(aim_folder+"/"+file):
                            file_directory = upload_folder + file
                            shutil.move(file_directory, aim_folder)


            files = os.listdir(aim_folder)

            if ".DS_Store" in files:
                files.remove(".DS_Store")

            if len(files) >=5:

                print("here1")

                tab_status = "data-processing"
                enabling= "tab-data-processing"

                return None, {'display' : 'none'},None

            else:
                print("here2")

                tab_status = "data-loading"
                enabling = "tab-data-loading"

                return "Please control your files", {'width': '30%', 'margin' : '10px 35%', 'display' : 'block', 'textAlign': 'center'},None

        else:
            print("here3")

            tab_status = "data-loading"
            enabling = "tab-data-loading"
            return None, {'display' : 'none'},None

###############################################################################

    @app.callback(
        Output('main-tabs', 'value'),
        Output("tab-data-processing", "disabled"),
        Output("tab-data-loading", "disabled"),
        Output("tab-TE-selection", "disabled"),
        Output("tab-TE-processing", "disabled"),
        Input('initiatition', 'n_clicks'),
        Input('submit-button', 'n_clicks'),
        Input("loading-submit-button", "children"),
        Input("main-text", "children"),
        prevent_initial_call=True
    )
    def tab_controller(init, submit, submit_wait_loading, initiatition_wait_time):

        tab_data_processing = True
        tab_data_loading = True
        tab_TE_selection = True
        tab_TE_processing = True

        if enabling == "tab-data-processing":
            tab_data_processing = False

        if enabling == "tab-data-loading":
            tab_data_loading = False

        if enabling == "tab-TE-selection":
            tab_TE_selection = False

        if enabling == "tab-TE-processing":
            tab_TE_processing = False

        return tab_status, tab_data_processing, tab_data_loading, tab_TE_selection, tab_TE_processing


###############################################################################

    @app.callback(
        Output('loading-repbase','children'), Output('repbase','style'),
        Input("loading-submit-button", "children"),
        prevent_initial_call=True
    )

    def run_process(click):
        global repbase

        repbase = ReadInfos_TE.LireRepbase('Scripts/DATA/Repbase/Data_Repbase.txt')

        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test

###############################################################################
    @app.callback(
        Output('loading-TE','children'), Output('TE','style'),
        Input('loading-repbase','children'),
        prevent_initial_call=True
    )

    def run_process(click):

        dash_functions.ReadRepeatMasker(fileTE, repbase, pathVisualDATA)

        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test


###############################################################################
    @app.callback(
        Output('loading-GFF','children'), Output('GFF','style'),
        Input('loading-TE','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        global nbSeq_Assemble
        global nameOrganism
        global maxSize
        global taxon


        files = os.listdir(pathVisualDATA)
        for file in files:
            if ".gff" in file:
                fileGFF = pathVisualDATA+"/"+file

        nbSeq_Assemble, nameOrganism, maxSize, taxon, dataFrame_Gene = dash_functions.ReadGFF(fileGFF, pathVisualDATA)

        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test

###############################################################################
    @app.callback(
        Output('loading-GO','children'), Output('GO','style'),
        Input('loading-GFF','children'),
        prevent_initial_call=True
    )

    def run_process(click):

        ReadInfos_GeneOntology.ParsingGeneOntologyDefinition(GO_basic_file, pathVisualDATA, 2)

        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test

###############################################################################
    @app.callback(
        Output('loading-wiki','children'), Output('wiki','style'),
        Input('loading-GO','children'),
        prevent_initial_call=True
    )

    def run_process(click):

        ReadInfos_WikiPathways.CopyPathWaysFile(pathVisualDATA)

        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test


###############################################################################
    @app.callback(
        Output('loading-CHIP','children'), Output('CHIP','style'),
        Input('loading-wiki','children'),
        prevent_initial_call=True
    )

    def run_process(click):
        global dictionary_organ
        global dictionary_tissue

        dictionary_organ, dictionary_tissue = dash_functions.TransformChipSEQ(pathVisualDATA, CHIP_files)

        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test


###############################################################################
    @app.callback(
        Output('loading-final','children'), Output('final','style'),
        Input('loading-CHIP','children'),
        prevent_initial_call=True
    )

    def run_process(click):

        files = os.listdir(pathVisualDATA)
        for file in files:
            if ".fna" in file:
                fileFNA = pathVisualDATA+"/"+file

        Create_MainFile.EcrireApp(pathVisual)

        if not os.path.exists(pathVisual+"/"+"Functions"):
            os.mkdir(pathVisual+"/"+"Functions")

        Create_Color.PrepareListeColor(pathVisual)
        Create_CommonDATA.PrepareCommonDATA(pathVisual, nameOrganism, nbSeq_Assemble, maxSize, taxon, fileFNA, dictionary_organ, dictionary_tissue)


        test = {
        'width': '80%',
        'font-size' : ' 24px',
        'float':'left',
        'display' : 'block',
        'margin' : '2% 0px',
        'background-color':'green'
        }

        return None, test


    app.run_server(debug=True)
