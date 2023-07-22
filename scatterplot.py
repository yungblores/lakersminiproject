import plotly.express as px
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.offline as pyo


# Connect to SQLite database
conn = sqlite3.connect('nba_defensive_teams.db')

# Query the specific data from the Players table into a pandas DataFrame
df = pd.read_sql_query("SELECT WS, DWS FROM Players;", conn)
df['DWS'] = pd.to_numeric(df['DWS'], errors='coerce')
df['WS'] = pd.to_numeric(df['WS'], errors='coerce')

# Close the connection
conn.close()

# Calculate the correlation coefficient
corr_coef = df['DWS'].corr(df['WS'])

# Define the scatter plot
fig = px.scatter(df, x='DWS', y='WS', title=f'Correlation between DWS and WS (Correlation Coefficient: {corr_coef:.2f})')

# Display the figure
fig.show()

