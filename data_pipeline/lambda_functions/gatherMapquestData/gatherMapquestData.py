import json
import requests
import boto3
from datetime import datetime
import os

def lambda_handler(event, context):
	
	# API Key
	api_key = os.environ.get("mapquest_key")
	
	# Parse event for needed data
	bucket = event['Records'][0]['s3']['bucket']['name']
	key = event['Records'][0]['s3']['object']['key']
	key = key.replace('%3A', ':').replace('+', ' ')
	
	# Read in the object
	s3 = boto3.resource('s3')
	content_object = s3.Object(bucket, key)
	file_content = content_object.get()['Body'].read().decode('utf-8')
	data = json.loads(file_content)
	
	# Enrich with Mapquest Data
	enhancedData = []
	for row in data:
		lat = row['geotag'][0]
		lon = row['geotag'][1]
		endpoint = "http://www.mapquestapi.com/geocoding/v1/reverse?key={}&location={},{}&includeRoadMetadata=true&includeNearestIntersection=true&outFormat=json".format(api_key, lat, lon)
		r = requests.get(endpoint)
		mapquestData = json.loads(r.content)
		row['postalCode'] = mapquestData['results'][0]['locations'][0]['postalCode']
		row['sideOfStreet'] = mapquestData['results'][0]['locations'][0]['sideOfStreet']
		try:
			row['distanceToNearestIntersection'] = mapquestData['results'][0]['locations'][0]['nearestIntersection']['distanceMeters']
		except TypeError:
			row['distanceToNearestIntersection'] = None
			
		row['address'] = mapquestData['results'][0]['locations'][0]['street']
		enhancedData.append(row)

	# Convert to JSON
	data = json.dumps(enhancedData)
	
	# Get current timestamp for file name
	now = str(datetime.today())

	# Upload enriched data to S3
	client = boto3.client('s3')
	response = client.put_object(Bucket='lazyapartment', 
					Body=data, 
					Key='mapquestEnhancedData/{}.json'.format(now))
