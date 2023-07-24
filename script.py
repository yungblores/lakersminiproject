import requests
from bs4 import BeautifulSoup
#Creating a SQL table
import sqlite3

def create_database():
    conn = sqlite3.connect('nba_defensive_teams.db')
    c = conn.cursor()
    
    # Drop the table if it already exists
    c.execute('DROP TABLE IF EXISTS Players;')

    c.execute('''
    CREATE TABLE Players(
    Name TEXT,
    Position TEXT,
    Year_of_Selection INTEGER,
    Team_Selection TEXT,
    Defensive_BPM REAL,
    Offensive_BPM REAL,
    BPM REAL,
    STL_PCT REAL,
    BLK_PCT REAL,
    OWS REAL,
    DWS REAL,
    WS REAL,
    WS_PER_48 REAL,
    Found BOOLEAN
    );
''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

create_database()




def get_defensive_teams_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('nba_defensive_teams.db')
    c = conn.cursor()
    
    # Get the page content
    url = 'https://www.nba.com/news/history-all-defensive-team'
    response = requests.get(url)
    
    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get the main article content
    article_content = soup.find('div', class_='ArticleContent_article__NBhQ8')

    # Find all h3 tags, which contain the year of selection
    years = article_content.find_all('h3')
    
    # Loop over each year
    for year in years:
        current_year = year.text.split("-")[0].strip()# Get the current year
        sibling = year.find_next_sibling()  # Get the next sibling of the year which contains the teams

        # Loop until we reach the next year
        while sibling and sibling.name != 'h3':
            if sibling.name == 'p' and ("First Team" in sibling.text or "Second Team" in sibling.text):
                # Get the team ("First Team" or "Second Team")
                team = "1st" if "First Team" in sibling.text else "2nd"

                # Get the list of players under the team
                sibling = sibling.find_next_sibling()

                # Extract the player names from the list
                while sibling and sibling.name == 'p' and "Team" not in sibling.text and "Official Release" not in sibling.text:
                    # Remove the '• ' from the player's name and append it to the list
                    player_name = sibling.text.strip()[2:].split(",")[0].strip()  # Get only the player's name, not the team name
                    if player_name == "O.G. Anunoby":
                        player_name = "OG Anunoby"
                    if player_name == "Robert Williams III":
                        player_name = "Robert Williams"
            
                    # Insert the data into the database
                    c.execute("INSERT INTO Players (Name, Year_of_Selection, Team_Selection) VALUES (?, ?, ?)",
                              (player_name, current_year, team))

                    sibling = sibling.find_next_sibling()

            else:
                sibling = sibling.find_next_sibling()

    # Save (commit) the changes
    conn.commit()
    
    # Close the connection
    conn.close()

get_defensive_teams_data()


data = get_defensive_teams_data()  # Get the scraped data


import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('nba_defensive_teams.db')

# Create a cursor object
c = conn.cursor()

# Fetch all records from the 'Players' table
c.execute("SELECT * FROM Players")

# Fetch all the rows
rows = c.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()






