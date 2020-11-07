# Seattle_Locations

# Import libraries
import pandas as pd 
import numpy as np 
import folium
import requests
from pandas import json_normalize

# View max columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Foursquare credentials and version
CLIENT_ID = 'AKP4HK4G0IALGN3GBG2SMNXVERYF3KKXLAXAEONYSNY51AV2'       # Foursquare ID
CLIENT_SECRET = 'CBOOAI2WHBKNVLYGDY4YRSCLKQNCAEJ5PGAWTIDGII20XH55'   # Foursquare secret
VERSION = '20201027'
LIMIT = 1000

# Look for Italian food
search_query = 'coffee'
radius = 1000

# Create dataframe object
df_region = pd.read_csv('Seattle_lat_long.csv')
df_region['Number of Nearby Coffeeshops'] = np.nan

# Find the number of coffeeshops for each neighborhood 

for i in range(len(df_region['RegionName'])):
	latitude = df_region.iloc[i, 1]
	longitude = df_region.iloc[i, 2]

	# Make an API call to Foursquare for number of coffeeshops within 1000 meters
	url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
	results = requests.get(url).json()
	venues = results['response']['venues']
	df = json_normalize(venues)
	df_region.loc[i, 'Number of Nearby Coffeeshops'] = len(df.index)

# Create bubble plot of Seattle Neighborhoods and coffeeshops
seattle_coffee_map = folium.Map(location=[47.6094, -122.3195706], zoom_start = 11)
for lat, lng, name, coffee in zip(df_region['Latitude'], df_region['Longitude'], df_region['RegionName'], df_region['Number of Nearby Coffeeshops']):
	if coffee != 0:
		folium.CircleMarker(
			[lat, lng],
			radius = coffee/3,
			color = 'purple',
			popup = name + ' ' + str(round(coffee)),
			fill = True,
			fill_color = 'purple',
			fill_opacity = 0.4,
		).add_to(seattle_coffee_map)

# Add title
title_html = '''
			 <h3 align = 'center' style = 'font-size:15px'><b> Number of Coffeeshops in Seattle Neighborhoods </b></h3>
			 '''
seattle_coffee_map.get_root().html.add_child(folium.Element(title_html))

# Save coffee map
seattle_coffee_map.save('seattle_coffee_map.html')
