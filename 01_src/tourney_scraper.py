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
from utils.google_api import Create_Service, write_to_sheet, read_from_sheet
import datetime
import json
import pandas as pd
import uuid

def get_tournaments_metadata() -> list:

    """This function grabs the tournament metadata and returns it in a list.
    The UUID's from each tournament are reused in the function: get_match_data. The uuid is concatinated to the url

    Returns:
        list: of tournament metadata, such as the start and enddate, but also the UUID.
    """

    tournaments_metadata = []

    response = get_html(base_url)
    json_data = (response.json())

    for tournament in json_data["tournaments"]:
        original_uuid = tournament['id']['value']
        tournament_name = tournament["name"]
        tournament_id = str(uuid.uuid4())
        time_created = str(datetime.datetime.now())

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
        
        data_to_append = [
            original_uuid, 
            start_date, 
            end_date, 
            tournament_name,
            tournament_id,
            time_created,
            1
            ]
        tournaments_metadata.append(data_to_append)

    return tournaments_metadata

def get_match_data(url: str, tournament_id: str, tournament_raw_id) -> list:

    """This function gets the data from each tournament and returns the data as a list

    Returns:
        list: Data of the tournament such as matches, teams played
    """
    
    match_data_to_return = []
    game_event_data_to_return = []

    print(url)
    response = get_html(url)
    json_data = (response.json())
    
    #TODO: The code, the for loops, below is slightly ugly, but I couldn't come up with a quick neater solution. Too many nested loops which makes it hard to read.

    # Data is separeted by day
    for gameday in json_data["gameDates"]:

        # If gametimes is empty. Skip that tournament.
        if len(gameday["gameTimes"]) == 0:
            continue

        gameday_date = gameday["date"]["value"]
        gametimes = gameday["gameTimes"]
        gameday_id = gameday["id"]["value"]

        # A game day can have multiple pitches.
        for pitch in gameday["pitches"]:
            pitch_number = pitch["name"]
            pitch_id = pitch["id"]["value"]

            # Counter for the matches played on a pitch. Start with 0 as it's used for slicing the gametimes and adding the gametime to the right match
            match_counter = 0

            # For each match on pitch. Save the match data.
            for match in pitch["games"]:
                match_uuid = str(uuid.uuid4())
                try:
                    match_time_of_day = gametimes[match_counter]
                except IndexError:
                    match_time_of_day = "Unknown"
                match_id = match["id"]["value"]
                poule = match["group"]
                team1 = match["team1"]
                team1_original = match["team1Original"]
                team1_score = match["team1Score"]
                team1_defaulted = match["team1Defaulted"]
                team2 = match["team2"]
                team2_original = match["team2Original"]
                team2_score = match["team2Score"]
                team2_defaulted = match["team2Defaulted"]
                dutyteam = match["dutyTeam"]
                dutyteamoriginal = match["dutyTeamOriginal"]
                gamestatus = match["status"]
                current_datetime = str(datetime.datetime.now())

                data_to_append = [
                    match_uuid,
                    None,
                    poule,
                    gameday_date,
                    None,
                    match_time_of_day,
                    pitch_number,
                    team1,
                    team2,
                    team1_score,
                    team2_score,
                    tournament_id,
                    None,
                    None,
                    dutyteam,
                    None,
                    current_datetime,
                    None,
                    None,
                    team1_original,
                    team2_original,
                    team1_defaulted,
                    team2_defaulted,
                    dutyteamoriginal,
                    gamestatus,
                    match_id
                ]
                
                match_data_to_return.append(data_to_append)

                game_event_data = get_match_events_data(tournament_raw_id, gameday_id, pitch_id, match_id, match_uuid)
                game_event_data_to_return.append(game_event_data)

                match_counter += 1

    return match_data_to_return, game_event_data_to_return

def get_match_events_data(tournament_id, date_id, pitch_id, match_id, match_uuid) -> list:

    url = f"https://www.tourney.nz/data/tournament/{tournament_id}/date/{date_id}/pitch/{pitch_id}/game/{match_id}"
    
    response = get_html(url)
    json_data = (response.json())
    game_data = json_data["eventLog"]

    data_to_return = []

    for event in game_data:
        raw_game_id = event["id"]["value"]
        game_uuid = str(uuid.uuid4())
        game_time = event["time"]
        type_of_event = event["eventType"]
        what_team_did_event = event["team"]
        player = event["player"]
        notes = event["notes"]
        time_created = str(datetime.datetime.now())

        event_data = [
            raw_game_id,
            game_uuid,
            match_uuid,
            game_time,
            type_of_event,
            what_team_did_event,
            player,
            notes,
            time_created
        ]
        
        data_to_return.append(event_data)

    return data_to_return

def main():
    
    # Launch the google API
    service = Create_Service()

    # Get the already scrapped webpages, to see if the ID exists
    scrapper_data = read_from_sheet('Scrappers', service)
    scrapper_links = []

    # Get all scraped links into a list so we can easily check if the link has being scraped
    for scrapped_link in scrapper_data:
        scrapper_links.append(scrapped_link[1])

    links_scrapped = []
    match_data_list = []
    match_event_data_list = []
    tournament_data_list = []

    # Grabbing the tournaments metadata. Links to their respective urls to start the webscrapping process
    tournaments_metadata = get_tournaments_metadata()

    # Grabbing data from each tournament
    for tournament in tournaments_metadata:

        tournament_data_list.append(tournament)

        # Check if tournament has being scrapped before
        if "https://www.tourney.nz/data/tournament/"+tournament[0] not in scrapper_links:
            print(tournament)
            url_to_scrape = f"https://www.tourney.nz/data/tournament/{tournament[0]}"

            match_data = get_match_data(url_to_scrape, tournament[4], tournament[0])

            print(len(match_data))
            if len(match_data) > 2:
                links_scrapped.append([1,url_to_scrape])

                for row in match_data:
                    match_data_list.append(row[0])
                    event_data = row[1]

                    for event in event_data:
                        match_event_data_list.append(event)
                    
        else:
            print("Already scrapped")

    
    if len(links_scrapped) > 0:
        
        write_to_sheet(match_data_list,"Match_data!A1", service)
        write_to_sheet(match_event_data_list, "Game_event_data!A1", service)
        write_to_sheet(tournament_data_list, "Tournaments!A1", service)
        write_to_sheet(links_scrapped, "Links_scraped!A1", service)

if __name__ == "__main__":
    base_url = "https://www.tourney.nz/data/tournaments"
    main()