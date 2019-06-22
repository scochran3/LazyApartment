from craigslist import CraigslistHousing
import json
import requests
import boto3
from datetime import datetime

def lambda_handler(event, context):
	# Connect to craigslist
	cl = CraigslistHousing(site='newyork', 
							area=None, 
							category='aap')

	# Pull data from Craigslist
	results = cl.get_results(sort_by='newest', geotagged=True, limit=20)
	resultsList = [result for result in results]
	
	# Convert data to json
	data = json.dumps(resultsList)

	# Get the current datetime for the file name
	now = str(datetime.today())
	
	# Export the data
	client = boto3.client('s3')
	response = client.put_object(Bucket='lazyapartment', 
					Body=data, 
					Key='rawdata/{}.json'.format(now))