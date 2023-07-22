from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import sqlite3
import time



#THIS SCRIPT IS USED TO SCRAPE THE ADVANCED STATS OF THE PLAYERS IN THE PLAYERS TABLE OF THE NBA_DEFENSIVE_TEAMS DATABASE

# connect to the SQLite database
conn = sqlite3.connect('nba_defensive_teams.db')
c = conn.cursor()

# Fetch player names and selection years from the database
c.execute("SELECT Name, Year_of_Selection FROM Players")
players = c.fetchall()

# set the location of the SafariDriver
driver = webdriver.Safari()

players = players[1:5]

for player in players:
    name, year = player
    driver.execute_script("window.location.href='https://www.basketball-reference.com/';")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, 'search')

    try:
        # Try to search using full name
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#modal-close'))).click()
        except TimeoutException:
            pass

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="search-item-name"]//a[contains(text(), "{name}")]'))).click()

    except NoSuchElementException:
        try:
            # If full name search fails, clear the search box
            search_box.clear()
            # Extract the last name and try to search using it
            last_name = name.split()[-1]
            search_box.send_keys(last_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)

            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#modal-close'))).click()
            except TimeoutException:
                pass

            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="search-item-name"]//strong/a[contains(text(), "{last_name}")]'))).click()

        except NoSuchElementException:
            # If search by last name also fails, update the 'Found' field to 0
            c.execute('''
                UPDATE Players 
                SET Found = 0 
                WHERE Name = ? AND Year_of_Selection = ?
            ''', (name, year))
            conn.commit()
            print(f"Player {name} not found.")
            continue  # Skip to the next iteration

    # Code here is executed if either the full name or the last name search was successful
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    advanced_table = soup.find('table', {'id': 'advanced'})
    searched_year = str(int(year) + 1)
    row = advanced_table.find('tr', {'id': f'advanced.{searched_year}'})

    # Extract the required stats and position
    position = row.find('td', {'data-stat': 'pos'}).text
    dbpm = row.find('td', {'data-stat': 'dbpm'}).text
    obpm = row.find('td', {'data-stat': 'obpm'}).text
    bpm = row.find('td', {'data-stat': 'bpm'}).text
    stl_pct = row.find('td', {'data-stat': 'stl_pct'}).text
    blk_pct = row.find('td', {'data-stat': 'blk_pct'}).text
    ows = row.find('td', {'data-stat': 'ows'}).text
    dws = row.find('td', {'data-stat': 'dws'}).text
    ws = row.find('td', {'data-stat': 'ws'}).text
    ws_per_48 = row.find('td', {'data-stat': 'ws_per_48'}).text

    c.execute('''
        UPDATE Players 
        SET Position = ?, Defensive_BPM = ?, Offensive_BPM = ?, BPM = ?, STL_PCT = ?, BLK_PCT = ?, OWS = ?, DWS = ?, WS = ?, WS_PER_48 = ?, Found = 1
        WHERE Name = ? AND Year_of_Selection = ?
    ''', (position, dbpm, obpm, bpm, stl_pct, blk_pct, ows, dws, ws, ws_per_48, name, year))  # use the original year here
    conn.commit()

driver.quit()
conn.close()
