import json
import boto3
import psycopg2
from psycopg2.extras import execute_values

def lambda_handler(event, context):
    
    # Get parameters for database
    ssm = boto3.client('ssm', 'us-east-1')
    user = ssm.get_parameter(Name='/apartments/db/user', WithDecryption=True)['Parameter']['Value']
    password = ssm.get_parameter(Name='/apartments/db/password', WithDecryption=True)['Parameter']['Value']
    host = ssm.get_parameter(Name='/apartments/db/host', WithDecryption=True)['Parameter']['Value']
    database = ssm.get_parameter(Name='/apartments/db/database', WithDecryption=True)['Parameter']['Value']
    
    # Connect
    connection = psycopg2.connect(user = "shawncochran",
                                    password = "710Dart$",
                                    host = "aa10uxjrfmskobd.cf8tqavognjx.us-east-1.rds.amazonaws.com",
                                    port = "5432",
                                    database = "ebdb")
    cursor = connection.cursor()
    
    # Parse event for needed data
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    key = key.replace('%3A', ':').replace('+', ' ')
    
    # Read in the object
    s3 = boto3.resource('s3')
    content_object = s3.Object(bucket, key)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_data = json.loads(file_content)


    # Neighborhood Map
    neighborhoodMaps = {'10453': 'Central Bronx',
                            '10457': 'Central Bronx',
                            '10460': 'Central Bronx',
                            '10458': 'Bronx Park and Fordham',
                            '10467': 'Bronx Park and Fordham',
                            '10468': 'Bronx Park and Fordham',
                            '10451': 'High Bridge and Morrisania',
                            '10452': 'High Bridge and Morrisania',
                            '10456': 'High Bridge and Morrisania',
                            '10454': 'Hunts Point and Mott Haven',
                            '10455': 'Hunts Point and Mott Haven',
                            '10459': 'Hunts Point and Mott Haven',
                            '10474': 'Hunts Point and Mott Haven',
                            '10463': 'Kingsbridge and Riverdale',
                            '10471': 'Kingsbridge and Riverdale',
                            '10466': 'Northeast Bronx',
                            '10469': 'Northeast Bronx',
                            '10470': 'Northeast Bronx',
                            '10475': 'Northeast Bronx',
                            '10461': 'Southeast Bronx',
                            '10462': 'Southeast Bronx',
                            '10464': 'Southeast Bronx',
                            '10465': 'Southeast Bronx',
                            '10472': 'Southeast Bronx',
                            '10473': 'Southeast Bronx',
                            '11212': 'Central Brooklyn',
                            '11213': 'Central Brooklyn',
                            '11216': 'Central Brooklyn',
                            '11233': 'Central Brooklyn',
                            '11238': 'Central Brooklyn',
                            '11209': 'Southwest Brooklyn',
                            '11214': 'Southwest Brooklyn',
                            '11228': 'Southwest Brooklyn',
                            '11204': 'Borough Park',
                            '11218': 'Borough Park',
                            '11219': 'Borough Park',
                            '11230': 'Borough Park',
                            '11234': 'Canarsie and Flatlands',
                            '11236': 'Canarsie and Flatlands',
                            '11239': 'Canarsie and Flatlands',
                            '11223': 'Southern Brooklyn',
                            '11224': 'Southern Brooklyn',
                            '11229': 'Southern Brooklyn',
                            '11235': 'Southern Brooklyn',
                            '11201': 'Northwest Brooklyn',
                            '11205': 'Northwest Brooklyn',
                            '11215': 'Northwest Brooklyn',
                            '11217': 'Northwest Brooklyn',
                            '11231': 'Northwest Brooklyn',
                            '11203': 'Flatbush',
                            '11210': 'Flatbush',
                            '11225': 'Flatbush',
                            '11226': 'Flatbush',
                            '11207': 'East New York and New Lots',
                            '11208': 'East New York and New Lots',
                            '11211': 'Greenpoint',
                            '11222': 'Greenpoint',
                            '11220': 'Sunset Park',
                            '11232': 'Sunset Park',
                            '11206': 'Bushwick and Williamsburg',
                            '11221': 'Bushwick and Williamsburg',
                            '11237': 'Bushwick and Williamsburg',
                            '10026': 'Central Harlem',
                            '10027': 'Central Harlem',
                            '10030': 'Central Harlem',
                            '10037': 'Central Harlem',
                            '10039': 'Central Harlem',
                            '10001': 'Chelsea and Clinton',
                            '10011': 'Chelsea and Clinton',
                            '10018': 'Chelsea and Clinton',
                            '10019': 'Chelsea and Clinton',
                            '10020': 'Chelsea and Clinton',
                            '10036': 'Chelsea and Clinton',
                            '10029': 'East Harlem',
                            '10035': 'East Harlem',
                            '10010': 'Gramercy Park and Murray Hill',
                            '10016': 'Gramercy Park and Murray Hill',
                            '10017': 'Gramercy Park and Murray Hill',
                            '10022': 'Gramercy Park and Murray Hill',
                            '10012': 'Greenwich Village and Soho',
                            '10013': 'Greenwich Village and Soho',
                            '10014': 'Greenwich Village and Soho',
                            '10004': 'Lower Manhattan',
                            '10005': 'Lower Manhattan',
                            '10006': 'Lower Manhattan',
                            '10007': 'Lower Manhattan',
                            '10038': 'Lower Manhattan',
                            '10280': 'Lower Manhattan',
                            '10002': 'Lower East Side',
                            '10003': 'Lower East Side',
                            '10009': 'Lower East Side',
                            '10021': 'Upper East Side',
                            '10028': 'Upper East Side',
                            '10044': 'Upper East Side',
                            '10065': 'Upper East Side',
                            '10075': 'Upper East Side',
                            '10128': 'Upper East Side',
                            '10023': 'Upper West Side',
                            '10024': 'Upper West Side',
                            '10025': 'Upper West Side',
                            '10031': 'Inwood and Washington Heights',
                            '10032': 'Inwood and Washington Heights',
                            '10033': 'Inwood and Washington Heights',
                            '10034': 'Inwood and Washington Heights',
                            '10040': 'Inwood and Washington Heights',
                            '11361': 'Northeast Queens',
                            '11362': 'Northeast Queens',
                            '11363': 'Northeast Queens',
                            '11364': 'Northeast Queens',
                            '11354': 'North Queens',
                            '11355': 'North Queens',
                            '11356': 'North Queens',
                            '11357': 'North Queens',
                            '11358': 'North Queens',
                            '11359': 'North Queens',
                            '11360': 'North Queens',
                            '11365': 'Central Queens',
                            '11366': 'Central Queens',
                            '11367': 'Central Queens',
                            '11412': 'Jamaica',
                            '11423': 'Jamaica',
                            '11432': 'Jamaica',
                            '11433': 'Jamaica',
                            '11434': 'Jamaica',
                            '11435': 'Jamaica',
                            '11436': 'Jamaica',
                            '11101': 'Northwest Queens',
                            '11102': 'Northwest Queens',
                            '11103': 'Northwest Queens',
                            '11104': 'Northwest Queens',
                            '11105': 'Northwest Queens',
                            '11106': 'Northwest Queens',
                            '11374': 'West Central Queens',
                            '11375': 'West Central Queens',
                            '11379': 'West Central Queens',
                            '11385': 'West Central Queens',
                            '11691': 'Rockaways',
                            '11692': 'Rockaways',
                            '11693': 'Rockaways',
                            '11694': 'Rockaways',
                            '11695': 'Rockaways',
                            '11697': 'Rockaways',
                            '11004': 'Southeast Queens',
                            '11005': 'Southeast Queens',
                            '11411': 'Southeast Queens',
                            '11413': 'Southeast Queens',
                            '11422': 'Southeast Queens',
                            '11426': 'Southeast Queens',
                            '11427': 'Southeast Queens',
                            '11428': 'Southeast Queens',
                            '11429': 'Southeast Queens',
                            '11414': 'Southwest Queens',
                            '11415': 'Southwest Queens',
                            '11416': 'Southwest Queens',
                            '11417': 'Southwest Queens',
                            '11418': 'Southwest Queens',
                            '11419': 'Southwest Queens',
                            '11420': 'Southwest Queens',
                            '11421': 'Southwest Queens',
                            '11368': 'West Queens',
                            '11369': 'West Queens',
                            '11370': 'West Queens',
                            '11372': 'West Queens',
                            '11373': 'West Queens',
                            '11377': 'West Queens',
                            '11378': 'West Queens',
                            '10302': 'Port Richmond',
                            '10303': 'Port Richmond',
                            '10310': 'Port Richmond',
                            '10306': 'South Shore',
                            '10307': 'South Shore',
                            '10308': 'South Shore',
                            '10309': 'South Shore',
                            '10312': 'South Shore',
                            '10301': 'Stapleton and St. George',
                            '10304': 'Stapleton and St. George',
                            '10305': 'Stapleton and St. George',
                            '10314': 'Mid-Island'
                        }


    # Borough Maps
    boroughMaps = {'Central Bronx': 'Bronx', 
                'Bronx Park and Fordham': 'Bronx', 
                'High Bridge and Morrisania': 'Bronx', 
                'Hunts Point and Mott Haven': 'Bronx', 
                'Kingsbridge and Riverdale': 'Bronx', 
                'Northeast Bronx': 'Bronx',
                'Southeast Bronx': 'Bronx',
                'Central Brooklyn': 'Brooklyn',
                'Southwest Brooklyn': 'Brooklyn', 
                'Borough Park': 'Brooklyn', 
                'Canarsie and Flatlands': 'Brooklyn', 
                'Southern Brooklyn': 'Brooklyn', 
                'Northwest Brooklyn': 'Brooklyn', 
                'Flatbush': 'Brooklyn',
                'East New York and New Lots': 'Brooklyn', 
                'Greenpoint': 'Brooklyn', 
                'Sunset Park': 'Brooklyn', 
                'Bushwick and Williamsburg': 'Brooklyn',
                'Central Harlem': 'Manhattan', 
                'Chelsea and Clinton': 'Manhattan', 
                'East Harlem': 'Manhattan', 
                'Gramercy Park and Murray Hill': 'Manhattan',
                'Greenwich Village and Soho': 'Manhattan', 
                'Lower Manhattan': 'Manhattan', 
                'Lower East Side': 'Manhattan', 
                'Upper East Side': 'Manhattan',
                'Upper West Side': 'Manhattan', 
                'Inwood and Washington Heights': 'Manhattan',
                'Northeast Queens': 'Queens', 
                'North Queens': 'Queens', 
                'Central Queens': 'Queens', 
                'Jamaica': 'Queens', 
                'Northwest Queens': 'Queens',
                'West Central Queens': 'Queens', 
                'Rockaways': 'Queens', 
                'Southeast Queens': 'Queens', 
                'Southwest Queens': 'Queens', 
                'West Queens': 'Queens',
                'Port Richmond': 'Staten Island', 
                'South Shore': 'Staten Island', 
                'Stapleton and St. George': 'Staten Island', 
                'Mid-Island': 'Staten Island',
                'No Neighborhood Found': 'None',
                'Kearney': 'None',
                'Stamford': 'None'
            }

    # Check data in database
    sqlCurrentDataInDB = "SELECT DISTINCT name, address FROM website_apartment;"
    cursor.execute(sqlCurrentDataInDB)
    currentDataInDB = cursor.fetchall()

    rowsToInsert = []
    for i, row in enumerate(json_data):
        address = row['address']
        area = row['area']

        if type(area) == str:
            area = area.replace('ft2', '')

        bedrooms = row['bedrooms']
        bikeScore = row['bikeScore']
        transitScore = row['transitScore']
        walkScore = row['walkScore']
        datetime = row['datetime']
        distanceToNearestIntersection = row['distanceToNearestIntersection']
        hasImage = row['has_image']
        hasMap = row['has_map']
        name = row['name']
        price = row['price']

        if type(price) == str:
            price = price.replace('$', '')

        sideOfStreet = row['sideOfStreet']
        url = row['url']
        longitude = row['geotag'][0]
        latitude = row['geotag'][1]
        
        # Check for area
        if row['area']:
            includesArea = True
        else:
            includesArea = False
        
        # Check for no fee
        if 'no fee' in row['name'].lower():
            advertisesNoFee = True
        else:
            advertisesNoFee = False
        
        # Check if repost
        if row['repost_of']:
            is_repost = True
        else:
            is_repost = False

        postalCode = row['postalCode'][0:5]

        try:
            neighborhood = neighborhoodMaps[postalCode]
        except KeyError:
            neighborhood = 'No Neighborhood Found'
        borough = boroughMaps[neighborhood]

        thisRow = (address, area, bedrooms, bikeScore, transitScore, walkScore, datetime, distanceToNearestIntersection, hasImage, hasMap, name, price, sideOfStreet, url, longitude, latitude, includesArea, advertisesNoFee, is_repost, postalCode, neighborhood, borough)
        
        rowAlreadyInDatabase = False

        # Check data in this file
        if i > 0:
            for row in rowsToInsert:
                if thisRow[10] == row[10] and thisRow[0] == row[0]:
                    rowAlreadyInDatabase = True

        if (thisRow[10], thisRow[0]) in currentDataInDB:
            rowAlreadyInDatabase = True

        if not rowAlreadyInDatabase:
            rowsToInsert.append(thisRow)



    insert_query = 'INSERT INTO website_apartment (address, area, bedrooms, bike_score, transit_score, walk_score, datetime, distance_to_nearest_intersection, has_image, has_map, name, price, side_of_street, url, longitude, latitude, includes_area, advertises_no_fee, is_repost, postal_code, Neighborhood, borough) values %s'

    execute_values(cursor, insert_query, rowsToInsert, template=None)

    connection.commit()

    return None