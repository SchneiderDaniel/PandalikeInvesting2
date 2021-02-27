# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output, ClientsideFunction
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

#https://stackoverflow.com/questions/52905569/dynamic-list-of-python-dash-core-components


df2 = pd.read_csv('./app/base/static/testdata/solar.csv')


def step():
     return html.Div(
        children=[
            dbc.Row(
                [
                    dbc.Col( 
                        children=[
                            html.Div("Ticker:"),
                            dbc.Input(type="text", placeholder="Enter a ticker symbol",id=str(np.random.randn()))
                        ]
                    ),
                    dbc.Col( 
                        children=[
                            html.Div("Percent:"),
                            dbc.Input(type="number", placeholder="Enter percentage (%)",id=str(np.random.randn()))
                        ]
                    )
                ]
            ),
    ])

def description_card():
    return html.Div(
        id="description-card",
        children="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    )

def ticker_card():

    return html.Div(
        children=[
            html.H3(children='Portfolio'),
            html.Div(children=[step()], id='step_list'),
            html.Br(),
            html.Button('Add Ticker', id='add_step_button', n_clicks_timestamp='0'),
            html.Button('Remove Ticker', id='remove_step_button', n_clicks_timestamp='0')])



# The Layout
layout = html.Div(style={'font-family':'"Poppins", sans-serif'}, children=[
    html.H1(
        children='Correlation Matrix',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children=description_card(), style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Br(),
    ticker_card(),
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
        'color': colors['text']
    })
])



def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    app.config.suppress_callback_exceptions = True
    apply_layout_without_auth(app, layout)

    @app.callback(
        dash.dependencies.Output('step_list', 'children'),
        [dash.dependencies.Input('add_step_button', 'n_clicks_timestamp'),
        dash.dependencies.Input('remove_step_button', 'n_clicks_timestamp')],
        [dash.dependencies.State('step_list', 'children')])
    def add_step(add_ts, remove_ts, div_list):
        add_ts = int(add_ts)
        remove_ts = int(remove_ts)
        if add_ts > 0 and add_ts > remove_ts:
            div_list += [step()]
        if len(div_list) > 1 and remove_ts > add_ts:
            div_list = div_list[:-1]
        return div_list

    return app.server