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

url_base = '/dash/app1/'

def description_card():
    return html.Div(
        id="description_card",
        children="This tool wants to help you to rebalance your portfolio. If you have a desired distribution among a set of assets, it comes the time where this distribution is not longer the same. Some assets have increased and some decreased in value. If you now want to reblance your assets, this tool should make it easy for you.",
    style={
        'backgroundColor': colors['background'],
    })

def asset_card():
    return html.Div(
        children=[
            html.H3(children='Portfolio'),
            html.Div(children=[], id='container_asset'),
            dbc.Button('Add Asset', color="secondary", id='add_ticker_button',  n_clicks=1, className="mr-1"),
            ],
        style={
        'backgroundColor': colors['background'],
        }
    )

# The Layout
layout = html.Div(style={'font-family':'"Poppins", sans-serif', 'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Portfolio Rebalancing',
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
    asset_card(),
    html.Span(id="compute-output", style={"vertical-align": "middle","font-style": "italic" }),
    html.Br(),
    html.Br(),
    html.Div(children=warning_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    })
])

def get_dummy_result(l,text):  
    result = []
    text = [text]
    for i in range(l):
        result.append("-")
    return result,result,result,text

def sumsTo100(percents):
    sum = 0
    for p in percents:
        if p is not None:
            sum+=float(p)
    return sum==100

def hasNoneType(quantities,prices,percents):
    for q in quantities:
        if q is None:
            return True
    for pr in prices:
        if pr is None:
            return True
    for p in percents:
        if p is None:
            return True
    return False

def getPortfolioSize(quantities,prices):
    sum = 0
    for i in range(len(quantities)):
        sum+=(float(quantities[i])*float(prices[i]))
    return sum

def getValues(quantities,prices):
    result =[]
    for i in range(len(quantities)):
        result.append(float(quantities[i])*float(prices[i]))
    return result

def getNewValues(portfolioSize,percents):
    newValues = []
    for i in range(len(percents)):
        newValues.append(float(portfolioSize)*float(percents[i])/100.0)
    return newValues
    
def getChanges(values,new_Values):
    changes = []
    for i in range(len(values)):
        changes.append(float(new_Values[i])-float(values[i]))
    return changes

def getPieces(changes,prices):
    pieces = []
    for i in range(len(changes)):
        pieces.append(float(changes[i])/float(prices[i]))
    return pieces

def convertToString(value_list):
    result = []
    for i in range(len(value_list)):
        if (value_list[i]>=0):
            result.append("+"+"{:.2f}".format(value_list[i]))
        if (value_list[i]<0):
            result.append("{:.2f}".format(value_list[i]))
    return result

def convertToStringNoSign(value_list):
    result = []
    for i in range(len(value_list)):
        result.append("{:.2f}".format(value_list[i]))
    return result

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    apply_layout_with_auth(app, layout)

    @app.callback(
        [Output(component_id={'type': 'dynamic-new_value', 'index': ALL}, component_property='children'),
        Output(component_id={'type': 'dynamic-change', 'index': ALL}, component_property='children'),
        Output(component_id={'type': 'dynamic-piece-exact', 'index': ALL}, component_property='children'),
        Output("compute-output", "children")],
        [Input(component_id={'type': 'dynamic-quantity', 'index': ALL}, component_property='value'),
        Input(component_id={'type': 'dynamic-price', 'index': ALL}, component_property='value'),
        Input(component_id={'type': 'dynamic-percent', 'index': ALL}, component_property='value'),]
    )
    def computeBalance(quantities,prices,percents):      
        
        if len(quantities)==1:
            return get_dummy_result(len(quantities),"You need at least 2 assets")

        if hasNoneType(quantities,prices,percents):
            return get_dummy_result(len(quantities),"A field is empty")

        if not sumsTo100(percents):
            return get_dummy_result(len(quantities),"Goal does not sum to 100%")

        portfolioSize = getPortfolioSize(quantities,prices)
        values = getValues(quantities,prices)
        new_Values = getNewValues(portfolioSize,percents)
        changes  = getChanges(values,new_Values)
        pieces = getPieces(changes,prices)
        resutlText = []
        resutlText.append("The result is ready.")

        return convertToStringNoSign(new_Values), convertToString(changes), convertToString(pieces), resutlText

    @app.callback(
        [Output(component_id={'type': 'dynamic-sum', 'index': MATCH}, component_property='children')],
        [Input(component_id={'type': 'dynamic-quantity', 'index': MATCH}, component_property='value'),
        Input(component_id={'type': 'dynamic-price', 'index': MATCH}, component_property='value')]
    )
    def updateSumValue(quantity,price):      
        if quantity is not None:
            quantity = float(quantity)
        else:
            quantity = 0.0
        if price is not None: 
            price= float(price)
        else:
            price = 0.0
        result = price*quantity
        return ["%.2f" % result]

    @app.callback(
        Output('container_asset', 'children'),
        [Input('add_ticker_button', 'n_clicks')],
        [State('container_asset', 'children')]
    )
    def display_tickers(n_clicks, div_children):

        new_child= html.Div(
            children=[
                html.P("Asset #" + str(n_clicks) ,style = {"color": "#00b0f0"}),
                dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Pieces:"),
                                dbc.Input(type="number", value='4', placeholder="Enter the number of pieces ",
                                id={
                                    'type': 'dynamic-quantity',
                                    'index': n_clicks
                                })
                            ],
                            width=3
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Price:"),
                                dbc.Input(type="number", value='213.13', placeholder="Enter price per piece",
                                id={
                                    'type': 'dynamic-price',
                                    'index': n_clicks
                                })
                            ],
                            width=3
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Value:"),
                                html.P(children='-',
                                id={
                                    'type': 'dynamic-sum',
                                    'index': n_clicks
                                })
                            ],
                            width=3
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Goal (%):"),
                                dbc.Input(type="number", value='10', placeholder="Enter percent of asset",
                                id={
                                    'type': 'dynamic-percent',
                                    'index': n_clicks
                                })
                            ],
                            width=3
                        )
                    ],
                    style = { 'width': '100%'}
                ),
                dbc.Toast([
                dbc.Row(
                    [
                        
                        dbc.Col( 
                            children=[
                                html.Div("New Value:"),
                                html.P(children='4',
                                id={
                                    'type': 'dynamic-new_value',
                                    'index': n_clicks
                                })
                            ],
                            width=4
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Change:"),
                                html.P(children='-1000',
                                id={
                                    'type': 'dynamic-change',
                                    'index': n_clicks
                                })
                            ],
                            width=4
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Pieces:"),
                                html.P(children='-5.5',
                                id={
                                    'type': 'dynamic-piece-exact',
                                    'index': n_clicks
                                })
                            ],
                            width=4
                        )
                    ],
                    style = { 'width': '100%'}
                ),
                ],header="Change the asset to:", style={"maxWidth": "450px"}),

                html.Br(),
        ])
        div_children.append(new_child)
        return div_children

    return app.server