# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER, ClientsideFunction
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from .dash_base import warning_card, colors
import dash_table

url_base = '/dash/app3/'

def description_card():
    return html.Div(
        id="description_card",
        children="The question about an active vs. passive investment fund is present in many discussions about investing. What is true for most instances is, that an active investment fund is often more expensive than their passive counterparts (the ones that are based on the same benchmark). The question that this tool wants to answer is, how much outperformance (%, pa) does the more expensive active investment needs, to get close to their benchmark index, as well as to the correspondig index ETF. Also be aware, this tool can not only be used to compare an active vs an passive investment. You can also use it to compare two active funds or two passive funds.",
    style={
        'backgroundColor': colors['background'],
    })

def basic_card():
    return html.Div(
        children=[
            html.H3(children='General Input'),
            dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Benchmark Perf. (%,pa)"),
                                dbc.Input(type="number", value='6', placeholder="Enter the performance "),
                                html.Div("One Time Investment:"),
                                dbc.Input(type="number", value='10000', placeholder="Enter the investment ")
                            ],
                            width=6
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Investment Duration"),
                                dbc.Input(type="number", value='30', placeholder="Enter the duration"),
                                html.Div("Monthly Investment:"),
                                dbc.Input(type="number", value='500', placeholder="Enter the investment ")
                            ],
                            width=6
                        ),
                    ]
            ) 
        ],
        style={
        'backgroundColor': colors['background'],
        }
    )

def cheap_card():
    return "TODO"

def exp_card():
    return "TODO"


# The Layout
layout = html.Div(style={'font-family':'"Poppins", sans-serif', 'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Active vs Passive',
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
    html.Div(children=basic_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    html.Div(children=cheap_card(), style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    html.Div(children=exp_card(), style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    html.Br(),
    html.Div(children=warning_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    })
])


def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    apply_layout_with_auth(app, layout)

    return app.server