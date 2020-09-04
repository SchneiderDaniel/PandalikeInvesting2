# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html

url_base = '/dash/app1/'

import plotly.graph_objs as go
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])


layout = html.Div( [

    html.Div([
        html.Label('Dropdown'), html.Br(), html.Br(),
        dcc.Dropdown(
            options=[
                {'label': 'BR206', 'value': 'C'},
                {'label': u'BR177', 'value': 'A'},
                {'label': 'BR213', 'value': 'E'}
            ],
            value='MTL'
        ), 
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ]),
    html.Div([
        html.Br(), html.Label('Checkboxes'), html.Br(), html.Br(),
        dcc.Checklist(
            options=[
                {'label': 'BR206', 'value': 'C'},
                {'label': u'BR177', 'value': 'A'},
                {'label': 'BR213', 'value': 'E'}
            ],
            value=['MTL', 'SF']
        ),
        
        html.Br(),
        dcc.Graph(
            id='example-graph-2',
            figure=fig
        )
    ])
], style={'font-family':'"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif'})

#font-family: "Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif;

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(app, layout)

    @app.callback(
            Output('target', 'children'),
            [Input('input_text', 'value')])
    def callback_fun(value):
        return 'your input is {}'.format(value)
    
    return app.server