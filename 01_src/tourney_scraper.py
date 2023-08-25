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
 
from utils.get_web_data import get_html, parse_html
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_tournaments_metadata() -> list:

    tournaments_metadata = [["UUID", "Startdate", "Enddate"]]

    response = get_html(base_url)
    json_data = (response.json())



def main():

    # Grabbing the tournaments metadata. Links to their respective urls to start the webscrapping process
    get_tournaments_metadata()

if __name__ == "__main__":
    base_url = "https://www.tourney.nz/data/tournaments"
    main()