# Seattle_Condo

# Import libraries
import pandas as pd
import folium

# View max columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load the json file of the countries
seattle_geo = 'Seattle_Neighborhoods.json'
seattle_geo_transit = 'Seattle_Neighborhoods_Transit.json'

# Download the walk scores
df_1bd = pd.read_csv('Neighborhood_ZHVI_1BD.csv')
df_1bd = df_1bd.loc[df_1bd['City'] == 'Seattle']
df_transit = pd.read_csv('Walk_Scores.csv')
df = pd.read_csv('Seattle_lat_long.csv')
df_1bd['5 year increase'] = 100 * (df_1bd['9/30/2020'] - df_1bd['9/30/2015']) / df_1bd['9/30/2015']
df_combined = pd.merge(df_1bd, df, how = 'inner', on = "RegionName")

# Initialize the maps
seattle_1Bd_map = folium.Map(location=[47.6264317, -122.3195706], zoom_start = 11)
seattle_walk_map = folium.Map(location=[47.6264317, -122.3195706], zoom_start = 11)
seattle_transit_map = folium.Map(location=[47.6264317, -122.3195706], zoom_start = 11)

# Add the color for the chloropleth maps
def create_map(geo_data, data, columns, fill_color, legend_name, map):
	folium.Choropleth(
		geo_data = geo_data,
		data = data,
		columns = columns,
		key_on = 'feature.properties.S_HOOD',
		fill_color = fill_color,
		fill_opacity = 0.7,
		line_opacity = 0.2,
		legend_name = legend_name
	).add_to(map)

	for lat, lng, name in zip(df['Latitude'], df['Longitude'], df['RegionName']):
		folium.CircleMarker(
			[lat, lng],
			radius = 2,
			color = 'blue',
			popup = name,
			fill = True,
			fill_color = 'blue',
			fill_opacity = 0.4,
		).add_to(map)

# Create 1-Bd, Walk Score, and Transit Score maps
create_map(seattle_geo, df_1bd, ['RegionName', '9/30/2020'], 'YlOrRd', '1-Bd Price ($)', seattle_1Bd_map)
create_map(seattle_geo_transit, df_transit, ['RegionName', 'Walk Score'], 'PuRd', 'Walk Score', seattle_walk_map)
create_map(seattle_geo_transit, df_transit, ['RegionName', 'Transit Score'], 'PuRd', 'Transit Score', seattle_transit_map)

# Create 5 year increase map
seattle_increase_map = folium.Map(location=[47.6094, -122.3195706], zoom_start = 11)
for lat, lng, name, increase in zip(df_combined['Latitude'], df_combined['Longitude'], df_combined['RegionName'], df_combined['5 year increase']):
	folium.CircleMarker(
		[lat, lng],
		radius = increase/7,
		color = 'purple',
		popup = name + ' ' + str((round(increase))) + '%',
		fill = True,
		fill_color = 'purple',
		fill_opacity = 0.4,
	).add_to(seattle_increase_map)

# Add title
title_html = '''
			 <h3 align = 'center' style = 'font-size:15px'><b> 1-Bed Property Increase in Seattle Neighborhoods from 2015 to 2020 </b></h3>
			 '''
seattle_increase_map.get_root().html.add_child(folium.Element(title_html))

# Display maps
seattle_1Bd_map.save('seattle_1Bd_map.html')
seattle_walk_map.save('seattle_walk_map.html')
seattle_transit_map.save('seattle_transit_map.html')
seattle_increase_map.save('seattle_increase_map.html')


