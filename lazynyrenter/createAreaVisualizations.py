import pandas as pd
from bokeh.io import show
from bokeh.models import ColumnDataSource, Range1d, LabelSet, HoverTool
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

colorA = '#3b5794'
colorB = '#5F5F5F'


def plotOverTime(df_area, df_all, grouping, aggregation, resample_freq='d', compare=False):

    # Resample per day
    df_area = removeOutliers(df_area, remove_price_outliers=True)
    df_all = removeOutliers(df_all, remove_price_outliers=True)
    df_per_day_area = resamplePerDay(df_area, aggregation, resample_freq)
    df_per_day_city = resamplePerDay(df_all, aggregation, resample_freq)

    # Create the plot
    sourceArea = ColumnDataSource(df_per_day_area)
    sourceCity = ColumnDataSource(df_per_day_city)
    p = figure(x_axis_type='datetime', tools=[])
    p.line(x='datetime', y='price', line_width=2, color=colorA,
           source=sourceArea, legend=df_area[grouping].iloc[0])

    if compare:
        p.line(x='datetime', y='price', line_width=2, line_dash='dotdash',
               color='#A9A9A9', source=sourceCity, legend='All of NYC')
        maxPrice = max(df_per_day_area['price'].max(),
                       df_per_day_city['price'].max())
    else:
        maxPrice = df_per_day_area['price'].max()

    # Style chart
    p.y_range = Range1d(0, maxPrice*1.2)
    # p.x_range = Range1d(df_per_day_city['datetime'].min(), df_per_day_city['datetime'].max())

    return returnFigure(p)


def priceHistogram(df, bins):

    # Remove outliers
    df = removeOutliers(df, remove_price_nulls=True, remove_price_outliers=True)

    hist, edges = np.histogram(df['price'],
                               bins=bins,
                               range=[df['price'].min(), df['price'].max()])

    # Put the information in a dataframe
    hist_df = pd.DataFrame({'count': hist,
                            'left': edges[:-1],
                            'right': edges[1:]})

    # Create the blank plot
    source = ColumnDataSource(hist_df)
    p = figure(y_axis_label='Number of Apartments',
               x_axis_label="Price ($)", tools=[])
    p.quad(bottom=0, top='count', left='left', right='right',
           fill_color=colorB, line_color='black', source=source)
    p.y_range = Range1d(0, hist_df['count'].max()*1.05)

    # Get variables for page
    mostCommonLowerBound = int(hist_df['left'].iloc[hist_df['count'].idxmax()])
    mostCommonUpperBound = int(
        hist_df['right'].iloc[hist_df['count'].idxmax()])

    # Add a hovertool
    tooltips = """
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Number Of Apartments: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@count{0,0}</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Price Range: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">$@left{0,0} to $@right{0,0}</h5>
    </div>
    """

    p.add_tools(HoverTool(tooltips=tooltips))

    # Show the plot
    script, div = components(p)
    script = jsmin(script)
    return script, div, mostCommonLowerBound, mostCommonUpperBound


def averagePriceByBedrooms(df):

    df.to_csv('delete.csv')

    # Group by bedrooms and remove price outliers
    df_bedrooms = df.copy()
    df_bedrooms = removeOutliers(df_bedrooms, remove_price_outliers=True, remove_price_nulls=True, remove_bedroom_nulls=True)
    bedroomCounts = df_bedrooms['bedrooms'].astype(
        int).value_counts() / len(df)
    bedroomCounts = bedroomCounts.to_dict()

    for key, value in bedroomCounts.items():
        bedroomCounts[key] = "{0:0.1%}".format(value)

    df_bedrooms = df_bedrooms[(df_bedrooms['bedrooms'].isnull() == False) & (
        df_bedrooms['price'] < np.percentile(df_bedrooms['price'], 99))]
    df_bedrooms['bedroom_string'] = df_bedrooms['bedrooms'].astype(
        int).astype(str) + ' Bedrooms'
    df_bedrooms['bedroom_string'] = df_bedrooms['bedroom_string'].str.replace(
        '0 Bedrooms', 'Studios')
    df_bedrooms = df_bedrooms.groupby('bedroom_string')[
        ['price']].mean().reset_index().sort_values(by='price')
    df_bedrooms['label'] = df_bedrooms['price'].apply(
        lambda x: '${:,}'.format(int(x)))

    # Create a column data source
    source = ColumnDataSource(df_bedrooms)

    # Create our figure
    p = figure(y_range=df_bedrooms['bedroom_string'].astype(str), tools=[])
    p.hbar(y='bedroom_string', right='price', height=.5,
           line_color='#000000', color=colorA, source=source)

    # Style our chart
    p.xaxis.visible = False
    p.yaxis.axis_line_color = None
    p.yaxis.major_tick_line_color = None
    p.x_range = Range1d(0, df_bedrooms['price'].max()*1.2)

    # Create Labelset
    labels = LabelSet(x='price', y='bedroom_string', text='label', level='glyph',
                      x_offset=5, y_offset=-10, source=source, text_font_size='10pt',
                      text_font_style='bold')
    p.add_layout(labels)

    script, div = components(p)
    script = jsmin(script)

    return script, div, bedroomCounts


def squareFootageHistogram(df, bins):

    df_has_area = df.copy()
    df_has_area = removeOutliers(df_has_area, remove_area_nulls=True, remove_area_outliers=True)

    # Create numpy histogram
    hist, edges = np.histogram(df_has_area['area'],
                               bins=bins,
                               range=[df_has_area['area'].min(), df_has_area['area'].max()])

    # Put the information in a dataframe
    hist_df = pd.DataFrame({'count': hist,
                            'left': edges[:-1],
                            'right': edges[1:]})

    # Create the blank plot
    source = ColumnDataSource(hist_df)
    p = figure(y_axis_label='Number of Apartments',
               x_axis_label="Square Footage", tools=[])
    p.quad(bottom=0, top='count', left='left', right='right',
           fill_color=colorB, line_color='black', source=source)
    p.y_range = Range1d(0, hist_df['count'].max()*1.05)

    # Get variables for page
    mostCommonLowerBound = int(hist_df['left'].iloc[hist_df['count'].idxmax()])
    mostCommonUpperBound = int(
        hist_df['right'].iloc[hist_df['count'].idxmax()])

    # Add a hovertool
    tooltips = """
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Number Of Apartments: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@count{0,0}</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Square Footage: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@left{0,0} to @right{0,0} SF</h5>
    </div>
    """

    p.add_tools(HoverTool(tooltips=tooltips))

    # Return the plot and page variables
    script, div = components(p)
    script = jsmin(script)
    return script, div, mostCommonLowerBound, mostCommonUpperBound


def bedroomsPie(df):

    # Get data in proper format
    data = df['bedrooms'].value_counts().reset_index(
        name='Count').rename(columns={'index': 'Number Of Bedrooms'})
    data['bedrooms_string'] = data['Number Of Bedrooms'].apply(
        lambda x: '{} Bedrooms'.format(int(x))).str.replace('0 Bedrooms', 'Studios')
    data['angle'] = data['Count']/data['Count'].sum() * 2*pi
    data['color'] = Blues[len(data['Number Of Bedrooms'].value_counts())]
    data = data.sort_values('bedrooms_string')

    # Create a figure
    source = ColumnDataSource(data)
    p = figure(x_range=(-0.5, 1.0), tools=[])
    p.wedge(x=0, y=1, radius=0.2,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="#000000", fill_color='color', legend='bedrooms_string', source=source)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # Add a hovertool
    tooltips = """
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Number Of Bedrooms: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@bedrooms_string</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Number Of Bedrooms: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@Count</h5>
    </div>

    """

    p.add_tools(HoverTool(tooltips=tooltips))

    labels = LabelSet(x=0, y=1, text='value',
                      angle=cumsum('angle', include_zero=True), source=source)

    # Show the plot
    script, div = components(p)
    script = jsmin(script)
    return script, div


def areaVersusPrice(df):

    # Create a copy amd remove useless data points]
    df_has_area = removeOutliers(df, remove_area_nulls=True, remove_area_outliers=True, remove_price_nulls=True, remove_price_outliers=True, remove_bedroom_nulls=True)

    df_has_area = df_has_area[['area', 'bedrooms', 'price']]

    # Rename to be user friendly
    df_has_area['bedrooms'] = df_has_area['bedrooms'].astype(
        int).astype(str) + " Bedrooms"
    df_has_area['bedrooms'] = df_has_area['bedrooms'].str.replace(
        '0 Bedrooms', 'Studios')

    # Create colors
    colorMappings = {'Studios': Category20[10][0],
                     '1 Bedrooms': Category20[10][1],
                     '2 Bedrooms': Category20[10][2],
                     '3 Bedrooms': Category20[10][3],
                     '4 Bedrooms': Category20[10][4],
                     '5 Bedrooms': Category20[10][5],
                     '6 Bedrooms': Category20[10][6],
                     '7 Bedrooms': Category20[10][7],
                     '8 Bedrooms': Category20[10][8]}

    df_has_area['color'] = df_has_area['bedrooms'].map(colorMappings)
    df_has_area = df_has_area.sort_values(by='bedrooms')

    # Create figure
    source = ColumnDataSource(df_has_area)
    p = figure(x_axis_label="Square Feet", y_axis_label="Price ($)", tools=[])
    p.scatter(x='area', y='price', color='color', size=15,
              line_color='#000000', alpha=.7, source=source, legend='bedrooms')
    p.y_range = Range1d(0, df_has_area['price'].max()*1.05)
    p.legend.location = 'bottom_right'
    p.legend.click_policy = "hide"

    # Add a hovertool
    tooltips = """
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Number Of Bedrooms: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@bedrooms</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Price: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@price{0,0}</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Square Footage: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@area{0,0}</h5>
    </div>

    """

    p.add_tools(HoverTool(tooltips=tooltips))


    # Show the plot
    return returnFigure(p)


def listOfApartments(df, table_type):

    # Create a copy of the table and filter for the last 30 days
    df_table = removeOutliers(df, remove_price_outliers=True, remove_price_nulls=True)
    today = datetime.today().date()
    df_table['date'] = pd.to_datetime(
        df_table['datetime'], infer_datetime_format=True).dt.date
    df_table = df_table[df_table['date'] > (today-timedelta(days=30))]

    if table_type == 'cheapest':
        df_table = removeOutliers(df_table, remove_price_outliers=True, remove_price_nulls=True)
        df_table = df_table.sort_values(by='price').head(
            5)[['date', 'url', 'price', 'name']]
    elif table_type == 'priciest':
        df_table = df_table.sort_values(by='price').tail(
            5)[['date', 'url', 'price', 'name']][::-1]
    elif table_type == 'recent':
        df_table = df_table.sort_values(by='date').tail(
            5)[['date', 'url', 'price', 'name']]

    # Create the list HTML
    ul = "<ul>"

    for i, row in df_table.iterrows():
        ul += "<li class='hvr-grow'><a target='_blank' href='{}'>{}, ${} - {}</a></li>".format(
            row['url'], row['date'], row['price'], row['name'][0:30])

    ul += "</ul>"

    # Encode our list so we can use it in HTML
    ul = ul.encode('ascii', 'ignore')
    ul = ul.decode('ascii')

    return ul


def areaPrices(df, area, grouping):

    # Group by area
    df_areas = df.copy()
    df_areas = (df_areas.groupby(grouping)[['price']]
                        .median().sort_values('price').reset_index().reset_index())

    # Get this area and the most expenisve area
    thisAreaRank = len(
        df_areas) - df_areas[df_areas[grouping] == area]['index'].values[0]
    thisAreaPrice = int(
        df_areas[df_areas[grouping] == area]['price'].iloc[0])
    mostExpensiveArea = df_areas[grouping].iloc[-1]
    mostExpensivePrice = int(df_areas['price'].iloc[-1])
    medianPrice = int(df['price'].median())
    numberOfAreas = len(df_areas)

    return {'thisAreaRank': thisAreaRank, 'thisAreaPrice': thisAreaPrice,
            'mostExpensiveArea': mostExpensiveArea, 'mostExpensivePrice': mostExpensivePrice,
            'medianPrice': medianPrice, 'numberOfAreas': numberOfAreas}


def averageSizeByBedrooms(df):

    bedroomMappings = {0.0: 'Studios',
                       1.0: '1 Bedroom',
                       2.0: '2 Bedroom',
                       3.0: '3 Bedroom',
                       4.0: '4 Bedroom',
                       5.0: '5 Bedroom',
                       6.0: '6 Bedroom',
                       7.0: '7 Bedroom',
                       8.0: '8 Bedroom'}

    # Filter for apartments that have area
    df_bedrooms = removeOutliers(df, remove_area_nulls=True, remove_area_outliers=True)
    df_bedrooms = df_bedrooms[df_bedrooms['area'].isnull() == False]
    df_bedrooms['bedrooms'] = df_bedrooms['bedrooms'].map(bedroomMappings)
    df_bedrooms = df_bedrooms.groupby(
        'bedrooms')[['area']].median().reset_index().sort_values('area')
    df_bedrooms['area'] = df_bedrooms['area'].astype(int)
    df_bedrooms['label'] = df_bedrooms['area'].apply(lambda x: str(x) + ' SF')

    # Create the figure
    source = ColumnDataSource(df_bedrooms)
    p = figure(y_range=df_bedrooms['bedrooms'],
               x_axis_label='Square Feet', tools=[])
    p.hbar(y='bedrooms', right='area', height=.5, source=source, color=colorA)
    p.x_range = Range1d(0, df_bedrooms['area'].max()*1.15)
    p.xaxis.visible = False
    p.yaxis.axis_line_color = None
    p.yaxis.major_tick_line_color = None

    # Add Hover
    tooltips = """
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Number Of Bedrooms: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@bedrooms</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Price: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@area{0,0}</h5>
    </div>
    """
    p.add_tools(HoverTool(tooltips=tooltips))

    # Add Labelset
    labels = LabelSet(x='area', y='bedrooms', x_offset=3, y_offset=-8,
                      text='label', text_font_style='bold', source=source)
    p.add_layout(labels)

    # Return the figure
    return returnFigure(p)


def easeOfGettingAround(df_all_nyc, area_of_interest, grouping):

    if grouping == 'postalCode':
        df_all_nyc['postalCode'] = df_all_nyc['postalCode'].apply(lambda x: '0' + str(x) if len(str(x)) == 4 else x)

    # Find average walk and transit score across all cities
    df_walkability = df_all_nyc.copy()
    df_walkability = (df_walkability.groupby(grouping)
                        [['walk_score', 'transit_score']]
                        .mean().sort_values('walk_score').reset_index())

    df_walkability = df_walkability.rename(columns={'{}'.format(grouping): 'area'})

    # Create rank columns
    df_walkability['walkScoreRank'] = df_walkability['walk_score'].rank(ascending=False)
    df_walkability['transitScoreRank'] = df_walkability['transit_score'].rank(method='min', ascending=False)

    # Create columns for chart aesthetics
    df_walkability['color'] = df_walkability['area'].apply(
        lambda x: colorA if x == area_of_interest else '#C0C0C0')
    df_walkability['size'] = df_walkability['area'].apply(
        lambda x: 35 if x == area_of_interest else 15)
    df_walkability['alpha'] = df_walkability['area'].apply(
        lambda x: 1 if x == area_of_interest else .65)

    # Get the ranks and values for hover and paragraph
    areaWalkScoreRank = int(df_walkability[df_walkability['area']==area_of_interest]['walkScoreRank'].iloc[0])
    areaWalkScore = round(
        df_walkability[df_walkability['area'] == area_of_interest]['walk_score'].iloc[0], 1)
    areaTransitScoreRank = int(df_walkability[df_walkability['area']==area_of_interest]['transitScoreRank'].iloc[0])
    areaTransitScore = round(
        df_walkability[df_walkability['area'] == area_of_interest]['transit_score'].iloc[0], 1)

    # Create figure
    source = ColumnDataSource(df_walkability)
    p = figure(x_axis_label='Walk Score (Out of 100)',
               y_axis_label='Transit Score (Out Of 100)')
    p.scatter(x='walk_score', y='transit_score', size='size', color='color',
              line_color='#000000', alpha='alpha', source=source)
    p.y_range, p.x_range = Range1d(75, 105), Range1d(75, 105)

    # Add Hover
    tooltips = """
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Area: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@area</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Walk Score: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@walkScore{0.0}</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Walk Score Rank: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@walkScoreRank</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Transit Score: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@transitScore{0.0}</h5>
    </div>
    <div class="tooltip-section">
        <h5 style="color:#3b5794; display:inline; font-size:1.2em">Transit Score Rank: </h5>
        <h5 style="color:#000000; font-size: 1.2em; display:inline;">@transitScoreRank</h5>
    </div>
    """

    p.add_tools(HoverTool(tooltips=tooltips))

    # Return figure
    script, div = components(p)
    script = jsmin(script)

    return script, div, areaWalkScore, areaWalkScoreRank, areaTransitScore, areaTransitScoreRank


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
    area = pd.read_csv('tester.csv')
    nyc = pd.read_csv('all_apartments.csv')

    areaVersusPrice(area)