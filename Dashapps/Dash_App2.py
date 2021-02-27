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


df2 = pd.read_csv('./app/base/static/testdata/solar.csv')

list_id_tickier =  []
list_id_percent = []

def step():
    id_ticker = str(np.random.randn())
    id_percent = str(np.random.randn())
    return html.Div(
        children=[
            dbc.Row(
                [
                    dbc.Col( 
                        children=[
                            html.Div("Ticker:"),
                            dbc.Input(type="text", placeholder="Enter a ticker",id=id_ticker)
                        ],
                        width=6
                    ),
                    dbc.Col( 
                        children=[
                            html.Div("Percent:"),
                            dbc.Input(type="number", placeholder="Enter %",id=id_percent)
                        ],
                        width=4
                    )
                ],
                style = { 'width': '80%'}
            ),
            html.Br(),
    ])

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
            html.Div(children=[step()], id='step_list'),
            dbc.Button('Add Ticker', color="secondary", id='add_step_button', n_clicks_timestamp='0', className="mr-1"),
            dbc.Button('Remove Ticker', color="secondary", id='remove_step_button', n_clicks_timestamp='0', className="mr-1")
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


    @app.callback(
    Output("compute-output", "children"), [Input("compute-button", "n_clicks")])
    def on_button_click(n):
        if n is None:
            return "Not clicked."
        else:
            return f"Clicked {n} times."

    return app.server