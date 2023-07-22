import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go




# Connect to SQLite database
conn = sqlite3.connect('nba_defensive_teams.db')

# Query all data from the Players table into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM Players;", conn)

# Close the connection
conn.close()

# List of columns to visualize
columns_to_visualize = ['Defensive_BPM', 'Offensive_BPM', 'BPM', 'STL_PCT', 'BLK_PCT', 'DWS', 'WS', 'WS_PER_48']

# Create a subplot with as many box plots as there are columns to visualize
fig = go.Figure()

# Loop over the columns to visualize
for column in columns_to_visualize:

    # Convert the column to numeric, coerce errors (non-numeric values) to NaN
    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Drop NaN values from the column
    df = df.dropna(subset=[column])

    # Calculate basic statistics
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # We'll consider any point outside of 1.5*IQR as an outlier
    outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]

    # Box trace for the main data
    fig.add_trace(go.Box(y=df[column], name=column))

    # Scatter trace for the outliers with hover text
    outliers_text = [f"Player: {row['Name']}<br>{column}: {row[column]}" for _, row in outliers.iterrows()]
    fig.add_trace(go.Scatter(
        x=[column]*len(outliers),
        y=outliers[column],
        mode='markers',
        marker=dict(color='red', size=5),
        name=f'Outliers in {column}',
        text=outliers_text,
        hoverinfo='text'
    ))

# Set plot title and axis labels
fig.update_layout(
    title_text='Box-and-Whisker Plots',
    yaxis_title_text='Value',
    boxmode='group'  # group together boxes of the different traces for each value of x
)

fig.show()


