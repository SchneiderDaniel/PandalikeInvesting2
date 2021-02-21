# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

url_base = '/dash/app1/'

import plotly.graph_objs as go
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])


layout = html.Div([

    #First row
    html.Div([
        #Description
        html.Div([
            html.H3('Description'),
            dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),

        #Parameters
        html.Div([
            html.H3('Parameters'),
            dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="six columns"),
    ], className="row"),

    #Result
        html.Div([
            html.H3('Result'),
            dcc.Graph(id='g3', figure={'data': [{'y': [1, 2, 3]}]})
        ], className="twelve columns"),


], style={'font-family':'"Poppins", sans-serif'})

# layout = html.Div(className='row', children=[
#     html.H1("Tips database analysis (First dashboard)"),
#     dcc.Dropdown(),
#     html.Div(children=[
#         dcc.Graph(id="graph1", style={'display': 'inline-block'}),
#         dcc.Graph(id="graph2", style={'display': 'inline-block'})
#     ])
# ])

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