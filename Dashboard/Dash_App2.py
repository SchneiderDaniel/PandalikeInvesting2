# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth,apply_layout_without_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html

url_base = '/dash/app2/'

layout = html.Div([
    html.Div('This is dash app2'), html.Br(),
    dcc.Input(id = 'input_text'), html.Br(), html.Br(),
    html.Div(id = 'target')
], style={'font-family':'"Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif'})

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base)
    apply_layout_without_auth(app, layout)

    @app.callback(
            Output('target', 'children'),
            [Input('input_text', 'value')])
    def callback_fun(value):
        return 'your input is {}'.format(value)

    return app.server