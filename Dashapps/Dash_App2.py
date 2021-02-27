# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER, ClientsideFunction
from .Dash_fun import apply_layout_with_auth,apply_layout_without_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html


import dash
import dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from .dash_base import warning_card, colors

url_base = '/dash/app2/'


df2 = pd.read_csv('./app/base/static/testdata/solar.csv')



def description_card():
    return html.Div(
        id="description-card",
        children="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    style={
        'backgroundColor': colors['background'],
    })

def ticker_card():

    return html.Div(
        children=[
            html.H3(children='Portfolio'),
            html.Div(children=[], id='container_ticker'),
            dbc.Button('Add Ticker', color="secondary", id='add_ticker_button',  n_clicks=1, className="mr-1"),
            ],
        style={
        'backgroundColor': colors['background'],
        }
    )



# The Layout
layout = html.Div(style={'font-family':'"Poppins", sans-serif', 'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Correlation Matrix',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': colors['background']
        }
    ),
    html.Div(children=description_card(), style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    ticker_card(),
    html.Br(),
    dbc.Button("Compute", id="compute-button", color="primary", block=True),
    html.Span(id="compute-output", style={"vertical-align": "middle"}),
    html.Br(),
    dash_table.DataTable(
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
               'if': {'column_id': 'State'},
               'backgroundColor': 'rgb(230, 230, 230)' 
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            # 'fontWeight': 'bold'
        },
        style_cell={
            'font-family':'"Poppins", sans-serif'
        },
        id='table',
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('records'),
    ),
    html.Br(),
    html.Div(children=warning_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    })
])



def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    app.config.suppress_callback_exceptions = True
    apply_layout_without_auth(app, layout)

    @app.callback(
        Output("compute-output", "children"),
        [Input(component_id={'type': 'dynamic-ticker', 'index': ALL}, component_property='value'),
        Input(component_id={'type': 'dynamic-percent', 'index': ALL}, component_property='value')]
    )
    def compute(ticker_values, percent_values):
        print(ticker_values)
        print(percent_values)
        # return "Testi"


    
    @app.callback(
        Output('container_ticker', 'children'),
        [Input('add_ticker_button', 'n_clicks')],
        [State('container_ticker', 'children')]
    )
    def display_tickers(n_clicks, div_children):

        new_child= html.Div(
            children=[
                dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Ticker:"),
                                dbc.Input(type="text", value='MSFT', placeholder="Enter a ticker",
                                id={
                                    'type': 'dynamic-ticker',
                                    'index': n_clicks
                                })
                            ],
                            width=6
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Percent:"),
                                dbc.Input(type="number", value='5', placeholder="Enter %",
                                id={
                                    'type': 'dynamic-percent',
                                    'index': n_clicks
                                })
                            ],
                            width=4
                        )
                    ],
                    style = { 'width': '80%'}
                ),
                html.Br(),
        ])
        div_children.append(new_child)
        return div_children

 







    return app.server