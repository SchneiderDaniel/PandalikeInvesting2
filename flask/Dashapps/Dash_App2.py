# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER, ClientsideFunction
from .Dash_fun import apply_layout_with_auth,apply_layout_without_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html

import dash
import dash_table
from dash_table.Format import Format, Group, Prefix, Scheme, Symbol
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from .dash_base import warning_card, colors
import datetime as dt 
from .compute_util.stockinterface import isTickerValid, getCorrelationMatrix, getPortfolioCorrelation,getCorrelationMatrix_List, getPortfolioCorrelation_List, getTickerDataframesList, getTickerDataframe
from flask import request
import locale

# from ./compute_util/stockinterface import isTickerValid

url_base = '/dash/app2/'

def get_dummy_df():
    d = {'-': [0, 0], '- ': [0, 0]}
    df = pd.DataFrame(data=d)
    return df

df_corr =  get_dummy_df()

def description_card():
    return html.Div(
        id="description_card",
        children = [dcc.Markdown('''This tool can compute the correlation of your assets. It uses the ticker of yahoo and computes the correlation for all combinations of your assets. This is called the correlation matrix. The coorelation is computed on the daily, as well as on the monthly performance. We compute it for the maximum timeframe of the data. But additionally, you can also enter a custom timeframe. You have to be careful with currency. We don't check the currency, so **don't mix currencies**.''')],
    style={
        'backgroundColor': colors['background'],
    })

def ticker_card():

    return html.Div(
        children=[
            html.H3(children='Portfolio'),
            dbc.Alert(
                [
                    "You can get Tickers from www.finance.yahoo.com ",
                    # html.A(" www.finance.yahoo.com", href="https://finance.yahoo.com", className="alert-link", target='_blank'),
                ],
                color="primary",
            ),
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
    html.P("Custom Timeframe (Optional):",style={"font-style": "italic" }),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt.datetime(1971,1,1),
        max_date_allowed= dt.datetime.now(),
        initial_visible_month=dt.datetime.now(),
        start_date=dt.datetime(2019,1,1),
        end_date=dt.datetime.now()
    ),
    html.Br(),
    html.Br(),
    dbc.Button("Compute (Takes a few minutes!)", id="compute-button", color="primary", block=True),
    html.Span(id="compute-output", style={"vertical-align": "middle","font-style": "italic" }),
    html.Br(),
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
            'font-family':'"Poppins", sans-serif',
            
        },
        id='compute-table-daily',
        columns=[{"name": i, "id": i} for i in df_corr.columns],
        data=df_corr.to_dict('records')
        
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
    html.P(children='Daily - Custom Timeframe',style={"font-style": "italic" }),
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
        id='compute-table-daily_c',
        columns=[{"name": i, "id": i} for i in df_corr.columns],
        data=df_corr.to_dict('records'),
    ),
    html.Br(),
    html.P(children='Monthly - Custom Timeframe',style={"font-style": "italic" }),
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
        id='compute-table-monthly_c',
        columns=[{"name": i, "id": i} for i in df_corr.columns],
        data=df_corr.to_dict('records'),
    ),
    html.Br(),
    html.P(children='Portfolio Correlations',style={"font-style": "italic" }),
    dash_table.DataTable(
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
               'if': {'column_id': 'Correlation'},
               'backgroundColor': 'rgb(230, 230, 230)',
               'color' : 'blue',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            # 'fontWeight': 'bold'
        },
        style_cell={
            'font-family':'"Poppins", sans-serif'
        },
        id='portfolio-table',
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


def getAllPortfolioCorrelation_List(dfList,tickers,percents,start,end):
    benchTickers = []
    benchTickers.append('IWDA.AS')
    benchTickers.append('SPY')
    benchTickers.append('EXSA.MI')

    benchName = []
    benchName.append('MSCI World')
    benchName.append('S&P 500')
    benchName.append('Stoxx Europe 600')

    benchDataframes = []
    benchDataframes.append(getTickerDataframe(benchTickers[0]))
    benchDataframes.append(getTickerDataframe(benchTickers[1]))
    benchDataframes.append(getTickerDataframe(benchTickers[2]))



    pfResults = []
    for i in range(len(benchTickers)):
        pfCorr=[]
        pfCorr.append(benchName[i])
        pfCorr.append('Daily')
        pfCorrRes = getPortfolioCorrelation_List(dfList,percents,benchDataframes[i])
        for a in pfCorrRes:
            pfCorr.append(a)
     
        pfCorrMonthly = []
        pfCorrMonthly.append(benchName[i])
        pfCorrMonthly.append('Monthly')
        pfCorrMonthlyRes = getPortfolioCorrelation_List(dfList,percents,benchDataframes[i], daily=False)
        for a in pfCorrMonthlyRes:
            pfCorrMonthly.append(a)
        
        pfCorrCustom = []
        pfCorrCustom.append(benchName[i])
        pfCorrCustom.append('Daily')
        pfCorrCustomRes = getPortfolioCorrelation_List(dfList,percents,benchDataframes[i], start,end)
        for a in pfCorrCustomRes:
            pfCorrCustom.append(a)
        
        pfCorrCustomMonthly = []
        pfCorrCustomMonthly.append(benchName[i])
        pfCorrCustomMonthly.append('Monthly')
        pfCorrCustomMonthlyRes = getPortfolioCorrelation_List(dfList,percents,benchDataframes[i],start,end, daily=False)
        for a in pfCorrCustomMonthlyRes:
            pfCorrCustomMonthly.append(a)
      

        pfResults.append(pfCorr)
        pfResults.append(pfCorrMonthly)
        pfResults.append(pfCorrCustom)
        pfResults.append(pfCorrCustomMonthly)

    # print (pfResults)
    result = pd.DataFrame.from_records(pfResults)
    result.columns = ['Benchmark:', 'Intervall', 'Correlation', 'from', 'to']

    return result


def getAllPortfolioCorrelation(tickers,percents,start,end):
    benchTickers = []
    benchTickers.append('IWDA.AS')
    benchTickers.append('SPY')
    benchTickers.append('EXSA.MI')

    benchName = []
    benchName.append('MSCI World')
    benchName.append('S&P 500')
    benchName.append('Stoxx Europe 600')

    pfResults = []
    for i in range(len(benchTickers)):
        pfCorr=[]
        pfCorr.append(benchName[i])
        pfCorr.append('Daily')
        pfCorrRes = getPortfolioCorrelation(tickers,percents,benchTickers[i])
        for a in pfCorrRes:
            pfCorr.append(a)
     
        pfCorrMonthly = []
        pfCorrMonthly.append(benchName[i])
        pfCorrMonthly.append('Monthly')
        pfCorrMonthlyRes = getPortfolioCorrelation(tickers,percents,benchTickers[i], daily=False)
        for a in pfCorrMonthlyRes:
            pfCorrMonthly.append(a)
        
        pfCorrCustom = []
        pfCorrCustom.append(benchName[i])
        pfCorrCustom.append('Daily')
        pfCorrCustomRes = getPortfolioCorrelation(tickers,percents,benchTickers[i], start,end)
        for a in pfCorrCustomRes:
            pfCorrCustom.append(a)
        
        pfCorrCustomMonthly = []
        pfCorrCustomMonthly.append(benchName[i])
        pfCorrCustomMonthly.append('Monthly')
        pfCorrCustomMonthlyRes = getPortfolioCorrelation(tickers,percents,benchTickers[i],start,end, daily=False)
        for a in pfCorrCustomMonthlyRes:
            pfCorrCustomMonthly.append(a)
      

        pfResults.append(pfCorr)
        pfResults.append(pfCorrMonthly)
        pfResults.append(pfCorrCustom)
        pfResults.append(pfCorrCustomMonthly)

    # print (pfResults)
    result = pd.DataFrame.from_records(pfResults)
    result.columns = ['Benchmark:', 'Intervall', 'Correlation', 'from', 'to']

    return result


def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], external_scripts = ["https://cdn.plot.ly/plotly-locale-de-latest.js"], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    app.config.suppress_callback_exceptions = True
    apply_layout_without_auth(app, layout)

    @app.callback(
        [Output("compute-output", "children"),
        Output(component_id='compute-table-daily', component_property='data'),
        Output(component_id='compute-table-daily', component_property='columns'),
        Output(component_id='compute-table-monthly', component_property='data'),
        Output(component_id='compute-table-monthly', component_property='columns'),
        Output(component_id='compute-table-daily_c', component_property='data'),
        Output(component_id='compute-table-daily_c', component_property='columns'),
        Output(component_id='compute-table-monthly_c', component_property='data'),
        Output(component_id='compute-table-monthly_c', component_property='columns'),
        Output(component_id='portfolio-table', component_property='data'),
        Output(component_id='portfolio-table', component_property='columns')],
        [Input(component_id={'type': 'dynamic-ticker', 'index': ALL}, component_property='value'),
        Input(component_id={'type': 'dynamic-percent', 'index': ALL}, component_property='value'),
        Input('compute-button', 'n_clicks'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date')]
    )
    def compute(ticker_values, percent_values,n_clicks,start_date, end_date):    
        

        request_locale  = request.accept_languages.best_match(['en_US','de_DE'])
        if (request_locale=='en_US'): 
             dash_locale = 'en'
             sep_locale = "."
        else:
            dash_locale = 'de'
            sep_locale = ","


        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        msg = ""
        df_corr_result_max = get_dummy_df()
        columns_corr_result_max = [{'name': col, 'id': col, 'type': 'numeric', 'format' : dict(specifier='.2f', locale=dict(decimal=sep_locale)) } for col in df_corr_result_max.columns]
        if 'compute-button' in changed_id:

            if len(ticker_values)<2: return 'You need at least 2 tickers.', df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max

            result_percents = isValid_percents(percent_values)
            if (result_percents==2): return 'Sum of percent needs to be 0 or 100', df_corr_result_max.to_dict(orient='records'), columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max

            result_tickers = isValid_tickers(ticker_values)
            if not result_tickers[1]:
                return 'Ticker at position {} cannot be found on yahoo'.format(result_tickers[0]+1), df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max

            print ('Start Correlation Computation')

            dfList = getTickerDataframesList(ticker_values)

            corr_result_max = getCorrelationMatrix_List(dfList, daily=True)
            corr_result_max_monthly = getCorrelationMatrix_List(dfList, daily=False)

            # print(start_date)
            # print(end_date)
            corr_result_max_c = getCorrelationMatrix_List(dfList, filterStart=start_date, filterEnd=end_date, daily=True)
            corr_result_max_monthly_c = getCorrelationMatrix_List(dfList, filterStart=start_date, filterEnd=end_date, daily=False)
            
            # print(corr_result_max)
            df_corr_result_max = pd.DataFrame(data=corr_result_max[0], index=ticker_values, columns=ticker_values)
            df_corr_result_max.insert(loc=0, column='Ticker', value=ticker_values)

            df_corr_result_max_monthly = pd.DataFrame(data=corr_result_max_monthly[0], index=ticker_values, columns=ticker_values)
            df_corr_result_max_monthly.insert(loc=0, column='Ticker', value=ticker_values)

            df_corr_result_max_c = pd.DataFrame(data=corr_result_max_c[0], index=ticker_values, columns=ticker_values)
            df_corr_result_max_c.insert(loc=0, column='Ticker', value=ticker_values)

            df_corr_result_max_monthly_c = pd.DataFrame(data=corr_result_max_monthly_c[0], index=ticker_values, columns=ticker_values)
            df_corr_result_max_monthly_c.insert(loc=0, column='Ticker', value=ticker_values)

            correlationsDF = get_dummy_df()
            if (result_percents==1): correlationsDF = getAllPortfolioCorrelation_List(dfList,ticker_values,percent_values,start_date,end_date)

            # print(df_corr_result_max)
            columns_corr_result_max = [{'name': col, 'id': col, 'type': 'numeric', 'format' : dict(specifier='.2f', locale=dict(decimal=sep_locale))} for col in df_corr_result_max.columns]
            columns_corr_result_max_monthly = [{'name': col, 'id': col, 'type': 'numeric', 'format' : dict(specifier='.2f', locale=dict(decimal=sep_locale))} for col in df_corr_result_max_monthly.columns]
            columns_corr_result_max_c = [{'name': col, 'id': col, 'type': 'numeric', 'format' : dict(specifier='.2f', locale=dict(decimal=sep_locale))} for col in df_corr_result_max_c.columns]
            columns_corr_result_max_monthly_c = [{'name': col, 'id': col, 'type': 'numeric', 'format' : dict(specifier='.2f', locale=dict(decimal=sep_locale))} for col in df_corr_result_max_monthly_c.columns]

            columns_correlationsDF = [{'name': col, 'id': col, 'type': 'numeric', 'format' : dict(specifier='.2f', locale=dict(decimal=sep_locale))} for col in correlationsDF.columns]

            

            print ('End Correlation Computation')
            return 'Finished: Maximum timeframe from {} to {}'.format(corr_result_max[1],corr_result_max[2]), df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max_monthly.to_dict(orient='records'),columns_corr_result_max_monthly, df_corr_result_max_c.to_dict(orient='records'),columns_corr_result_max_c, df_corr_result_max_monthly_c.to_dict(orient='records'),columns_corr_result_max_monthly_c, correlationsDF.to_dict(orient='records'),columns_correlationsDF
             
        return msg, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max, df_corr_result_max.to_dict(orient='records'),columns_corr_result_max


    
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
                                html.Div("%"),
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