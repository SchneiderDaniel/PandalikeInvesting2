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

from .compute_util.stockinterface import isTickerValid, getCorrelationMatrix

# from ./compute_util/stockinterface import isTickerValid

url_base = '/dash/app2/'

def get_dummy_df():
    d = {'-': [0, 0], '--': [0, 0]}
    df = pd.DataFrame(data=d)
    return df

df_corr =  get_dummy_df()

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
    dbc.Button("Compute (Takes some time)", id="compute-button", color="primary", block=True),
    html.Span(id="compute-output", style={"vertical-align": "middle","font-style": "italic" }),
    html.Br(),
    html.H3(children='Result'),
    html.P(children='Daily - Maximum Timeframe',style={"font-style": "italic" }),
    dash_table.DataTable(
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
               'if': {'column_id': 'Ticker'},
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
        id='compute-table-daily',
        columns=[{"name": i, "id": i} for i in df_corr.columns],
        data=df_corr.to_dict('records'),
    ),
    html.Br(),
    html.P(children='Monthly - Maximum Timeframe',style={"font-style": "italic" }),
    dash_table.DataTable(
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
               'if': {'column_id': 'Ticker'},
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
        id='compute-table-monthly',
        columns=[{"name": i, "id": i} for i in df_corr.columns],
        data=df_corr.to_dict('records'),
    ),
    html.Br(),
    html.Div(children=warning_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    })
])

def isValid_tickers(ticker_values):

    for i in range(len(ticker_values)):
        if  ticker_values[i]=="": return [i,False]
    
    for i in range(len(ticker_values)):
        if not isTickerValid(ticker_values[i]): return [i,False]
    return [0,True]

def isValid_percents(percent_values):
    sum=0
    for percent in percent_values:
        percent = float(percent)
        sum+=percent
    if (sum==0): return 0
    if (sum==100): return 1
    return 2




def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    app.config.suppress_callback_exceptions = True
    apply_layout_without_auth(app, layout)

    @app.callback(
        [Output("compute-output", "children"),
        Output(component_id='compute-table-daily', component_property='data'),
        Output(component_id='compute-table-daily', component_property='columns'),
        Output(component_id='compute-table-monthly', component_property='data'),
        Output(component_id='compute-table-monthly', component_property='columns')],
        [Input(component_id={'type': 'dynamic-ticker', 'index': ALL}, component_property='value'),
        Input(component_id={'type': 'dynamic-percent', 'index': ALL}, component_property='value'),
        Input('compute-button', 'n_clicks')]
    )
    def compute(ticker_values, percent_values,n_clicks):    
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        msg = ""
        df_corr_result_max = get_dummy_df()
        columns_corr_result_max = [{'name': col, 'id': col} for col in df_corr_result_max.columns]
        if 'compute-button' in changed_id:

            if len(ticker_values)<2: return 'You need at least 2 tickers.', df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, f_corr_result_max.to_dict(orient='records'),columns_corr_result_max

            result_percents = isValid_percents(percent_values)
            if (result_percents==2): return 'Sum of percent needs to be 0 or 100', df_corr_result_max.to_dict(orient='records'), columns_corr_result_max, f_corr_result_max.to_dict(orient='records'),columns_corr_result_max

            result_tickers = isValid_tickers(ticker_values)
            if not result_tickers[1]:
                return 'Ticker at position {} is not valid'.format(result_tickers[0]+1), df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, f_corr_result_max.to_dict(orient='records'),columns_corr_result_max

            corr_result_max = getCorrelationMatrix(ticker_values)
            corr_result_max_monthly = getCorrelationMatrix(ticker_values,daily=False)
            
            # print(corr_result_max)
            df_corr_result_max = pd.DataFrame(data=corr_result_max[0], index=ticker_values, columns=ticker_values)
            df_corr_result_max.insert(loc=0, column='Ticker', value=ticker_values)
            df_corr_result_max_monthly = pd.DataFrame(data=corr_result_max_monthly[0], index=ticker_values, columns=ticker_values)
            df_corr_result_max_monthly.insert(loc=0, column='Ticker', value=ticker_values)

            # print(df_corr_result_max)
            columns_corr_result_max = [{'name': col, 'id': col} for col in df_corr_result_max.columns]
            columns_corr_result_max_monthly = [{'name': col, 'id': col} for col in df_corr_result_max_monthly.columns]
    
            return 'Computation finished: Timeframe from {} to {}'.format(corr_result_max[1],corr_result_max[2]), df_corr_result_max.to_dict('records'),columns_corr_result_max, df_corr_result_max_monthly.to_dict('records'),columns_corr_result_max_monthly
             
        return msg, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, f_corr_result_max.to_dict(orient='records'),columns_corr_result_max


    
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
                                dbc.Input(type="number", value='0', placeholder="Enter %",
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