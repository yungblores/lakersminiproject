import sqlite3
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import percentileofscore
import plotly.offline as pyo

# Connect to SQLite database
conn = sqlite3.connect('nba_defensive_teams.db')

# Query all data from the Players table into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM Players;", conn)

# Close the connection
conn.close()

# Define the stats you want to visualize
stat_cols = ['Defensive_BPM','BPM','STL_PCT', 'BLK_PCT', 'DWS', 'WS', 'WS_PER_48']
# Value to hold the sum of all percentile ranks
sum_percentiles = 0

# Loop over each stat column
for i, col in enumerate(stat_cols):
    # Convert the stat column to numeric, coerce errors (non-numeric values) to NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop NaN values from the stat column
    df_stat = df.dropna(subset=[col])

    # Calculate basic statistics
    Q1 = df_stat[col].quantile(0.25)
    Q3 = df_stat[col].quantile(0.75)
    IQR = Q3 - Q1

    # We'll consider any point outside of 1.5*IQR as an outlier
    outliers = df_stat[(df_stat[col] < (Q1 - 1.5 * IQR)) | (df_stat[col] > (Q3 + 1.5 * IQR))]

    # Create a box-and-whisker plot
    fig = go.Figure()

    # Box trace for the main data, change x to y for vertical box plot
    fig.add_trace(go.Box(y=df_stat[col], name=col))

    # Scatter trace for the outliers with hover text
    outliers_text = [f"Player: {row['Name']}<br>{col}: {row[col]}" for _, row in outliers.iterrows()]
    fig.add_trace(go.Scatter(
        x=[col]*len(outliers),
        y=outliers[col],
        mode='markers',
        marker=dict(color='red', size=5),
        name='Outliers',
        text=outliers_text,
        hoverinfo='text'
    ))

    # Add a point for 'Jarred Vanderbilt' with percentile rank
    player = df_stat[df_stat['Name'] == 'Jarred Vanderbilt Max']
    player_percentile = percentileofscore(df_stat[col], player[col].iloc[0])
    print(f"Percentile of 'Jarred Vanderbilt Max' in {col}: {player_percentile}")
    #Seperate tracker to print average percentile in console
    sum_percentiles += player_percentile
    average_percentile = sum_percentiles / len(stat_cols)
    print(f"\nAverage percentile of 'Jarred Vanderbilt Max' across all categories: {average_percentile}")
    
    fig.add_trace(go.Scatter(
        x=[col],
        y=player[col],
        mode='markers',
        marker=dict(
            color='gold', 
            size=9,
            line=dict(
                color='black', # Color of the border
                width=1 # Border width
            )
        ),
        name='Jarred Vanderbilt',
        text=[f"Player: {player['Name'].iloc[0]}<br>{col}: {player[col].iloc[0]}<br>Percentile: {player_percentile}"],
        hoverinfo='text'
    ))

    # Set plot title and axis labels
    fig.update_layout(
    autosize=True,
    title_text=f'Box-and-Whisker Plot of {col} with Jarred Vanderbilt Max-Stats',
    yaxis_title_text=f'{col} Scores',
    )


    # Save the figure to an HTML file
    pyo.plot(fig, filename=f'testmax{i+1}.html', auto_open=False, config={'responsive': True})

