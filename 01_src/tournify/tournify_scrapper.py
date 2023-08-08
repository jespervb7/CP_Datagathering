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

def main():
    """
    Main function to execute the script.
    """
    base_url = get_url()

if __name__ == "__main__":    
    main()