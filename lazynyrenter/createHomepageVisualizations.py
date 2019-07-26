import pandas as pd
from bokeh.io import show
from bokeh.models import ColumnDataSource, Range1d, LabelSet, HoverTool, NumeralTickFormatter
from bokeh.io import curdoc
from bokeh.themes import Theme
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Blues, Category20
from bokeh.transform import cumsum
import numpy as np
from jsmin import jsmin
from math import pi
from datetime import datetime, timedelta


# Create our plot theme
curdoc().theme = Theme(json={'attrs': {

    # apply defaults to Figure properties
    'Figure': {
        'toolbar_location': None,
        'outline_line_color': None,
        'min_border_right': 10,
        'sizing_mode': 'stretch_width'
    },

    'Grid': {
        'grid_line_color': None,
    },
    'Title': {
        'text_font_size': '14pt'
    },

    # apply defaults to Axis properties
    'Axis': {
        'minor_tick_out': None,
        'minor_tick_in': None,
        'axis_label_text_font_style': 'bold',
        'major_label_text_font_size': '11pt',
        'major_label_text_font_style': 'bold',
        'axis_label_text_font_size': '13pt',
        'axis_label_text_font': 'Work Sans'
    },
    # apply defaults to Legend properties
    'Legend': {
        'background_fill_alpha': 0.8,
    }}})

colorA = '#221131'
colorB = '#832424'
colorC = '#ec5b1d'
colorD = '#445c4b'
colorE = '#12a3a7'


def plotOverTime(df, aggregation='median', resample_freq='d'):

    # Remove outliers and resample
    df = removeOutliers(df, remove_price_nulls=True, remove_price_outliers=True)
    df['date'] = pd.to_datetime(df['datetime'], infer_datetime_format=True).dt.date
    df = df[df['date'] > (df['date'].max() - timedelta(days=7))]

    # Group
    df_grouped = df.groupby(['date', 'borough'])[['price']].median().reset_index()

    # Create the chart
    manhattanSource = ColumnDataSource(df_grouped[df_grouped['borough']=='Manhattan'])
    brooklynSource = ColumnDataSource(df_grouped[df_grouped['borough']=='Brooklyn'])
    bronxSource = ColumnDataSource(df_grouped[df_grouped['borough']=='Bronx'])
    queensSource = ColumnDataSource(df_grouped[df_grouped['borough']=='Queens'])
    statenIslandSource = ColumnDataSource(df_grouped[df_grouped['borough']=='Staten Island'])

    # Create the plot
    p = figure(x_axis_type='datetime', tools=[])
    p.line(x='date', y='price', line_width=2, color=colorA,
           source=manhattanSource, legend='Manhattan')
    p.line(x='date', y='price', line_width=2, color=colorB,
           source=brooklynSource, legend='Brooklyn')
    p.line(x='date', y='price', line_width=2, color=colorC,
           source=bronxSource, legend='Bronx')
    p.line(x='date', y='price', line_width=2, color=colorD,
           source=queensSource, legend='Queens')
    p.line(x='date', y='price', line_width=2, color=colorE,
           source=statenIslandSource, legend='Staten Island')

    # Style chart
    p.y_range = Range1d(0, df_grouped['price'].max()*1.1)
    p.yaxis.formatter=NumeralTickFormatter(format="0a")

    # Move legend
    p.legend.location = 'bottom_left'
    p.legend.border_line_color = None

    return returnFigure(p)


def listOfApartments(df, table_type):

    # Create a copy of the table and filter for the last 3 days
    df_table = removeOutliers(df, remove_price_outliers=True, remove_price_nulls=True)
    df_table['date'] = df_table['datetime'].dt.date
    maxDate = df_table['date'].max()

    df_table['date'] = pd.to_datetime(
        df_table['datetime'], infer_datetime_format=True).dt.date
    df_table = df_table[df_table['date'] > (maxDate-timedelta(days=3))]

    if table_type == 'cheapest':
        df_table = df_table.sort_values(by='price').head(
            5)[['date', 'url', 'price', 'name']]
    elif table_type == 'priciest':
        df_table = df_table.sort_values(by='price').tail(
            5)[['date', 'url', 'price', 'name']][::-1]

    # Create the list HTML
    ul = "<ul>"

    for i, row in df_table.iterrows():
        ul += "<li><a class='hvr-push' target='_blank' href='{}'>{}, ${} - {}</a></li>".format(
            row['url'], row['date'], row['price'], row['name'][0:30])

    ul += "</ul>"

    # Encode our list so we can use it in HTML
    ul = ul.encode('ascii', 'ignore')
    ul = ul.decode('ascii')

    return ul


def resamplePerDay(df, aggregation='mean', resample_freq='d'):
    df_per_day = df.copy()
    df_per_day.dropna(subset=['price'], inplace=True)
    df_per_day = df_per_day[df_per_day['price']
                            < np.percentile(df_per_day['price'], 99)]
    df_per_day['datetime'] = pd.to_datetime(
        df_per_day['datetime'], infer_datetime_format=True)

    if aggregation == 'mean':
        df_per_day = df_per_day[['datetime', 'price']].set_index(
            'datetime').resample(resample_freq).mean().reset_index()
    elif aggregation == 'count':
        df_per_day = df_per_day[['datetime', 'price']].set_index(
            'datetime').resample(resample_freq).count().reset_index()

    return df_per_day


def returnFigure(p):
    script, div = components(p)
    script = jsmin(script)

    return script, div


def removeOutliers(df, 
                    remove_area_outliers=False, 
                    remove_area_nulls=False,
                    remove_price_outliers=False,
                    remove_price_nulls=False, 
                    remove_bedroom_nulls=False):

    df_copy = df.copy()

    # Remove price nulls
    if remove_price_nulls:
        df_copy = df_copy[df_copy['price'].isnull()==False]

    # Remove price outliers
    if remove_price_outliers:
        df_copy = df_copy[(df_copy['price'] < np.percentile(df_copy['price'],99)) & (df_copy['price'] > np.percentile(df_copy['price'], 1))]

        df_copy = df_copy[df_copy['price'] != 0]

    # Remove rows without area
    if remove_area_nulls:
        df_copy = df_copy[df_copy['area'].isnull()==False]

    # Remove area outliers
    if remove_area_outliers:
        df_copy = df_copy[(df_copy['area'] < np.percentile(df_copy['area'],99)) & (df_copy['area'] > np.percentile(df_copy['area'], 1))]

    # Remove bedroom nulls
    if remove_bedroom_nulls:
        df_copy = df_copy[df_copy['bedrooms'].isnull()==False]


    return df_copy

if __name__ == '__main__':
    nyc = pd.read_csv('all_apartments_df.csv')
    plotOverTime(nyc, 'median', 'd')