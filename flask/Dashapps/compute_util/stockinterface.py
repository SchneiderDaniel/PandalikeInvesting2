import yfinance as yf
import datetime as dt 
import  pandas  as pd 
import pandas_datareader.data as web
from flask import url_for, current_app
import os
import sys
import requests

def isTickerValid(ticker):
    try:
        df = web.DataReader(ticker, 'yahoo', dt.datetime(2020,1,1), dt.datetime.now())
        return True
    except:
        return False
    

def getNameToTicker(ticker):
    companyName = ""
    try:
        aTicker = yf.Ticker(ticker)
        companyName = aTicker.info['longName']
    except:
        try:
            url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(ticker)

            result = requests.get(url).json()

            for x in result['ResultSet']['Result']:
                if x['symbol'] == ticker:
                    companyName=  x['name']

        except:
            companyName = " Name NA (Data found) "
    return companyName

def getCurrencyToTicker(ticker):
    currency = 'NA'

    try:
        aTicker = yf.Ticker(ticker)
        currency = aTicker.info['currency']
    except:
        currency = 'NA'

    return currency


def getTickerDataframesList(tickers):
    dfList = []
    for p in tickers:
        dfToAdd = web.DataReader(p, 'yahoo', dt.datetime(1971,1,1),  dt.datetime.now()) 

        dfToAdd.drop(dfToAdd.columns.difference(['Adj Close']), 1, inplace=True)
    
     
        dfList.append(dfToAdd)
    return dfList

def getTickerDataframe(ticker):
    dfBench = web.DataReader(ticker, 'yahoo', dt.datetime(1971,1,1),  dt.datetime.now()) 
    dfBench.drop(dfBench.columns.difference(['Adj Close']), 1, inplace=True)
    return dfBench



def getPortfolioCorrelation_List(dfList,percents, dfBench, filterStart = dt.datetime(1971,1,1), filterEnd = dt.datetime.now(), daily=True):
  

    merge = dfList[0]
    for i in range (1,len(dfList)):
        merge  = pd.merge(merge,dfList[i], how='inner', left_index=True, right_index=True) 


    dfBench.columns = ['Benchmark']



    merge  = pd.merge(merge,dfBench, how='inner', left_index=True, right_index=True) 

    if not daily:
            # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
            merge=merge[~merge.index.strftime('%Y-%m').duplicated()].copy()

    mask = (merge.index > pd.to_datetime(filterStart)) & (merge.index <= pd.to_datetime(filterEnd))
    merge = merge.loc[mask]

    for i in range(len(dfList)+1):
        divisor= merge[merge.columns[i]].iloc[0]
        merge[merge.columns[i]] = merge[merge.columns[i]]/divisor

    for i in range(len(percents)):
        merge[merge.columns[i]] = (0.01*percents[i])*merge[merge.columns[i]]


    merge['Portfolio'] = merge.drop('Benchmark', axis=1).sum(axis=1)

    merge.drop(merge.columns.difference(['Portfolio', 'Benchmark']), 1, inplace=True)

    if not merge.empty:
        evaluatedFrom = merge.index[0].strftime('%d. %B %Y')
        evaluatedTo = merge.index[-1].strftime('%d. %B %Y')
    else:
        evaluatedFrom = filterStart.strftime('%d. %B %Y')
        evaluatedTo = filterEnd.strftime('%d. %B %Y')

    result = merge.corr().values
    result= result.round(4)

    return result[0][1], evaluatedFrom, evaluatedTo




def getPortfolioCorrelation(tickers,percents, ticker, filterStart = dt.datetime(1971,1,1), filterEnd = dt.datetime.now(), daily=True):
  
    dfList = []
    for p in tickers:
        dfToAdd = web.DataReader(p, 'yahoo', dt.datetime(1971,1,1),  dt.datetime.now()) 

        dfToAdd.drop(dfToAdd.columns.difference(['Adj Close']), 1, inplace=True)
    
     
        dfList.append(dfToAdd)

    merge = dfList[0]
    for i in range (1,len(dfList)):
        merge  = pd.merge(merge,dfList[i], how='inner', left_index=True, right_index=True) 

    dfBench =  web.DataReader(ticker, 'yahoo', dt.datetime(1971,1,1),  dt.datetime.now()) 


    dfBench.drop(dfBench.columns.difference(['Adj Close']), 1, inplace=True)

    dfBench.columns = ['Benchmark']



    merge  = pd.merge(merge,dfBench, how='inner', left_index=True, right_index=True) 

    if not daily:
            # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
            merge=merge[~merge.index.strftime('%Y-%m').duplicated()].copy()

    mask = (merge.index > pd.to_datetime(filterStart)) & (merge.index <= pd.to_datetime(filterEnd))
    merge = merge.loc[mask]

    for i in range(len(tickers)+1):
        divisor= merge[merge.columns[i]].iloc[0]
        merge[merge.columns[i]] = merge[merge.columns[i]]/divisor

    for i in range(len(percents)):
        merge[merge.columns[i]] = (0.01*percents[i])*merge[merge.columns[i]]


    merge['Portfolio'] = merge.drop('Benchmark', axis=1).sum(axis=1)

    merge.drop(merge.columns.difference(['Portfolio', 'Benchmark']), 1, inplace=True)

    if not merge.empty:
        evaluatedFrom = merge.index[0].strftime('%d. %B %Y')
        evaluatedTo = merge.index[-1].strftime('%d. %B %Y')
    else:
        evaluatedFrom = filterStart.strftime('%d. %B %Y')
        evaluatedTo = filterEnd.strftime('%d. %B %Y')

    result = merge.corr().values
    result= result.round(4)

    return result[0][1], evaluatedFrom, evaluatedTo


def getCorrelationMatrix_List(dfList, filterStart = dt.datetime(1971,1,1), filterEnd = dt.datetime.now(), daily=True  ):
    
    merge = dfList[0]
    for i in range (1,len(dfList)):
        merge = pd.merge(merge,dfList[i],how='inner', left_index=True, right_index=True)

    mask = (merge.index > pd.to_datetime(filterStart)) & (merge.index <= pd.to_datetime(filterEnd))

    merge = merge.loc[mask]

    if not daily:
        # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
        merge=merge[~merge.index.strftime('%Y-%m').duplicated()].copy()
    
    if not merge.empty:
        evaluatedFrom = merge.index[0].strftime('%d. %B %Y')
        evaluatedTo = merge.index[-1].strftime('%d. %B %Y')
    else:
        evaluatedFrom = filterStart.strftime('%d. %B %Y')
        evaluatedTo = filterEnd.strftime('%d. %B %Y')

    result = merge.corr().values
    result= result.round(4)

    return result, evaluatedFrom, evaluatedTo



def getCorrelationMatrix(tickers, filterStart = dt.datetime(1971,1,1), filterEnd = dt.datetime.now(), daily=True  ):
    
    dfList = []

    for tick in tickers:
        dfToAdd = web.DataReader(tick, 'yahoo', dt.datetime(1971,1,1),  dt.datetime.now()) 
        dfReduce= dfToAdd.drop(dfToAdd.columns.difference(['Adj Close']), 1)

        if not daily:
            # https://stackoverflow.com/questions/60590945/extract-first-day-of-month-in-dataframe
            dfReduce=dfReduce[~dfReduce.index.strftime('%Y-%m').duplicated()].copy()

        
        dfList.append(dfReduce)


    merge = dfList[0]
    for i in range (1,len(dfList)):
        merge = pd.merge(merge,dfList[i],how='inner', left_index=True, right_index=True)

    mask = (merge.index > pd.to_datetime(filterStart)) & (merge.index <= pd.to_datetime(filterEnd))

    merge = merge.loc[mask]

    
    if not merge.empty:
        evaluatedFrom = merge.index[0].strftime('%d. %B %Y')
        evaluatedTo = merge.index[-1].strftime('%d. %B %Y')
    else:
        evaluatedFrom = filterStart.strftime('%d. %B %Y')
        evaluatedTo = filterEnd.strftime('%d. %B %Y')

    result = merge.corr().values
    result= result.round(4)

    return result, evaluatedFrom, evaluatedTo
