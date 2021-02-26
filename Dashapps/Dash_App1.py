# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from .dash_base import warning_card, colors

url_base = '/dash/app1/'

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

def description_card():
    return html.Div(
        id="description-card",
        children="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    )

# The Layout
layout = html.Div(style={'font-family':'"Poppins", sans-serif'}, children=[
    html.H1(
        children='This is a title',
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

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    ),

    html.Div(children=warning_card(), style={
        'textAlign': 'left',
        'color': colors['text']
    })



])


def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(app, layout)

    @app.callback(
            Output('target', 'children'),
            [Input('input_text', 'value')])
    def callback_fun(value):
        return 'your input is {}'.format(value)
    
    return app.server