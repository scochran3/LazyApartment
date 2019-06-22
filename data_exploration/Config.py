"""
This script reads credentials for the various databases. It reads info from the credentials.txt
file and returns the information required to connect to the database. The following credentials 
are needed for the automation:

	-Growth Data Store (GDS): This has the data for Growth TTV levers such as
	sessions, activations, etc.

	-Analytics: This has information for redirects, downstream conversions, and more
"""
from configparser import ConfigParser

def read_credentials(section=None):
	credentials_path = '../../credentials.txt'
	credentials = ConfigParser(interpolation=None)
	credentials.read(credentials_path)
	if section is None:
		return credentials
	return credentials[section]
