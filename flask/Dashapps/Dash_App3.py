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
from datetime import datetime
import numpy as np
from flask import request
import locale


url_base = '/dash/app3/' 

def description_card():
    return html.Div(
        id="description_card",
        children = [dcc.Markdown('''If you have to choose between two investment funds that are based on the **same benchmark**, chances are high that they have different costs. This tool wants to give you an idea on the impact of the costs for the performance. In addition, we give you the opportunity to simulate a scenario where a fund delivers an outperformance to its benchmark. This can give you an idea how much outperformance per year is needed, in order to outperform the benchmark after costs.''')],
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
                                html.Div("Benchmark Perf. (%, pa)"),
                                dbc.Input(type="number", id="edit_perf", value='5.5', placeholder="Enter the performance "),
                                html.Div("One Time Investment"),
                                dbc.Input(type="number", id="edit_onetime_invest", value='10000', placeholder="Enter the investment ")
                            ],
                            width=6
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Investment Duration (years)"),
                                dbc.Input(type="number", id="edit_duration", value='30', placeholder="Enter the duration"),
                                html.Div("Monthly Investment"),
                                dbc.Input(type="number", id="edit_month_invest", value='500', placeholder="Enter the investment ")
                            ],
                            width=6
                        ),
                    ],
                    style = { 'width': '80%'}
            ) 
        ],
        style={
        'backgroundColor': colors['background'],
        }
    )

def cheap_card():
    return html.Div(
        children=[
            html.H3(children='Fund #1'),
            dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Total Expense Ratio - TER (%, pa)"),
                                dbc.Input(type="number", id="edit_cheap_ter", value='0.25', placeholder="Enter the performance "),
                            ],
                            width=6
                        ),
                    ],
                    style = { 'width': '80%'}
            ),
            dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Transaction fee (%)"),
                                dbc.Input(type="number", id="edit_cheap_trans_fee_per", value='0', placeholder="Enter the performance "),
                                html.Div("Other costs (once, pa, %)"),
                                dbc.Input(type="number", id="edit_cheap_other_per", value='0', placeholder="Enter the duration"),
                            ],
                            width=6
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Transaction fee (abs)"),
                                dbc.Input(type="number", id="edit_cheap_trans_fee_abs", value='1', placeholder="Enter the investment "),
                                html.Div("Other costs (once, pa, abs)"),
                                dbc.Input(type="number", id="edit_cheap_other_abs", value='4.99', placeholder="Enter the investment ")
                            ],
                            width=6
                        ),
                    ],
                    style = { 'width': '80%'}
            ) 
        ],
        style={
        'backgroundColor': colors['background'],
        }
    )

def exp_card():
    return html.Div(
        children=[
            html.H3(children='Fund #2'),
            dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Total Expense Ratio - TER (%, pa)"),
                                dbc.Input(type="number", id="edit_exp_ter", value='1.25', placeholder="Enter the performance "),
                            ],
                            width=6
                        ),
                    ],
                    style = { 'width': '80%'}
            ),
            dbc.Row(
                    [
                        dbc.Col( 
                            children=[
                                html.Div("Transaction fee (%)"),
                                dbc.Input(type="number", id="edit_exp_trans_fee_per", value='0.2', placeholder="Enter the performance "),
                                html.Div("Other costs (once, pa, %)"),
                                dbc.Input(type="number", id="edit_exp_other_per", value='0.0', placeholder="Enter the duration"),
                                html.Br(),
                                html.Div("Outperformance (%, pa)"),
                                dbc.Input(type="number", id="edit_outperf", value='1.45', placeholder="Enter the outperformance ")
                                
                            ],
                            width=6
                        ),
                        dbc.Col( 
                            children=[
                                html.Div("Transaction fee (abs)"),
                                dbc.Input(type="number", id="edit_exp_trans_fee_abs", value='7.99', placeholder="Enter the investment "),
                                html.Div("Other costs (once, pa, abs)"),
                                dbc.Input(type="number", id="edit_exp_other_abs", value='9.99', placeholder="Enter the investment "),                                
                            ],
                            width=6
                        ),
                    ],
                    style = { 'width': '80%'}
            ),
        ],
        style={
        'backgroundColor': colors['background'],
        }
    )

def result_card():
    return html.Div(
            children=[
                html.H3(children='End results'),
                dbc.Row([
                    dbc.Col( 
                            children=[
                                html.Div("Benchmark"),
                                html.Span(id="benchmark-output", style={"vertical-align": "middle","font-style": "italic","color" : "blue" }),
                            ],
                            width=4
                        ),
                    dbc.Col( 
                            children=[
                                html.Div("Fund #1"), 
                                html.Span(id="cheaper-output", style={"vertical-align": "middle","font-style": "italic","color" : "red" }),
                                
                            ],
                            width=4
                        ),
                    dbc.Col( 
                            children=[
                                html.Div("Fund #2"),
                                html.Span(id="other-output", style={"vertical-align": "middle","font-style": "italic","color" : "green" }),
                                
                            ],
                            width=4
                        ),


                ],
                    style = { 'width': '80%'})
            ]
        )



# The Layout
layout = html.Div(style={'font-family':'"Poppins", sans-serif', 'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Impact of Costs to your Performance',
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
    html.Hr(className="my-2"),
    html.Br(),
    html.Div(children=cheap_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    html.Hr(className="my-2"),
    html.Br(),
    html.Div(children=exp_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    html.Hr(className="my-2"),
    html.Br(),
    dcc.Graph(id='graph'),
    html.Br(),
    html.Hr(className="my-2"),
    
    html.Br(),
    html.Div(children=result_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    }),
    html.Br(),
    html.Hr(className="my-2"),
    html.Br(),
    html.Div(children=warning_card(), style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background']
    })
])

def cast_int(val):
    if val is None: return 1
    return int(val)

def cast_float(val):
    if val is None: return 1.0
    return float(val)

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets = [dbc.themes.BOOTSTRAP], external_scripts = ["https://cdn.plot.ly/plotly-locale-de-latest.js"], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
    
    apply_layout_with_auth(app, layout)

    

    @app.callback(
        [Output('graph', 'figure'),
        Output('graph', 'config'),
        Output("benchmark-output", "children"),
        Output("cheaper-output", "children"),
        Output("other-output", "children")],
        [
        Input('edit_perf', 'value'),
        Input('edit_onetime_invest', 'value'),
        Input('edit_duration', 'value'),
        Input('edit_month_invest', 'value'),
        Input('edit_cheap_ter', 'value'),
        Input('edit_cheap_trans_fee_per', 'value'),
        Input('edit_cheap_other_per', 'value'),
        Input('edit_cheap_trans_fee_abs', 'value'),
        Input('edit_cheap_other_abs', 'value'),
        Input('edit_exp_ter', 'value'),
        Input('edit_exp_trans_fee_per', 'value'),
        Input('edit_exp_other_per', 'value'),
        Input('edit_outperf', 'value'),
        Input('edit_exp_trans_fee_abs', 'value'),
        Input('edit_exp_other_abs', 'value')
        ]
    )
    def display_tickers(perf,onetime_invest,duration,month_invest,cheap_ter,cheap_trans_fee_per,cheap_other_per,
    cheap_trans_fee_abs,cheap_other_abs,exp_ter,exp_trans_fee_per,exp_other_per,outperf,exp_trans_fee_abs,exp_other_abs):
        
        perf  = cast_float(perf)
        onetime_invest  = cast_float(onetime_invest)
        duration  = cast_int(duration)
        month_invest = cast_float(month_invest)

        cheap_ter = cast_float(cheap_ter)
        cheap_trans_fee_per = cast_float(cheap_trans_fee_per)
        cheap_other_per = cast_float(cheap_other_per)
        cheap_trans_fee_abs = cast_float(cheap_trans_fee_abs)
        cheap_other_abs = cast_float(cheap_other_abs)

        exp_ter = cast_float(exp_ter)
        exp_trans_fee_per = cast_float(exp_trans_fee_per)
        exp_other_per = cast_float(exp_other_per)
        outperf = cast_float(outperf)
        exp_trans_fee_abs = cast_float(exp_trans_fee_abs)
        exp_other_abs = cast_float(exp_other_abs)


        duration_months = duration*12
        ref_up_months = pow(1.0+(perf/100.0),(1.0/12.0))
        cheap_up_months =  pow(1.0+((perf-cheap_ter)/100.0),(1.0/12.0))
        exp_up_months =  pow(1.0+((perf-exp_ter+outperf)/100.0),(1.0/12.0))


        start_eval = datetime.now()
        start_eval = start_eval.replace(minute=0, hour=0, second=0, microsecond=0)

        dates = pd.date_range(start=start_eval, periods=duration_months, freq='M')
        
        resultReference = []
        resultCheap = []
        resultExp = []
        
        #Init the results
        for i in range(duration_months):
            resultReference.append(0.0)
            resultCheap.append(0.0)
            resultExp.append(0.0)


        for i in range(len(resultReference)):

            if i==0:
                resultReference[0]+=onetime_invest
                resultCheap[0]+=onetime_invest
                resultExp[0]+=onetime_invest
            else:
                resultReference[i] = resultReference[i-1] 
                resultCheap[i] = resultCheap[i-1]
                resultExp[i] = resultExp[i-1]

                if i%12==0:
                    resultCheap[i]*= (1.0-(cheap_other_per/100.0))
                    resultExp[i]*= (1.0-(exp_other_per/100.0))

                    resultCheap[i]-=cheap_other_abs
                    resultExp[i]-=exp_other_abs




            resultReference[i]+=month_invest
            resultCheap[i]+=month_invest
            resultExp[i]+=month_invest

            resultCheap[i]-=cheap_trans_fee_abs
            resultExp[i]-=exp_trans_fee_abs

            resultCheap[i]-=(month_invest*(cheap_trans_fee_per/100.0))
            resultExp[i]-=(month_invest*(exp_trans_fee_per/100.0))

            resultReference[i]*=ref_up_months
            resultCheap[i]*=cheap_up_months
            resultExp[i]*=exp_up_months

    
        request_locale  = request.accept_languages.best_match(['en_US','de_DE'])
        if (request_locale=='en_US'): 
            dash_locale = 'en'
            sep_locale = "."
            request_locale_utf8 = 'en_US.utf8'
        else:
            dash_locale = 'de'
            sep_locale = ","
            request_locale_utf8 = 'de_DE.utf8'
        locale.setlocale(locale.LC_ALL, request_locale_utf8)

        # print('dash_locale:')
        # print(dash_locale)
        # print('request_locale')
        # print(request_locale)

        # df = pd.Series(resultReference,index=dates)
        # df.insert(1,'Cheap', resultCheap)
        # df.insert(2,'Other', resultExp)


        

        # str_res_ref = "%.2f" % resultReference[len(resultReference)-1]
        # str_res_cheap =  "%.2f" % resultCheap[len(resultCheap)-1]
        # str_res_exp  =  "%.2f" %  resultExp[len(resultExp)-1]

        # print("{:n}".format(str_res_ref))

        str_res_ref ="{:n}".format(resultReference[len(resultReference)-1])
        str_res_cheap =  "{:n}".format(resultCheap[len(resultCheap)-1])
        str_res_exp  =  "{:n}".format(resultExp[len(resultExp)-1]
)



        resultReference = list(np.around(np.array(resultReference),0))
        resultCheap = list(np.around(np.array(resultCheap),0))
        resultExp = list(np.around(np.array(resultExp),0))

        df = pd.DataFrame(
                    {
                    'Dates' : dates,
                    'Reference': resultReference,
                    'Cheap': resultCheap,
                    'Other': resultExp                    
                    })

        # df.set_index('Dates', inplace=True)
        # df['Cheap'] = resultCheap
        # df['Other'] = resultExp
        pd.set_option('display.max_rows', None)  # or 1000
        # print(df)

     

 

        # Build graph
        layoutGraph = go.Layout(
            title="Performance Comparison",    
            plot_bgcolor="#FFFFFF",
            hovermode="x",
            hoverdistance=100, # Distance to show hover label of data point
            spikedistance=1000, # Distance to show spike
            xaxis=dict(
                title="time",
                linecolor="#BCCCDC",
                showspikes=True, # Show spike line for X-axis
                # Format spike
                
                spikethickness=2,
                spikedash="dot",
                spikecolor="#999999",
                spikemode="across",
            ),
            yaxis=dict(
                title="value",
                linecolor="#BCCCDC",
                tickformat=",r"
            )
        )




        fig = go.Figure(layout = layoutGraph)
        fig.add_trace(go.Scatter(x=dates, y=resultReference,
                    mode='lines',
                    name='Benchmark'))
        fig.add_trace(go.Scatter(x=dates, y=resultCheap,
                    mode='lines',
                    name='Fund #1'))
        fig.add_trace(go.Scatter(x=dates, y=resultExp,
                    mode='lines',
                    name='Fund #2'))

     

        # print(str_res_ref)

        # fig = px.line(df, x='Dates')
        return fig,dict(locale=dash_locale), str_res_ref,str_res_cheap,str_res_exp

    return app.server