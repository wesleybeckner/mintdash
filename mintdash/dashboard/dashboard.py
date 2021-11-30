import os
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
import numpy as np
import pandas as pd
from .plotlyfunctions import *
from datetime import datetime, date
from dash.exceptions import PreventUpdate

# Initialize dataframe
df = pd.read_csv("data/transactions.csv")
df = process_data(df, pivot_dates=False)

categories = list(df.Category.unique())
income = ['Income', 'Paycheck', 'Transfer', 'Federal Tax', 'Taxes', 'Rental Income', 'Interest Income']
taxes = ['Federal Tax', 'Taxes']
internal_acc = ['Credit Card Payment', 'Transfer', 'Financial']
non_expense =  income + taxes + internal_acc
expenses = [i for i in categories if i not in non_expense]

df = df.loc[df['Category'].isin(expenses)]

# Build App
def init_dashboard(server, debug=False):

    if debug == False:
        dash_app = Dash(
            server=server,
            routes_pathname_prefix='/',
            external_stylesheets=external_stylesheets,
            title = "MintDash"
            # prevent_initial_callbacks=True,
        )

    else:
        dash_app = Dash(__name__, 
        prevent_initial_callbacks=False,
        external_stylesheets = external_stylesheets,
        title = "MintDash"
        )

    UPLOAD = html.Div([
    dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        html.A('Drag and Drop or Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin-top': '10px'
                    },
                    multiple=False
                ),
                html.Div(id='output-data-upload'),
                dcc.Store(id='df-describe'),
                ])

    CONTROLS = html.Div([
        html.Div([
        html.H2("Controls"),
        UPLOAD,
        dbc.Row([
            dbc.Col([
                html.P("Primary Comparison", style={'margin-top': '15px'}),
                dcc.Dropdown(
                multi=False,
                id="comparison1",
                options=[{'label': 'Top/Bottom 10%', 'value': 0.1},
                    {'label': 'Top/Bottom Quartiles', 'value': 0.25},
                    {'label': 'Above/Bellow Median', 'value': 0.5}  ],
                value=None,
                style={'color': colors['text']},
                ),
            ]),
            dbc.Col([
                html.P("Secondary Comparison", style={'margin-top': '15px'}),
                dcc.Dropdown(
                multi=False,
                id="comparison2",
                options=[{'label': 'Time-Based', 'value': 'Time Comparison'},
                    {'label': 'Spend Threshold', 'value': '[20, 150]'}  ],
                value=None,
                style={'color': colors['text']},
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Years", style={'margin-top': '15px'}),
                dcc.Dropdown(
                multi=True,
                id="time",
                options=[{'label': i, 'value': i} for i in [2020, 2021]],
                value=[2020, 2021],
                style={'color': colors['text']},
                ),
            ]),
            dbc.Col([
                html.P("Ignore Transactions Over ($)", style={'margin-top': '15px'}),
                dbc.Input(type="number", value=8000, id='limit'),
            ])

        ]),
        ], style={'height': style['height']}),
        
        html.Div(id='table'),
    ])

    dash_app.layout = html.Div([
        NAVBAR,
        html.Div([
            html.Div([
                CONTROLS,   
            ],
            className = "four columns",
            ),
            html.Div([
                dcc.Store(id='df', data=df.to_json()),
                html.Div([
                    dcc.Graph(
                                id='fig-1',
                                style={'height': style['height']},
                    ),
                    dcc.Graph(
                                id='fig-2',
                                style={'height': style['height']},
                    ),
                ], id='figures'),
                html.Div(id='dummydiv'),
                ],
                className = "eight columns",
                ),
            ], 
            className = "twelve columns",
            style = {'padding': '10px'}
            ),
    ])

    init_callbacks(dash_app)

    if debug == False:
        return dash_app.server
    else:
        return dash_app

def init_callbacks(app):
    @app.callback(Output('df', 'data'),
                Output('time', 'options'),
                Output('loaddummy', 'children'),
                Input('upload-data', 'contents'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'),
                prevent_inital_call=True)
    def update_output(content, name, date):
        if content is not None:
            table, groups, target, dfjson, dates = parse_contents(content, name, date)
            datestyle = {'display': 'none'}
            if dates is not None:
                datestyle = {'margin-top': '15px',
                    'font-size': '15px',
                    'display': 'block'}
                options = [{'label': i, 'value': i} for i in dates]
            return dfjson, options, None
        else:
            raise PreventUpdate

    @app.callback(
        Output('fig-1', 'figure'),
        Output('fig-2', 'figure'),
        Output('table', 'children'),
        Output('header', 'children'),
        Input('comparison1', 'value'),
        Input('comparison2', 'value'),
        Input('time', 'value'),
        Input('df', 'data'),
        Input('limit', 'value'),)
    def update_fig(quantile, bins, year, data, limit):
        ctx = dash.callback_context
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        
        df = pd.read_json(data)
        df = process_data(df, pivot_dates=False)
        df = df.loc[(df.Amount < limit)]

        categories = list(df.Category.unique())
        income = ['Income', 'Paycheck', 'Transfer', 'Federal Tax', 'Taxes', 'Rental Income', 'Interest Income']
        taxes = ['Federal Tax', 'Taxes']
        internal_acc = ['Credit Card Payment', 'Transfer', 'Financial']
        non_expense =  income + taxes + internal_acc
        expenses = [i for i in categories if i not in non_expense]

        df = df.loc[df['Category'].isin(expenses)]

        x = 'Category'
        if bins == "[20, 150]":
            bins = [20, 150]
        topcut = 20
        fig1, fig2, fig3 = make_figs(df, 
                                     year, x, 
                                     bins, 
                                     quantile, 
                                     topcut, 
                                     duplicate_legends=False, 
                                     showfig=False)
        if fig3 == None:
            obj3 = None
        else:
            obj3 = dcc.Graph(
                                id='fig-3',
                                figure=fig3,
                                style={'height': style['height'],
                                        'margin': '10px',
                                        'padding': '0px'}
                    ),
        return fig1, fig2, obj3, "MintDash"