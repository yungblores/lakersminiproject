import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('nba_defensive_teams.db')

# Execute a query to get the list of tables
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Print all tables
for row in cursor:
    print(row)

# Close the connection
conn.close()
