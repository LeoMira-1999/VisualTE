#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import os.path
import base64
import requests, json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from . import Interface_DownloadGenomes
from . import dash_functions

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#######################################################################
def Dash_CreateGenomeDATA():

    global pathVisual
    global pathVisualDATA

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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

        html.Hr(),

        ##############################################################
        html.Div([

            html.H6("Upload your TE file"),
            dcc.Upload(
                id="upload-TE",
                children = html.Div([
                'Drag and Drop or ',
                html.A('Select a File')
                ]),
                style={
                    'width': '80%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'}),
            html.Div(id='TE-filename')
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
                  dcc.Upload(
                      id="upload-FNA",
                      children = html.Div([
                      'Drag and Drop or ',
                      html.A('Select File')
                      ]),
                      style={
                          'width': '80%',
                          'height': '60px',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center'}),

                  html.P("Upload your GFF file"),
                  dcc.Upload(
                      id="upload-GFF",
                      children = html.Div([
                      'Drag and Drop or ',
                      html.A('Select File')
                      ]),
                      style={
                          'width': '80%',
                          'height': '60px',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center'}),

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
                  dcc.Upload(
                      id="upload-GO-basic",
                      children = html.Div([
                      'Drag and Drop or ',
                      html.A('Select File')
                      ]),
                      style={
                          'width': '80%',
                          'height': '60px',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center'}),

                  html.P("Upload your Gene 2 GO file"),
                  dcc.Upload(
                      id="upload-G-2-O",
                      children = html.Div([
                      'Drag and Drop or ',
                      html.A('Select File')
                      ]),
                      style={
                          'width': '80%',
                          'height': '60px',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center'}),

              ], id = 'GO-container-yes'),

        html.Div([

            html.Button("Download GO files", id="GO-download", n_clicks = 0, style={
                'width': '80%',
                'margin' : '10px'
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
                  html.P("Upload your CHIP-Seq file(s)"),
                  dcc.Upload(
                      id="upload-CHIP",
                      multiple=True,
                      children = html.Div([
                      'Drag and Drop or ',
                      html.A('Select File(s)')
                      ]),
                      style={
                          'width': '80%',
                          'height': '60px',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center'}),

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
                'margin' : '10px'
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

    ])

###############################################################################
    @app.callback(
        [Output("genome-name-entry", "style"), Output("method-name-entry", "style"), Output("initiatition", "style"), Output("main-text", "children"), Output("main-text", "style"), Output("TE-container", "style")],
        Input("initiatition", "n_clicks"),
        State("genome-name-entry", "value"),
        State("method-name-entry", "value"),
    )

    def start(click, GenomeName, TEmethod):

        global pathVisual
        global pathVisualDATA

        if click and GenomeName is not None and TEmethod is not None:

            pathVisual = 'VisualTE3__' + str(GenomeName) + '__' + str(TEmethod)

            if not os.path.exists(pathVisual):
                os.mkdir(pathVisual)

            pathVisualDATA = pathVisual + '/Downloaded'

            if not os.path.exists(pathVisualDATA):
                os.mkdir(pathVisualDATA)

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

            return genome_name_entry, genome_name_entry, init_button, main_text, main_text_style, style
        else:
            style = {
                'float':'left',
                'width' :'25%',
                'height': '10%',
                'display' : 'none'

                }
            return {'display': 'inline', 'width': '20%'}, {'display': 'inline', 'width': '20%','margin' : '20px'}, {'display': 'inline'}, "Enter your genome name and method name" , None, style



    @app.callback(
        [Output('TE-filename', 'children'), Output('genome-container', 'style'), Output('GO-container', 'style'), Output('CHIP-container', 'style')],
        Input('upload-TE','filename')
        )
    def update_TE(filename):
        if filename is not None:
            if len(filename) > 30:
                filename = filename[:10]+"..."+filename[-10:]
            return 'Selected file : {}'.format(filename), {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}, {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}, {'display': 'block', 'float':'left', 'width' :'20%', 'height': '10%', 'margin' : '20px'}
        else:
            return None, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


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

    @app.callback(
        [Output("genome-download-output","children"), Output("loading-output-genome", "children")],
        Input("submit-genome", "n_clicks"),
        State('genome-entry','value')
        )

    def download_genome(submit, GenomeName):

        if GenomeName is None:
            return None, None
        try:
            FNAaTelecharger, FNAsize, GFFaTelecharger, GFFsize, ftpAdress = Interface_DownloadGenomes.lanceTelechargement(GenomeName, pathVisualDATA)

            temp = pathVisualDATA + '/' + FNAaTelecharger
            url = ftpAdress + FNAaTelecharger
            dash_functions.online_download(url, temp)

            temp = pathVisualDATA + '/' + GFFaTelecharger
            url = ftpAdress + GFFaTelecharger
            dash_functions.online_download(url, temp)

            return "Downloaded {} FNA and GFF files".format(GenomeName), None
        except Exception:

            return "Couldn't find {} genome files".format(GenomeName), None

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

    @app.callback(
        [Output("GO-download-output", "children"), Output("loading-output-GO", "children")],
        Input("GO-download", "n_clicks")
        )

    def download_GO(click):
        if click:
            temp = pathVisualDATA + '/go-basic.obo'
            url = 'http://purl.obolibrary.org/obo/go/go-basic.obo'
            dash_functions.online_download(url, temp)

            temp = pathVisualDATA + '/gene2go.gz'
            url = 'http://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz'
            dash_functions.online_download(url, temp)

            return "Downloaded all necessary GO files", None
        else:
            return None, None

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

    @app.callback(
        [Output("CHIP-download-output","children"), Output("loading-output-CHIP", "children")],
        Input("CHIP-download", "n_clicks"),
        State('CHIP-entry','value'),
        State("genome-name-entry", "value"),
        State("method-name-entry", "value"),
        )

    def download_genome_CHIP_SEQ(submit, GenomeName, GenomeNameMain, TEmethod):

        pathVisual = 'VisualTE3__' + str(GenomeNameMain) + '__' + str(TEmethod)

        pathVisualDATA = pathVisual + '/Downloaded'

        if GenomeName is None:
            return None, None
        try:
            dash_functions.downloadENCODE(GenomeName, pathVisualDATA)

            return "Downloaded {} CHIP-Seq files".format(GenomeName), None
        except Exception as e:
            print(e)
            return "Couldn't find {} CHIP-Seq files".format(GenomeName), None

    app.run_server(debug=True)