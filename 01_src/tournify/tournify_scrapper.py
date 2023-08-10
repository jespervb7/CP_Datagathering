"""
[Script Name]: tournify_scrapper

[Description]
This script scrapes data from the tournify website. It's made to be for the Canoe Polo tournaments, but I suppose it could be used for other tournaments too.

[Usage]
1. You just need to provide an input URL. The script will output some CSV files with data.

[Author]: Jesper van Beemdelust

[Notes]
- [Any additional notes or information you want to include.]
"""

# Import necessary libraries

from bs4 import BeautifulSoup
import sys
import requests
import pandas as pd
import uuid

def get_url() -> str:
    """
    This function prompts the user to give us an link to scrape from tournify.
    There are checks in place to deal with invalid urls.

    Returns:
        str: returns the url to scrape the website with. 
    """    

    print("")
    user_url = input("Please provide us the link of the tournament you want to scrape. An example link is: https://www.tournify.de/live/eca-cup-essen \n")
    print("")
    
    if user_url[:20] != "https://www.tournify":
        print("The script received a invalid link")
        print("")
        print(f"The url you provided is: {user_url}")
        print("")
        user_url = input("Provide a proper link. An example link is: https://www.tournify.de/live/eca-cup-essen \n")
    else:
        return user_url
    
def get_html(base_url: str) -> str:
    """
    This functions handles the connection to the website and handles errors, if they occur.
    It's supposed to return the html or end the script.

    Args:
        base_url (str): The url to make a request to

    Returns:
        str: returns the html in text format. So that it can be parsed later.
    """    

    try:
        html_str = requests.get(base_url).text
        return html_str
    except requests.exceptions.RequestException as e:
        # Handles any network-related exceptions
        print(f"An error occurred while fetching the HTML: {e} from {base_url}")
        print("Check your network settings and try again")
        sys.exit(1)

def parse_html(base_url: str) -> BeautifulSoup:
    html_str = get_html(base_url)

    soup = BeautifulSoup(html_str, "html.parser")

    return soup

def get_tournament_data(soup_object: BeautifulSoup):
    pass

def main() -> None:
    """
    Main function to execute the script.
    """
    base_url = get_url()
    home_page_soup = parse_html(base_url)

if __name__ == "__main__":    
    main()