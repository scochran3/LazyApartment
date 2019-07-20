import os, sys
import django
import pandas as pd
import warnings
from django.db import IntegrityError
warnings.filterwarnings("ignore")

# Connect to Django
sys.path.append('../..') # add path to project root dir
os.environ["DJANGO_SETTINGS_MODULE"] = "lazynyrenter.settings"
django.setup()

# Import model
from website.models import Apartment

# Read in data
df = pd.read_csv('data/housing_cleaned_deduped.csv')

# Replace nan with None for database
df = df.where((pd.notnull(df)), None)

df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
# Borough Mapping
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
				'Canarsie and Flatlands': 
				'Brooklyn', 
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

for row_num, row in df.iterrows():

	try:
		Apartment.objects.create(
			address = row['address'],
			area = row['area'],
			bedrooms = row['bedrooms'],
			bikeScore = row['bikeScore'],
			transitScore = row['transitScore'],
			walkScore = row['walkScore'],
			datetime = row['datetime'],
			distanceToNearestIntersection = row['distanceToNearestIntersection'],
			hasImage = row['has_image'],
			hasMap = row['has_map'],
			name = row['name'], 
			price = row['price'],
			sideOfStreet = row['sideOfStreet'],
			url = row['url'],
			longitude = row['lon'],
			latitude = row['lat'],
			includesArea = row['includes_area'],
			advertisesNoFee = row['advertises_no_fee'],
			isRepost = row['is_repost'],
			postalCode = row['postalCode'][0:5],
			neighborhood = row['neighborhood'],
			borough=boroughMaps[row['neighborhood']])
			
	except TypeError:
		continue
	except IntegrityError:
		continue