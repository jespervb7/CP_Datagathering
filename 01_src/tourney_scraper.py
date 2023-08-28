"""
[Script Name]
Tourney_scraper

[Description]
This webscraper automatically scrapes webpages from the tourney website. 
The website is for Canoe Polo matches and their scores. 

[Usage]
This should be an automated script. No input required.

[Author]
Jesper van Beemdelust

"""

# Import necessary libraries
 
from utils.get_web_data import get_html
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_tournaments_metadata() -> list:

    tournaments_metadata = [["UUID", "Startdate", "Enddate"]]

    response = get_html(base_url)
    json_data = (response.json())

    for tournament in json_data["tournaments"]:
        original_uuid = tournament['id']['value']

        try:
            start_date = tournament["startDate"]["value"]
        except TypeError:
            print("Something went wrong with grabbing the start date")
            start_date = None

        try:
            end_date = tournament["endDate"]["value"]
        except TypeError:
            print("Something went wrong with grabbing the end date")
            end_date = None
        
        data_to_append = [original_uuid, start_date, end_date]
        tournaments_metadata.append(data_to_append)
    return tournaments_metadata

def get_tournament_data(tournament_uuid: str) -> list:
    
    url_to_send_get = f"https://www.tourney.nz/data/tournament/{tournament_uuid}" 
        
    response = get_html(url_to_send_get)
    json_data = response.json

    for gameday in json_data["gameDates"]:
        gametimes = gameday["gameTimes"]

        for pitch in gameday["pitches"]:
            pass

def main():

    # Grabbing the tournaments metadata. Links to their respective urls to start the webscrapping process
    tournaments_metadata = get_tournaments_metadata()

    for tournament in tournaments_metadata:
        if isinstance(tournament[0], str):
            get_tournament_data(tournament[0])
        else:
            print("Invalid UUID")

if __name__ == "__main__":
    base_url = "https://www.tourney.nz/data/tournaments"
    main()