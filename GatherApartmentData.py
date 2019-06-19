import pandas as pd
from craigslist import CraigslistHousing
import json
from pprint import pprint
import requests
import Config

class GatherApartmentData():

	cityMappings = {
					'New York City': {'site': 'newyork', 'area': {'Manhattan': 'mnh', 'Brooklyn': 'brk'}},
					'San Francisco': {'site': 'sfbay', 'area': {'San Francisco': 'sfc'}}
					}

	def __init__(self, city, area=None):
		self.city = city
		self.craigslistSite = self.cityMappings[self.city]['site']

		if area:
			self.area = area
			self.craigslistArea = self.cityMappings[self.city]['area'][self.area]
		else:
			self.craigslistArea = None


	def getApartmentData(self):

		# Connect to craigslist
		if self.craigslistArea:
			cl = CraigslistHousing(site=self.craigslistSite, 
									area=self.craigslistArea, 
									category='aap')
		else:
			cl = CraigslistHousing(site=self.craigslistSite, 
									area=self.craigslistArea, 
									category='aap')


		# Pull data from Craigslist
		results = cl.get_results(sort_by='newest', geotagged=True, limit=100)
		resultsList = [result for result in results]
		df = pd.DataFrame(resultsList)

		# Split latitude and longitude
		df['latitude'] = df['geotag'].apply(lambda x: x[0] if type(x)==tuple else None)
		df['longitude'] = df['geotag'].apply(lambda x: x[1] if type(x)==tuple else None)

		# Clean up money
		df['price'] = df['price'].str.replace('$', '').str.replace(',', '')

		# Enrich the data with Mapquest and Walkscore data
		df = enrichMapquestData(df)
		df = enrichWalkScore(df)

		# Remove duplicates
		df.drop_duplicates(keep='last', inplace=True)
		df.drop('geotag', axis=1, inplace=True)

		# Set index
		df = df.set_index('id')

		# Export the data
		df.to_csv('test.csv')

def enrichMapquestData(df):	

	# Define api key and endpoint
	credentials = Config.read_credentials()
	key = credentials['mapquest']['api_key']
	
	# Create dataframe with Mapquest data
	geotagList, postalCodesList, sideOfStreetList, distanceList, addressList = [], [], [], [], []

	# Create df that has geotags
	df_geotags = df.copy()
	df_geotags = df_geotags[df_geotags['geotag'].notnull()]

	for geotag in df_geotags['geotag'].unique():
		endpoint = """http://www.mapquestapi.com/geocoding/v1/reverse?key={}&location={},{}&includeRoadMetadata=true&includeNearestIntersection=true&outFormat=json""".format(key, geotag[0], geotag[1])
		r = requests.get(endpoint)
		data = json.loads(r.content)
		geotagList.append(geotag)
		postalCode = data['results'][0]['locations'][0]['postalCode']
		sideOfStreet = data['results'][0]['locations'][0]['sideOfStreet']
		distanceToNearestIntersection = data['results'][0]['locations'][0]['nearestIntersection']['distanceMeters']
		address = data['results'][0]['locations'][0]['street']

		postalCodesList.append(postalCode)
		sideOfStreetList.append(sideOfStreet)
		distanceList.append(distanceToNearestIntersection)
		addressList.append(address)

	dfMapquest = pd.DataFrame({'geotag': geotagList,
								'postcalCode': postalCodesList,
								'sideOfStreet': sideOfStreetList,
								'distanceToNearestIntersection': distanceList,
								'address': addressList})

	# Join original df with the new Mapquest data
	combined_df = pd.merge(df, dfMapquest, how='inner', on='geotag')

	return combined_df


def enrichWalkScore(df):	

	# Pull in the API key
	credentials = Config.read_credentials()
	key = credentials['walkscore']['api_key']
	
	# Create dataframe with Walkscore data
	geotagList, walkscoreList, bikeScoreList, transiteScoreList = [], [], [], []

	# Create df that has geotags
	df_geotags = df.copy()
	df_geotags = df_geotags[df_geotags['geotag'].notnull()]

	for i in range(len(df)):
		endpoint = ("""http://api.walkscore.com/score?format=json&address={}&lat={}&lon={}&key&transit=1&bike=1&wsapikey={}"""
						.format(df['address'].iloc[i],
								df['geotag'].iloc[i][0], 
								df['geotag'].iloc[i][1], 
								key))
		r = requests.get(endpoint)

		try:
			data = json.loads(r.content)
		except json.JSONDecodeError:
			walkscoreList.append(None) 
			bikeScoreList.append(None)
			transiteScoreList.append(None)
			continue
			
		geotagList.append(df['geotag'].iloc[i])

		# If the scores exists grab them
		try:
			walkScore = data['walkscore']
		except KeyError:
			walkScore = None

		try:
			transitScore = data['transit']['score']
		except KeyError:
			transitScore = None

		try:
			bikeScore = data['bike']['score']
		except:
			bikeScore = None

		walkscoreList.append(walkScore)
		transiteScoreList.append(transitScore)
		bikeScoreList.append(bikeScore)
		

	dfMapquest = pd.DataFrame({'geotag': geotagList,
								'walkScore': walkscoreList,
								'transitScore': transiteScoreList,
								'bikeScore': bikeScoreList})

	# Join original df with the new Walkscore data
	combined_df = pd.merge(df, dfMapquest, how='inner', on='geotag')

	return combined_df


if __name__ == '__main__':
	GatherApartmentData('New York City').getApartmentData()
	# endpoint = """http://api.walkscore.com/score?format=json&address=74 Broad Street&lat=40.704519&lon=-74.011599&transit=1&bike=1&wsapikey=ffd1c56f9abcf84872116b4cc2dfcf31"""
	# r = requests.get(endpoint)
	# data = json.loads(r.content)
	# pprint (data['walkscore'])
