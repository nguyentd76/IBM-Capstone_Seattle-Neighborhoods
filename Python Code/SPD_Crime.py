# SPD_Crime

# Import libraries
import pandas as pd
import numpy as np 
import folium
import matplotlib.pyplot as plt

# View max columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Download the walk scores
df_crime = pd.read_csv('SPD_Crime_Data.csv')
df_crime = df_crime.head(3580)
df_crime['Neighborhood'] = np.nan

# Update the neighborhood name to lowercase
def upperlower(input):
	return input[0:1].upper() + input[1:].lower()
for i in range(len(df_crime['Neighborhood'])):
	df_crime.loc[i, 'Neighborhood'] = upperlower(df_crime.loc[i, 'MCPP'])

# Turn column to datetime
df_crime['Offense Start DateTime'] = pd.to_datetime(df_crime['Offense Start DateTime'])

# Add a year column
df_crime['Year'] = np.nan
for i in range(len(df_crime['Year'])):
	if df_crime.loc[i, 'Offense Start DateTime'].year == 2020:
		df_crime.loc[i, 'Year'] = 2020

# Drop rows if there is no entry in Year column
df_crime.dropna(subset = ['Year'], inplace = True)

# Group by neighborhoods
df_neighbor = pd.DataFrame(df_crime.groupby('Neighborhood')['MCPP'].count())
df_neighbor.reset_index(inplace = True)
top_crime = df_neighbor.sort_values('MCPP', ascending = False)
top_crime = top_crime.head(10)

# Plot bar graph
plt.figure(figsize = (20, 10))
plt.bar(top_crime['Neighborhood'], top_crime['MCPP'])
plt.xlabel('Neighborhood')
plt.ylabel('Number of Crimes in 2020 (Jan to Oct)')
plt.title('Crime Rate in Seattle')
plt.show()
