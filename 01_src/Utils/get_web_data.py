import requests
from bs4 import BeautifulSoup

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