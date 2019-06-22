import json
import requests
import boto3
from datetime import datetime
import os

def lambda_handler(event, context):
	
	# Get API Key
	api_key = os.environ.get("walkscore_key")
	
	# Parse event for needed data
	bucket = event['Records'][0]['s3']['bucket']['name']
	key = event['Records'][0]['s3']['object']['key']
	key = key.replace('%3A', ':').replace('+', ' ')
	
	# Read in the object
	s3 = boto3.resource('s3')
	content_object = s3.Object(bucket, key)
	file_content = content_object.get()['Body'].read().decode('utf-8')
	data = json.loads(file_content)
	
	# Enrich with the Walk Score data
	enhancedData = []
	for row in data:
		endpoint = ("""http://api.walkscore.com/score?format=json&address={}&lat={}&lon={}&key&transit=1&bike=1&wsapikey={}"""
						.format(row['address'],
								row['geotag'][0],
								row['geotag'][1],
								api_key))

		r = requests.get(endpoint)

		try:
			walkScoreData = json.loads(r.content)
		except json.JSONDecodeError:
			row['walkScore'] = None
			row['bikeScore'] = None
			row['transiteScore'] = None
			continue
			

		# If the scores exists grab them
		try:
			row['walkScore'] = walkScoreData['walkscore']
		except KeyError:
			row['walkScore'] = None

		try:
			row['transitScore'] = walkScoreData['transit']['score']
		except KeyError:
			row['transitScore'] = None

		try:
			row['bikeScore'] = walkScoreData['bike']['score']
		except:
			row['bikeScore'] = None
	
		enhancedData.append(row)

	# Convert to JSON
	data = json.dumps(enhancedData)
	
	# Get current timestamp for file name
	now = str(datetime.today())

	# Upload enriched data to S3
	client = boto3.client('s3')
	response = client.put_object(Bucket='lazyapartment', 
					Body=data, 
					Key='walkScoreEnhancedData/{}.json'.format(now))