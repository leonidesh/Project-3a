import requests
from datetime import datetime
from datetime import date
import pygal
import re

apikey = "36NQ38WWUFOJUP9W"

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


def makeGraph(data, chartType, chartTimeSeries, chartStartDate, chartEndDate,symbol):
    #ticker = data['Meta Data']['2. Symbol']

    opening = []
    highs = []
    lows = []
    closing = []
    dates = []

    labels = list(data)[1]
    dailyInformation = data[labels]
    for i in dailyInformation:
        date = str(i)
        # Only for TIME_SERIES_INTRADAY or the same day query
        if chartStartDate == chartEndDate:
            if chartTimeSeries == 'TIME_SERIES_INTRADAY':
                if str(chartStartDate) in date:
                    # split and append time in the list
                    timeonly = str(date).split(' ')[1]
                    dates.append(timeonly)
                    dataOpening = (dailyInformation[date]["1. open"])
                    opening.append(float(dataOpening))

                    dataHigh = (dailyInformation[date]["2. high"])
                    highs.append(float(dataHigh))

                    dataLow = (dailyInformation[date]["3. low"])
                    lows.append(float(dataLow))

                    dataClosing = (dailyInformation[date]["4. close"])
                    closing.append(float(dataClosing))

        else:
            # check the valid of date
            if chartStartDate < date < chartEndDate or chartEndDate in date:
                dates.append(date)

                dataOpening = (dailyInformation[date]["1. open"])
                opening.append(float(dataOpening))

                dataHigh = (dailyInformation[date]["2. high"])
                highs.append(float(dataHigh))

                dataLow = (dailyInformation[date]["3. low"])
                lows.append(float(dataLow))

                dataClosing = (dailyInformation[date]["4. close"])
                closing.append(float(dataClosing))

    chart = chartType
    #chart.title = 'Stock Data for {}: {} to {} '.format(ticker, chartStartDate, chartEndDate)
    chart.title = 'Stock Data for {}: {} to {}'.format(symbol, chartStartDate, chartEndDate)
    chart.x_labels = dates.reverse()
    chart.add('Opening', opening.reverse())
    chart.add('High', highs.reverse())
    chart.add('Low', lows.reverse())
    chart.add('Closing', closing.reverse())
    return chart.render()

def getData(symbol, time_series, chart_type, start_date, end_date):
    chartType = int(time_series)
    if chartType == 1: chartType = pygal.Bar(x_label_rotation=-45)
    elif chartType == 2: chartType = pygal.Line(x_label_rotation=-45)
    intraDayInfo = "&interval=60min"
    chartTimeSeries = chart_type
    if chartTimeSeries == "1": chartTimeSeries = "TIME_SERIES_INTRADAY"
    elif chartTimeSeries == "2": chartTimeSeries = "TIME_SERIES_DAILY"
    elif chartTimeSeries == "3": chartTimeSeries = "TIME_SERIES_WEEKLY"
    elif chartTimeSeries == "4": chartTimeSeries = "TIME_SERIES_MONTHLY"

    chartStartDate = str(start_date)
    chartEndDate = str(end_date)

    # connect website by their API
    baseLink = "https://www.alphavantage.co/query?"
    queryData = "function={}&symbol={}{}&apikey={}".format(chartTimeSeries, symbol, intraDayInfo, apikey)
    req = requests.get(baseLink + queryData)
    print(req.url)
    data = req.json()

    # Check API
    if 'Invalid API call' not in req.text:
        return makeGraph(data, chartType, chartTimeSeries, chartStartDate, chartEndDate,symbol)
    else:
        print("The Ticker You Entered is Not in The API\n")