# Seattle Correlation

# Import libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# View max columns and rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Download the walk scores
df_1bd = pd.read_csv('Neighborhood_ZHVI_1BD.csv')
df_1bd = df_1bd.loc[df_1bd['City'] == 'Seattle']
df_transit = pd.read_csv('Walk_Scores.csv')
df_location = pd.merge(df_1bd, df_transit, how = 'inner', on = "RegionName")
df_location['Property Price'] = df_location['9/30/2020'] / 1000

# Create scatterplots with linear regression
def create_scatter(xlabel):
	# Create plots
	plt.figure(figsize = (8, 5))
	plt.scatter(x = df_location[xlabel], y = df_location['Property Price'])
	plt.xlabel(xlabel)
	plt.ylabel('1-Bedroom Property Price ($1K)')
	plt.title('Relationship between ' + xlabel + ' and Property Price in Seattle Neighborhoods')

	# Create linear regression models
	x = df_location[xlabel].values.reshape(-1, 1)
	y = df_location['Property Price'].values.reshape(-1, 1)
	linear_regressor = LinearRegression()
	linear_regressor.fit(x, y)
	y_pred = linear_regressor.predict(x)
	plt.plot(x, y_pred)

	# Print correlation scores
	corr_score = r2_score(y, y_pred)
	print('The R2 score for', xlabel, ':', round(corr_score, 5))

create_scatter('Walk Score')
create_scatter('Transit Score')
create_scatter('Bike Score')
plt.show()

